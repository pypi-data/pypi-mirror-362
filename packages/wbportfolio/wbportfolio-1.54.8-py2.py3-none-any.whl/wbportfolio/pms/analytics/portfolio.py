import numpy as np
import pandas as pd
from skfolio import Portfolio as BasePortfolio


class Portfolio(BasePortfolio):
    @property
    def all_weights_per_observation(self) -> pd.DataFrame:
        """DataFrame of the Portfolio weights containing even near zero weight per observation."""
        weights = self.weights
        assets = self.assets
        df = pd.DataFrame(
            np.ones((len(self.observations), len(assets))) * weights,
            index=self.observations,
            columns=assets,
        )
        return df

    def get_next_weights(self) -> dict[int, float]:
        """
        Given the next returns, compute the drifted weights of this portfolio

        Returns:
            A dictionary of weights (instrument ids as keys and weights as values)
        """
        returns = self.X.iloc[-1, :].T
        weights = self.all_weights_per_observation.iloc[-1, :].T
        portfolio_returns = (weights * (returns + 1.0)).sum()
        next_weights = weights * (returns + 1.0) / portfolio_returns
        next_weights = next_weights.dropna()
        next_weights = next_weights / next_weights.sum()
        return next_weights.to_dict()

    def get_estimate_net_value(self, previous_net_asset_value: float) -> float:
        expected_returns = self.weights @ self.X.iloc[-1, :].T
        return previous_net_asset_value * (1.0 + expected_returns)
