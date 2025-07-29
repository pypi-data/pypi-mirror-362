import pandas as pd
from factorlab.transformations.base import BaseTransform


class VWAP(BaseTransform):
    """
    Computes Volume Weighted Average Price (VWAP):

    VWAP_t = (Close + (Open + High + Low)/3) / 2

    This is not a classical volume-weighted average, but a simplified alternative
    when volume data is not available.
    """

    def __init__(
            self,
            open_col: str = "open",
            high_col: str = "high",
            low_col: str = "low",
            close_col: str = "close",
            output_col: str = "vwap"
    ):
        super().__init__(name="VWAP",
                         description="Computes Volume Weighted Average Price (VWAP) using OHLC data.")
        self.open_col = open_col
        self.high_col = high_col
        self.low_col = low_col
        self.close_col = close_col
        self.output_col = output_col

    def compute(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        required_cols = {self.open_col, self.high_col, self.low_col, self.close_col}
        missing = required_cols - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns for VWAP calculation: {missing}")

        typical_price = (df[self.open_col] + df[self.high_col] + df[self.low_col]) / 3
        df[self.output_col] = (df[self.close_col] + typical_price) / 2

        return df



