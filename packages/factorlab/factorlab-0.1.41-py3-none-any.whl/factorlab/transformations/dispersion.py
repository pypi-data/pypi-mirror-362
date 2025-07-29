import pandas as pd
import numpy as np
from typing import Union
from factorlab.utils import to_dataframe, grouped, maybe_droplevel
from factorlab.transformations.base import BaseTransform


class StandardDeviation(BaseTransform):
    """
    Computes the standard deviation over time series or cross-section.

    Parameters
    ----------
    axis : str, {'ts', 'cs'}, default 'ts'
        Whether to compute time series ('ts') or cross-sectional ('cs') standard deviation.
    window_type : str, {'rolling', 'expanding', 'fixed', 'ewm'}, default 'expanding'
        Type of window: 'rolling', 'expanding', 'ewm', or 'fixed'.
    window_size : int, default 30
        Number of periods in the rolling or EWM window.
    min_periods : int, optional
        Minimum number of observations in window required to have a value.
    """

    def __init__(self,
                 axis: str = 'ts',
                 window_type: str = 'expanding',
                 window_size: int = 30,
                 min_periods: int = 1):
        super().__init__(name="StandardDeviation",
                         description="Computes standard deviation over time series or cross-section.")
        self.axis = axis
        self.window_type = window_type
        self.window_size = window_size
        self.min_periods = min_periods

    def compute(self, df: Union[pd.Series, pd.DataFrame]) -> pd.DataFrame:
        df = to_dataframe(df).copy()

        if self.axis == 'ts':
            g = grouped(df)

            if self.window_type == 'rolling':
                res = g.rolling(window=self.window_size, min_periods=self.min_periods).std()

            elif self.window_type == 'expanding':
                res = g.expanding(min_periods=self.min_periods).std()

            elif self.window_type == 'ewm':
                res = g.ewm(span=self.window_size, min_periods=self.min_periods).std()

            elif self.window_type == 'fixed':
                res = g.std()

            else:
                raise ValueError(f"Unsupported window type: {self.window_type}")

            std = maybe_droplevel(res, level=0)
            # Convert to DataFrame if needed
            return to_dataframe(std)

        elif self.axis == 'cs':
            std = df.groupby(level=0).std() if isinstance(df.index, pd.MultiIndex) else df.std(axis=1)
            # Convert to DataFrame if needed
            return to_dataframe(std)

        else:
            raise ValueError(f"Unsupported axis: {self.axis}")


class Quantile(BaseTransform):
    """Computes quantiles over time series or cross-section.

    Parameters
    ----------
    q : float, default 0.5
        The quantile to compute (0 < q < 1).
    axis : str, {'ts', 'cs'}, default 'ts'
        Whether to compute time series ('ts') or cross-sectional ('cs') quantiles.
    window_type : str, {'rolling', 'expanding', 'fixed'}, default 'expanding'
        Type of window: 'rolling', 'expanding', or 'fixed'.
    window_size : int, default 30
        Number of periods in the rolling.
    min_periods : int, default 1
        Minimum number of observations in window required to have a value.
    """

    def __init__(self,
                 q: float = 0.5,
                 axis: str = 'ts',
                 window_type: str = 'expanding',
                 window_size: int = 30,
                 min_periods: int = 1):
        super().__init__(name="Quantile", description="Computes quantiles over time series or cross-section.")
        self.q = q
        self.axis = axis
        self.window_type = window_type
        self.window_size = window_size
        self.min_periods = min_periods

    def compute(self, df: Union[pd.Series, pd.DataFrame]) -> pd.DataFrame:
        df = to_dataframe(df).copy()

        if self.axis == 'ts':
            g = grouped(df)

            if self.window_type == 'rolling':
                res = g.rolling(window=self.window_size, min_periods=self.min_periods).quantile(self.q)

            elif self.window_type == 'expanding':
                res = g.expanding(min_periods=self.min_periods).quantile(self.q)

            elif self.window_type == 'fixed':
                res = g.quantile(self.q)

            else:
                raise ValueError(f"Unsupported window type: {self.window_type}")

            quantile = maybe_droplevel(res, level=0)
            return to_dataframe(quantile)

        elif self.axis == 'cs':
            if isinstance(df.index, pd.MultiIndex):
                quantile = df.groupby(level=0).quantile(self.q)
            else:
                quantile = df.quantile(self.q, axis=1)
            # Convert to DataFrame if needed
            return to_dataframe(quantile)

        else:
            raise ValueError(f"Unsupported axis: {self.axis}")


