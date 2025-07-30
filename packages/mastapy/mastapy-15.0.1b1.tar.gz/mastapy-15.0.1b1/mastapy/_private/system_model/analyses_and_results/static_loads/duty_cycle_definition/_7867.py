"""MomentInputOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition import (
    _7869,
)

_MOMENT_INPUT_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.DutyCycleDefinition",
    "MomentInputOptions",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility_gui import _2050

    Self = TypeVar("Self", bound="MomentInputOptions")
    CastSelf = TypeVar("CastSelf", bound="MomentInputOptions._Cast_MomentInputOptions")


__docformat__ = "restructuredtext en"
__all__ = ("MomentInputOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MomentInputOptions:
    """Special nested class for casting MomentInputOptions to subclasses."""

    __parent__: "MomentInputOptions"

    @property
    def point_load_input_options(self: "CastSelf") -> "_7869.PointLoadInputOptions":
        return self.__parent__._cast(_7869.PointLoadInputOptions)

    @property
    def column_input_options(self: "CastSelf") -> "_2050.ColumnInputOptions":
        from mastapy._private.utility_gui import _2050

        return self.__parent__._cast(_2050.ColumnInputOptions)

    @property
    def moment_input_options(self: "CastSelf") -> "MomentInputOptions":
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
class MomentInputOptions(_7869.PointLoadInputOptions):
    """MomentInputOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MOMENT_INPUT_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_MomentInputOptions":
        """Cast to another type.

        Returns:
            _Cast_MomentInputOptions
        """
        return _Cast_MomentInputOptions(self)
