"""CylindricalGearOptimizationStep"""

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
from mastapy._private.system_model.optimization import _2445

_CYLINDRICAL_GEAR_OPTIMIZATION_STEP = python_net_import(
    "SMT.MastaAPI.SystemModel.Optimization", "CylindricalGearOptimizationStep"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CylindricalGearOptimizationStep")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearOptimizationStep._Cast_CylindricalGearOptimizationStep",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearOptimizationStep",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearOptimizationStep:
    """Special nested class for casting CylindricalGearOptimizationStep to subclasses."""

    __parent__: "CylindricalGearOptimizationStep"

    @property
    def optimization_step(self: "CastSelf") -> "_2445.OptimizationStep":
        return self.__parent__._cast(_2445.OptimizationStep)

    @property
    def cylindrical_gear_optimization_step(
        self: "CastSelf",
    ) -> "CylindricalGearOptimizationStep":
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
class CylindricalGearOptimizationStep(_2445.OptimizationStep):
    """CylindricalGearOptimizationStep

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_OPTIMIZATION_STEP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def include_extended_tip_contact(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeExtendedTipContact")

        if temp is None:
            return False

        return temp

    @include_extended_tip_contact.setter
    @exception_bridge
    @enforce_parameter_types
    def include_extended_tip_contact(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeExtendedTipContact",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def include_tip_edge_stresses(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeTipEdgeStresses")

        if temp is None:
            return False

        return temp

    @include_tip_edge_stresses.setter
    @exception_bridge
    @enforce_parameter_types
    def include_tip_edge_stresses(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeTipEdgeStresses",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_advanced_ltca(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseAdvancedLTCA")

        if temp is None:
            return False

        return temp

    @use_advanced_ltca.setter
    @exception_bridge
    @enforce_parameter_types
    def use_advanced_ltca(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "UseAdvancedLTCA", bool(value) if value is not None else False
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearOptimizationStep":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearOptimizationStep
        """
        return _Cast_CylindricalGearOptimizationStep(self)
