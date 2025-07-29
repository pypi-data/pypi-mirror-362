import pandas as pd
import numpy as np
from typing import Union, Optional
from sklearn.preprocessing import power_transform

from factorlab.transformations.dispersion import AverageTrueRange, StandardDeviation, IQR, MedianAbsoluteDeviation, \
    Range
from factorlab.utils import to_dataframe, grouped, maybe_droplevel, safe_divide
from factorlab.transformations.base import BaseTransform


class Center(BaseTransform):
    """
    Centers the data by subtracting a central tendency measure (mean, median or mode).

    This transformation is useful for normalizing data to have a central tendency of zero.

    Parameters
    ----------
    method : str or callable, default 'mean'
        Method to compute the center: 'mean', 'median', or a custom callable.
    axis : str, {'ts', 'cs'}, default 'ts'
        Axis to center across: 'ts' = time series, 'cs' = cross-section.
    window_type : str, {'ewm', 'rolling', 'expanding', 'fixed'}, default 'expanding'
        Type of window: 'ewm', 'rolling', 'expanding', or 'fixed'.
    window_size : int, default 30
        Number of periods in the rolling window (ignored for fixed).
    min_periods : int, default 1
        Minimum number of observations in window required to have a value.
    """

    def __init__(self,
                 method: str = 'mean',
                 axis: str = 'ts',
                 window_type: str = 'expanding',
                 window_size: int = 30,
                 min_periods: int = 1):
        super().__init__(name="Center", description="Centers the data by subtracting a central tendency measure.")
        self.method = method
        self.axis = axis
        self.window_type = window_type
        self.window_size = window_size
        self.min_periods = min_periods

    def compute(self, df: Union[pd.DataFrame, pd.Series]) -> pd.DataFrame:
        df = to_dataframe(df).copy()
        g = grouped(df)

        if self.axis == 'ts':

            if self.window_type == 'ewm':
                center = g.ewm(span=self.window_size, min_periods=self.min_periods).mean()

            elif self.window_type == 'rolling':
                center = getattr(g.rolling(window=self.window_size, min_periods=self.min_periods), self.method)()

            elif self.window_type == 'expanding':
                center = getattr(g.expanding(min_periods=self.min_periods), self.method)()

            elif self.window_type == 'fixed':
                center = getattr(g, self.method)()

            else:
                raise ValueError(f"Invalid window_type: {self.window_type}"
                                 f". Must be one of 'ewm', 'rolling', 'expanding', or 'fixed'.")

            # Handle MultiIndex by dropping the first level if necessary
            center = maybe_droplevel(center, level=0)
            # Center the data by subtracting the computed center
            centered = df - center
            return centered

        elif self.axis == 'cs':
            # fixed window
            if isinstance(df.index, pd.MultiIndex):
                center = getattr(df.groupby(level=0), self.method)()
            else:
                center = getattr(df, self.method)(axis=1)

            # Handle MultiIndex by dropping the first level if necessary
            center = maybe_droplevel(center, level=0)
            # Center the data by subtracting the computed center
            centered = df.sub(center, axis=0)
            return centered

        else:
            raise ValueError(f"Invalid axis: {self.axis}. Must be 'ts' or 'cs'.")


class ZScore(BaseTransform):
    """
    Normalizes the data by computing the z-score.

    This transformation is useful for standardizing data to have a mean of 0 and standard deviation of 1.

    Parameters
    ----------
    axis : str, {'ts', 'cs'}, default 'ts'
        Axis to normalize across: 'ts' = time series, 'cs' = cross-section.
    centering : bool, default True
        Whether to center the data before normalization. If True, subtracts the mean.
        If False, uses the raw values.
    window_type : str, {'ewm', 'rolling', 'expanding', 'fixed'}, default 'expanding'
        Type of window: 'ewm', 'rolling', 'expanding', or 'fixed'.
    window_size : int, default 30
        Number of periods in the rolling window (ignored for fixed).
    min_periods : int, default 1
        Minimum number of observations in window required to have a value.
    winsorize : int, optional
        If specified, applies winsorization to the data after computing z-scores.
        This can help reduce the influence of outliers.
    """

    def __init__(self,
                 axis: str = 'ts',
                 centering: bool = True,
                 window_type: str = 'expanding',
                 window_size: int = 10,
                 min_periods: int = 2,
                 winsorize: Optional[int] = None):
        super().__init__(name="ZScore",
                         description="Normalizes the data by computing the z-score.")
        self.axis = axis
        self.centering = centering
        self.window_type = window_type
        self.window_size = window_size
        self.min_periods = min_periods
        self.winsorize = winsorize

    def compute(self, df: Union[pd.DataFrame, pd.Series]) -> pd.DataFrame:
        df = to_dataframe(df).copy()

        if self.centering:
            centered = Center(axis=self.axis, method='mean', window_type=self.window_type,
                            window_size=self.window_size, min_periods=self.min_periods).compute(df)
        else:
            centered = df

        disp = StandardDeviation(axis=self.axis, window_type=self.window_type,
                                 window_size=self.window_size, min_periods=self.min_periods).compute(df)

        # Handle cases where standard deviation is zero to avoid division by zero
        disp = disp.replace(0, np.nan)

        # Compute z-scores
        z_scores = safe_divide(centered, disp)

        # Apply winsorization if specified
        if self.winsorize is not None:
            z_scores = z_scores.clip(lower=-self.winsorize, upper=self.winsorize)

        return z_scores


