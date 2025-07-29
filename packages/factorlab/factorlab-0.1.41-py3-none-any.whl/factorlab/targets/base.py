from abc import ABC, abstractmethod
import pandas as pd
import uuid
from typing import Optional, Union


class Target(ABC):
    """
    Base class for supervised learning targets.

    A Target takes in a DataFrame and outputs a Series or DataFrame.
    """

    name: str
    description: Optional[str] = None
    target_id: str

    def __init__(self, name: Optional[str] = None, description: Optional[str] = None):
        self.name = name if name else self.__class__.__name__
        self.description = description
        self.target_id = str(uuid.uuid4())

    @abstractmethod
    def compute(self, df: pd.DataFrame) -> Union[pd.Series, pd.DataFrame]:
        """Compute a target variable for supervised learning."""
        raise NotImplementedError("Each target must implement compute().")

    def get_metadata(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "class": self.__class__.__name__,
            "target_id": self.target_id,
        }

    def __repr__(self):
        return f"<Target {self.name} ({self.__class__.__name__})>"
