"""OptimizationVariable"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_OPTIMIZATION_VARIABLE = python_net_import(
    "SMT.MastaAPI.MathUtility.Optimisation", "OptimizationVariable"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.math_utility.bayesian_optimization import _1762
    from mastapy._private.math_utility.optimisation import _1727, _1740
    from mastapy._private.utility.units_and_measurements import _1797

    Self = TypeVar("Self", bound="OptimizationVariable")
    CastSelf = TypeVar(
        "CastSelf", bound="OptimizationVariable._Cast_OptimizationVariable"
    )


__docformat__ = "restructuredtext en"
__all__ = ("OptimizationVariable",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_OptimizationVariable:
    """Special nested class for casting OptimizationVariable to subclasses."""

    __parent__: "OptimizationVariable"

    @property
    def optimization_input(self: "CastSelf") -> "_1727.OptimizationInput":
        from mastapy._private.math_utility.optimisation import _1727

        return self.__parent__._cast(_1727.OptimizationInput)

    @property
    def reporting_optimization_input(
        self: "CastSelf",
    ) -> "_1740.ReportingOptimizationInput":
        from mastapy._private.math_utility.optimisation import _1740

        return self.__parent__._cast(_1740.ReportingOptimizationInput)

    @property
    def bayesian_optimization_variable(
        self: "CastSelf",
    ) -> "_1762.BayesianOptimizationVariable":
        from mastapy._private.math_utility.bayesian_optimization import _1762

        return self.__parent__._cast(_1762.BayesianOptimizationVariable)

    @property
    def optimization_variable(self: "CastSelf") -> "OptimizationVariable":
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
class OptimizationVariable(_0.APIBase):
    """OptimizationVariable

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _OPTIMIZATION_VARIABLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def measurement(self: "Self") -> "_1797.MeasurementBase":
        """mastapy.utility.units_and_measurements.MeasurementBase"""
        temp = pythonnet_property_get(self.wrapped, "Measurement")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @measurement.setter
    @exception_bridge
    @enforce_parameter_types
    def measurement(self: "Self", value: "_1797.MeasurementBase") -> None:
        pythonnet_property_set(self.wrapped, "Measurement", value.wrapped)

    @property
    @exception_bridge
    def results(self: "Self") -> "List[float]":
        """List[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Results")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, float)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_OptimizationVariable":
        """Cast to another type.

        Returns:
            _Cast_OptimizationVariable
        """
        return _Cast_OptimizationVariable(self)
