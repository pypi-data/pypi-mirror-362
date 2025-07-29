import pandas as pd
import numpy as np
import warnings
from typing import Union
from factorlab.factors.base import Factor
from factorlab.utils import to_dataframe, grouped


class HighLowSpreadEstimator(Factor):
    """
    Computes the high-low spread estimator from Corwin & Schultz (2011),
    which estimates bid-ask spreads using high/low price ranges over two days.

    This nonparametric estimator is useful for liquidity analysis when quote data is unavailable.

    See: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1106193

    Parameters
    ----------
    high_col : str, default "high"
        Column name for high prices.
    low_col : str, default "low"
        Column name for low prices.
    close_col : str, default "close"
        Column name for close prices.
    output_col : str, default "hl_spread"
        Name of the output column to store the spread estimate.
    frequency : {'d', 'w', 'm'}, default "daily"
        Frequency at which to return the spread estimate.
    """

    def __init__(
        self,
        high_col: str = "high",
        low_col: str = "low",
        close_col: str = "close",
        output_col: str = "hl_spread",
        frequency: str = "d"
    ):
        super().__init__(name="HighLowSpreadEstimator", category="liquidity",
                         tags=["microstructure", "bid-ask", "nonparametric"])
        self.high_col = high_col
        self.low_col = low_col
        self.close_col = close_col
        self.output_col = output_col
        self.frequency = frequency

    @property
    def inputs(self):
        return [self.high_col, self.low_col, self.close_col]

    def compute(self, df: pd.DataFrame) -> pd.DataFrame:
        df = to_dataframe(df).copy()

        # Ensure the DataFrame has the required columns
        self.validate_inputs(df)

        # Preserve shape
        is_multi = isinstance(df.index, pd.MultiIndex)
        df_unstacked = df.unstack().copy() if is_multi else df.copy()

        high = df_unstacked[self.high_col]
        low = df_unstacked[self.low_col]
        close = df_unstacked[self.close_col]

        # Step 1: 2-day highs/lows and midpoint
        high_2d = high.rolling(2).max()
        low_2d = low.rolling(2).min()

        # Step 2: Adjust for overnight gaps
        prev_close = close.shift(1)
        gap_up = low - prev_close
        gap_down = high - prev_close

        high_adj = high.where(gap_down >= 0, high - gap_down)
        low_adj = low.where(gap_down >= 0, low - gap_down)
        high_adj = high_adj.where(gap_up <= 0, high_adj - gap_up)
        low_adj = low_adj.where(gap_up <= 0, low_adj - gap_up)

        # Step 3: Compute B and G
        B = (np.log(high_adj / low_adj)) ** 2 + (np.log(high_adj.shift(1) / low_adj.shift(1))) ** 2
        G = (np.log(high_2d / low_2d)) ** 2

        # Step 4: Compute alpha
        denom = (3 - 2 * np.sqrt(2))
        alpha = (np.sqrt(2 * B) - np.sqrt(B)) / denom - np.sqrt(G / denom)
        alpha = np.clip(alpha, 0, None)

        # Step 5: Compute high-low spread estimator
        S = (2 * (np.exp(alpha) - 1)) / (1 + np.exp(alpha))

        # Step 6: Resample if needed
        freq_map = {"w": "W", "m": "ME"}
        if self.frequency in freq_map:
            S = S.resample(freq_map[self.frequency]).mean()

        # Restore original index structure
        if is_multi:
            S = S.stack().reindex(df.index).to_frame(name=self.output_col)
        else:
            S = S.reindex(df.index).to_frame(name=self.output_col)

        return S


