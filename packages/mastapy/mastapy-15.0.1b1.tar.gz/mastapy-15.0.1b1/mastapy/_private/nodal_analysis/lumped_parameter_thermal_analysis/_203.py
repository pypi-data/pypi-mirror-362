"""FluidChannelCuboidElement"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import _206

_FLUID_CHANNEL_CUBOID_ELEMENT = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.LumpedParameterThermalAnalysis",
    "FluidChannelCuboidElement",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import _218

    Self = TypeVar("Self", bound="FluidChannelCuboidElement")
    CastSelf = TypeVar(
        "CastSelf", bound="FluidChannelCuboidElement._Cast_FluidChannelCuboidElement"
    )


__docformat__ = "restructuredtext en"
__all__ = ("FluidChannelCuboidElement",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FluidChannelCuboidElement:
    """Special nested class for casting FluidChannelCuboidElement to subclasses."""

    __parent__: "FluidChannelCuboidElement"

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
    def fluid_channel_cuboid_element(self: "CastSelf") -> "FluidChannelCuboidElement":
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
class FluidChannelCuboidElement(_206.FluidChannelElement):
    """FluidChannelCuboidElement

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FLUID_CHANNEL_CUBOID_ELEMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_FluidChannelCuboidElement":
        """Cast to another type.

        Returns:
            _Cast_FluidChannelCuboidElement
        """
        return _Cast_FluidChannelCuboidElement(self)