class IQR(BaseTransform):
    """Computes the interquartile range (IQR) over time series or cross-section.

    Parameters
    ----------
    axis : str, {'ts', 'cs'}, default 'ts'
        Whether to compute time series ('ts') or cross-sectional ('cs') IQR.
    window_type : str, {'rolling', 'expanding', 'fixed'}, default 'expanding'
        Type of window: 'rolling', 'expanding', or 'fixed'.
    window_size : int, default 30
        Number of periods in the rolling.
    min_periods : int, default 1
        Minimum number of observations in window required to have a value.
    """

    def __init__(self,
                 axis: str = 'ts',
                 window_type: str = 'expanding',
                 window_size: int = 30,
                 min_periods: int = 1):
        super().__init__(name="IQR",
                         description="Computes interquartile range (IQR) over time series or cross-section.")
        self.axis = axis
        self.window_type = window_type
        self.window_size = window_size
        self.min_periods = min_periods

    def compute(self, df: Union[pd.Series, pd.DataFrame]) -> pd.DataFrame:
        df = to_dataframe(df).copy()

        if self.axis == 'ts':
            g = grouped(df)

            if self.window_type == 'rolling':
                q75 = g.rolling(window=self.window_size, min_periods=self.min_periods).quantile(0.75)
                q25 = g.rolling(window=self.window_size, min_periods=self.min_periods).quantile(0.25)
                res = q75 - q25

            elif self.window_type == 'expanding':
                q75 = g.expanding(min_periods=self.min_periods).quantile(0.75)
                q25 = g.expanding(min_periods=self.min_periods).quantile(0.25)
                res = q75 - q25

            elif self.window_type == 'fixed':
                res = g.quantile(0.75) - g.quantile(0.25)

            else:
                raise ValueError(f"Unsupported window type: {self.window_type}")

            iqr = maybe_droplevel(res, level=0)
            return to_dataframe(iqr)

        elif self.axis == 'cs':
            if isinstance(df.index, pd.MultiIndex):
                q75 = df.groupby(level=0).quantile(0.75)
                q25 = df.groupby(level=0).quantile(0.25)
            else:
                q75 = df.quantile(0.75, axis=1)
                q25 = df.quantile(0.25, axis=1)

            iqr = q75 - q25
            # Convert to DataFrame if needed
            return to_dataframe(iqr)

        else:
            raise ValueError(f"Unsupported axis: {self.axis}")


class MedianAbsoluteDeviation(BaseTransform):
    """Computes the median absolute deviation (MAD) over time series or cross-section.

    Parameters
    ----------
    axis : str, {'ts', 'cs'}, default 'ts'
        Whether to compute time series ('ts') or cross-sectional ('cs') MAD.
    window_type : str, {'rolling', 'expanding', 'fixed'}, default 'expanding'
        Type of window: 'rolling', 'expanding', or 'fixed'.
    window_size : int, default 30
        Number of periods in the rolling.
    min_periods : int, default 1
        Minimum number of observations in window required to have a value.
    """

    def __init__(self,
                 axis: str = 'ts',
                 window_type: str = 'expanding',
                 window_size: int = 30,
                 min_periods: int = 1):
        super().__init__(name="MedianAbsoluteDeviation",
                         description="Computes median absolute deviation (MAD) over time series or cross-section.")
        self.axis = axis
        self.window_type = window_type
        self.window_size = window_size
        self.min_periods = min_periods

    def compute(self, df: Union[pd.Series, pd.DataFrame]) -> pd.DataFrame:
        df = to_dataframe(df).copy()

        if self.axis == 'ts':
            g = grouped(df)  # Group by second level if MultiIndex

            if self.window_type == 'rolling':
                median = g.rolling(window=self.window_size, min_periods=self.min_periods).median()
                median = maybe_droplevel(median, level=0)  # Drop level if MultiIndex
                abs_dev = (df - median).abs()
                res = grouped(abs_dev).rolling(window=self.window_size, min_periods=self.min_periods).median()

            elif self.window_type == 'expanding':
                median = g.expanding(min_periods=self.min_periods).median()
                median = maybe_droplevel(median, level=0)
                abs_dev = (df - median).abs()
                res = grouped(abs_dev).expanding(min_periods=self.min_periods).median()

            elif self.window_type == 'fixed':
                median = g.median()
                median = maybe_droplevel(median, level=0)
                abs_dev = (df - median).abs()
                res = grouped(abs_dev).median()

            else:
                raise ValueError(f"Unsupported window type: {self.window_type}")

            mad = maybe_droplevel(res, level=0)
            # Convert to DataFrame if needed
            return to_dataframe(mad)

        elif self.axis == 'cs':
            if isinstance(df.index, pd.MultiIndex):
                median = df.groupby(level=0).median()
                abs_dev = (df - median).abs()
                mad = abs_dev.groupby(level=0).median()
            else:
                median = df.median(axis=1)
                abs_dev = (df.T - median).abs().T
                mad = abs_dev.median(axis=1)

            return to_dataframe(mad)


