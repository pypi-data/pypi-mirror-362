"""SystemOptimisationGearSet"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)

_SYSTEM_OPTIMISATION_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups",
    "SystemOptimisationGearSet",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SystemOptimisationGearSet")
    CastSelf = TypeVar(
        "CastSelf", bound="SystemOptimisationGearSet._Cast_SystemOptimisationGearSet"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SystemOptimisationGearSet",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SystemOptimisationGearSet:
    """Special nested class for casting SystemOptimisationGearSet to subclasses."""

    __parent__: "SystemOptimisationGearSet"

    @property
    def system_optimisation_gear_set(self: "CastSelf") -> "SystemOptimisationGearSet":
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
class SystemOptimisationGearSet(_0.APIBase):
    """SystemOptimisationGearSet

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SYSTEM_OPTIMISATION_GEAR_SET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def highest_teeth_numbers(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HighestTeethNumbers")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def lowest_teeth_numbers(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LowestTeethNumbers")

        if temp is None:
            return ""

        return temp

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
    def number_of_candidate_designs(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfCandidateDesigns")

        if temp is None:
            return 0

        return temp

    @exception_bridge
    def create_designs(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CreateDesigns")

    @exception_bridge
    def create_designs_dont_attempt_to_fix(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CreateDesignsDontAttemptToFix")

    @property
    def cast_to(self: "Self") -> "_Cast_SystemOptimisationGearSet":
        """Cast to another type.

        Returns:
            _Cast_SystemOptimisationGearSet
        """
        return _Cast_SystemOptimisationGearSet(self)
