"""ManufacturingOperationConstraints"""

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
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_MANUFACTURING_OPERATION_CONSTRAINTS = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.CutterSimulation",
    "ManufacturingOperationConstraints",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ManufacturingOperationConstraints")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ManufacturingOperationConstraints._Cast_ManufacturingOperationConstraints",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ManufacturingOperationConstraints",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ManufacturingOperationConstraints:
    """Special nested class for casting ManufacturingOperationConstraints to subclasses."""

    __parent__: "ManufacturingOperationConstraints"

    @property
    def manufacturing_operation_constraints(
        self: "CastSelf",
    ) -> "ManufacturingOperationConstraints":
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
class ManufacturingOperationConstraints(_0.APIBase):
    """ManufacturingOperationConstraints

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MANUFACTURING_OPERATION_CONSTRAINTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def gear_root_clearance_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "GearRootClearanceFactor")

        if temp is None:
            return 0.0

        return temp

    @gear_root_clearance_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def gear_root_clearance_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "GearRootClearanceFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def gear_tip_clearance_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "GearTipClearanceFactor")

        if temp is None:
            return 0.0

        return temp

    @gear_tip_clearance_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def gear_tip_clearance_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "GearTipClearanceFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ManufacturingOperationConstraints":
        """Cast to another type.

        Returns:
            _Cast_ManufacturingOperationConstraints
        """
        return _Cast_ManufacturingOperationConstraints(self)
