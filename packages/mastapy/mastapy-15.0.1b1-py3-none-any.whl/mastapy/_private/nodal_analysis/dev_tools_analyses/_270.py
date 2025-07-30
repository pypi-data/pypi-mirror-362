"""FEModelComponentDrawStyle"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_FE_MODEL_COMPONENT_DRAW_STYLE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses", "FEModelComponentDrawStyle"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FEModelComponentDrawStyle")
    CastSelf = TypeVar(
        "CastSelf", bound="FEModelComponentDrawStyle._Cast_FEModelComponentDrawStyle"
    )


__docformat__ = "restructuredtext en"
__all__ = ("FEModelComponentDrawStyle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FEModelComponentDrawStyle:
    """Special nested class for casting FEModelComponentDrawStyle to subclasses."""

    __parent__: "FEModelComponentDrawStyle"

    @property
    def fe_model_component_draw_style(self: "CastSelf") -> "FEModelComponentDrawStyle":
        return self.__parent__

    def __getattr__(self: "CastSelf", name: str) -> "Any":
        try:
            return self.__getattribute__(name)
        except AttributeError:
            class_name = utility.camel(name)
            raise CastException(
                f'Detected an invalid cast. Cannot cast to type "{class_name}"'
            ) from None


@extended_dataclass(frozen=True, slots=True, weakref_slot=True, eq=False)
class FEModelComponentDrawStyle(_0.APIBase):
    """FEModelComponentDrawStyle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_MODEL_COMPONENT_DRAW_STYLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connectable_components(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ConnectableComponents")

        if temp is None:
            return False

        return temp

    @connectable_components.setter
    @exception_bridge
    @enforce_parameter_types
    def connectable_components(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ConnectableComponents",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def solid_components(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "SolidComponents")

        if temp is None:
            return False

        return temp

    @solid_components.setter
    @exception_bridge
    @enforce_parameter_types
    def solid_components(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "SolidComponents", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def solid_shafts(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "SolidShafts")

        if temp is None:
            return False

        return temp

    @solid_shafts.setter
    @exception_bridge
    @enforce_parameter_types
    def solid_shafts(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "SolidShafts", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def transparent_model(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "TransparentModel")

        if temp is None:
            return False

        return temp

    @transparent_model.setter
    @exception_bridge
    @enforce_parameter_types
    def transparent_model(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TransparentModel",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_FEModelComponentDrawStyle":
        """Cast to another type.

        Returns:
            _Cast_FEModelComponentDrawStyle
        """
        return _Cast_FEModelComponentDrawStyle(self)
