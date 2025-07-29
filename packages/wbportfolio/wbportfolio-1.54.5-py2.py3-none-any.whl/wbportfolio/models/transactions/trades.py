from contextlib import suppress
from datetime import date, timedelta
from decimal import Decimal

from celery import shared_task
from django.contrib import admin
from django.db import models
from django.db.models import (
    Case,
    DateField,
    ExpressionWrapper,
    F,
    OuterRef,
    Q,
    Subquery,
    Sum,
    When,
)
from django.db.models.functions import Coalesce, Round
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django_fsm import GET_STATE, FSMField, transition
from ordered_model.models import OrderedModel, OrderedModelManager, OrderedModelQuerySet
from wbcore.contrib.icons import WBIcon
from wbcore.contrib.io.mixins import ImportMixin
from wbcore.enums import RequestType
from wbcore.metadata.configs.buttons import ActionButton
from wbcore.signals import pre_merge
from wbcore.signals.models import pre_collection
from wbfdm.models import Instrument
from wbfdm.models.instruments.instrument_prices import InstrumentPrice
from wbfdm.signals import add_instrument_to_investable_universe

from wbportfolio.import_export.handlers.trade import TradeImportHandler
from wbportfolio.models.asset import AssetPosition
from wbportfolio.models.custodians import Custodian
from wbportfolio.models.roles import PortfolioRole
from wbportfolio.pms.typing import Trade as TradeDTO

from .transactions import TransactionMixin


class TradeQueryset(OrderedModelQuerySet):
    def annotate_base_info(self):
        return self.annotate(
            last_effective_date=Subquery(
                AssetPosition.unannotated_objects.filter(
                    date__lte=OuterRef("value_date"),
                    portfolio=OuterRef("portfolio"),
                )
                .order_by("-date")
                .values("date")[:1]
            ),
            previous_weight=Coalesce(
                Subquery(
                    AssetPosition.unannotated_objects.filter(
                        underlying_quote=OuterRef("underlying_instrument"),
                        date=OuterRef("last_effective_date"),
                        portfolio=OuterRef("portfolio"),
                    )
                    .values("portfolio")
                    .annotate(s=Sum("weighting"))
                    .values("s")[:1]
                ),
                Decimal(0),
            ),
            effective_weight=Round(
                F("previous_weight") * F("drift_factor"), precision=Trade.TRADE_WEIGHTING_PRECISION
            ),
            target_weight=Round(F("effective_weight") + F("weighting"), precision=Trade.TRADE_WEIGHTING_PRECISION),
            effective_shares=Coalesce(
                Subquery(
                    AssetPosition.objects.filter(
                        underlying_quote=OuterRef("underlying_instrument"),
                        date=OuterRef("last_effective_date"),
                        portfolio=OuterRef("portfolio"),
                    )
                    .values("portfolio")
                    .annotate(s=Sum("shares"))
                    .values("s")[:1]
                ),
                Decimal(0),
            ),
            target_shares=F("effective_shares") + F("shares"),
        )


class DefaultTradeManager(OrderedModelManager):
    """This manager is expect to be the trade default manager and annotate by default the effective weight (extracted
    from the associated portfolio) and the target weight as an addition between the effective weight and the delta weight
    """

    def __init__(self, with_annotation: bool = False, *args, **kwargs):
        self.with_annotation = with_annotation
        super().__init__(*args, **kwargs)

    def get_queryset(self) -> TradeQueryset:
        qs = TradeQueryset(self.model, using=self._db)
        if self.with_annotation:
            qs = qs.annotate_base_info()
        return qs


class ValidCustomerTradeManager(DefaultTradeManager):
    def __init__(self, without_internal_trade: bool = False):
        self.without_internal_trade = without_internal_trade
        super().__init__()

    def get_queryset(self):
        qs = (
            super()
            .get_queryset()
            .filter(
                transaction_subtype__in=[Trade.Type.SUBSCRIPTION, Trade.Type.REDEMPTION],
                marked_for_deletion=False,
                pending=False,
            )
        )
        if self.without_internal_trade:
            qs = qs.exclude(marked_as_internal=True)
        return qs


