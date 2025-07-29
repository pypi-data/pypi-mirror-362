# -*- coding: utf-8 -*-

"""This module contains the value type classes that are used in the ``kiara_plugin.core_types`` package."""

from functools import lru_cache
from typing import Any, ClassVar, Generic, List, Mapping, Type, TypeVar, Union

import structlog
from pydantic import BaseModel, ConfigDict, Field
from rich.syntax import Syntax

from kiara.data_types import DataTypeConfig
from kiara.data_types.included_core_types import AnyType
from kiara.defaults import NO_SERIALIZATION_MARKER
from kiara.exceptions import KiaraException
from kiara.models import KiaraModel
from kiara.models.values.value import SerializedData, Value
from kiara.registries.models import ModelRegistry
from kiara_plugin.core_types.defaults import DEFAULT_MODEL_KEY

logger = structlog.getLogger()


class KiaraModelTypeConfig(DataTypeConfig):
    kiara_model_id: str = Field(
        description="The ID of a registered kiara model.",
        default="you.must.specify.your.own.here",
    )


class KiaraModelType(AnyType[KiaraModel, KiaraModelTypeConfig]):
    """A model."""

    _data_type_name: ClassVar = "kiara_model"
    # _cls_cache: Union[Type[KiaraModel], None] = PrivateAttr(default=None)

    @classmethod
    def data_type_config_class(cls) -> Type[KiaraModelTypeConfig]:
        """The Python class that holds the (optional) configuration for a data type instance."""
        return KiaraModelTypeConfig  # type: ignore

    def serialize(self, data: KiaraModel) -> Union[str, SerializedData]:
        if self.type_config.kiara_model_id is None:
            logger.debug(
                "ignore.serialize_request",
                data_type="kiara_model",
                cls=data.__class__.__name__,
                reason="no model id in type config",
            )
            return NO_SERIALIZATION_MARKER

        _data = {
            "data": {
                "type": "inline-json",
                "inline_data": data.model_dump(),
                "codec": "json",
            },
        }

        serialized_data = {
            "data_type": self.data_type_name,
            "data_type_config": self.type_config.model_dump(),
            "data": _data,
            "serialization_profile": "json",
            "metadata": {
                "environment": {},
                "deserialize": {
                    "python_object": {
                        "module_type": "load.kiara_model",
                        "module_config": {
                            "value_type": "kiara_model",
                            "target_profile": "python_object",
                            "serialization_profile": "json",
                        },
                    }
                },
            },
        }
        from kiara.models.values.value import SerializationResult

        serialized = SerializationResult(**serialized_data)
        return serialized

    @classmethod
    def python_class(cls) -> Type[KiaraModel]:
        result: Type[KiaraModel] = KiaraModel  # make mypy happy
        return result

    @lru_cache(maxsize=1)
    def get_model_cls(self) -> Type[KiaraModel]:
        model_type_id = self.type_config.kiara_model_id
        assert model_type_id is not None

        model_registry = ModelRegistry.instance()

        model_cls: Type[KiaraModel] = model_registry.get_model_cls(
            model_type_id, required_subclass=KiaraModel
        )

        return model_cls

    def parse_python_obj(self, data: Any) -> KiaraModel:
        if isinstance(data, KiaraModel):
            return data
        elif isinstance(data, Mapping):
            return self.get_model_cls()(**data)
        else:
            _data = {DEFAULT_MODEL_KEY: data}
            try:
                result = self.get_model_cls()(**_data)
                return result
            except Exception as e:
                raise KiaraException(
                    msg=f"Can't instantiate model of type '{self.type_config.kiara_model_id}' with data of type '{type(data)}': {e}"
                )

    def _validate(self, value: KiaraModel) -> None:
        if not isinstance(value, KiaraModel):
            raise Exception(f"Invalid type: {type(value)}.")

        if value._kiara_model_id != self.type_config.kiara_model_id:  # type: ignore
            raise Exception(
                f"Invalid model type '{value._kiara_model_id}': expected '{self.type_config.kiara_model_id}'."  # type: ignore
            )

    def _pretty_print_as__terminal_renderable(
        self, value: "Value", render_config: Mapping[str, Any]
    ):
        json_str = value.data.model_dump_json(indent=2)
        return Syntax(json_str, "json", background_color="default")


KIARA_MODEL = TypeVar("KIARA_MODEL", bound=KiaraModel)


