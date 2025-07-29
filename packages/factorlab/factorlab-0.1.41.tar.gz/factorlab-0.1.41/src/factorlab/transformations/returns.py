import pandas as pd
import numpy as np
from typing import Union

from factorlab.transformations.base import BaseTransform
from factorlab.utils import to_dataframe, grouped


class Difference(BaseTransform):
    """Computes the difference between current and lagged values: p_t - p_{t-lag}"""

    def __init__(self, lags: int = 1):
        """
        Initializes the Difference transformation.

        Parameters
        ----------
        lags: int
            The number of periods to lag the values. Default is 1.
        """
        super().__init__(name="Difference", description="Computes the difference between current and lagged values.")
        self.lags = lags

    def compute(self, df: Union[pd.Series, pd.DataFrame]) -> pd.DataFrame:
        """
        Computes the difference between current and lagged values.

        Parameters
        ----------
        df: Union[pd.Series, pd.DataFrame]

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the difference between current and lagged values.
        """

        df = to_dataframe(df).copy()
        return grouped(df).diff(self.lags)


class LogReturn(BaseTransform):
    """Computes log returns: log(p_t / p_{t-lag})"""

    def __init__(self, lags: int = 1):
        super().__init__(name="LogReturn", description="Computes log returns: log(p_t / p_{t-lag})")
        self.lags = lags

    def compute(self, df: Union[pd.Series, pd.DataFrame]) -> pd.DataFrame:
        """
        Computes log returns for the input DataFrame or Series.

        Parameters
        ----------
        df: Union[pd.Series, pd.DataFrame]

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the log returns, with non-positive values replaced by NaN.
        """
        df = to_dataframe(df).copy()
        df[df <= 0] = np.nan
        df = grouped(np.log(df)).diff(self.lags)
        return df.replace([np.inf, -np.inf], np.nan)


class PercentChange(BaseTransform):
    """Computes arithmetic percent change: (p_t / p_{t-lag}) - 1"""

    def __init__(self, lags: int = 1):
        super().__init__(name="PercentChange", description="Computes arithmetic percent change: (p_t / p_{t-lag}) - 1")
        self.lags = lags

    def compute(self, df: Union[pd.Series, pd.DataFrame]) -> pd.DataFrame:
        """
        Computes the percent change for the input DataFrame or Series.

        Parameters
        ----------
        df: Union[pd.Series, pd.DataFrame]

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the percent change, with non-positive values replaced by NaN.
        """
        df = to_dataframe(df).copy()
        return grouped(df).pct_change(periods=self.lags, fill_method=None)


class CumulativeReturn(BaseTransform):
    """Computes cumulative return: (p_t / p_0) - 1"""

    def __init__(self, base_index: int = 0):
        super().__init__(name="CumulativeReturn", description="Computes cumulative return: (p_t / p_0) - 1")
        self.base_index = base_index

    def compute(self, df: Union[pd.Series, pd.DataFrame]) -> pd.DataFrame:
        """
        Computes the cumulative return for the input DataFrame or Series.

        Parameters
        ----------
        df: Union[pd.Series, pd.DataFrame]

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the cumulative return, with the base price at the specified index.
        """
        df = to_dataframe(df).copy()

        # Check index
        if not (0 <= self.base_index < len(df)):
            raise IndexError(f"base_index {self.base_index} is out of bounds for DataFrame of length {len(df)}")

        if isinstance(df.index, pd.MultiIndex):
            # Grouped base prices using transform
            def _get_base(g):
                return g.iloc[self.base_index]
            base = df.groupby(level=1).transform(_get_base)
        else:
            # Single-index case
            base = df.iloc[self.base_index]
            # Align shape for broadcasting
            base = pd.DataFrame([base] * len(df), index=df.index)

        return df / base - 1
