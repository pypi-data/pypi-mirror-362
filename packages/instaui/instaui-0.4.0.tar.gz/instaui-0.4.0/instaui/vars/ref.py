from __future__ import annotations
from typing import Dict, Generic, Literal, Optional, TypeVar, TypedDict
from typing_extensions import Unpack
from instaui.common.jsonable import Jsonable
from instaui.runtime._app import get_current_scope
from instaui.vars._types import InputBindingType, OutputSetType
from instaui.vars.path_var import PathVar

from .mixin_types.var_type import VarMixin
from .mixin_types.py_binding import CanInputMixin, CanOutputMixin
from .mixin_types.observable import ObservableMixin
from .mixin_types.element_binding import ElementBindingMixin
from .mixin_types.pathable import CanPathPropMixin
from .mixin_types.str_format_binding import StrFormatBindingMixin


_T_Value = TypeVar("_T_Value")


class Ref(
    Jsonable,
    PathVar,
    VarMixin,
    ObservableMixin,
    CanInputMixin,
    CanOutputMixin,
    CanPathPropMixin,
    StrFormatBindingMixin,
    ElementBindingMixin[_T_Value],
    Generic[_T_Value],
):
    VAR_TYPE = "var"

    def __init__(
        self, value: Optional[_T_Value] = None, **kwargs: Unpack[RefArgs]
    ) -> None:
        self.value = value  # type: ignore
        scope = get_current_scope()
        self.__register_info = scope.register_ref_task(self)

        self._deep_compare = kwargs.get("deep_compare", False)
        self._storage = kwargs.get("storage", None)
        self._storage_key = kwargs.get("storage_key", None)

    def __to_binding_config(self):
        return {
            "id": self.__register_info.var_id,
            "sid": self.__register_info.scope_id,
        }

    def _to_pathable_binding_config(self) -> Dict:
        return self.__to_binding_config()

    def _to_path_prop_binding_config(self) -> Dict:
        return self.__to_binding_config()

    def _to_observable_config(self):
        return self.__to_binding_config()

    def _to_input_config(self):
        return self.__to_binding_config()

    def _to_output_config(self):
        return self.__to_binding_config()

    def _to_element_binding_config(self):
        return self.__to_binding_config()

    def _to_json_dict(self):
        data = super()._to_json_dict()
        data["id"] = self.__register_info.var_id

        if self._deep_compare is True:
            data["deepCompare"] = True

        if self._storage is not None:
            assert self._storage_key is not None, (
                "storage_key is required when storage is set"
            )
            data["storage"] = {
                "type": self._storage,
                "key": self._storage_key,
            }

        return data

    def _to_event_input_type(self) -> InputBindingType:
        return InputBindingType.Ref

    def _to_event_output_type(self) -> OutputSetType:
        return OutputSetType.Ref


class RefArgs(TypedDict, total=False):
    deep_compare: bool
    storage: Literal["local", "session"]
    storage_key: str
