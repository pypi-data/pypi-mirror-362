# -*- coding: utf-8 -*-

"""This module contains the value type classes that are used in the ``kiara_plugin.core_types`` package."""

import datetime
from typing import Any, ClassVar, Iterable, Mapping, Type, Union

import orjson

from kiara.data_types import DataTypeCharacteristics, DataTypeConfig
from kiara.data_types.included_core_types import SCALAR_CHARACTERISTICS, AnyType
from kiara.models.python_class import PythonClass
from kiara.models.values.value import SerializedData
from kiara_plugin.core_types.models import KiaraList


class IntegerType(AnyType[int, DataTypeConfig]):
    """An integer."""

    _data_type_name: ClassVar[str] = "integer"

    @classmethod
    def python_class(cls) -> Type:
        return int

    def serialize(self, data: int) -> Union[None, str, "SerializedData"]:
        result = self.serialize_as_json(data)
        return result

    def _retrieve_characteristics(self) -> DataTypeCharacteristics:
        return SCALAR_CHARACTERISTICS

    def parse_python_obj(self, data: Any) -> int:
        return int(data)


class FloatType(AnyType[float, DataTypeConfig]):
    "A float."

    _data_type_name: ClassVar[str] = "float"

    @classmethod
    def python_class(cls) -> Type:
        return float

    def serialize(self, data: float) -> Union[None, str, "SerializedData"]:
        result = self.serialize_as_json(data)
        return result

    def _retrieve_characteristics(self) -> DataTypeCharacteristics:
        return SCALAR_CHARACTERISTICS

    def _validate(cls, value: Any) -> Any:
        if not isinstance(value, float):
            raise ValueError(f"Invalid type '{type(value)}' for float: {value}")


class DateType(AnyType[datetime.datetime, DataTypeConfig]):
    """A date.

    Internally, this will always be represented as a Python ``datetime`` object. Iff provided as input, it can also
    be as string, in which case the [``dateutils.parser.parse``](https://dateutil.readthedocs.io/en/stable/parser.html#dateutil.parser.parse) method will be used to parse the string into a datetime object.
    """

    _data_type_name: ClassVar[str] = "date"

    @classmethod
    def python_class(cls) -> Type:
        return datetime.datetime

    def serialize(self, data: datetime.datetime) -> SerializedData:
        result = self.serialize_as_json(data)
        return result

    def _retrieve_characteristics(self) -> DataTypeCharacteristics:
        return SCALAR_CHARACTERISTICS

    def parse_python_obj(self, data: Any) -> datetime.datetime:
        from dateutil import parser

        if isinstance(data, str):
            d = parser.parse(data)
            return d
        elif isinstance(data, datetime.date):
            _d = datetime.datetime(year=data.year, month=data.month, day=data.day)
            return _d

        raise Exception(f"Can't parse data into a 'datetime' object: {data}")

    def validate(cls, value: Any):
        assert isinstance(value, datetime.datetime)


class ListValueType(AnyType[KiaraList, DataTypeConfig]):
    """A list.

    Backed by the [kiara_plugin.core_types.models.ListModel] class, this data type allows to (optionally) specify
    a schema for the items in the list.
    """

    _data_type_name: ClassVar[str] = "list"

    @classmethod
    def python_class(cls) -> Type:
        result: Type[KiaraList] = KiaraList  # make mypy happy
        return result

    def _retrieve_characteristics(self) -> DataTypeCharacteristics:
        return DataTypeCharacteristics(is_scalar=False, is_json_serializable=True)

    def parse_python_obj(self, data: Any) -> KiaraList:
        python_cls = data.__class__
        _data = None
        _schema = None

        if isinstance(data, Mapping) and "list_data" in data.keys():
            list_model = KiaraList(**data)
            return list_model

        if isinstance(data, Iterable):
            _schema = {"title": "list", "type": "object"}
            _data = data
        elif isinstance(data, str):
            try:
                _data = orjson.loads(data)
                if not isinstance(_data, str) and isinstance(list, Iterable):
                    _schema = {"title": "dict", "type": "object"}
            except Exception:
                if isinstance(_data, str):
                    raise Exception(
                        "Can't create list: can't parse string as json into list."
                    )

        if _data is None or _schema is None:
            raise Exception(f"Invalid data for value type 'list': {data}")

        result = {
            "list_data": _data,
            "item_schema": _schema,
            "python_class": PythonClass.from_class(python_cls).model_dump(),
        }

        result_model = KiaraList(**result)
        return result_model

    def _validate(self, data: KiaraList) -> None:
        if not isinstance(data, KiaraList):
            raise Exception(f"Invalid type: {type(data)}.")

    # def render_as__string(self, value: Value, render_config: Mapping[str, Any]) -> str:
    #
    #     data: ListModel = value.data
    #     return orjson_dumps(data.list_data, option=orjson.OPT_INDENT_2)

    def serialize(self, data: KiaraList) -> SerializedData:
        result = self.serialize_as_json(data.model_dump())
        return result
