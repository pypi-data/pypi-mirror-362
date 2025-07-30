"""DutyCycleResultsForSingleShaft"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_DUTY_CYCLE_RESULTS_FOR_SINGLE_SHAFT = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "DutyCycleResultsForSingleShaft",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.shafts import _19

    Self = TypeVar("Self", bound="DutyCycleResultsForSingleShaft")
    CastSelf = TypeVar(
        "CastSelf",
        bound="DutyCycleResultsForSingleShaft._Cast_DutyCycleResultsForSingleShaft",
    )


__docformat__ = "restructuredtext en"
__all__ = ("DutyCycleResultsForSingleShaft",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DutyCycleResultsForSingleShaft:
    """Special nested class for casting DutyCycleResultsForSingleShaft to subclasses."""

    __parent__: "DutyCycleResultsForSingleShaft"

    @property
    def duty_cycle_results_for_single_shaft(
        self: "CastSelf",
    ) -> "DutyCycleResultsForSingleShaft":
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
class DutyCycleResultsForSingleShaft(_0.APIBase):
    """DutyCycleResultsForSingleShaft

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DUTY_CYCLE_RESULTS_FOR_SINGLE_SHAFT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def duty_cycle_results(self: "Self") -> "_19.ShaftDamageResults":
        """mastapy.shafts.ShaftDamageResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DutyCycleResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_DutyCycleResultsForSingleShaft":
        """Cast to another type.

        Returns:
            _Cast_DutyCycleResultsForSingleShaft
        """
        return _Cast_DutyCycleResultsForSingleShaft(self)
