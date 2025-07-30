"""FluidChannelCylindricalRadialElement"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import _206

_FLUID_CHANNEL_CYLINDRICAL_RADIAL_ELEMENT = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.LumpedParameterThermalAnalysis",
    "FluidChannelCylindricalRadialElement",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import _218

    Self = TypeVar("Self", bound="FluidChannelCylindricalRadialElement")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FluidChannelCylindricalRadialElement._Cast_FluidChannelCylindricalRadialElement",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FluidChannelCylindricalRadialElement",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FluidChannelCylindricalRadialElement:
    """Special nested class for casting FluidChannelCylindricalRadialElement to subclasses."""

    __parent__: "FluidChannelCylindricalRadialElement"

    @property
    def fluid_channel_element(self: "CastSelf") -> "_206.FluidChannelElement":
        return self.__parent__._cast(_206.FluidChannelElement)

    @property
    def thermal_element(self: "CastSelf") -> "_218.ThermalElement":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _218,
        )

        return self.__parent__._cast(_218.ThermalElement)

    @property
    def fluid_channel_cylindrical_radial_element(
        self: "CastSelf",
    ) -> "FluidChannelCylindricalRadialElement":
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
class FluidChannelCylindricalRadialElement(_206.FluidChannelElement):
    """FluidChannelCylindricalRadialElement

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FLUID_CHANNEL_CYLINDRICAL_RADIAL_ELEMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_FluidChannelCylindricalRadialElement":
        """Cast to another type.

        Returns:
            _Cast_FluidChannelCylindricalRadialElement
        """
        return _Cast_FluidChannelCylindricalRadialElement(self)
