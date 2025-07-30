"""FluidChannelCuboidConvectionFace"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import _184

_FLUID_CHANNEL_CUBOID_CONVECTION_FACE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.LumpedParameterThermalAnalysis",
    "FluidChannelCuboidConvectionFace",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
        _186,
        _187,
        _219,
    )

    Self = TypeVar("Self", bound="FluidChannelCuboidConvectionFace")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FluidChannelCuboidConvectionFace._Cast_FluidChannelCuboidConvectionFace",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FluidChannelCuboidConvectionFace",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FluidChannelCuboidConvectionFace:
    """Special nested class for casting FluidChannelCuboidConvectionFace to subclasses."""

    __parent__: "FluidChannelCuboidConvectionFace"

    @property
    def channel_convection_face(self: "CastSelf") -> "_184.ChannelConvectionFace":
        return self.__parent__._cast(_184.ChannelConvectionFace)

    @property
    def convection_face(self: "CastSelf") -> "_186.ConvectionFace":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _186,
        )

        return self.__parent__._cast(_186.ConvectionFace)

    @property
    def convection_face_base(self: "CastSelf") -> "_187.ConvectionFaceBase":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _187,
        )

        return self.__parent__._cast(_187.ConvectionFaceBase)

    @property
    def thermal_face(self: "CastSelf") -> "_219.ThermalFace":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _219,
        )

        return self.__parent__._cast(_219.ThermalFace)

    @property
    def fluid_channel_cuboid_convection_face(
        self: "CastSelf",
    ) -> "FluidChannelCuboidConvectionFace":
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
class FluidChannelCuboidConvectionFace(_184.ChannelConvectionFace):
    """FluidChannelCuboidConvectionFace

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FLUID_CHANNEL_CUBOID_CONVECTION_FACE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_FluidChannelCuboidConvectionFace":
        """Cast to another type.

        Returns:
            _Cast_FluidChannelCuboidConvectionFace
        """
        return _Cast_FluidChannelCuboidConvectionFace(self)