class RobustZScore(BaseTransform):
    """
    Computes a robust z-score using median and IQR (Interquartile Range).

    This transformation is useful for standardizing data while being less sensitive to outliers.

    Parameters
    ----------
    axis : str, {'ts', 'cs'}, default 'ts'
        Axis to normalize across: 'ts' = time series, 'cs' = cross-section.
    centering : bool, default True
        Whether to center the data before normalization. If True, subtracts the median. If False, uses the raw values.
    window_type : str, {'rolling', 'expanding', 'fixed'}, default 'expanding'
        Type of window: 'rolling', 'expanding', or 'fixed'.
    window_size : int, default 30
        Number of periods in the rolling window (ignored for fixed).
    min_periods : int, default 1
        Minimum number of observations in window required to have a value.
    winsorize : int, optional
        If specified, applies winsorization to the data after computing robust z-scores.
        This can help reduce the influence of outliers.
    """

    def __init__(self,
                 axis: str = 'ts',
                 centering: bool = True,
                 window_type: str = 'expanding',
                 window_size: int = 30,
                 min_periods: int = 1,
                 winsorize: Optional[int] = None):
        super().__init__(name="RobustZScore",
                         description="Computes a robust z-score using median and MAD.")
        self.axis = axis
        self.centering = centering
        self.window_type = window_type
        self.window_size = window_size
        self.min_periods = min_periods
        self.winsorize = winsorize

    def compute(self, df: Union[pd.DataFrame, pd.Series]) -> pd.DataFrame:
        df = to_dataframe(df).copy()

        if self.centering:
            # Compute median
            centered = Center(axis=self.axis, method='median', window_type=self.window_type,
                            window_size=self.window_size, min_periods=self.min_periods).compute(df)
        else:
            centered = df

        # Compute IQR
        disp = IQR(axis=self.axis, window_type=self.window_type,
                   window_size=self.window_size, min_periods=self.min_periods).compute(df)

        # Handle cases where IQR is zero to avoid division by zero
        disp = disp.replace(0, np.nan)

        # Compute robust z-scores
        robust_z_scores = safe_divide(centered, disp)

        # Apply winsorization if specified
        if self.winsorize is not None:
            robust_z_scores = robust_z_scores.clip(lower=-self.winsorize, upper=self.winsorize)

        return robust_z_scores


class ModZScore(BaseTransform):
    """
    Computes the modified z-score using median and MAD (Median Absolute Deviation).

    This transformation is useful for standardizing data while being robust to outliers.

    Parameters
    ----------
    axis : str, {'ts', 'cs'}, default 'ts'
        Axis to normalize across: 'ts' = time series, 'cs' = cross-section.
    centering : bool, default True
        Whether to center the data before normalization. If True, subtracts the median.
    window_type : str, {'ewm', 'rolling', 'expanding', 'fixed'}, default 'expanding'
        Type of window: 'ewm', 'rolling', 'expanding', or 'fixed'.
    window_size : int, default 30
        Number of periods in the rolling window (ignored for fixed).
    min_periods : int, default 1
        Minimum number of observations in window required to have a value.
    winsorize : int, optional
        If specified, applies winsorization to the data after computing modified z-scores.
        This can help reduce the influence of outliers.
    """

    def __init__(self,
                 axis: str = 'ts',
                 centering: bool = True,
                 window_type: str = 'expanding',
                 window_size: int = 30,
                 min_periods: int = 1,
                 winsorize: Optional[int] = None):
        super().__init__(name="ModZScore",
                         description="Computes the modified z-score using median and MAD.")
        self.axis = axis
        self.centering = centering
        self.window_type = window_type
        self.window_size = window_size
        self.min_periods = min_periods
        self.winsorize = winsorize

    def compute(self, df: Union[pd.DataFrame, pd.Series]) -> pd.DataFrame:
        df = to_dataframe(df).copy()

        # Compute median
        centered = Center(axis=self.axis, method='median', window_type=self.window_type,
                        window_size=self.window_size, min_periods=self.min_periods).compute(df)

        # Compute MAD
        mad = MedianAbsoluteDeviation(axis=self.axis, window_type=self.window_type,
                                      window_size=self.window_size, min_periods=self.min_periods).compute(df)

        # Handle cases where MAD is zero to avoid division by zero
        mad = mad.replace(0, np.nan)

        # Compute modified z-scores
        mod_z_scores = safe_divide(centered, mad)

        return mod_z_scores


