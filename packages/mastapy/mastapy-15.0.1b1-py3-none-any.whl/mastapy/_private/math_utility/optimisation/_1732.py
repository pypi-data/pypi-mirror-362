"""ParetoOptimisationOutput"""

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
from mastapy._private.math_utility.optimisation import _1737

_PARETO_OPTIMISATION_OUTPUT = python_net_import(
    "SMT.MastaAPI.MathUtility.Optimisation", "ParetoOptimisationOutput"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility.optimisation import _1738

    Self = TypeVar("Self", bound="ParetoOptimisationOutput")
    CastSelf = TypeVar(
        "CastSelf", bound="ParetoOptimisationOutput._Cast_ParetoOptimisationOutput"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ParetoOptimisationOutput",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ParetoOptimisationOutput:
    """Special nested class for casting ParetoOptimisationOutput to subclasses."""

    __parent__: "ParetoOptimisationOutput"

    @property
    def pareto_optimisation_variable(
        self: "CastSelf",
    ) -> "_1737.ParetoOptimisationVariable":
        return self.__parent__._cast(_1737.ParetoOptimisationVariable)

    @property
    def pareto_optimisation_variable_base(
        self: "CastSelf",
    ) -> "_1738.ParetoOptimisationVariableBase":
        from mastapy._private.math_utility.optimisation import _1738

        return self.__parent__._cast(_1738.ParetoOptimisationVariableBase)

    @property
    def pareto_optimisation_output(self: "CastSelf") -> "ParetoOptimisationOutput":
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
class ParetoOptimisationOutput(_1737.ParetoOptimisationVariable):
    """ParetoOptimisationOutput

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PARETO_OPTIMISATION_OUTPUT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def percent(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Percent")

        if temp is None:
            return 0.0

        return temp

    @percent.setter
    @exception_bridge
    @enforce_parameter_types
    def percent(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Percent", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def exclude_from_dominant_candidates_search(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "ExcludeFromDominantCandidatesSearch"
        )

        if temp is None:
            return False

        return temp

    @exclude_from_dominant_candidates_search.setter
    @exception_bridge
    @enforce_parameter_types
    def exclude_from_dominant_candidates_search(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ExcludeFromDominantCandidatesSearch",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_original_design_value(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseOriginalDesignValue")

        if temp is None:
            return False

        return temp

    @use_original_design_value.setter
    @exception_bridge
    @enforce_parameter_types
    def use_original_design_value(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseOriginalDesignValue",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ParetoOptimisationOutput":
        """Cast to another type.

        Returns:
            _Cast_ParetoOptimisationOutput
        """
        return _Cast_ParetoOptimisationOutput(self)
