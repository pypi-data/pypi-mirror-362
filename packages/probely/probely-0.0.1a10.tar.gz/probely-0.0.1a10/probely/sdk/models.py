import importlib
from abc import ABC, abstractmethod
from typing import Type

from pydantic import BaseModel

from probely.sdk.schemas import (
    ExtraHostDataModel,
    FindingDataModel,
    ScanDataModel,
    SequenceDataModel,
    TargetDataModel,
    TargetLabelDataModel,
)


class SdkBaseModel(ABC):
    """
    Base class for all resource models, providing common serialization methods.
    """

    manager = None  # To be assigned in __init__ (circular import workaround)

    @property
    @abstractmethod
    def serializer_class(self) -> Type[BaseModel]:
        pass

    @property
    @abstractmethod
    def manager_class_str(self) -> str:
        pass

    def __init__(self, data_model):
        self._data = data_model

        if not self.__class__.manager and self.manager_class_str:
            module_name, class_name = self.manager_class_str.rsplit(".", 1)
            manager_class = getattr(importlib.import_module(module_name), class_name)
            self.__class__.manager = manager_class()

    def __getattr__(self, name):
        return getattr(self._data, name)

    def to_dict(self, *args, **kwargs) -> dict:
        """
        Serialize the object to a dictionary.
        """
        return self._data.model_dump(*args, **kwargs)

    def to_json(self, *args, **kwargs) -> str:
        """
        Serialize the object to a JSON string.
        """
        return self._data.model_dump_json(*args, **kwargs)


class Finding(SdkBaseModel):
    serializer_class = FindingDataModel
    manager_class_str = "probely.sdk.managers.FindingManager"


class Target(SdkBaseModel):
    serializer_class = TargetDataModel
    manager_class_str = "probely.sdk.managers.TargetManager"

    def start_scan(self):
        return self.manager.start_scan(self)


class TargetLabel(SdkBaseModel):
    serializer_class = TargetLabelDataModel
    manager_class_str = "probely.sdk.managers.TargetLabelManager"


class Scan(SdkBaseModel):
    serializer_class = ScanDataModel
    manager_class_str = "probely.sdk.managers.ScanManager"

    def cancel(self):
        return self.manager.cancel(self)

    def pause(self):
        return self.manager.pause(self)

    def resume(self, ignore_blackout_period: bool = False):
        return self.manager.resume(self, ignore_blackout_period=ignore_blackout_period)


class Sequence(SdkBaseModel):
    serializer_class = SequenceDataModel
    manager_class_str = "probely.sdk.managers.TargetSequenceManager"


class ExtraHost(SdkBaseModel):
    serializer_class = ExtraHostDataModel
    manager_class_str = "probely.sdk.managers.ExtraHostManager"
