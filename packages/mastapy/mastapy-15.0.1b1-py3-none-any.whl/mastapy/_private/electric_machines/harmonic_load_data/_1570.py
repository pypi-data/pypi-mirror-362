"""StatorToothLoadInterpolator"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.electric_machines.harmonic_load_data import _1569

_STATOR_TOOTH_LOAD_INTERPOLATOR = python_net_import(
    "SMT.MastaAPI.ElectricMachines.HarmonicLoadData", "StatorToothLoadInterpolator"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="StatorToothLoadInterpolator")
    CastSelf = TypeVar(
        "CastSelf",
        bound="StatorToothLoadInterpolator._Cast_StatorToothLoadInterpolator",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StatorToothLoadInterpolator",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StatorToothLoadInterpolator:
    """Special nested class for casting StatorToothLoadInterpolator to subclasses."""

    __parent__: "StatorToothLoadInterpolator"

    @property
    def stator_tooth_interpolator(self: "CastSelf") -> "_1569.StatorToothInterpolator":
        return self.__parent__._cast(_1569.StatorToothInterpolator)

    @property
    def stator_tooth_load_interpolator(
        self: "CastSelf",
    ) -> "StatorToothLoadInterpolator":
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
class StatorToothLoadInterpolator(_1569.StatorToothInterpolator):
    """StatorToothLoadInterpolator

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STATOR_TOOTH_LOAD_INTERPOLATOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def spatial_force_absolute_tolerance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpatialForceAbsoluteTolerance")

        if temp is None:
            return 0.0

        return temp

    @spatial_force_absolute_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def spatial_force_absolute_tolerance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpatialForceAbsoluteTolerance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def spatial_force_relative_tolerance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpatialForceRelativeTolerance")

        if temp is None:
            return 0.0

        return temp

    @spatial_force_relative_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def spatial_force_relative_tolerance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpatialForceRelativeTolerance",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_StatorToothLoadInterpolator":
        """Cast to another type.

        Returns:
            _Cast_StatorToothLoadInterpolator
        """
        return _Cast_StatorToothLoadInterpolator(self)
