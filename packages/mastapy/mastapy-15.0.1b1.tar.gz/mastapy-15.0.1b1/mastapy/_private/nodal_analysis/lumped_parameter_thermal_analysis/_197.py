"""CylindricalThermalElement"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import _218

_CYLINDRICAL_THERMAL_ELEMENT = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.LumpedParameterThermalAnalysis",
    "CylindricalThermalElement",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CylindricalThermalElement")
    CastSelf = TypeVar(
        "CastSelf", bound="CylindricalThermalElement._Cast_CylindricalThermalElement"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalThermalElement",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalThermalElement:
    """Special nested class for casting CylindricalThermalElement to subclasses."""

    __parent__: "CylindricalThermalElement"

    @property
    def thermal_element(self: "CastSelf") -> "_218.ThermalElement":
        return self.__parent__._cast(_218.ThermalElement)

    @property
    def cylindrical_thermal_element(self: "CastSelf") -> "CylindricalThermalElement":
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
class CylindricalThermalElement(_218.ThermalElement):
    """CylindricalThermalElement

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_THERMAL_ELEMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalThermalElement":
        """Cast to another type.

        Returns:
            _Cast_CylindricalThermalElement
        """
        return _Cast_CylindricalThermalElement(self)
