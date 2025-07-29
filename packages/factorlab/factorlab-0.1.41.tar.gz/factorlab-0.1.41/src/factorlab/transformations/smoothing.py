import pandas as pd
from typing import Union, Optional
from factorlab.utils import to_dataframe, grouped
from factorlab.transformations.base import BaseTransform


class WindowSmoother(BaseTransform):
    """
    Applies smoothing techniques using rolling, expanding, or exponentially weighted windows.

    Parameters
    ----------
    window_type : str, {'rolling', 'expanding', 'ewm'}, default 'rolling'
        Type of window applied for smoothing.
    window_size : int, default 30
        Size of the rolling/ewm window.
    central_tendency : str, {'mean', 'median'}, default 'mean'
        Measure of central tendency to apply.
    window_fcn : str or None, default None
        Rolling window function (e.g. 'hann', 'gaussian') if applicable.
    lags : int, default 0
        Number of periods to lag the result.
    kwargs : dict
        Additional arguments passed to the rolling/ewm method.
    """

    def __init__(self,
                 window_type: str = 'rolling',
                 window_size: int = 30,
                 central_tendency: str = 'mean',
                 window_fcn: Optional[str] = None,
                 lags: int = 0,
                 **kwargs):
        super().__init__(name="WindowSmoother", description="Applies rolling, expanding, or ewm smoothing.")
        self.window_type = window_type
        self.window_size = window_size
        self.central_tendency = central_tendency
        self.window_fcn = window_fcn
        self.lags = lags
        self.kwargs = kwargs

    def compute(self, df: Union[pd.Series, pd.DataFrame]) -> Union[pd.Series, pd.DataFrame]:
        df = to_dataframe(df).copy()  # Ensure input is a DataFrame with float64 dtype
        multiindex = isinstance(df.index, pd.MultiIndex)
        g = grouped(df)  # Group by second level if MultiIndex, else return original DataFrame

        # Validate central tendency
        if self.window_type == 'ewm' and self.central_tendency == 'median':
            raise ValueError("Median is not supported for ewm smoothing.")

        # Determine the window operation based on the type
        if self.window_type == 'rolling':
            window_op = g.rolling(window=self.window_size, win_type=self.window_fcn, **self.kwargs)
        elif self.window_type == 'expanding':
            window_op = g.expanding()
        elif self.window_type == 'ewm':
            window_op = g.ewm(span=self.window_size, **self.kwargs)
        else:
            raise ValueError(f"Unsupported window_type: {self.window_type}")

        # Apply mean or median
        if self.central_tendency not in ['mean', 'median']:
            raise ValueError(f"Unsupported central_tendency: {self.central_tendency}")

        # Apply the central tendency function
        smooth_df = getattr(window_op, self.central_tendency)()

        # Handle lagging
        if multiindex:
            smooth_df = smooth_df.droplevel(0).groupby(level=1).shift(self.lags).sort_index()
        else:
            smooth_df = smooth_df.shift(self.lags)

        return to_dataframe(smooth_df)
