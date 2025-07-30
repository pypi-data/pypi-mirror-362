"""RampOrSteadyStateInputOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility_gui import _2050

_RAMP_OR_STEADY_STATE_INPUT_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.DutyCycleDefinition",
    "RampOrSteadyStateInputOptions",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RampOrSteadyStateInputOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RampOrSteadyStateInputOptions._Cast_RampOrSteadyStateInputOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RampOrSteadyStateInputOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RampOrSteadyStateInputOptions:
    """Special nested class for casting RampOrSteadyStateInputOptions to subclasses."""

    __parent__: "RampOrSteadyStateInputOptions"

    @property
    def column_input_options(self: "CastSelf") -> "_2050.ColumnInputOptions":
        return self.__parent__._cast(_2050.ColumnInputOptions)

    @property
    def ramp_or_steady_state_input_options(
        self: "CastSelf",
    ) -> "RampOrSteadyStateInputOptions":
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
class RampOrSteadyStateInputOptions(_2050.ColumnInputOptions):
    """RampOrSteadyStateInputOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RAMP_OR_STEADY_STATE_INPUT_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_RampOrSteadyStateInputOptions":
        """Cast to another type.

        Returns:
            _Cast_RampOrSteadyStateInputOptions
        """
        return _Cast_RampOrSteadyStateInputOptions(self)
