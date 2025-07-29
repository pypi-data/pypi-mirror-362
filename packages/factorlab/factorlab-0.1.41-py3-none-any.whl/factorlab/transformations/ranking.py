import typing
import pandas as pd
from factorlab.transformations.base import BaseTransform
from factorlab.utils import grouped, maybe_droplevel, to_dataframe


class Rank(BaseTransform):
    """
    Computes ranks or percentile ranks of values along a specified axis.

    Parameters
    ----------
    axis : {'ts', 'cs'}, default 'ts'
        Direction of ranking, either time-series ('ts') or cross-section ('cs').
    percentile : bool, default False
        If True, returns percentile ranks (0-1); otherwise, ordinal ranks.
    window_type : {'fixed', 'rolling', 'expanding'}, default 'expanding'
        Windowing method used for time-series ranking.
    window_size : int, default 30
        Size of the window for rolling computations.
    min_periods : int, default 2
        Minimum observations required in window to produce a value.
    """

    def __init__(self,
                 axis: str = 'ts',
                 percentile: bool = False,
                 window_type: str = 'expanding',
                 window_size: int = 30,
                 min_periods: int = 2):
        super().__init__(name="Rank", description="Ranks values along time or cross-section.")
        self.axis = axis
        self.percentile = percentile
        self.window_type = window_type
        self.window_size = window_size
        self.min_periods = min_periods

    def compute(self, df: typing.Union[pd.Series, pd.DataFrame]) -> pd.DataFrame:
        df = to_dataframe(df).copy()
        multiindex = isinstance(df.index, pd.MultiIndex)

        # Time series ranking
        if self.axis == 'ts':
            g = grouped(df)  # Group by second level if MultiIndex

            if self.window_type == 'rolling':
                rank = g.rolling(window=self.window_size, min_periods=self.min_periods).rank(pct=self.percentile)

            elif self.window_type == 'expanding':
                rank = g.expanding(min_periods=self.min_periods).rank(pct=self.percentile)

            elif self.window_type == 'fixed':
                rank = g.rank(pct=self.percentile)

            else:
                raise ValueError(f"Unsupported window_type: {self.window_type}")

            # If MultiIndex, stack the result to maintain the original structure
            rank = maybe_droplevel(rank, level=0)

        # Cross-sectional ranking
        elif self.axis == 'cs':
            g = grouped(df, axis='cs')  # Group by first level if MultiIndex
            if multiindex:
                rank = g.rank(pct=self.percentile)
            else:
                rank = g.rank(axis=1, pct=self.percentile)

        else:
            raise ValueError(f"Unsupported axis: {self.axis}")

        return to_dataframe(rank)
