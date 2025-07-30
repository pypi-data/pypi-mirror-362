"""ParetoOptimisationFilter"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_PARETO_OPTIMISATION_FILTER = python_net_import(
    "SMT.MastaAPI.MathUtility.Optimisation", "ParetoOptimisationFilter"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar

    Self = TypeVar("Self", bound="ParetoOptimisationFilter")
    CastSelf = TypeVar(
        "CastSelf", bound="ParetoOptimisationFilter._Cast_ParetoOptimisationFilter"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ParetoOptimisationFilter",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ParetoOptimisationFilter:
    """Special nested class for casting ParetoOptimisationFilter to subclasses."""

    __parent__: "ParetoOptimisationFilter"

    @property
    def pareto_optimisation_filter(self: "CastSelf") -> "ParetoOptimisationFilter":
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
class ParetoOptimisationFilter(_0.APIBase):
    """ParetoOptimisationFilter

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PARETO_OPTIMISATION_FILTER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def filter_range(self: "Self") -> "Tuple[float, float]":
        """Tuple[float, float]"""
        temp = pythonnet_property_get(self.wrapped, "FilterRange")

        if temp is None:
            return None

        value = conversion.pn_to_mp_range(temp)

        if value is None:
            return None

        return value

    @filter_range.setter
    @exception_bridge
    @enforce_parameter_types
    def filter_range(self: "Self", value: "Tuple[float, float]") -> None:
        value = conversion.mp_to_pn_range(value)
        pythonnet_property_set(self.wrapped, "FilterRange", value)

    @property
    @exception_bridge
    def property_(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Property")

        if temp is None:
            return ""

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ParetoOptimisationFilter":
        """Cast to another type.

        Returns:
            _Cast_ParetoOptimisationFilter
        """
        return _Cast_ParetoOptimisationFilter(self)
