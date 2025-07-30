"""CylindricalAxialThermalFace"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import _219

_CYLINDRICAL_AXIAL_THERMAL_FACE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.LumpedParameterThermalAnalysis",
    "CylindricalAxialThermalFace",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CylindricalAxialThermalFace")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalAxialThermalFace._Cast_CylindricalAxialThermalFace",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalAxialThermalFace",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalAxialThermalFace:
    """Special nested class for casting CylindricalAxialThermalFace to subclasses."""

    __parent__: "CylindricalAxialThermalFace"

    @property
    def thermal_face(self: "CastSelf") -> "_219.ThermalFace":
        return self.__parent__._cast(_219.ThermalFace)

    @property
    def cylindrical_axial_thermal_face(
        self: "CastSelf",
    ) -> "CylindricalAxialThermalFace":
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
class CylindricalAxialThermalFace(_219.ThermalFace):
    """CylindricalAxialThermalFace

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_AXIAL_THERMAL_FACE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalAxialThermalFace":
        """Cast to another type.

        Returns:
            _Cast_CylindricalAxialThermalFace
        """
        return _Cast_CylindricalAxialThermalFace(self)
