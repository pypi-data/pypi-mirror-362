import pandas as pd
import numpy as np
from typing import Union

from factorlab.transformations.base import BaseTransform
from factorlab.utils import to_dataframe


class Log(BaseTransform):
    """Computes the natural logarithm of the input values.
    """

    def __init__(self):
        super().__init__(name="Log", description="Computes the natural logarithm of the input values.")

    def compute(self, df: Union[pd.Series, pd.DataFrame]) -> pd.DataFrame:
        df = to_dataframe(df).copy()
        # Ensure all values are positive, as log is undefined for non-positive values
        df[df <= 0] = np.nan
        # Apply log transformation
        df = np.log(df).replace([np.inf, -np.inf], np.nan)

        return df


class SquareRoot(BaseTransform):
    """Computes the square root of the input values.
    """

    def __init__(self):
        super().__init__(name="SquareRoot", description="Computes the square root of the input values.")

    def compute(self, df: Union[pd.Series, pd.DataFrame]) -> pd.DataFrame:
        df = to_dataframe(df).copy()
        # Ensure all values are non-negative, as sqrt is undefined for negative values
        df[df < 0] = np.nan
        # Apply square root transformation
        df = np.sqrt(df).replace([np.inf, -np.inf], np.nan)

        return df


class Square(BaseTransform):
    """Computes the square of the input values.
    """

    def __init__(self):
        super().__init__(name="Square", description="Computes the square of the input values.")

    def compute(self, df: Union[pd.Series, pd.DataFrame]) -> pd.DataFrame:
        df = to_dataframe(df).copy()
        return np.square(df)


class Power(BaseTransform):
    """Computes the power of the input values raised to a specified exponent.

    Parameters
    ----------
    exponent : int
        The exponent to which the input values are raised. Must be a positive integer.
    """

    def __init__(self, exponent: int):
        super().__init__(name="Power", description=f"Computes the power of the input values raised to {exponent}.")
        self.exponent = exponent

    def compute(self, df: Union[pd.Series, pd.DataFrame]) -> pd.DataFrame:
        if not isinstance(self.exponent, int) or self.exponent <= 0:
            raise ValueError("Exponent must be a positive integer.")
        df = to_dataframe(df).copy()
        return np.power(df, self.exponent)
