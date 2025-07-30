"""InitialFill"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.bearings.bearing_results.rolling.skf_module import _2305

_INITIAL_FILL = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule", "InitialFill"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="InitialFill")
    CastSelf = TypeVar("CastSelf", bound="InitialFill._Cast_InitialFill")


__docformat__ = "restructuredtext en"
__all__ = ("InitialFill",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InitialFill:
    """Special nested class for casting InitialFill to subclasses."""

    __parent__: "InitialFill"

    @property
    def skf_calculation_result(self: "CastSelf") -> "_2305.SKFCalculationResult":
        return self.__parent__._cast(_2305.SKFCalculationResult)

    @property
    def initial_fill(self: "CastSelf") -> "InitialFill":
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
class InitialFill(_2305.SKFCalculationResult):
    """InitialFill

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INITIAL_FILL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def ring(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Ring")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def side(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Side")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_InitialFill":
        """Cast to another type.

        Returns:
            _Cast_InitialFill
        """
        return _Cast_InitialFill(self)
