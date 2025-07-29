# -*- coding: utf-8 -*-
from typing import Any, Mapping, Type

import orjson

from kiara.models import KiaraModel
from kiara.models.values.value import SerializedData
from kiara.modules.included_core_modules.serialization import DeserializeValueModule
from kiara.registries.models import ModelRegistry
from kiara_plugin.core_types.data_types.models import KiaraModelList


class LoadKiaraModel(DeserializeValueModule):
    _module_type_name = "load.kiara_model"

    @classmethod
    def retrieve_supported_target_profiles(cls) -> Mapping[str, Type]:
        return {"python_object": KiaraModel}

    @classmethod
    def retrieve_supported_serialization_profile(cls) -> str:
        return "json"

    @classmethod
    def retrieve_serialized_value_type(cls) -> str:
        return "kiara_model"

    def to__python_object(self, data: SerializedData, **config: Any) -> KiaraModel:
        chunks = data.get_serialized_data("data")
        assert chunks.get_number_of_chunks() == 1
        _chunks = list(chunks.get_chunks(as_files=False))
        assert len(_chunks) == 1

        bytes_string: bytes = _chunks[0]  # type: ignore
        model_data = orjson.loads(bytes_string)

        model_id: str = data.data_type_config["kiara_model_id"]
        model_registry = ModelRegistry.instance()
        m_cls = model_registry.get_model_cls(kiara_model_id=model_id)

        obj = m_cls(**model_data)
        return obj


class LoadKiaraModelList(DeserializeValueModule):
    _module_type_name = "load.kiara_model_list"

    @classmethod
    def retrieve_supported_target_profiles(cls) -> Mapping[str, Type]:
        return {"python_object": KiaraModelList}

    @classmethod
    def retrieve_supported_serialization_profile(cls) -> str:
        return "json"

    @classmethod
    def retrieve_serialized_value_type(cls) -> str:
        return "kiara_model_list"

    def to__python_object(self, data: SerializedData, **config: Any) -> KiaraModelList:
        model_id: str = data.data_type_config["kiara_model_id"]
        model_registry = ModelRegistry.instance()
        m_cls = model_registry.get_model_cls(kiara_model_id=model_id)

        items = []

        for chunk_id in sorted(data.get_keys()):
            chunks = data.get_serialized_data(chunk_id)
            assert chunks.get_number_of_chunks() == 1

            _chunks = list(chunks.get_chunks(as_files=False))
            assert len(_chunks) == 1

            bytes_string: bytes = _chunks[0]  # type: ignore
            model_data = orjson.loads(bytes_string)

            _obj = m_cls(**model_data)
            items.append(_obj)

        obj: KiaraModelList[KiaraModel] = KiaraModelList(
            list_items=items, kiara_model_id=model_id
        )
        return obj
