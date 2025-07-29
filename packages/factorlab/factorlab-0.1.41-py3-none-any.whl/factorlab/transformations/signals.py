import pandas as pd
import numpy as np
from typing import Union
from scipy.stats import norm, logistic
from factorlab.utils import to_dataframe, grouped
from factorlab.transformations.base import BaseTransform


class ScoresToSignals(BaseTransform):
    """
    Converts standardized scores to signals in the range [-1, 1].

    Parameters
    ----------
    method : str, {'norm',  'logistic', 'adj_norm', 'tanh', 'percentile', 'min-max'}, default 'norm'
            norm: normal cumulative distribution function.
            logistic: logistic cumulative distribution function.
            adj_norm: adjusted normal distribution.
            tanh: hyperbolic tangent.
            percentile: percentile rank.
            min-max: values between 0 and 1.

    """

    def __init__(self, method: str = 'norm'):
        super().__init__(name="ScoresToSignals",
                         description="Converts standardized scores to signals in the range [-1, 1].")
        self.method = method

    def compute(self, df: Union[pd.Series, pd.DataFrame]) -> pd.DataFrame:
        df = to_dataframe(df)

        if self.method == 'norm':
            signals = pd.DataFrame(norm.cdf(df),
                                  index=df.index,
                                  columns=df.columns)

        elif self.method == 'logistic':
            signals = pd.DataFrame(logistic.cdf(df),
                                  index=df.index,
                                  columns=df.columns)
        elif self.method == 'adj_norm':
            signals = df * np.exp((-1 * df ** 2) / 4) / 0.89
        elif self.method == 'tanh':
            signals = np.tanh(df)
        elif self.method == 'percentile':
            signals = df
        elif self.method == 'min-max':
            signals = df
        else:
            raise ValueError(f"Unsupported method: {self.method}")

        if self.method in {'norm', 'logistic', 'min-max', 'percentile'}:
            signals = (signals * 2) - 1

        return signals


class QuantilesToSignals(BaseTransform):
    """
    Converts quantile ranks to signals in the range [-1, 1].

    Parameters
    ----------
    bins : int, optional
        Number of quantile bins to use. If None, defaults to the median number of unique values in the DataFrame.
    axis : str, {'ts', 'cs'}, default 'ts'
        Axis along which to compute the quantiles. If 'ts', computes across time series;
        if 'cs', computes across cross-sections.

    """

    def __init__(self, bins: int = None, axis: str = 'ts'):
        super().__init__(name="QuantileToSignal",
                         description="Converts quantile ranks to signals in the range [-1, 1].")
        self.bins = bins
        self.axis = axis

    def compute(self, df: Union[pd.Series, pd.DataFrame]) -> pd.DataFrame:
        df = to_dataframe(df)

        # number of bins
        if self.bins is None:
            self.bins = df.nunique().median()

        # axis time series
        if self.axis == 'ts':
            g = grouped(df)
            ts_min = g.min()
            ts_max = g.max()
            ts_range = ts_max - ts_min

            signals = ((df - ts_min) / ts_range) * 2 - 1

        # axis cross-section
        else:
            if isinstance(df.index, pd.MultiIndex):
                # min number of observations in the cross-section
                df = df[(df.groupby(level=0).count() >= self.bins)].dropna()
                if df.empty:
                    raise ValueError("Number of bins is larger than the number of observations in the cross-section.")
                cs_min = df.groupby(level=0).min()
                cs_range = df.groupby(level=0).max() - df.groupby(level=0).min()
                signals = (df - cs_min) / cs_range * 2 - 1

            else:
                if df.shape[1] < self.bins:
                    raise ValueError("Number of bins is larger than the number of observations in the cross-section.")
                cs_min = df.min(axis=1)
                cs_range = df.max(axis=1) - df.min(axis=1)
                signals = df.subtract(cs_min, axis=0).div(cs_range, axis=0) * 2 - 1

        return signals


class RanksToSignals(BaseTransform):
    """
    Converts ranks to signals in the range [-1, 1].

    Parameters
    ----------
    axis : str, {'ts', 'cs'}, default 'ts'
        Axis along which to compute the ranks. If 'ts', computes across time series;
        if 'cs', computes across cross-sections.
    """

    def __init__(self,
                 axis: str = 'ts'):
        super().__init__(name="RankToSignal",
                         description="Converts ranks to signals in the range [-1, 1].")
        self.axis = axis

    def compute(self, df: Union[pd.Series, pd.DataFrame]) -> pd.DataFrame:
        df = to_dataframe(df)

        # axis time series
        if self.axis == 'ts':
            g = grouped(df)
            ts_min = g.min()
            ts_range = g.max() - g.min()

            signals = ((df - ts_min) / ts_range) * 2 - 1

        # axis cross-section
        else:
            if isinstance(df.index, pd.MultiIndex):
                cs_min = df.groupby(level=0).min()
                cs_range = df.groupby(level=0).max() - df.groupby(level=0).min()
                signals = (df - cs_min) / cs_range * 2 - 1
            else:
                cs_min = df.min(axis=1)
                cs_range = df.max(axis=1) - df.min(axis=1)
                signals = df.subtract(cs_min, axis=0).div(cs_range, axis=0) * 2 - 1

        return signals
