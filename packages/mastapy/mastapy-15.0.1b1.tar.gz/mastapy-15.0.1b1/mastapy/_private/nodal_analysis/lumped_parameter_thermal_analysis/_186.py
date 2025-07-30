"""ConvectionFace"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import _187

_CONVECTION_FACE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.LumpedParameterThermalAnalysis", "ConvectionFace"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
        _184,
        _202,
        _204,
        _207,
        _219,
    )

    Self = TypeVar("Self", bound="ConvectionFace")
    CastSelf = TypeVar("CastSelf", bound="ConvectionFace._Cast_ConvectionFace")


__docformat__ = "restructuredtext en"
__all__ = ("ConvectionFace",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConvectionFace:
    """Special nested class for casting ConvectionFace to subclasses."""

    __parent__: "ConvectionFace"

    @property
    def convection_face_base(self: "CastSelf") -> "_187.ConvectionFaceBase":
        return self.__parent__._cast(_187.ConvectionFaceBase)

    @property
    def thermal_face(self: "CastSelf") -> "_219.ThermalFace":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _219,
        )

        return self.__parent__._cast(_219.ThermalFace)

    @property
    def channel_convection_face(self: "CastSelf") -> "_184.ChannelConvectionFace":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _184,
        )

        return self.__parent__._cast(_184.ChannelConvectionFace)

    @property
    def fluid_channel_cuboid_convection_face(
        self: "CastSelf",
    ) -> "_202.FluidChannelCuboidConvectionFace":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _202,
        )

        return self.__parent__._cast(_202.FluidChannelCuboidConvectionFace)

    @property
    def fluid_channel_cylindrical_radial_convection_face(
        self: "CastSelf",
    ) -> "_204.FluidChannelCylindricalRadialConvectionFace":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _204,
        )

        return self.__parent__._cast(_204.FluidChannelCylindricalRadialConvectionFace)

    @property
    def generic_convection_face(self: "CastSelf") -> "_207.GenericConvectionFace":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _207,
        )

        return self.__parent__._cast(_207.GenericConvectionFace)

    @property
    def convection_face(self: "CastSelf") -> "ConvectionFace":
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
class ConvectionFace(_187.ConvectionFaceBase):
    """ConvectionFace

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONVECTION_FACE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConvectionFace":
        """Cast to another type.

        Returns:
            _Cast_ConvectionFace
        """
        return _Cast_ConvectionFace(self)
