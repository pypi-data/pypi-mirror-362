# -*- coding: utf-8 -*-
import re
from typing import Any, Dict, Mapping, Union

from pydantic import Field

from kiara.exceptions import KiaraProcessingException
from kiara.models.module import KiaraModuleConfig
from kiara.models.values.value import Value, ValueMap
from kiara.modules import KiaraModule, ValueMapSchema
from kiara.modules.included_core_modules.filter import FilterModule


class StringFiltersModule(FilterModule):
    _module_type_name = "string.filters"

    @classmethod
    def retrieve_supported_type(cls) -> Union[Dict[str, Any], str]:
        return "string"

    def create_filter_inputs(self, filter_name: str) -> Union[None, ValueMapSchema]:
        if filter_name == "tokens":
            return {
                "filter_tokens": {
                    "type": "list",
                    "doc": "A list of tokens to filter out.",
                    "optional": True,
                },
                "replacement": {
                    "type": "string",
                    "doc": "The string to replace the tokens with.",
                    "default": "",
                },
            }

        return None

    def filter__tokens(self, value: Value, filter_inputs: Mapping[str, Any]):
        tokens = filter_inputs.get("filter_tokens", None)
        if not tokens:
            return None

        repl = filter_inputs.get("replacement")

        result: str = value.data
        for token in tokens:
            result = result.replace(token, repl)  # type: ignore

        return result


class RegexModuleConfig(KiaraModuleConfig):
    regex: str = Field(description="The regex to apply.")
    only_first_match: bool = Field(
        description="Whether to only return the first match, or all matches.",
        default=False,
    )


class RegexModule(KiaraModule):
    """Match a string using a regular expression."""

    _config_cls = RegexModuleConfig
    _module_type_name = "string.match_regex"

    def create_inputs_schema(
        self,
    ) -> ValueMapSchema:
        return {"text": {"type": "string", "doc": "The text to match."}}

    def create_outputs_schema(
        self,
    ) -> ValueMapSchema:
        if self.get_config_value("only_first_match"):
            output_schema = {"text": {"type": "string", "doc": "The first match."}}
        else:
            raise NotImplementedError()

        return output_schema

    def process(self, inputs: ValueMap, outputs: ValueMap) -> None:
        text = inputs.get_value_data("text")
        regex = self.get_config_value("regex")
        matches = re.findall(regex, text)

        if not matches:
            raise KiaraProcessingException(f"No match for regex: {regex}")

        if self.get_config_value("only_first_match"):
            result = matches[0]
        else:
            result = matches

        outputs.set_value("text", result)


class ReplaceModuleConfig(KiaraModuleConfig):
    replacement_map: Dict[str, str] = Field(
        description="A map, containing the strings to be replaced as keys, and the replacements as values."
    )
    default_value: Union[str, None] = Field(
        description="The default value to use if the string to be replaced is not in the replacement map. By default, this just returns the string itself.",
        default=None,
    )


class ReplaceStringModule(KiaraModule):
    """Replace a string if it matches a key in a mapping dictionary."""

    _config_cls = ReplaceModuleConfig
    _module_type_name = "string.replace"

    def create_inputs_schema(
        self,
    ) -> ValueMapSchema:
        return {"text": {"type": "string", "doc": "The input string."}}

    def create_outputs_schema(
        self,
    ) -> ValueMapSchema:
        return {"text": {"type": "string", "doc": "The replaced string."}}

    def process(self, inputs: ValueMap, outputs: ValueMap) -> None:
        text = inputs.get_value_data("text")
        repl_map = self.get_config_value("replacement_map")
        default = self.get_config_value("default_value")

        if text not in repl_map.keys():
            if default is None:
                result = text
            else:
                result = default
        else:
            result = repl_map[text]

        outputs.set_value("text", result)
