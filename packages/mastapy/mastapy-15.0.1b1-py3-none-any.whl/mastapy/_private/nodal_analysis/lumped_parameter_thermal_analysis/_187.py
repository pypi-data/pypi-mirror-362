"""ConvectionFaceBase"""

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
from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import _219

_CONVECTION_FACE_BASE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.LumpedParameterThermalAnalysis", "ConvectionFaceBase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
        _176,
        _184,
        _186,
        _202,
        _204,
        _207,
        _223,
    )

    Self = TypeVar("Self", bound="ConvectionFaceBase")
    CastSelf = TypeVar("CastSelf", bound="ConvectionFaceBase._Cast_ConvectionFaceBase")


__docformat__ = "restructuredtext en"
__all__ = ("ConvectionFaceBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConvectionFaceBase:
    """Special nested class for casting ConvectionFaceBase to subclasses."""

    __parent__: "ConvectionFaceBase"

    @property
    def thermal_face(self: "CastSelf") -> "_219.ThermalFace":
        return self.__parent__._cast(_219.ThermalFace)

    @property
    def air_gap_convection_face(self: "CastSelf") -> "_176.AirGapConvectionFace":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _176,
        )

        return self.__parent__._cast(_176.AirGapConvectionFace)

    @property
    def channel_convection_face(self: "CastSelf") -> "_184.ChannelConvectionFace":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _184,
        )

        return self.__parent__._cast(_184.ChannelConvectionFace)

    @property
    def convection_face(self: "CastSelf") -> "_186.ConvectionFace":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _186,
        )

        return self.__parent__._cast(_186.ConvectionFace)

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
    def convection_face_base(self: "CastSelf") -> "ConvectionFaceBase":
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
class ConvectionFaceBase(_219.ThermalFace):
    """ConvectionFaceBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONVECTION_FACE_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def user_defined_heat_transfer_coefficient(
        self: "Self",
    ) -> "_223.UserDefinedHeatTransferCoefficient":
        """mastapy.nodal_analysis.lumped_parameter_thermal_analysis.UserDefinedHeatTransferCoefficient

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "UserDefinedHeatTransferCoefficient"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConvectionFaceBase":
        """Cast to another type.

        Returns:
            _Cast_ConvectionFaceBase
        """
        return _Cast_ConvectionFaceBase(self)
