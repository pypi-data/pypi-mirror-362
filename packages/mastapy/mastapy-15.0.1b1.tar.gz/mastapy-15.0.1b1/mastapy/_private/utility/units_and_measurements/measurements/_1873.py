"""MagneticVectorPotential"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.units_and_measurements import _1797

_MAGNETIC_VECTOR_POTENTIAL = python_net_import(
    "SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements", "MagneticVectorPotential"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MagneticVectorPotential")
    CastSelf = TypeVar(
        "CastSelf", bound="MagneticVectorPotential._Cast_MagneticVectorPotential"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MagneticVectorPotential",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MagneticVectorPotential:
    """Special nested class for casting MagneticVectorPotential to subclasses."""

    __parent__: "MagneticVectorPotential"

    @property
    def measurement_base(self: "CastSelf") -> "_1797.MeasurementBase":
        return self.__parent__._cast(_1797.MeasurementBase)

    @property
    def magnetic_vector_potential(self: "CastSelf") -> "MagneticVectorPotential":
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
class MagneticVectorPotential(_1797.MeasurementBase):
    """MagneticVectorPotential

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MAGNETIC_VECTOR_POTENTIAL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_MagneticVectorPotential":
        """Cast to another type.

        Returns:
            _Cast_MagneticVectorPotential
        """
        return _Cast_MagneticVectorPotential(self)
