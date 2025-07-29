# -*- coding: utf-8 -*-
from typing import Any, Dict, List, Mapping, Type, TypeVar, Union

import structlog
from pydantic import Field

from kiara.api import KiaraModule, KiaraModuleConfig, ValueMap, ValueSchema
from kiara.utils.values import create_schema_dict, overlay_constants_and_defaults

log = structlog.getLogger()


class KiaraInputsConfig(KiaraModuleConfig):
    """Base configuration that helps translating module config options into user input schemas."""

    add_inputs: bool = Field(
        description="If set to 'True', parse options will be available as inputs.",
        default=True,
    )
    input_fields: List[str] = Field(
        description="If not empty, only add the fields specified in here to the module inputs schema.",
        default_factory=list,
    )

    def augment_inputs_schema(
        self, inputs_schema: Mapping[str, Union[Mapping[str, Any], ValueSchema]]
    ) -> Mapping[str, Union[Mapping[str, Any], ValueSchema]]:
        if not self.add_inputs:
            return inputs_schema

        result: Dict[str, Any] = dict(inputs_schema)
        # TODO: pydantic refactor

        for field_name, field in self.__class__.model_fields.items():
            if self.input_fields and field_name not in self.input_fields:
                continue

            if field_name in inputs_schema.keys() or field_name in [
                "constants",
                "defaults",
                "add_inputs",
                "input_fields",
            ]:
                log.debug(
                    "ignore.autoadd_input_field",
                    field_name=field_name,
                    reason="field with that name already exists.",
                )
                continue

            kiara_type: Union[None, str] = None

            if field.annotation == bool:  # noqa
                kiara_type = "boolean"
            elif field.annotation == Union[None, int]:
                kiara_type = "integer"
            elif field.annotation == List[str]:
                kiara_type = "list"
            else:
                raise Exception(
                    f"Can't auto-generate inputs schema, type '{field.annotation}' for field '{field_name}' not supported."
                )
            # elif field.shape == SHAPE_LIST:
            #     kiara_type = "list"
            # elif field.shape == SHAPE_DICT:
            #     kiara_type = "dict"
            # elif field.type_ == str:
            #     kiara_type = "string"
            # elif field.type_ == int:
            #     kiara_type = "integer"
            # elif field.type_ == float:
            #     kiara_type = "float"
            # elif issubclass(field.type_, Mapping):
            #     kiara_type = "dict"
            # elif issubclass(field.type_, List):
            #     kiara_type = "list"

            result[field_name] = {
                "type": kiara_type,
                "doc": field.description,
                "optional": not field.is_required(),
            }
            if field.default:
                result[field_name]["default"] = field.default
            elif field.default_factory:
                result[field_name]["default"] = field.default_factory()  # type: ignore

        return result


KIARA_INPUTS_CONFIG = TypeVar("KIARA_INPUTS_CONFIG", bound=KiaraInputsConfig)


class AutoInputsKiaraModule(KiaraModule):
    """Base class for kiara modules that want to expose module configuration via user inputs."""

    _config_cls: Type[KIARA_INPUTS_CONFIG] = KiaraInputsConfig  # type: ignore
    _is_abstract = True

    def _create_inputs_schema(self) -> None:
        """Assemble the inputs schema and assign it to the approriate instance attributes."""

        try:
            _input_schemas_data = self.create_inputs_schema()
            _input_schemas_data = self.config.augment_inputs_schema(
                inputs_schema=_input_schemas_data
            )

            if _input_schemas_data is None:
                raise Exception(
                    f"Invalid inputs implementation for '{self.alias}': no inputs schema"
                )

            if not _input_schemas_data and not self._allow_empty_inputs:
                raise Exception(
                    f"Invalid inputs implementation for '{self.alias}': empty inputs schema"
                )
            try:
                _input_schemas = create_schema_dict(schema_config=_input_schemas_data)
            except Exception as e:
                raise Exception(f"Can't create input schemas for '{self.alias}': {e}")

            defaults = self._config.defaults
            constants = self._config.constants

            for k, v in defaults.items():
                if k not in _input_schemas.keys():
                    raise Exception(
                        f"Can't create inputs for '{self.alias}', invalid default field name '{k}'. Available field names: '{', '.join(_input_schemas.keys())}'"  # type: ignore
                    )

            for k, v in constants.items():
                if k not in _input_schemas.keys():
                    raise Exception(
                        f"Can't create inputs for '{self.alias}', invalid constant field name '{k}'. Available field names: '{', '.join(_input_schemas.keys())}'"  # type: ignore
                    )

            self._inputs_schema, self._constants = overlay_constants_and_defaults(
                _input_schemas, defaults=defaults, constants=constants
            )

        except Exception as e:
            raise Exception(
                f"Can't create input schemas for instance '{self.alias}': {e}"
            )  # type: ignore

    def get_data_for_field(self, field_name: str, inputs: ValueMap) -> Any:
        """Convenience method to quickly access data for a config or input field, depending on the module configuration."""

        if not self.config.add_inputs:
            return self.get_config_value(field_name)

        if self.config.input_fields and field_name not in self.config.input_fields:
            return self.get_config_value(field_name)

        return inputs.get_value_data(field_name=field_name)
