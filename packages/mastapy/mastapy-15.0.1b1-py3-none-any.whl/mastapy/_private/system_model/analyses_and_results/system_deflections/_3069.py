"""SystemDeflectionDrawStyle"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.drawing import _2467

_SYSTEM_DEFLECTION_DRAW_STYLE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "SystemDeflectionDrawStyle",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.geometry import _397
    from mastapy._private.utility_gui import _2054

    Self = TypeVar("Self", bound="SystemDeflectionDrawStyle")
    CastSelf = TypeVar(
        "CastSelf", bound="SystemDeflectionDrawStyle._Cast_SystemDeflectionDrawStyle"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SystemDeflectionDrawStyle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SystemDeflectionDrawStyle:
    """Special nested class for casting SystemDeflectionDrawStyle to subclasses."""

    __parent__: "SystemDeflectionDrawStyle"

    @property
    def contour_draw_style(self: "CastSelf") -> "_2467.ContourDrawStyle":
        return self.__parent__._cast(_2467.ContourDrawStyle)

    @property
    def draw_style_base(self: "CastSelf") -> "_397.DrawStyleBase":
        from mastapy._private.geometry import _397

        return self.__parent__._cast(_397.DrawStyleBase)

    @property
    def system_deflection_draw_style(self: "CastSelf") -> "SystemDeflectionDrawStyle":
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
class SystemDeflectionDrawStyle(_2467.ContourDrawStyle):
    """SystemDeflectionDrawStyle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SYSTEM_DEFLECTION_DRAW_STYLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def show_arrows(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowArrows")

        if temp is None:
            return False

        return temp

    @show_arrows.setter
    @exception_bridge
    @enforce_parameter_types
    def show_arrows(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ShowArrows", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def force_arrow_scaling(self: "Self") -> "_2054.ScalingDrawStyle":
        """mastapy.utility_gui.ScalingDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceArrowScaling")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_SystemDeflectionDrawStyle":
        """Cast to another type.

        Returns:
            _Cast_SystemDeflectionDrawStyle
        """
        return _Cast_SystemDeflectionDrawStyle(self)
