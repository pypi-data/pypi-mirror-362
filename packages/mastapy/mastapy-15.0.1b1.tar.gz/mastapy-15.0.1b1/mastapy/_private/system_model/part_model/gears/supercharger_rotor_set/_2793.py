"""BoostPressureInputOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility_gui import _2050

_BOOST_PRESSURE_INPUT_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears.SuperchargerRotorSet",
    "BoostPressureInputOptions",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BoostPressureInputOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="BoostPressureInputOptions._Cast_BoostPressureInputOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BoostPressureInputOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BoostPressureInputOptions:
    """Special nested class for casting BoostPressureInputOptions to subclasses."""

    __parent__: "BoostPressureInputOptions"

    @property
    def column_input_options(self: "CastSelf") -> "_2050.ColumnInputOptions":
        return self.__parent__._cast(_2050.ColumnInputOptions)

    @property
    def boost_pressure_input_options(self: "CastSelf") -> "BoostPressureInputOptions":
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
class BoostPressureInputOptions(_2050.ColumnInputOptions):
    """BoostPressureInputOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BOOST_PRESSURE_INPUT_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_BoostPressureInputOptions":
        """Cast to another type.

        Returns:
            _Cast_BoostPressureInputOptions
        """
        return _Cast_BoostPressureInputOptions(self)
