"""ArbitraryThermalElement"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import _218

_ARBITRARY_THERMAL_ELEMENT = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.LumpedParameterThermalAnalysis",
    "ArbitraryThermalElement",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
        _177,
        _191,
    )

    Self = TypeVar("Self", bound="ArbitraryThermalElement")
    CastSelf = TypeVar(
        "CastSelf", bound="ArbitraryThermalElement._Cast_ArbitraryThermalElement"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ArbitraryThermalElement",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ArbitraryThermalElement:
    """Special nested class for casting ArbitraryThermalElement to subclasses."""

    __parent__: "ArbitraryThermalElement"

    @property
    def thermal_element(self: "CastSelf") -> "_218.ThermalElement":
        return self.__parent__._cast(_218.ThermalElement)

    @property
    def air_gap_thermal_element(self: "CastSelf") -> "_177.AirGapThermalElement":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _177,
        )

        return self.__parent__._cast(_177.AirGapThermalElement)

    @property
    def cuboid_wall_thermal_element(
        self: "CastSelf",
    ) -> "_191.CuboidWallThermalElement":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _191,
        )

        return self.__parent__._cast(_191.CuboidWallThermalElement)

    @property
    def arbitrary_thermal_element(self: "CastSelf") -> "ArbitraryThermalElement":
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
class ArbitraryThermalElement(_218.ThermalElement):
    """ArbitraryThermalElement

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ARBITRARY_THERMAL_ELEMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ArbitraryThermalElement":
        """Cast to another type.

        Returns:
            _Cast_ArbitraryThermalElement
        """
        return _Cast_ArbitraryThermalElement(self)
