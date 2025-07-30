"""CapacitiveTransportFace"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import _219

_CAPACITIVE_TRANSPORT_FACE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.LumpedParameterThermalAnalysis",
    "CapacitiveTransportFace",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CapacitiveTransportFace")
    CastSelf = TypeVar(
        "CastSelf", bound="CapacitiveTransportFace._Cast_CapacitiveTransportFace"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CapacitiveTransportFace",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CapacitiveTransportFace:
    """Special nested class for casting CapacitiveTransportFace to subclasses."""

    __parent__: "CapacitiveTransportFace"

    @property
    def thermal_face(self: "CastSelf") -> "_219.ThermalFace":
        return self.__parent__._cast(_219.ThermalFace)

    @property
    def capacitive_transport_face(self: "CastSelf") -> "CapacitiveTransportFace":
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
class CapacitiveTransportFace(_219.ThermalFace):
    """CapacitiveTransportFace

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CAPACITIVE_TRANSPORT_FACE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CapacitiveTransportFace":
        """Cast to another type.

        Returns:
            _Cast_CapacitiveTransportFace
        """
        return _Cast_CapacitiveTransportFace(self)
