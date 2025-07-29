import uuid
from abc import ABC, abstractmethod
import pandas as pd


class BaseTransform(ABC):
    """
    Abstract base class for transformation components in a quant pipeline.

    Provides metadata, chaining interface, and standard structure for reusable transforms.
    """

    def __init__(self, name=None, description=None):
        self.name = name or self.__class__.__name__
        self.description = description
        self.transform_id = str(uuid.uuid4())

    @abstractmethod
    def compute(self, df: pd.DataFrame) -> pd.DataFrame:
        """Each transformation must implement this."""
        pass

    def get_metadata(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "class": self.__class__.__name__,
            "transform_id": self.transform_id,
        }

    def __repr__(self):
        return f"<Transform {self.name} ({self.__class__.__name__})>"