class EDGE(Factor):
    """
    Computes the EDGE bid-ask spread estimator from Open/High/Low/Close prices.

    Based on Ardia, Guidotti, & Kroencke (2024), Journal of Financial Economics.
    https://doi.org/10.1016/j.jfineco.2024.103916

    Parameters
    ----------
    sign : bool, default False
        Whether to return the signed root spread.
    window_type : {'fixed', 'rolling', 'expanding'}, default 'fixed'
        Type of window to apply over the time index.
    window_size : int, default 30
        Size of the rolling window.
    """

    def __init__(self, sign: bool = False, window_type: str = 'fixed', window_size: int = 30):
        super().__init__(name="Edge Estimator", category="liquidity",
                         tags=["microstructure", "bid-ask"])
        self.sign = sign
        self.window_type = window_type
        self.window_size = window_size

    def _compute_edge_series(self, df: pd.DataFrame) -> float:
        if df.shape[0] < 3:
            return np.nan
        try:
            o, h, l, c = df["open"], df["high"], df["low"], df["close"]
        except KeyError:
            raise ValueError("Input DataFrame must contain columns: open, high, low, close")

        o = np.log(o.to_numpy())
        h = np.log(h.to_numpy())
        l = np.log(l.to_numpy())
        c = np.log(c.to_numpy())
        m = (h + l) / 2.

        h1, l1, c1, m1 = h[:-1], l[:-1], c[:-1], m[:-1]
        o, h, l, c, m = o[1:], h[1:], l[1:], c[1:], m[1:]

        r1 = m - o
        r2 = o - m1
        r3 = m - c1
        r4 = c1 - m1
        r5 = o - c1

        tau = np.where(np.isnan(h) | np.isnan(l) | np.isnan(c1), np.nan, (h != l) | (l != c1))
        po1 = tau * np.where(np.isnan(o) | np.isnan(h), np.nan, o != h)
        po2 = tau * np.where(np.isnan(o) | np.isnan(l), np.nan, o != l)
        pc1 = tau * np.where(np.isnan(c1) | np.isnan(h1), np.nan, c1 != h1)
        pc2 = tau * np.where(np.isnan(c1) | np.isnan(l1), np.nan, c1 != l1)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            pt = np.nanmean(tau)
            po = np.nanmean(po1) + np.nanmean(po2)
            pc = np.nanmean(pc1) + np.nanmean(pc2)

            if np.nansum(tau) < 2 or po == 0 or pc == 0:
                return np.nan

            d1 = r1 - np.nanmean(r1) / pt * tau
            d3 = r3 - np.nanmean(r3) / pt * tau
            d5 = r5 - np.nanmean(r5) / pt * tau

            x1 = -4.0 / po * d1 * r2 + -4.0 / pc * d3 * r4
            x2 = -4.0 / po * d1 * r5 + -4.0 / pc * d5 * r4

            e1 = np.nanmean(x1)
            e2 = np.nanmean(x2)
            v1 = np.nanmean(x1 ** 2) - e1 ** 2
            v2 = np.nanmean(x2 ** 2) - e2 ** 2

        vt = v1 + v2
        s2 = (v2 * e1 + v1 * e2) / vt if vt > 0 else (e1 + e2) / 2.
        s = np.sqrt(np.abs(s2))
        return float(s * np.sign(s2)) if self.sign else float(s)

    def compute(self, df: Union[pd.DataFrame, pd.Series]) -> pd.Series:
        df = to_dataframe(df).copy()
        multiindex = isinstance(df.index, pd.MultiIndex)
        g = grouped(df, axis="ts")

        if multiindex:
            results, out = [], None

            for group, gdf in g:
                if self.window_type == "fixed":
                    val = self._compute_edge_series(gdf)
                    out = pd.Series([val], index=[group])  # just the ticker, no datetime
                    results.append(out)

                elif self.window_type == "rolling":
                    idx = gdf.index[self.window_size - 1:]
                    out = pd.Series([
                        self._compute_edge_series(gdf.iloc[i - self.window_size:i])
                        for i in range(self.window_size, len(gdf) + 1)
                    ], index=idx)

                elif self.window_type == "expanding":
                    idx = gdf.index[2:]
                    out = pd.Series([
                        self._compute_edge_series(gdf.iloc[:i])
                        for i in range(3, len(gdf) + 1)
                    ], index=idx)

                results.append(out)

            # Combine all series and sort index
            result = to_dataframe(pd.concat(results).sort_index(), name='bid_ask_spread')

        else:
            if self.window_type == "fixed":
                result = pd.Series(self._compute_edge_series(df), index=[df.index[-1]])

            elif self.window_type == "rolling":
                result = []
                index = g.index[self.window_size - 1:]

                for i in range(self.window_size, len(g) + 1):
                    window = g.iloc[i - self.window_size:i]
                    val = self._compute_edge_series(window)
                    result.append(val)

                result = pd.Series(result, index=index)

            elif self.window_type == "expanding":
                result = []
                index = g.index[2:]

                for i in range(3, len(g) + 1):
                    window = g.iloc[:i]  # expanding window: start from 0 to i
                    val = self._compute_edge_series(window)
                    result.append(val)

                result = pd.Series(result, index=index)

            else:
                raise ValueError(f"Invalid window_type: {self.window_type}")

            result = to_dataframe(result, name='bid_ask_spread').sort_index()

        return result
