import pandas as pd
import numpy as np
from factorlab.features.base import Factor


class RollEstimator(Factor):
    """
    Computes the Roll (1984) bid-ask spread estimator using price return autocovariance.
    """

    def __init__(
        self,
        return_col: str = None,
        output_col: str = "roll_spread",
        window: int = 20
    ):
        super().__init__(name="RollEstimator")
        self.return_col = return_col
        self.output_col = output_col
        self.window = window
        self.return_col_candidates = ["log_return", "return", "ret", "pct_change"]

    def _detect_return_column(self, df: pd.DataFrame) -> str:
        if self.return_col:
            return self.return_col
        for col in self.return_col_candidates:
            if col in df.columns:
                return col
        raise ValueError(
            f"No valid return column found in DataFrame. Expected one of: {self.return_col_candidates}"
        )

    def compute(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        return_col = self._detect_return_column(df)

        def roll_spread(series):
            cov = series.rolling(self.window).apply(
                lambda x: np.cov(x[:-1], x[1:])[0, 1], raw=False
            )
            spread = 2 * np.sqrt(-cov)
            spread = spread.replace([np.inf, -np.inf], np.nan)
            spread[cov > 0] = np.nan  # valid only when covariance is negative
            return spread

        if isinstance(df.index, pd.MultiIndex):
            df[self.output_col] = (
                df.groupby(level=1)[return_col]
                .apply(roll_spread)
                .droplevel(0)
            )
        else:
            df[self.output_col] = roll_spread(df[return_col])

        return df
