# -*- coding: utf-8 -*-

"""This module contains the metadata (and other) models that are used in the ``kiara_plugin.core_types`` package.

Those models are convenience wrappers that make it easier for *kiara* to find, create, manage and version metadata -- but also
other type of models -- that is attached to data, as well as *kiara* modules.

Metadata models must be a sub-class of [kiara.metadata.MetadataModel][kiara.metadata.MetadataModel]. Other models usually
sub-class a pydantic BaseModel or implement custom base classes.
"""

from typing import TYPE_CHECKING, Any, ClassVar, Dict, Iterable, List, Sequence

from pydantic import BaseModel, Field, PrivateAttr

from kiara.exceptions import KiaraException
from kiara.models.python_class import PythonClass
from kiara.models.values.value_metadata import ValueMetadata
from kiara.registries.models import ModelRegistry
from kiara.utils.hashing import compute_cid

if TYPE_CHECKING:
    from kiara.api import Value
    from kiara_plugin.core_types.data_types.models import KiaraModelList


class KiaraList(BaseModel, Sequence):
    """A list implentation that contains (optional) schema information of the lists items."""

    list_data: List[Any] = Field(description="The data.")
    item_schema: Dict[str, Any] = Field(description="The schema.")
    python_class: PythonClass = Field(
        description="The python class of which model instances are created. This is mostly meant as a hint for client applications."
    )

    _size_cache: int = PrivateAttr(default=None)  # type: ignore
    _hash_cache: int = PrivateAttr(default=None)  # type: ignore
    _data_hash: int = PrivateAttr(default=None)  # type: ignore
    _schema_hash: int = PrivateAttr(default=None)  # type: ignore
    _value_hash: int = PrivateAttr(default=None)  # type: ignore

    @property
    def size(self):
        if self._size_cache is not None:
            return self._size_cache

        self._size_cache = len(self.list_data) + len(self.item_schema)
        return self._size_cache

    @property
    def data_hash(self) -> int:
        if self._data_hash is not None:
            return self._data_hash

        self._data_hash = compute_cid(self.list_data)
        return self._data_hash

    @property
    def schema_hash(self) -> int:
        if self._schema_hash is not None:
            return self._schema_hash

        self._schema_hash = compute_cid(self.item_schema)
        return self._schema_hash

    @property
    def value_hash(self) -> int:
        if self._value_hash is not None:
            return self._value_hash

        obj = {"data": self.data_hash, "item_schema": self.schema_hash}
        self._value_hash = compute_cid(obj)
        return self._value_hash

    def __getitem__(self, item):
        return self.list_data.__getitem__(item)

    def __iter__(self):
        return self.list_data.__iter__()

    def __len__(self):
        return self.list_data.__len__()


class KiaraModelSchemaMetadata(ValueMetadata):
    """File stats."""

    _metadata_key: ClassVar[str] = "kiara_model_schema"

    @classmethod
    def retrieve_supported_data_types(cls) -> Iterable[str]:
        return ["kiara_model", "kiara_model_list"]

    @classmethod
    def create_value_metadata(cls, value: "Value") -> "KiaraModelSchemaMetadata":
        kiara_model_id = value.data_type_config.get("kiara_model_id", None)
        if not kiara_model_id:
            raise KiaraException(
                "No kiara model id found in data type config. This is a bug."
            )

        model_cls = ModelRegistry.instance().get_model_cls(kiara_model_id)

        md = KiaraModelSchemaMetadata(
            kiara_model_id=kiara_model_id, kiara_model_schema=model_cls.schema_json()
        )
        return md

    kiara_model_id: str = Field(
        description="The id of the kiara model that is contained in this list."
    )
    kiara_model_schema: str = Field(description="The (JSON) schema of the model.")


class KiaraModelListMetadata(ValueMetadata):
    """File stats."""

    _metadata_key: ClassVar[str] = "kiara_model_list"

    @classmethod
    def retrieve_supported_data_types(cls) -> Iterable[str]:
        return ["kiara_model_list"]

    @classmethod
    def create_value_metadata(cls, value: "Value") -> "KiaraModelListMetadata":
        model_list: "KiaraModelList" = value.data
        length = len(model_list.list_items)

        md = KiaraModelListMetadata(length=length)
        return md

    length: int = Field(
        description="The number of model instances that are contained in this list."
    )