class Range(BaseTransform):
    """Computes the range (max - min) over time series or cross-section.

    Parameters
    ----------
    axis : str, {'ts', 'cs'}, default 'ts'
        Whether to compute time series ('ts') or cross-sectional ('cs') range.
    window_type : str, {'rolling', 'expanding', 'fixed'}, default 'expanding'
        Type of window: 'rolling', 'expanding', or 'fixed'.
    window_size : int, default 30
        Number of periods in the rolling.
    min_periods : int, default 1
        Minimum number of observations in window required to have a value.
    """

    def __init__(self,
                 axis: str = 'ts',
                 window_type: str = 'expanding',
                 window_size: int = 30,
                 min_periods: int = 1):
        super().__init__(name="Range", description="Computes range (max - min) over time series or cross-section.")
        self.axis = axis
        self.window_type = window_type
        self.window_size = window_size
        self.min_periods = min_periods

    def compute(self, df: Union[pd.Series, pd.DataFrame]) -> pd.DataFrame:
        df = to_dataframe(df).copy()

        if self.axis == 'ts':
            g = grouped(df)

            if self.window_type == 'rolling':
                rolling = g.rolling(window=self.window_size, min_periods=self.min_periods)
                res = rolling.max() - rolling.min()

            elif self.window_type == 'expanding':
                expanding = g.expanding(min_periods=self.min_periods)
                res = expanding.max() - expanding.min()

            elif self.window_type == 'fixed':
                res = g.max() - g.min()

            else:
                raise ValueError(f"Unsupported window type: {self.window_type}")

            rng = maybe_droplevel(res, level=0)
            # Convert to DataFrame if needed
            return to_dataframe(rng)

        elif self.axis == 'cs':
            if isinstance(df.index, pd.MultiIndex):
                res = df.groupby(level=0).max() - df.groupby(level=0).min()
            else:
                res = df.max(axis=1) - df.min(axis=1)
            # Convert to DataFrame if needed
            return to_dataframe(res)

        else:
            raise ValueError(f"Unsupported axis: {self.axis}")


class Variance(BaseTransform):
    """Computes the variance over time series or cross-section.

    Parameters
    ----------
    axis : str, {'ts', 'cs'}, default 'ts'
        Whether to compute time series ('ts') or cross-sectional ('cs') variance.
    window_type : str, {'rolling', 'expanding', 'fixed'}, default 'expanding'
        Type of window: 'rolling', 'expanding', or 'fixed'.
    window_size : int, default 30
        Number of periods in the rolling.
    min_periods : int, default 1
        Minimum number of observations in window required to have a value.
    """

    def __init__(self,
                 axis: str = 'ts',
                 window_type: str = 'expanding',
                 window_size: int = 30,
                 min_periods: int = 1):
        super().__init__(name="Variance", description="Computes variance over time series or cross-section.")
        self.axis = axis
        self.window_type = window_type
        self.window_size = window_size
        self.min_periods = min_periods

    def compute(self, df: Union[pd.Series, pd.DataFrame]) -> pd.DataFrame:
        df = to_dataframe(df).copy()

        if self.axis == 'ts':
            g = grouped(df)

            if self.window_type == 'rolling':
                res = g.rolling(window=self.window_size, min_periods=self.min_periods).var()

            elif self.window_type == 'expanding':
                res = g.expanding(min_periods=self.min_periods).var()

            elif self.window_type == 'fixed':
                res = g.var()

            else:
                raise ValueError(f"Unsupported window type: {self.window_type}")

            var = maybe_droplevel(res, level=0)
            # Convert to DataFrame if needed
            return to_dataframe(var)

        elif self.axis == 'cs':
            var = df.groupby(level=0).var() if isinstance(df.index, pd.MultiIndex) else df.var(axis=1)
            # Convert to DataFrame if needed
            return to_dataframe(var)

        else:
            raise ValueError(f"Unsupported axis: {self.axis}")


