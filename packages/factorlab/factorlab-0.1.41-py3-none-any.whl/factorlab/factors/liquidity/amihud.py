import pandas as pd
import numpy as np
from factorlab.features.base import Factor


class AmihudIlliquidity(Factor):
    """
    Computes the Amihud (2002) illiquidity measure:
    Return impact per unit of volume traded.
    """

    def __init__(
        self,
        return_col: str = None,
        volume_col: str = "volume",
        output_col: str = "amihud_illiq"
    ):
        super().__init__(name="AmihudIlliquidity")
        self.return_col = return_col
        self.volume_col = volume_col
        self.output_col = output_col
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
        df[self.output_col] = np.abs(df[return_col]) / df[self.volume_col]
        df[self.output_col] = df[self.output_col].replace([np.inf, -np.inf], np.nan)
        return df
