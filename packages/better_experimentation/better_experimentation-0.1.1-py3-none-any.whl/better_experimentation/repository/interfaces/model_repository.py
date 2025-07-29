from abc import abstractmethod, ABC
from sklearn.base import BaseEstimator
from  typing import Union
from pathlib import Path

from better_experimentation.model.ml_model import MLModel


class IModelRepository(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def load_model_by_obj(self, model_idx: int, model_obj: Union[BaseEstimator]) -> MLModel:
        """Loads models from the instantiated object

        Args:
            model_idx (int): Model incidence for identification
            model_obj (BaseEstimator): Object that is parked the trained model to be loaded

        Raises:
            ValueError: If the instance type is not within the mapping

        Returns:
            MLModel: Model loaded and processed to be used in the testing phases
        """
        pass

    @abstractmethod
    def load_model_by_path(self, pathlib_obj: Path) -> list[MLModel]:
        """Loads models from the path that model is stored

        Args:
            pathlib_obj (Path): Base path where stored models exist loaded in PathLib

        Raises:
            ValueError: If the instance type is not within the mapping

        Returns:
            list[MLModel]: List of models loaded and processed to be used in the testing phases
        """
        pass