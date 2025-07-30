"""SafetyFactorOptimisationResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

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

_SAFETY_FACTOR_OPTIMISATION_RESULTS = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.Optimisation",
    "SafetyFactorOptimisationResults",
)

if TYPE_CHECKING:
    from typing import Any, List, Type

    from mastapy._private.gears.rating.cylindrical.optimisation import _595

    Self = TypeVar("Self", bound="SafetyFactorOptimisationResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SafetyFactorOptimisationResults._Cast_SafetyFactorOptimisationResults",
    )

T = TypeVar("T", bound="_595.SafetyFactorOptimisationStepResult")

__docformat__ = "restructuredtext en"
__all__ = ("SafetyFactorOptimisationResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SafetyFactorOptimisationResults:
    """Special nested class for casting SafetyFactorOptimisationResults to subclasses."""

    __parent__: "SafetyFactorOptimisationResults"

    @property
    def safety_factor_optimisation_results(
        self: "CastSelf",
    ) -> "SafetyFactorOptimisationResults":
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
class SafetyFactorOptimisationResults(_0.APIBase, Generic[T]):
    """SafetyFactorOptimisationResults

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _SAFETY_FACTOR_OPTIMISATION_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @name.setter
    @exception_bridge
    @enforce_parameter_types
    def name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Name", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def values(self: "Self") -> "List[T]":
        """List[T]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Values")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_SafetyFactorOptimisationResults":
        """Cast to another type.

        Returns:
            _Cast_SafetyFactorOptimisationResults
        """
        return _Cast_SafetyFactorOptimisationResults(self)
