"""ForceAndDisplacementResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.math_utility.measured_vectors import _1743

_FORCE_AND_DISPLACEMENT_RESULTS = python_net_import(
    "SMT.MastaAPI.MathUtility.MeasuredVectors", "ForceAndDisplacementResults"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility.measured_vectors import _1748

    Self = TypeVar("Self", bound="ForceAndDisplacementResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ForceAndDisplacementResults._Cast_ForceAndDisplacementResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ForceAndDisplacementResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ForceAndDisplacementResults:
    """Special nested class for casting ForceAndDisplacementResults to subclasses."""

    __parent__: "ForceAndDisplacementResults"

    @property
    def abstract_force_and_displacement_results(
        self: "CastSelf",
    ) -> "_1743.AbstractForceAndDisplacementResults":
        return self.__parent__._cast(_1743.AbstractForceAndDisplacementResults)

    @property
    def force_and_displacement_results(
        self: "CastSelf",
    ) -> "ForceAndDisplacementResults":
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
class ForceAndDisplacementResults(_1743.AbstractForceAndDisplacementResults):
    """ForceAndDisplacementResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FORCE_AND_DISPLACEMENT_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def displacement(self: "Self") -> "_1748.VectorWithLinearAndAngularComponents":
        """mastapy.math_utility.measured_vectors.VectorWithLinearAndAngularComponents

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Displacement")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ForceAndDisplacementResults":
        """Cast to another type.

        Returns:
            _Cast_ForceAndDisplacementResults
        """
        return _Cast_ForceAndDisplacementResults(self)
