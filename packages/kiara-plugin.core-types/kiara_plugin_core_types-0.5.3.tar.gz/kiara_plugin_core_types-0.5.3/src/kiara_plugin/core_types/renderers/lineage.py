# -*- coding: utf-8 -*-
import uuid
from typing import Any, Dict, Iterable, Type, Union

import orjson
from pydantic import Field, model_validator

from kiara.api import Kiara, Value
from kiara.exceptions import KiaraException
from kiara.models.values.lineage import ValueLineage
from kiara.renderers import (
    KiaraRenderer,
    KiaraRendererConfig,
    RenderInputsSchema,
    SourceTransformer,
)
from kiara.utils.json import orjson_dumps
from kiara.utils.yaml import StringYAML


class LineageDataInputs(RenderInputsSchema):
    render_style: str = Field(
        description="The style to use for rendering the lineage graph.",
        default="json",
    )
    config: Dict[str, Any] = Field(
        description="Additional, optional configuration for the renderer.",
        default_factory=dict,
    )

    @model_validator(mode="before")
    @classmethod
    def validate_linage_inputs(cls, values):
        result = {}
        result["render_style"] = values.pop("render_style", "json")
        config = values.pop("config", {})
        if config:
            result["config"] = config
        else:
            result["config"] = values
        return result


class LineageDataRendererConfig(KiaraRendererConfig):
    pass


class LineageTransformer(SourceTransformer):
    def __init__(self, kiara: Kiara):
        self._kiara: Kiara = kiara
        super().__init__()

    def retrieve_supported_python_classes(self) -> Iterable[Type]:
        return [Value, ValueLineage, str, uuid.UUID]

    def retrieve_supported_inputs_descs(self) -> Union[str, Iterable[str]]:
        return [
            "a value object",
            "a value alias",
            "a value id",
            "a value lineeage object",
        ]

    def validate_and_transform(self, source: Any) -> Union[ValueLineage, None]:
        if isinstance(source, ValueLineage):
            return source
        value = self._kiara.data_registry.get_value(source)
        return value.lineage


class LineageRendererData(
    KiaraRenderer[ValueLineage, LineageDataInputs, str, LineageDataRendererConfig]
):
    _renderer_name = "lineage_data"
    _renderer_config_cls = LineageDataRendererConfig  # type: ignore
    _inputs_schema = LineageDataInputs  # type: ignore

    def retrieve_doc(self) -> Union[str, None]:
        return "Render a value lineage as data."

    def retrieve_source_transformers(self) -> Iterable[SourceTransformer]:
        return [LineageTransformer(kiara=self._kiara)]

    def retrieve_supported_render_sources(self) -> str:
        return "value"

    def retrieve_supported_render_targets(self) -> Union[Iterable[str], str]:
        return "lineage_data"

    def _render(self, instance: ValueLineage, render_config: LineageDataInputs) -> str:
        render_style = render_config.render_style
        func_name = f"render__{render_style}"
        if not hasattr(self, func_name):
            details = "Available styles:\n\n"
            for attr in dir(self):
                if attr.startswith("render__"):
                    details += f" - {attr.replace('render__', '')}\n"
            raise KiaraException(
                f"Can't render lineage in requested style '{render_style}': style not available.",
                details=details,
            )

        func = getattr(self, func_name)
        result: str = func(lineage=instance, **render_config.config)

        return result

    def render__json(self, lineage: ValueLineage, **config) -> str:
        """Renders a html tree view using ul/li elements in a recursive helper function.

        There's a lot more we can do here, like replacing the value ids with aliases (if the values have one), or have a preview of the value whe hovering over it. This is really just the bare minimum.

        """

        data = lineage.as_dict(**config)
        result: str = orjson_dumps(data, option=orjson.OPT_INDENT_2)
        return result

    def render__yaml(self, lineage: ValueLineage, **config) -> str:
        """Renders a html tree view using ul/li elements in a recursive helper function.

        There's a lot more we can do here, like replacing the value ids with aliases (if the values have one), or have a preview of the value whe hovering over it. This is really just the bare minimum.

        """

        yaml = StringYAML()
        data = lineage.as_dict(**config)
        # we need to make sure there are no objects left...
        data = orjson.loads(orjson_dumps(data))
        result: str = yaml.dump(data)
        return result
