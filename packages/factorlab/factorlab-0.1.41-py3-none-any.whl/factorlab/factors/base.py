from typing import Optional, List
import pandas as pd
from abc import abstractmethod
from factorlab.features.base import Feature


class Factor(Feature):
    """
    Abstract base class for alpha or risk factors in quantitative research.

    Factors are used to capture specific characteristics of financial data
    that can be used to predict returns or assess risk.

    """

    category: Optional[str]
    tags: List[str]

    def __init__(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None
    ):
        super().__init__(name=name, description=description)
        self.category = category
        self.tags = tags or []

    @abstractmethod
    def compute(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Compute the factor values from input DataFrame.
        Must be implemented by subclasses.
        """
        raise NotImplementedError("Each factor must implement compute().")

    def get_metadata(self) -> dict:
        """
        Extend feature metadata to include factor-specific fields like category and tags.
        """
        metadata = super().get_metadata()
        metadata.update({
            "category": self.category,
            "tags": self.tags,
        })
        return metadata

    def __repr__(self):
        return f"<Factor {self.name} ({self.__class__.__name__})>"
