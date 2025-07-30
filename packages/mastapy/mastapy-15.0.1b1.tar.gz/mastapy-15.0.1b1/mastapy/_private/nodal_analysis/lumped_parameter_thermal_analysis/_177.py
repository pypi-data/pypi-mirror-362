"""AirGapThermalElement"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import _178

_AIR_GAP_THERMAL_ELEMENT = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.LumpedParameterThermalAnalysis", "AirGapThermalElement"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import _218

    Self = TypeVar("Self", bound="AirGapThermalElement")
    CastSelf = TypeVar(
        "CastSelf", bound="AirGapThermalElement._Cast_AirGapThermalElement"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AirGapThermalElement",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AirGapThermalElement:
    """Special nested class for casting AirGapThermalElement to subclasses."""

    __parent__: "AirGapThermalElement"

    @property
    def arbitrary_thermal_element(self: "CastSelf") -> "_178.ArbitraryThermalElement":
        return self.__parent__._cast(_178.ArbitraryThermalElement)

    @property
    def thermal_element(self: "CastSelf") -> "_218.ThermalElement":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _218,
        )

        return self.__parent__._cast(_218.ThermalElement)

    @property
    def air_gap_thermal_element(self: "CastSelf") -> "AirGapThermalElement":
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
class AirGapThermalElement(_178.ArbitraryThermalElement):
    """AirGapThermalElement

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AIR_GAP_THERMAL_ELEMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_AirGapThermalElement":
        """Cast to another type.

        Returns:
            _Cast_AirGapThermalElement
        """
        return _Cast_AirGapThermalElement(self)
