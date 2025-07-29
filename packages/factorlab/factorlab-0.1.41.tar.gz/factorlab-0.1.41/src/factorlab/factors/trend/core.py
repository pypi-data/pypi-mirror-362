from __future__ import annotations
import pandas as pd
from typing import Optional
from abc import ABC, abstractmethod

from factorlab.features.base import Factor
from factorlab.features.transformations.price import VWAP


class TrendFactor(Factor, ABC):
    """
    Base class for all trend-based factors.
    Provides shared attributes and methods for computing trend features.
    """

    def __init__(
        self,
        df: pd.DataFrame,
        window_size: int = 30,
        short_window_size: Optional[int] = None,
        long_window_size: Optional[int] = None,
        window_type: str = "rolling",
        central_tendency: str = "mean",
        window_fcn: Optional[str] = None,
        norm_method: str = "std",
        winsorize: Optional[int] = None,
        vwap: bool = True,
        log: bool = True,
        normalize: bool = True,
        lags: int = 0,
        **kwargs,
    ):
        super().__init__(df=df, **kwargs)  # Initialize base Factor class
        """
        Initialize common parameters for trend factors.
        """
        self.df = df
        self.window_size = window_size
        self.short_window_size = short_window_size
        self.long_window_size = long_window_size
        self.window_type = window_type
        self.central_tendency = central_tendency
        self.window_fcn = window_fcn
        self.norm_method = norm_method
        self.winsorize = winsorize
        self.vwap = vwap
        self.log = log
        self.normalize = normalize
        self.lags = lags
        self.kwargs = kwargs

        self.price = self.compute_price()
        self.trend = None
        self.disp = None

    def compute_price(self) -> pd.DataFrame:
        """
        Computes the input price series, optionally applying VWAP and log transform.
        """
        df = self.df.to_frame().astype('float64') if isinstance(self.df, pd.Series) else self.df.astype('float64')
        price = Transform(df).vwap()[['vwap']] if self.vwap else df.copy()
        return Transform(price).log() if self.log else price

    def compute_dispersion(self) -> pd.DataFrame:
        """
        Computes dispersion (volatility) using selected normalization method.
        """
        if self.norm_method not in ['std', 'iqr', 'mad', 'atr']:
            raise ValueError("Invalid dispersion method. Choose from: std, iqr, atr, mad.")

        if self.norm_method == 'atr':
            self.disp = Transform(self.df).dispersion(
                method='atr',
                window_type=self.window_type,
                window_size=self.window_size,
                min_periods=self.window_size
            )
        else:
            chg = Transform(self.price).diff()
            self.disp = Transform(chg).dispersion(
                method=self.norm_method,
                window_type=self.window_type,
                window_size=self.window_size,
                min_periods=self.window_size
            )

        return self.disp

    def gen_factor_name(self) -> pd.DataFrame:
        """
        Automatically names the output column based on calling method and window size.
        """
        import inspect
        caller = inspect.stack()[1].function
        if isinstance(self.trend, pd.Series):
            self.trend = self.trend.to_frame(f"{caller}_{self.window_size}")
        elif isinstance(self.trend, pd.DataFrame) and self.trend.shape[1] == 1:
            self.trend.columns = [f"{caller}_{self.window_size}"]
        return self.trend.sort_index()

    @abstractmethod
    def compute(self) -> pd.DataFrame:
        """
        Must be implemented by subclasses to compute the trend factor.
        """
        raise NotImplementedError("Subclasses must implement this method.")
