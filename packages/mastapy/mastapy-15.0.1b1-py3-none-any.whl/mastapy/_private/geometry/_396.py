"""DrawStyle"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

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
from mastapy._private.geometry import _397

_DRAW_STYLE = python_net_import("SMT.MastaAPI.Geometry", "DrawStyle")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4340,
        _4386,
    )
    from mastapy._private.system_model.drawing import _2473

    Self = TypeVar("Self", bound="DrawStyle")
    CastSelf = TypeVar("CastSelf", bound="DrawStyle._Cast_DrawStyle")


__docformat__ = "restructuredtext en"
__all__ = ("DrawStyle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DrawStyle:
    """Special nested class for casting DrawStyle to subclasses."""

    __parent__: "DrawStyle"

    @property
    def draw_style_base(self: "CastSelf") -> "_397.DrawStyleBase":
        return self.__parent__._cast(_397.DrawStyleBase)

    @property
    def model_view_options_draw_style(
        self: "CastSelf",
    ) -> "_2473.ModelViewOptionsDrawStyle":
        from mastapy._private.system_model.drawing import _2473

        return self.__parent__._cast(_2473.ModelViewOptionsDrawStyle)

    @property
    def cylindrical_gear_geometric_entity_draw_style(
        self: "CastSelf",
    ) -> "_4340.CylindricalGearGeometricEntityDrawStyle":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4340

        return self.__parent__._cast(_4340.CylindricalGearGeometricEntityDrawStyle)

    @property
    def power_flow_draw_style(self: "CastSelf") -> "_4386.PowerFlowDrawStyle":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4386

        return self.__parent__._cast(_4386.PowerFlowDrawStyle)

    @property
    def draw_style(self: "CastSelf") -> "DrawStyle":
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
class DrawStyle(_397.DrawStyleBase):
    """DrawStyle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DRAW_STYLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def outline_axis(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "OutlineAxis")

        if temp is None:
            return False

        return temp

    @outline_axis.setter
    @exception_bridge
    @enforce_parameter_types
    def outline_axis(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "OutlineAxis", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def show_part_labels(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowPartLabels")

        if temp is None:
            return False

        return temp

    @show_part_labels.setter
    @exception_bridge
    @enforce_parameter_types
    def show_part_labels(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ShowPartLabels", bool(value) if value is not None else False
        )

    @property
    def cast_to(self: "Self") -> "_Cast_DrawStyle":
        """Cast to another type.

        Returns:
            _Cast_DrawStyle
        """
        return _Cast_DrawStyle(self)
