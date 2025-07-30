"""OptimizationData"""

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
)

_OPTIMIZATION_DATA = python_net_import(
    "SMT.MastaAPI.MathUtility.BayesianOptimization", "OptimizationData"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility.bayesian_optimization import _1769

    Self = TypeVar("Self", bound="OptimizationData")
    CastSelf = TypeVar("CastSelf", bound="OptimizationData._Cast_OptimizationData")


__docformat__ = "restructuredtext en"
__all__ = ("OptimizationData",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_OptimizationData:
    """Special nested class for casting OptimizationData to subclasses."""

    __parent__: "OptimizationData"

    @property
    def optimization_data(self: "CastSelf") -> "OptimizationData":
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
class OptimizationData(_0.APIBase):
    """OptimizationData

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _OPTIMIZATION_DATA

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def constraints_met(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConstraintsMet")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def iteration(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Iteration")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def stage(self: "Self") -> "_1769.OptimizationStage":
        """mastapy.math_utility.bayesian_optimization.OptimizationStage

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Stage")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.MathUtility.BayesianOptimization.OptimizationStage"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.math_utility.bayesian_optimization._1769",
            "OptimizationStage",
        )(value)

    @property
    @exception_bridge
    def target(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Target")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_OptimizationData":
        """Cast to another type.

        Returns:
            _Cast_OptimizationData
        """
        return _Cast_OptimizationData(self)
