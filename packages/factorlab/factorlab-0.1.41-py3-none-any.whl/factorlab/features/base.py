from abc import ABC, abstractmethod
import pandas as pd
import uuid
from typing import Optional, List


class Feature(ABC):
    """
    Abstract base class for all feature engineering components in FactorLab.

    A Feature takes in a DataFrame and returns a modified DataFrame
    with one or more new columns.

    Includes metadata, traceability, and optional input validation.
    """

    name: str
    description: Optional[str]
    feature_id: str

    def __init__(self, name: Optional[str] = None, description: Optional[str] = None):
        self.name = name or self.__class__.__name__
        self.description = description
        self.feature_id = str(uuid.uuid4())  # Unique ID for traceability

    @abstractmethod
    def compute(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Compute the feature transformation and return a DataFrame.

        Must be implemented by subclasses.
        """
        raise NotImplementedError("Each feature must implement compute().")

    @property
    def inputs(self) -> List[str]:
        """
        Required input columns for the feature.
        Override in subclasses to enable input validation.
        """
        return []

    def validate_inputs(self, df: pd.DataFrame):
        """
        Validate that all required input columns are present in the DataFrame.
        """
        missing = set(self.inputs) - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns for feature '{self.name}': {missing}")

    def get_metadata(self) -> dict:
        """
        Return feature metadata for logging, reproducibility, or UI.
        """
        return {
            "name": self.name,
            "description": self.description,
            "class": self.__class__.__name__,
            "feature_id": self.feature_id,
            "inputs": self.inputs,
        }

    def __repr__(self):
        return f"<Feature {self.name} ({self.__class__.__name__})>"
