"""OptimisationResultsPair"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_OPTIMISATION_RESULTS_PAIR = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.Optimisation", "OptimisationResultsPair"
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.gears.rating.cylindrical.optimisation import _594, _595

    Self = TypeVar("Self", bound="OptimisationResultsPair")
    CastSelf = TypeVar(
        "CastSelf", bound="OptimisationResultsPair._Cast_OptimisationResultsPair"
    )

T = TypeVar("T", bound="_595.SafetyFactorOptimisationStepResult")

__docformat__ = "restructuredtext en"
__all__ = ("OptimisationResultsPair",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_OptimisationResultsPair:
    """Special nested class for casting OptimisationResultsPair to subclasses."""

    __parent__: "OptimisationResultsPair"

    @property
    def optimisation_results_pair(self: "CastSelf") -> "OptimisationResultsPair":
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
class OptimisationResultsPair(_0.APIBase, Generic[T]):
    """OptimisationResultsPair

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _OPTIMISATION_RESULTS_PAIR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def results(self: "Self") -> "_594.SafetyFactorOptimisationResults[T]":
        """mastapy.gears.rating.cylindrical.optimisation.SafetyFactorOptimisationResults[T]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Results")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[T](temp)

    @property
    @exception_bridge
    def results_without_warnings(
        self: "Self",
    ) -> "_594.SafetyFactorOptimisationResults[T]":
        """mastapy.gears.rating.cylindrical.optimisation.SafetyFactorOptimisationResults[T]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResultsWithoutWarnings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[T](temp)

    @property
    def cast_to(self: "Self") -> "_Cast_OptimisationResultsPair":
        """Cast to another type.

        Returns:
            _Cast_OptimisationResultsPair
        """
        return _Cast_OptimisationResultsPair(self)
