"""GearRatioInputOptions"""

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

_GEAR_RATIO_INPUT_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.DutyCycleDefinition",
    "GearRatioInputOptions",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="GearRatioInputOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="GearRatioInputOptions._Cast_GearRatioInputOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearRatioInputOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearRatioInputOptions:
    """Special nested class for casting GearRatioInputOptions to subclasses."""

    __parent__: "GearRatioInputOptions"

    @property
    def column_input_options(self: "CastSelf") -> "_2050.ColumnInputOptions":
        return self.__parent__._cast(_2050.ColumnInputOptions)

    @property
    def gear_ratio_input_options(self: "CastSelf") -> "GearRatioInputOptions":
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
class GearRatioInputOptions(_2050.ColumnInputOptions):
    """GearRatioInputOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_RATIO_INPUT_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def has_gear_ratio_column(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HasGearRatioColumn")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def tolerance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Tolerance")

        if temp is None:
            return 0.0

        return temp

    @tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def tolerance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Tolerance", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_GearRatioInputOptions":
        """Cast to another type.

        Returns:
            _Cast_GearRatioInputOptions
        """
        return _Cast_GearRatioInputOptions(self)
