"""PressureRatioInputOptions"""

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
from mastapy._private.utility_gui import _2050

_PRESSURE_RATIO_INPUT_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears.SuperchargerRotorSet",
    "PressureRatioInputOptions",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="PressureRatioInputOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="PressureRatioInputOptions._Cast_PressureRatioInputOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PressureRatioInputOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PressureRatioInputOptions:
    """Special nested class for casting PressureRatioInputOptions to subclasses."""

    __parent__: "PressureRatioInputOptions"

    @property
    def column_input_options(self: "CastSelf") -> "_2050.ColumnInputOptions":
        return self.__parent__._cast(_2050.ColumnInputOptions)

    @property
    def pressure_ratio_input_options(self: "CastSelf") -> "PressureRatioInputOptions":
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
class PressureRatioInputOptions(_2050.ColumnInputOptions):
    """PressureRatioInputOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PRESSURE_RATIO_INPUT_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def reference_pressure(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ReferencePressure")

        if temp is None:
            return 0.0

        return temp

    @reference_pressure.setter
    @exception_bridge
    @enforce_parameter_types
    def reference_pressure(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ReferencePressure",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_PressureRatioInputOptions":
        """Cast to another type.

        Returns:
            _Cast_PressureRatioInputOptions
        """
        return _Cast_PressureRatioInputOptions(self)