class Percentile(BaseTransform):
    """
    Computes the specified percentile over a time series or cross-section.

    Parameters
    ----------
    axis : str, {'ts', 'cs'}, default 'ts'
        Whether to compute time series ('ts') or cross-sectional ('cs') percentiles.
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
        super().__init__(name="Percentile",
                         description="Computes percentile rank over time series or cross-section.")
        self.axis = axis
        self.window_type = window_type
        self.window_size = window_size
        self.min_periods = min_periods

    def compute(self, df: Union[pd.Series, pd.DataFrame]) -> pd.DataFrame:
        df = to_dataframe(df).copy()

        if self.axis == 'ts':
            g = grouped(df)

            if self.window_type == 'rolling':
                res = g.rolling(window=self.window_size, min_periods=self.min_periods).rank(pct=True)

            elif self.window_type == 'expanding':
                res = g.expanding(min_periods=self.min_periods).rank(pct=True)

            elif self.window_type == 'fixed':
                res = g.rank(pct=True)

            else:
                raise ValueError(f"Unsupported window type: {self.window_type}")
            # Drop level if MultiIndex
            if self.window_type != 'fixed':
                res = maybe_droplevel(res, level=0)
            return to_dataframe(res)

        elif self.axis == 'cs':
            if isinstance(df.index, pd.MultiIndex):
                percentile = df.groupby(level=0).rank(pct=True)
            else:
                percentile = df.rank(pct=True, axis=1)
            # Convert to DataFrame if needed
            return to_dataframe(percentile)


class MinMaxScaler(BaseTransform):
    """
    Scales the data to a specified range, typically [0, 1].

    This transformation is useful for normalizing data to a common scale.

    Parameters
    ----------
    axis : str, {'ts', 'cs'}, default 'ts'
        Axis to normalize across: 'ts' = time series, 'cs' = cross-section.
    centering : bool, default True
        Whether to center the data before scaling. If True, subtracts the minimum.
    window_type : str, {'ewm', 'rolling', 'expanding', 'fixed'}, default 'expanding'
        Type of window: 'ewm', 'rolling', 'expanding', or 'fixed'.
    window_size : int, default 30
        Number of periods in the rolling window (ignored for fixed).
    min_periods : int, default 1
        Minimum number of observations in window required to have a value.
    """

    def __init__(self,
                 axis: str = 'ts',
                 centering: bool = True,
                 window_type: str = 'expanding',
                 window_size: int = 30,
                 min_periods: int = 1):
        super().__init__(name="MinMaxScaler", description="Scales the data to a specified range.")
        self.axis = axis
        self.centering = centering
        self.window_type = window_type
        self.window_size = window_size
        self.min_periods = min_periods

    def compute(self, df: Union[pd.DataFrame, pd.Series]) -> pd.DataFrame:
        df = to_dataframe(df).copy()

        if self.centering:
            centered = Center(axis=self.axis, method='min', window_type=self.window_type,
                            window_size=self.window_size, min_periods=self.min_periods).compute(df)
        else:
            centered = df

        disp = Range(axis=self.axis, window_type=self.window_type, window_size=self.window_size,
                     min_periods=self.min_periods).compute(df)

        # Handle cases where standard deviation is zero to avoid division by zero
        disp = disp.replace(0, np.nan)

        # Compute min-max scaled values
        min_max_scaled = safe_divide(centered, disp)
        # Clip values to the range [0, 1]
        min_max_scaled = min_max_scaled.clip(lower=0, upper=1)

        return min_max_scaled


class ATRScaler(BaseTransform):
    """
    Scales the data using the Average True Range (ATR).

    This transformation is useful for normalizing data based on volatility.

    Parameters
    ----------
    window_type : str, {'ewm', 'rolling', 'expanding', 'fixed'}, default 'expanding'
        Type of window: 'ewm', 'rolling', 'expanding', or 'fixed'.
    window_size : int, default 30
        Number of periods in the rolling window (ignored for fixed).
    min_periods : int, default 1
        Minimum number of observations in window required to have a value.
    """

    def __init__(self,
                 centering: bool = True,
                 window_type: str = 'expanding',
                 window_size: int = 30,
                 min_periods: int = 1):
        super().__init__(name="ATRScaler", description="Scales the data using the Average True Range (ATR).")
        self.centering = centering
        self.window_type = window_type
        self.window_size = window_size
        self.min_periods = min_periods

    def compute(self, df: Union[pd.DataFrame, pd.Series]) -> pd.DataFrame:
        df = to_dataframe(df).copy()

        if self.centering:
            # Compute median
            centered = Center(axis='ts', method='median', window_type=self.window_type,
                            window_size=self.window_size, min_periods=self.min_periods).compute(df)
        else:
            centered = df

        atr = AverageTrueRange(window_type=self.window_type, window_size=self.window_size,
                               min_periods=self.min_periods).compute(df)

        # Handle cases where ATR is zero to avoid division by zero
        atr = atr.replace(0, np.nan)

        # Scale the data by ATR
        atr_scaled = safe_divide(centered, atr)

        return atr_scaled


class PowerTransform(BaseTransform):
    """
    Applies power transformations ('box-cox' or 'yeo-johnson') to time series or cross-sectional data.

    Parameters
    ----------
    method : str, {'box-cox', 'yeo-johnson'}, default 'box-cox'
        Power transformation method.
    axis : str, {'ts', 'cs'}, default 'ts'
        Axis along which to apply the transformation.
    window_type : str, {'rolling', 'expanding', 'fixed'}, default 'expanding'
        Type of window applied to the transformation.
    window_size : int, default 30
        Size of the moving window.
    min_periods : int, default 2
        Minimum periods for rolling/expanding windows.
    adjustment : float, default 1e-6
        Adjustment for non-positive values (required for box-cox).
    """

    def __init__(self,
                 method: str = 'box-cox',
                 axis: str = 'ts',
                 window_type: str = 'expanding',
                 window_size: int = 30,
                 min_periods: int = 2,
                 adjustment: float = 1e-6):
        super().__init__(name="PowerTransform", description=f"Applies {method} transformation.")
        self.method = method
        self.axis = axis
        self.window_type = window_type
        self.window_size = window_size
        self.min_periods = min_periods
        self.adjustment = adjustment

    def compute(self, df: Union[pd.Series, pd.DataFrame]) -> pd.DataFrame:
        df = to_dataframe(df).copy()
        multiindex = isinstance(df.index, pd.MultiIndex)

        if self.axis == 'ts':
            df_unstacked = df.unstack() if multiindex else df
            df_transformed = pd.DataFrame(index=df_unstacked.index, columns=df_unstacked.columns)

            for col in df_unstacked.columns:
                series = df_unstacked[col]

                if self.window_type == 'rolling':
                    out = []
                    for i in range(self.window_size, len(series) + 1):
                        window = series.iloc[i - self.window_size:i]
                        adjusted = (window - window.min() + self.adjustment).to_frame() \
                            if self.method == 'box-cox' else window.to_frame()
                        transformed = power_transform(adjusted, method=self.method, standardize=True).flatten()
                        out.append(transformed[-1])
                    df_transformed.loc[df_transformed.index[-len(out):], col] = out

                elif self.window_type == 'expanding':
                    out = []
                    for i in range(self.min_periods, len(series) + 1):
                        window = series.iloc[:i]
                        adjusted = (window - window.min() + self.adjustment).to_frame() \
                            if self.method == 'box-cox' else window.to_frame()
                        transformed = power_transform(adjusted, method=self.method, standardize=True).flatten()
                        out.append(transformed[-1])
                    df_transformed.loc[df_transformed.index[-len(out):], col] = out

                elif self.window_type == 'fixed':
                    adjusted = (series - series.min() + self.adjustment).to_frame() \
                        if self.method == 'box-cox' else series.to_frame()
                    transformed = power_transform(adjusted, method=self.method, standardize=True).flatten()
                    df_transformed[col] = transformed

                else:
                    raise ValueError(f"Unsupported window_type: {self.window_type}")

            df_out = df_transformed.stack(future_stack=True).sort_index() if multiindex else df_transformed
            return to_dataframe(df_out).dropna(how='all')

        elif self.axis == 'cs':
            df = df.copy()

            if multiindex:
                if self.method == 'box-cox':
                    df = df - df.groupby(level=0).min() + self.adjustment
                df = df.groupby(level=0, group_keys=False).apply(
                    lambda x: pd.DataFrame(
                        power_transform(x, method=self.method, standardize=True, copy=True),
                        index=x.index, columns=x.columns
                    )
                )
            else:
                if self.method == 'box-cox':
                    df = df.subtract(df.min(axis=1), axis=0) + self.adjustment
                df = pd.DataFrame(
                    power_transform(df.T, method=self.method, standardize=True).T,
                    index=df.index, columns=df.columns
                )

            return to_dataframe(df).dropna(how='all')

        else:
            raise ValueError(f"Unsupported axis: {self.axis}")
