"""StressMeasurementShaftAxialBendingTorsionalComponentValues"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_STRESS_MEASUREMENT_SHAFT_AXIAL_BENDING_TORSIONAL_COMPONENT_VALUES = python_net_import(
    "SMT.MastaAPI.Shafts", "StressMeasurementShaftAxialBendingTorsionalComponentValues"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar(
        "Self", bound="StressMeasurementShaftAxialBendingTorsionalComponentValues"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="StressMeasurementShaftAxialBendingTorsionalComponentValues._Cast_StressMeasurementShaftAxialBendingTorsionalComponentValues",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StressMeasurementShaftAxialBendingTorsionalComponentValues",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StressMeasurementShaftAxialBendingTorsionalComponentValues:
    """Special nested class for casting StressMeasurementShaftAxialBendingTorsionalComponentValues to subclasses."""

    __parent__: "StressMeasurementShaftAxialBendingTorsionalComponentValues"

    @property
    def stress_measurement_shaft_axial_bending_torsional_component_values(
        self: "CastSelf",
    ) -> "StressMeasurementShaftAxialBendingTorsionalComponentValues":
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
class StressMeasurementShaftAxialBendingTorsionalComponentValues(_0.APIBase):
    """StressMeasurementShaftAxialBendingTorsionalComponentValues

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _STRESS_MEASUREMENT_SHAFT_AXIAL_BENDING_TORSIONAL_COMPONENT_VALUES
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def axial(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Axial")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Bending")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def torsional(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Torsional")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_StressMeasurementShaftAxialBendingTorsionalComponentValues":
        """Cast to another type.

        Returns:
            _Cast_StressMeasurementShaftAxialBendingTorsionalComponentValues
        """
        return _Cast_StressMeasurementShaftAxialBendingTorsionalComponentValues(self)
