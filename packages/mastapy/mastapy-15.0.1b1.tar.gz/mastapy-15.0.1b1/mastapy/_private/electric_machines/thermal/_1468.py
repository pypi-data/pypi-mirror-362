"""EndWindingThermalElement"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import _218

_END_WINDING_THERMAL_ELEMENT = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Thermal", "EndWindingThermalElement"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import _207

    Self = TypeVar("Self", bound="EndWindingThermalElement")
    CastSelf = TypeVar(
        "CastSelf", bound="EndWindingThermalElement._Cast_EndWindingThermalElement"
    )


__docformat__ = "restructuredtext en"
__all__ = ("EndWindingThermalElement",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_EndWindingThermalElement:
    """Special nested class for casting EndWindingThermalElement to subclasses."""

    __parent__: "EndWindingThermalElement"

    @property
    def thermal_element(self: "CastSelf") -> "_218.ThermalElement":
        return self.__parent__._cast(_218.ThermalElement)

    @property
    def end_winding_thermal_element(self: "CastSelf") -> "EndWindingThermalElement":
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
class EndWindingThermalElement(_218.ThermalElement):
    """EndWindingThermalElement

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _END_WINDING_THERMAL_ELEMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def face(self: "Self") -> "_207.GenericConvectionFace":
        """mastapy.nodal_analysis.lumped_parameter_thermal_analysis.GenericConvectionFace

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Face")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_EndWindingThermalElement":
        """Cast to another type.

        Returns:
            _Cast_EndWindingThermalElement
        """
        return _Cast_EndWindingThermalElement(self)
