"""TimeStepInputOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility_gui import _2050

_TIME_STEP_INPUT_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.DutyCycleDefinition",
    "TimeStepInputOptions",
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    Self = TypeVar("Self", bound="TimeStepInputOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="TimeStepInputOptions._Cast_TimeStepInputOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("TimeStepInputOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TimeStepInputOptions:
    """Special nested class for casting TimeStepInputOptions to subclasses."""

    __parent__: "TimeStepInputOptions"

    @property
    def column_input_options(self: "CastSelf") -> "_2050.ColumnInputOptions":
        return self.__parent__._cast(_2050.ColumnInputOptions)

    @property
    def time_step_input_options(self: "CastSelf") -> "TimeStepInputOptions":
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
class TimeStepInputOptions(_2050.ColumnInputOptions):
    """TimeStepInputOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TIME_STEP_INPUT_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def time_increment(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "TimeIncrement")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @time_increment.setter
    @exception_bridge
    @enforce_parameter_types
    def time_increment(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "TimeIncrement", value)

    @property
    def cast_to(self: "Self") -> "_Cast_TimeStepInputOptions":
        """Cast to another type.

        Returns:
            _Cast_TimeStepInputOptions
        """
        return _Cast_TimeStepInputOptions(self)
