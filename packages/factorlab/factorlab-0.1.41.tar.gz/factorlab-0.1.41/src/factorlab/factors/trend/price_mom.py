import pandas as pd
from factorlab.features.factors.trend.core import TrendFactor
from factorlab.features.transformations import Transform


class PriceMomentum(TrendFactor):
    """
    Computes the price momentum trend factor: return over the window_size period,
    optionally normalized and winsorized.
    """

    def compute(self) -> pd.DataFrame:

        # Compute return over lag period (i.e. momentum)
        self.trend = Transform(self.price).diff(lags=self.window_size)

        if self.normalize:
            self.compute_dispersion()
            self.trend = self.trend.div(self.disp, axis=0)

            if self.winsorize is not None:
                self.trend = self.trend.clip(lower=-self.winsorize, upper=self.winsorize)

        return self.gen_factor_name()