class Trade(TransactionMixin, ImportMixin, OrderedModel, models.Model):
    import_export_handler_class = TradeImportHandler

    TRADE_WINDOW_INTERVAL = 7
    TRADE_WEIGHTING_PRECISION = (
        8  # we need to match the assetposition weighting. Skfolio advices using a even smaller number (5)
    )

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        SUBMIT = "SUBMIT", "Submit"
        EXECUTED = "EXECUTED", "Executed"
        CONFIRMED = "CONFIRMED", "Confirmed"
        FAILED = "FAILED", "Failed"

    class Type(models.TextChoices):
        REBALANCE = "REBALANCE", "Rebalance"
        DECREASE = "DECREASE", "Decrease"
        INCREASE = "INCREASE", "Increase"
        SUBSCRIPTION = "SUBSCRIPTION", "Subscription"
        REDEMPTION = "REDEMPTION", "Redemption"
        BUY = "BUY", "Buy"
        SELL = "SELL", "Sell"
        NO_CHANGE = "NO_CHANGE", "No Change"  # default transaction subtype if weighing is 0

    transaction_subtype = models.CharField(
        max_length=32, default=Type.BUY, choices=Type.choices, verbose_name="Trade Type"
    )
    status = FSMField(default=Status.CONFIRMED, choices=Status.choices, verbose_name="Status")
    transaction_date = models.DateField(
        verbose_name="Trade Date",
        help_text="The date that this transaction was traded.",
    )
    book_date = models.DateField(
        verbose_name="Trade Date",
        help_text="The date that this transaction was booked.",
    )
    shares = models.DecimalField(
        max_digits=15,
        decimal_places=4,
        default=Decimal("0.0"),
        help_text="The number of shares that were traded.",
        verbose_name="Shares",
    )

    weighting = models.DecimalField(
        max_digits=9,
        decimal_places=TRADE_WEIGHTING_PRECISION,
        default=Decimal(0),
        help_text="The weight to be multiplied against the target",
        verbose_name="Weight",
    )
    claimed_shares = models.DecimalField(
        max_digits=15,
        decimal_places=4,
        default=Decimal(0),
        help_text="The number of shares that were claimed.",
        verbose_name="Claimed Shares",
    )
    diff_shares = models.GeneratedField(
        expression=F("shares") - F("claimed_shares"),
        output_field=models.DecimalField(max_digits=15, decimal_places=4),
        db_persist=True,
    )
    internal_trade = models.OneToOneField(
        "wbportfolio.Trade",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="internal_subscription_redemption_trade",
    )
    marked_for_deletion = models.BooleanField(
        default=False,
        help_text="If this is checked, then the trade is supposed to be deleted.",
        verbose_name="To be deleted",
    )
    marked_as_internal = models.BooleanField(
        default=False,
        help_text="If this is checked, then this subscription or redemption is considered internal and will not be considered in any AUM computation",
        verbose_name="Internal",
    )
    pending = models.BooleanField(default=False)
    exclude_from_history = models.BooleanField(default=False)
    bank = models.CharField(
        max_length=255,
        help_text="The bank/counterparty/custodian the trade went through.",
        verbose_name="Counterparty",
    )
    custodian = models.ForeignKey(
        "wbportfolio.Custodian", null=True, blank=True, on_delete=models.SET_NULL, related_name="trades"
    )
    register = models.ForeignKey(
        to="wbportfolio.Register",
        null=True,
        blank=True,
        related_name="trades",
        on_delete=models.PROTECT,
    )
    trade_proposal = models.ForeignKey(
        to="wbportfolio.TradeProposal",
        null=True,
        blank=True,
        related_name="trades",
        on_delete=models.CASCADE,
        help_text="The Trade Proposal this trade is coming from",
    )
    drift_factor = models.DecimalField(
        max_digits=16,
        decimal_places=TRADE_WEIGHTING_PRECISION,
        default=Decimal(1.0),
        verbose_name="Drift Factor",
        help_text="Drift factor to be applied to the previous portfolio weight to get the actual effective weight including daily return",
    )
    external_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="An external identifier that was supplied.",
        verbose_name="External Identifier",
    )
    external_id_alternative = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="A second external identifier that was supplied.",
        verbose_name="Alternative External Identifier",
    )

    # Manager
    objects = DefaultTradeManager()
    annotated_objects = DefaultTradeManager(with_annotation=True)
    valid_customer_trade_objects = ValidCustomerTradeManager()
    valid_external_customer_trade_objects = ValidCustomerTradeManager(without_internal_trade=True)

    @transition(
        field=status,
        source=Status.DRAFT,
        target=GET_STATE(
            lambda self, **kwargs: (self.Status.SUBMIT if self.price else self.Status.FAILED),
            states=[Status.SUBMIT, Status.FAILED],
        ),
        permission=lambda instance, user: PortfolioRole.is_portfolio_manager(
            user.profile, portfolio=instance.portfolio
        ),
        custom={
            "_transition_button": ActionButton(
                method=RequestType.PATCH,
                identifiers=("wbportfolio:trade",),
                icon=WBIcon.SEND.icon,
                key="submit",
                label="Submit",
                action_label="Submit",
                # description_fields="<p>Start: {{start}}</p><p>End: {{end}}</p><p>Title: {{title}}</p>",
            )
        },
        on_error="FAILED",
    )
    def submit(self, by=None, description=None, portfolio_total_asset_value=None, **kwargs):
        warnings = []
        # if shares is defined and the underlying instrument defines a round lot size different than 1 and exchange allows its application, we round the share accordingly
        if self.trade_proposal and not self.portfolio.only_weighting:
            shares = self.trade_proposal.get_round_lot_size(self.shares, self.underlying_instrument)
            if shares != self.shares:
                warnings.append(
                    f"{self.underlying_instrument.computed_str} has a round lot size of  {self.underlying_instrument.round_lot_size}: shares were rounded from {self.shares} to {shares}"
                )
            shares = round(shares)  # ensure fractional shares are converted into integer
            # we need to recompute the delta weight has we changed the number of shares
            if shares != self.shares:
                self.shares = shares
                if portfolio_total_asset_value:
                    self.weighting = self.shares * self.price * self.currency_fx_rate / portfolio_total_asset_value

        if not self.price:
            warnings.append(
                f"Trade failed because no price is found for {self.underlying_instrument.computed_str} on {self.transaction_date:%Y-%m-%d}"
            )
        return warnings

    def can_submit(self):
        pass

    @transition(
        field=status,
        source=Status.DRAFT,
        target=Status.FAILED,
        permission=lambda instance, user: PortfolioRole.is_portfolio_manager(
            user.profile, portfolio=instance.portfolio
        ),
    )
    def fail(self, **kwargs):
        pass

    # TODO To be removed
    @cached_property
    def last_underlying_quote_price(self) -> InstrumentPrice | None:
        try:
            # we try t0 first
            return InstrumentPrice.objects.filter_only_valid_prices().get(
                instrument=self.underlying_instrument, date=self.transaction_date
            )
        except InstrumentPrice.DoesNotExist:
            with suppress(InstrumentPrice.DoesNotExist):
                # we fall back to the latest price before t0
                return (
                    InstrumentPrice.objects.filter_only_valid_prices()
                    .filter(instrument=self.underlying_instrument, date__lte=self.transaction_date)
                    .latest("date")
                )

    @transition(
        field=status,
        source=Status.SUBMIT,
        target=Status.EXECUTED,
        permission=lambda instance, user: PortfolioRole.is_portfolio_manager(
            user.profile, portfolio=instance.portfolio
        ),
        custom={
            "_transition_button": ActionButton(
                method=RequestType.PATCH,
                identifiers=("wbportfolio:trade",),
                icon=WBIcon.CONFIRM.icon,
                key="execute",
                label="Execute",
                action_label="Execute",
                # description_fields="<p>Start: {{start}}</p><p>End: {{end}}</p><p>Title: {{title}}</p>",
            )
        },
    )
    def execute(self, **kwargs):
        with suppress(ValueError):
            asset = self.get_asset()
            AssetPosition.unannotated_objects.update_or_create(
                underlying_quote=asset.underlying_quote,
                portfolio_created=asset.portfolio_created,
                portfolio=asset.portfolio,
                date=asset.date,
                defaults={
                    "initial_currency_fx_rate": asset.initial_currency_fx_rate,
                    "initial_price": asset.initial_price,
                    "initial_shares": asset.initial_shares,
                    "underlying_quote_price": asset.underlying_quote_price,
                    "asset_valuation_date": asset.asset_valuation_date,
                    "currency": asset.currency,
                    "is_estimated": asset.is_estimated,
                    "weighting": asset.weighting,
                },
            )

    def can_execute(self):
        if not self.price:
            return {"underlying_instrument": [_("Cannot execute a trade without a valid quote price")]}
        if not self.portfolio.is_manageable:
            return {
                "portfolio": [_("The portfolio needs to be a model portfolio in order to execute this trade manually")]
            }

    @transition(
        field=status,
        source=Status.EXECUTED,
        target=Status.CONFIRMED,
        permission=lambda instance, user: PortfolioRole.is_portfolio_manager(
            user.profile, portfolio=instance.portfolio
        ),
        custom={
            "_transition_button": ActionButton(
                method=RequestType.PATCH,
                identifiers=("wbportfolio:trade",),
                icon=WBIcon.CONFIRM.icon,
                key="confirm",
                label="Confirm",
                action_label="Confirme",
                # description_fields="<p>Start: {{start}}</p><p>End: {{end}}</p><p>Title: {{title}}</p>",
            )
        },
    )
    def confirm(self, by=None, description=None, **kwargs):
        pass

    def can_confirm(self):
        pass

    @transition(
        field=status,
        source=Status.SUBMIT,
        target=Status.DRAFT,
        permission=lambda instance, user: PortfolioRole.is_portfolio_manager(
            user.profile, portfolio=instance.portfolio
        ),
        custom={
            "_transition_button": ActionButton(
                method=RequestType.PATCH,
                identifiers=("wbportfolio:trade",),
                icon=WBIcon.UNDO.icon,
                key="backtodraft",
                label="Back to Draft",
                action_label="backtodraft",
                # description_fields="<p>Start: {{start}}</p><p>End: {{end}}</p><p>Title: {{title}}</p>",
            )
        },
    )
    def backtodraft(self, **kwargs):
        pass

    @transition(
        field=status,
        source=Status.EXECUTED,
        target=Status.DRAFT,
        permission=lambda instance, user: PortfolioRole.is_portfolio_manager(
            user.profile, portfolio=instance.portfolio
        ),
        custom={
            "_transition_button": ActionButton(
                method=RequestType.PATCH,
                identifiers=("wbportfolio:trade",),
                icon=WBIcon.UNDO.icon,
                key="reverte",
                label="Revert",
                action_label="revert",
                # description_fields="<p>Start: {{start}}</p><p>End: {{end}}</p><p>Title: {{title}}</p>",
            )
        },
    )
    def revert(self, to_date=None, **kwargs):
        with suppress(AssetPosition.DoesNotExist):
            asset = AssetPosition.unannotated_objects.get(
                underlying_quote=self.underlying_instrument,
                portfolio=self.portfolio,
                date=self.transaction_date,
                is_estimated=False,
            )
            asset.set_weighting(asset.weighting - self.weighting)
            asset.save()

    @property
    def product(self):
        from wbportfolio.models.products import Product

        try:
            return Product.objects.get(id=self.underlying_instrument.id)
        except Product.DoesNotExist:
            return None

    @property
    @admin.display(description="Last Effective Date")
    def _last_effective_date(self) -> date:
        if hasattr(self, "last_effective_date"):
            return self.last_effective_date
        elif (
            assets := AssetPosition.unannotated_objects.filter(
                date__lte=self.value_date,
                portfolio=self.portfolio,
            )
        ).exists():
            return assets.latest("date").date

    @property
    @admin.display(description="Effective Weight")
    def _previous_weight(self) -> Decimal:
        if hasattr(self, "previous_weight"):
            return self.previous_weight
        return AssetPosition.unannotated_objects.filter(
            underlying_quote=self.underlying_instrument,
            date=self._last_effective_date,
            portfolio=self.portfolio,
        ).aggregate(s=Sum("weighting"))["s"] or Decimal(0)

    @property
    @admin.display(description="Effective Weight")
    def _effective_weight(self) -> Decimal:
        if hasattr(self, "effective_weight"):
            return self.effective_weight
        return round(self._previous_weight * self.drift_factor, self.TRADE_WEIGHTING_PRECISION)

    @property
    @admin.display(description="Effective Shares")
    def _effective_shares(self) -> Decimal:
        return getattr(
            self,
            "effective_shares",
            AssetPosition.objects.filter(
                underlying_quote=self.underlying_instrument,
                date=self.transaction_date,
                portfolio=self.portfolio,
            ).aggregate(s=Sum("shares"))["s"]
            or Decimal(0),
        )

    @property
    @admin.display(description="Target Weight")
    def _target_weight(self) -> Decimal:
        return getattr(
            self, "target_weight", round(self._effective_weight + self.weighting, self.TRADE_WEIGHTING_PRECISION)
        )

    @property
    @admin.display(description="Target Shares")
    def _target_shares(self) -> Decimal:
        return getattr(self, "target_shares", self._effective_shares + self.shares)

    order_with_respect_to = "trade_proposal"

    class Meta(OrderedModel.Meta):
        verbose_name = "Trade"
        verbose_name_plural = "Trades"
        indexes = [
            models.Index(fields=["underlying_instrument", "transaction_date"]),
            models.Index(fields=["portfolio", "underlying_instrument", "transaction_date"]),
            # models.Index(fields=["date", "underlying_instrument"]),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(marked_as_internal=False)
                | (
                    models.Q(marked_as_internal=True)
                    & models.Q(transaction_subtype__in=["REDEMPTION", "SUBSCRIPTION"])
                ),
                name="marked_as_internal_only_for_subred",
            ),
            models.CheckConstraint(
                check=models.Q(internal_trade__isnull=True)
                | (
                    models.Q(internal_trade__isnull=False)
                    & models.Q(transaction_subtype__in=["REDEMPTION", "SUBSCRIPTION"])
                ),
                name="internal_trade_set_only_for_subred",
            ),
            models.UniqueConstraint(
                fields=["portfolio", "transaction_date", "underlying_instrument"],
                name="unique_manual_trade",
                condition=Q(trade_proposal__isnull=False),
            ),
        ]
        # notification_email_template = "portfolio/email/trade_notification.html"

    def __init__(self, *args, target_weight: Decimal | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        if target_weight is not None:  # if target weight is provided, we guess the corresponding weighting
            self.weighting = Decimal(target_weight) - self._effective_weight
            self._set_type()

    def save(self, *args, **kwargs):
        if abs(self.weighting) < 10e-6:
            self.weighting = Decimal("0")
        if self.trade_proposal:
            if not self.underlying_instrument.is_investable_universe:
                self.underlying_instrument.is_investable_universe = True
                self.underlying_instrument.save()
            self.portfolio = self.trade_proposal.portfolio
            self.transaction_date = self.trade_proposal.trade_date
            self.value_date = self.trade_proposal.last_effective_date
        if self.price is None:
            # we try to get the price if not provided directly from the underlying instrument
            self.price = self.get_price()
        if self.trade_proposal and not self.portfolio.only_weighting:
            estimated_shares = self.trade_proposal.get_estimated_shares(
                self.weighting, self.underlying_instrument, self.price
            )
            if estimated_shares:
                self.shares = estimated_shares

        if not self.custodian and self.bank:
            self.custodian = Custodian.get_by_mapping(self.bank)

        if self.transaction_subtype is None or self.trade_proposal:
            # if subtype not provided, we extract it automatically from the existing data.
            self._set_type()
        if self.id and hasattr(self, "claims"):
            self.claimed_shares = self.claims.filter(status="APPROVED").aggregate(s=Sum("shares"))["s"] or Decimal(0)
        if self.internal_trade:
            self.marked_as_internal = True
        if not self.value_date:
            self.value_date = self.transaction_date
        if not self.book_date:
            self.book_date = self.transaction_date
        super().save(*args, **kwargs)

    def _set_type(self):
        if self.weighting == 0:
            self.transaction_subtype = Trade.Type.NO_CHANGE
        if self.underlying_instrument.instrument_type.key == "product":
            if self.shares is not None:
                if self.shares > 0:
                    self.transaction_subtype = Trade.Type.SUBSCRIPTION
                elif self.shares < 0:
                    self.transaction_subtype = Trade.Type.REDEMPTION
        elif self.weighting is not None:
            if self.weighting > 0:
                if self._effective_weight:
                    self.transaction_subtype = Trade.Type.INCREASE
                else:
                    self.transaction_subtype = Trade.Type.BUY
            elif self.weighting < 0:
                if self._target_weight:
                    self.transaction_subtype = Trade.Type.DECREASE
                else:
                    self.transaction_subtype = Trade.Type.SELL
        else:
            self.transaction_subtype = Trade.Type.REBALANCE

    def get_type(self) -> str:
        """
        Return the expected transaction subtype based n

        """

    def get_asset(self) -> AssetPosition:
        asset = AssetPosition(
            underlying_quote=self.underlying_instrument,
            portfolio_created=None,
            portfolio=self.portfolio,
            date=self.transaction_date,
            initial_currency_fx_rate=self.currency_fx_rate,
            weighting=self._target_weight,
            initial_price=self.price,
            initial_shares=None,
            asset_valuation_date=self.transaction_date,
            currency=self.currency,
            is_estimated=False,
        )
        asset.set_weighting(self._target_weight)
        asset.pre_save()
        return asset

    def get_price(self) -> Decimal | None:
        with suppress(ValueError):
            return Decimal.from_float(self.underlying_instrument.get_price(self.transaction_date))

    def delete(self, **kwargs):
        pre_collection.send(sender=self.__class__, instance=self)
        super().delete(**kwargs)

    def __str__(self):
        ticker = f"{self.underlying_instrument.ticker}:" if self.underlying_instrument.ticker else ""
        return f"{ticker}{self.shares} ({self.bank})"

    def _build_dto(self, drift_factor: Decimal = None) -> TradeDTO:
        """
        Data Transfer Object
        Returns:
            DTO trade object

        """
        if not drift_factor:
            drift_factor = self.drift_factor
        return TradeDTO(
            id=self.id,
            underlying_instrument=self.underlying_instrument.id,
            previous_weight=self._previous_weight,
            target_weight=self._previous_weight * drift_factor + self.weighting,
            effective_shares=self._effective_shares,
            target_shares=self._target_shares,
            drift_factor=drift_factor,
            currency_fx_rate=self.currency_fx_rate,
            price=self.price,
            instrument_type=self.underlying_instrument.security_instrument_type.id,
            currency=self.underlying_instrument.currency,
            date=self.transaction_date,
            is_cash=self.underlying_instrument.is_cash or self.underlying_instrument.is_cash_equivalent,
        )

    def get_alternative_valid_trades(self, share_delta: float = 0):
        return Trade.objects.filter(
            Q(underlying_instrument=self.underlying_instrument)
            & Q(portfolio=self.portfolio)
            & (
                Q(transaction_date__gte=self.transaction_date - timedelta(days=self.TRADE_WINDOW_INTERVAL))
                & Q(transaction_date__lte=self.transaction_date + timedelta(days=self.TRADE_WINDOW_INTERVAL))
            )
            & Q(transaction_subtype=self.transaction_subtype)
            & Q(shares__gte=self.shares * Decimal(1 - share_delta))
            & Q(shares__lte=self.shares * Decimal(1 + share_delta))
            & Q(marked_for_deletion=False)
            & Q(claims__isnull=True)
            & Q(pending=False)
        ).exclude(id=self.id)

    @property
    def is_claimable(self) -> bool:
        return self.is_customer_trade and not self.marked_for_deletion and not self.pending

    @property
    def is_customer_trade(self) -> bool:
        return self.transaction_subtype in [Trade.Type.REDEMPTION.name, Trade.Type.SUBSCRIPTION.name]

    @classmethod
    def subquery_shares_per_underlying_instrument(
        cls, val_date, underlying_instrument_name="pk", only_customer_trade=True
    ):
        """Returns a Subquery that returns the shares at a certain price date
        or 0

        Arguments:
            val_date {datetime.date} -- The  date that is used to determine which tradesare filtered

        Keyword Arguments:
            underlying_instrument_name {str} -- The reference to the underlying_instrument pk of the outer query (default: {"pk"})

        Returns:
            django.db.models.Subquery -- Subquery containing the sum of shares of each underlying_instrument
        """

        qs = cls.valid_customer_trade_objects
        if not only_customer_trade:
            qs = cls.objects
        qs = qs.filter(
            underlying_instrument=OuterRef(underlying_instrument_name),
            transaction_date__lt=val_date,
        )
        return Coalesce(
            Subquery(
                qs.values("underlying_instrument").annotate(sum_shares=Sum("shares")).values("sum_shares")[:1],
                output_field=models.DecimalField(),
            ),
            Decimal(0),
        )

    def link_to_internal_trade(self):
        qs = Trade.objects.filter(
            Q(underlying_instrument__instrument_type__key="product")
            & Q(shares=self.shares)
            & Q(underlying_instrument=self.underlying_instrument)
            & Q(transaction_date__gte=self.transaction_date - timedelta(days=self.TRADE_WINDOW_INTERVAL))
            & Q(transaction_date__lte=self.transaction_date + timedelta(days=self.TRADE_WINDOW_INTERVAL))
        ).exclude(id=self.id)
        if self.transaction_subtype in [Trade.Type.REDEMPTION, Trade.Type.SUBSCRIPTION]:
            qs = qs.exclude(transaction_subtype__in=[Trade.Type.REDEMPTION, Trade.Type.SUBSCRIPTION])
            if qs.count() == 1:
                self.internal_trade = qs.first()
                self.save()
        else:
            qs = qs.filter(transaction_subtype__in=[Trade.Type.REDEMPTION, Trade.Type.SUBSCRIPTION])
            if qs.count() == 1:
                trade = qs.first()
                trade.internal_trade = self
                trade.save()

    @classmethod
    def subquery_net_money(
        cls, date_gte=None, date_lte=None, underlying_instrument_name="pk", only_positive=False, only_negative=False
    ):
        """Return a subquery which computes the net negative/positive money per underlying_instrument

        Arguments:
            val_date1 {datetime.date} -- The start date, including
            val_date2 {datetime.date} -- The end date, including

        Keyword Arguments:
            underlying_instrument_name {str} -- The reference to the underlying_instrument pk from the outer query (default: {"pk"})

        Returns:
            django.db.models.Subquery -- The subquery containing the net negative money per underlying_instrument
        """
        qs = cls.valid_external_customer_trade_objects.annotate(
            date_considered=ExpressionWrapper(F("transaction_date") + 1, output_field=DateField())
        )

        if date_gte:
            qs = qs.filter(date_considered__gte=date_gte)
        if date_lte:
            qs = qs.filter(date_considered__lte=date_lte)

        if only_positive:
            qs = qs.filter(shares__gt=0)
        elif only_negative:
            qs = qs.filter(shares__lt=0)
        return Coalesce(
            Subquery(
                qs.filter(underlying_instrument=OuterRef(underlying_instrument_name))
                .annotate(
                    _price=Case(
                        When(
                            price__isnull=True,
                            then=InstrumentPrice.subquery_closest_value(
                                "net_value",
                                date_name="date_considered",
                                instrument_pk_name="underlying_instrument__pk",
                            ),
                        ),
                        default=F("price"),
                    ),
                    net_value=ExpressionWrapper(F("shares") * F("_price"), output_field=models.FloatField()),
                )
                .values("underlying_instrument")
                .annotate(sum_net_value=Sum(F("net_value")))
                .values("sum_net_value"),
                output_field=models.FloatField(),
            ),
            0.0,
        )

    @classmethod
    def get_endpoint_basename(cls):
        return "wbportfolio:trade"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbportfolio:traderepresentation-list"

    @classmethod
    def get_representation_label_key(cls):
        return "{{|:-}}{{transaction_date}}{{|::}}{{bank}}{{|-:}} {{claimed_shares}} / {{shares}} (∆ {{diff_shares}})"

    @classmethod
    def get_representation_value_key(cls):
        return "id"


@shared_task
def align_custodian():
    unaligned_qs = Trade.objects.annotate(
        proper_custodian_id=Subquery(Custodian.objects.filter(mapping__contains=OuterRef("bank")).values("id")[:1])
    ).exclude(custodian__id=F("proper_custodian_id"))

    unaligned_qs.update(custodian__id=F("proper_custodian_id"))


@receiver(post_save, sender="wbportfolio.Claim")
def compute_claimed_shares_on_claim_save(sender, instance, created, raw, **kwargs):
    if not raw and instance.trade:
        instance.trade.save()


@receiver(pre_merge, sender="wbfdm.Instrument")
def pre_merge_instrument(sender: models.Model, merged_object: "Instrument", main_object: "Instrument", **kwargs):
    """
    Simply reassign the transactions linked to the merged instrument to the main instrument
    """
    merged_object.trades.update(underlying_instrument=main_object)


@receiver(add_instrument_to_investable_universe, sender="wbfdm.Instrument")
def add_instrument_to_investable_universe_from_transactions(sender: models.Model, **kwargs) -> list[int]:
    """
    register all instrument linked to assets as within the investible universe
    """
    return list(
        (
            Instrument.objects.annotate(
                transaction_exists=models.Exists(Trade.objects.filter(underlying_instrument=models.OuterRef("pk")))
            ).filter(transaction_exists=True)
        )
        .distinct()
        .values_list("id", flat=True)
    )
