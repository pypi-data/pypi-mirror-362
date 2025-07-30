"""OptimizationProperty"""

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

_OPTIMIZATION_PROPERTY = python_net_import(
    "SMT.MastaAPI.MathUtility.Optimisation", "OptimizationProperty"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.optimization.machine_learning import _2454

    Self = TypeVar("Self", bound="OptimizationProperty")
    CastSelf = TypeVar(
        "CastSelf", bound="OptimizationProperty._Cast_OptimizationProperty"
    )


__docformat__ = "restructuredtext en"
__all__ = ("OptimizationProperty",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_OptimizationProperty:
    """Special nested class for casting OptimizationProperty to subclasses."""

    __parent__: "OptimizationProperty"

    @property
    def cylindrical_gear_flank_optimisation_parameter(
        self: "CastSelf",
    ) -> "_2454.CylindricalGearFlankOptimisationParameter":
        from mastapy._private.system_model.optimization.machine_learning import _2454

        return self.__parent__._cast(_2454.CylindricalGearFlankOptimisationParameter)

    @property
    def optimization_property(self: "CastSelf") -> "OptimizationProperty":
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
class OptimizationProperty(_0.APIBase):
    """OptimizationProperty

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _OPTIMIZATION_PROPERTY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def maximum(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Maximum")

        if temp is None:
            return 0.0

        return temp

    @maximum.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Maximum", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def minimum(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Minimum")

        if temp is None:
            return 0.0

        return temp

    @minimum.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Minimum", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def unit(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Unit")

        if temp is None:
            return ""

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_OptimizationProperty":
        """Cast to another type.

        Returns:
            _Cast_OptimizationProperty
        """
        return _Cast_OptimizationProperty(self)