class KiaraModelList(BaseModel, Generic[KIARA_MODEL]):
    model_config = ConfigDict(extra="forbid")

    kiara_model_id: str = Field(description="The ID of a registered kiara model.")
    list_items: List[KIARA_MODEL] = Field(
        description="The model instances in the list."
    )


class KiaraModelListType(AnyType[KiaraModelList, KiaraModelTypeConfig]):
    """A model."""

    _data_type_name: ClassVar = "kiara_model_list"

    @classmethod
    def data_type_config_class(cls) -> Type[KiaraModelTypeConfig]:
        """The Python class that holds the (optional) configuration for a data type instance."""
        return KiaraModelTypeConfig  # type: ignore

    def serialize(self, data: KiaraModelList) -> Union[str, SerializedData]:
        if self.type_config.kiara_model_id is None:
            logger.debug(
                "ignore.serialize_request",
                data_type="kiara_model",
                cls=data.__class__.__name__,
                reason="no model id in type config",
            )
            return NO_SERIALIZATION_MARKER

        _data = {
            "data": {
                "type": "inline-json",
                "inline_data": [x.model_dump() for x in data.list_items],
                "codec": "json",
            },
        }

        _data = {}
        for idx, x in enumerate(data.list_items):
            _data[f"item_{idx}"] = {
                "type": "inline-json",
                "inline_data": x.model_dump(),
                "codec": "json",
            }

        serialized_data = {
            "data_type": self.data_type_name,
            "data_type_config": self.type_config.model_dump(),
            "data": _data,
            "serialization_profile": "json",
            "metadata": {
                "environment": {},
                "deserialize": {
                    "python_object": {
                        "module_type": "load.kiara_model_list",
                        "module_config": {
                            "value_type": "kiara_model_list",
                            "target_profile": "python_object",
                            "serialization_profile": "json",
                        },
                    }
                },
            },
        }
        from kiara.models.values.value import SerializationResult

        serialized = SerializationResult(**serialized_data)
        return serialized

    @classmethod
    def python_class(cls) -> Type[KiaraModelList]:
        return KiaraModelList

    @lru_cache(maxsize=1)
    def get_model_cls(self) -> Type[KiaraModel]:
        model_type_id = self.type_config.kiara_model_id
        assert model_type_id is not None

        model_registry = ModelRegistry.instance()

        model_cls: Type[KiaraModel] = model_registry.get_model_cls(
            model_type_id, required_subclass=KiaraModel
        )

        return model_cls

    def parse_python_obj(self, data: Any) -> KiaraModelList[KiaraModel]:
        if isinstance(data, KiaraModelList):
            return data
        elif not isinstance(data, list):
            data = [data]
            # raise KiaraException(msg=f"Can't instantiate model of type '{self.type_config.kiara_model_id}' with data of type '{type(data)}': expected list.")

        result: List[KiaraModel] = []
        for item in data:
            if isinstance(item, KiaraModel):
                result.append(item)
            elif isinstance(item, Mapping):
                model_instance = self.get_model_cls()(**item)
                result.append(model_instance)
            else:
                _data = {DEFAULT_MODEL_KEY: item}
                try:
                    model_instance = self.get_model_cls()(**_data)
                    result.append(model_instance)
                except Exception as e:
                    raise KiaraException(
                        msg=f"Can't instantiate model of type '{self.type_config.kiara_model_id}' with data of type '{type(item)}': {e}"
                    )

        instance: KiaraModelList[KiaraModel] = KiaraModelList[self.get_model_cls()](  # type: ignore
            list_items=result, kiara_model_id=self.type_config.kiara_model_id
        )
        return instance

    def _validate(self, value: Any) -> None:
        if not isinstance(value, KiaraModelList):
            raise Exception(f"Invalid type: {type(value)}.")

        for item in value.list_items:
            if not isinstance(item, KiaraModel):
                raise Exception(f"Invalid type: {type(item)}.")
            if item._kiara_model_id != self.type_config.kiara_model_id:  # type: ignore
                raise Exception(
                    f"Invalid model type '{item._kiara_model_id}': expected '{self.type_config.kiara_model_id}'."  # type: ignore
                )

    def _pretty_print_as__terminal_renderable(
        self, value: "Value", render_config: Mapping[str, Any]
    ):
        json_str = value.data.model_dump_json(indent=2)
        return Syntax(json_str, "json", background_color="default")
