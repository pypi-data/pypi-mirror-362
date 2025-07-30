"""AirGapConvectionFace"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import _187

_AIR_GAP_CONVECTION_FACE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.LumpedParameterThermalAnalysis", "AirGapConvectionFace"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import _219

    Self = TypeVar("Self", bound="AirGapConvectionFace")
    CastSelf = TypeVar(
        "CastSelf", bound="AirGapConvectionFace._Cast_AirGapConvectionFace"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AirGapConvectionFace",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AirGapConvectionFace:
    """Special nested class for casting AirGapConvectionFace to subclasses."""

    __parent__: "AirGapConvectionFace"

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
    def air_gap_convection_face(self: "CastSelf") -> "AirGapConvectionFace":
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
class AirGapConvectionFace(_187.ConvectionFaceBase):
    """AirGapConvectionFace

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AIR_GAP_CONVECTION_FACE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_AirGapConvectionFace":
        """Cast to another type.

        Returns:
            _Cast_AirGapConvectionFace
        """
        return _Cast_AirGapConvectionFace(self)