class AverageTrueRange(BaseTransform):
    """
    Computes the Average True Range (ATR) over a time series using OHLC data.

    Parameters
    ----------
    window_type : str, {'rolling', 'expanding', 'fixed', 'ewm'}, default 'expanding'
        Type of window to use for smoothing the true range.
    window_size : int, default 30
        Number of periods in the window.
    min_periods : int, default 1
        Minimum number of observations required to compute the average.
    """

    def __init__(self,
                 window_type: str = 'expanding',
                 window_size: int = 30,
                 min_periods: int = 1):
        super().__init__(name="AverageTrueRange", description="Computes Average True Range (ATR) from OHLC data.")
        self.window_type = window_type
        self.window_size = window_size
        self.min_periods = min_periods

    def compute(self, df: Union[pd.Series, pd.DataFrame]) -> pd.DataFrame:
        df = to_dataframe(df).copy()

        required_cols = ['open', 'high', 'low', 'close']
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"DataFrame must contain {required_cols} columns to compute ATR.")

        # Unstack if MultiIndex
        is_multi = isinstance(df.index, pd.MultiIndex)
        df_ohlc = df.unstack() if is_multi else df

        # Compute True Range
        high = df_ohlc['high']
        low = df_ohlc['low']
        close = df_ohlc['close']

        tr1 = high - low
        tr2 = (high - close.shift()).abs()
        tr3 = (low - close.shift()).abs()

        if is_multi:
            tr = pd.concat([tr1.stack(), tr2.stack(), tr3.stack()], axis=1).max(axis=1)
        else:
            tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

        # Compute ATR using selected window
        g = grouped(tr.to_frame('tr'))

        if self.window_type == 'rolling':
            res = g.rolling(window=self.window_size, min_periods=self.min_periods).mean()

        elif self.window_type == 'expanding':
            res = g.expanding(min_periods=self.min_periods).mean()

        elif self.window_type == 'ewm':
            res = g.ewm(span=self.window_size, min_periods=self.min_periods).mean()

        elif self.window_type == 'fixed':
            res = g.mean()

        else:
            raise ValueError(f"Unsupported window type: {self.window_type}")

        atr = maybe_droplevel(res, level=0)
        return to_dataframe(atr).rename(columns={'tr': 'atr'})


class TargetVolatility(BaseTransform):
    """
    Computes the target volatility of a time series or cross-section.

    Parameters
    ----------
    target_vol : float, default 0.2
        The target volatility level to scale the series to.
    window_type : str, {'rolling', 'expanding', 'fixed'}, default 'expanding'
        Type of window: 'rolling', 'expanding', or 'fixed'.
    window_size : int, default 30
        Number of periods in the rolling.
    min_periods : int, default 1
        Minimum number of observations in window required to have a value.
    """

    def __init__(self,
                 target_vol: float = 0.2,
                 ann_factor: float = 365,
                 window_type: str = 'expanding',
                 window_size: int = 30,
                 min_periods: int = 1):
        super().__init__(name="TargetVolatility",
                         description="Computes target volatility over time series.")
        self.target_vol = target_vol
        self.ann_factor = ann_factor
        self.window_type = window_type
        self.window_size = window_size
        self.min_periods = min_periods

    def compute(self, returns: Union[pd.Series, pd.DataFrame]) -> pd.DataFrame:
        returns = to_dataframe(returns).copy()
        g = grouped(returns)

        if self.window_type == 'rolling':
            res = g.rolling(window=self.window_size, min_periods=self.min_periods).std()

        elif self.window_type == 'expanding':
            res = g.expanding(min_periods=self.min_periods).std()

        elif self.window_type == 'fixed':
            res = g.std()

        else:
            raise ValueError(f"Unsupported window type: {self.window_type}")

        # Drop level if MultiIndex
        res = maybe_droplevel(res, level=0)

        # Scale to target volatility
        norm_factor = 1 / ((res / self.target_vol) * np.sqrt(self.ann_factor))

        # Scale returns
        scaled_ret = returns * norm_factor

        return to_dataframe(scaled_ret)
