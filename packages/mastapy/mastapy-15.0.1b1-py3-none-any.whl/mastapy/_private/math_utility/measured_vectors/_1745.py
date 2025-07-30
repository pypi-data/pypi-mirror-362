"""ForceResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.math_utility.measured_vectors import _1743

_FORCE_RESULTS = python_net_import(
    "SMT.MastaAPI.MathUtility.MeasuredVectors", "ForceResults"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ForceResults")
    CastSelf = TypeVar("CastSelf", bound="ForceResults._Cast_ForceResults")


__docformat__ = "restructuredtext en"
__all__ = ("ForceResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ForceResults:
    """Special nested class for casting ForceResults to subclasses."""

    __parent__: "ForceResults"

    @property
    def abstract_force_and_displacement_results(
        self: "CastSelf",
    ) -> "_1743.AbstractForceAndDisplacementResults":
        return self.__parent__._cast(_1743.AbstractForceAndDisplacementResults)

    @property
    def force_results(self: "CastSelf") -> "ForceResults":
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
class ForceResults(_1743.AbstractForceAndDisplacementResults):
    """ForceResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FORCE_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ForceResults":
        """Cast to another type.

        Returns:
            _Cast_ForceResults
        """
        return _Cast_ForceResults(self)
