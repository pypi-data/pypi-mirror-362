"""RollingBearingElementLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_designs.rolling import _2376

_ROLLING_BEARING_ELEMENT_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "RollingBearingElementLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RollingBearingElementLoadCase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RollingBearingElementLoadCase._Cast_RollingBearingElementLoadCase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RollingBearingElementLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RollingBearingElementLoadCase:
    """Special nested class for casting RollingBearingElementLoadCase to subclasses."""

    __parent__: "RollingBearingElementLoadCase"

    @property
    def rolling_bearing_element(self: "CastSelf") -> "_2376.RollingBearingElement":
        return self.__parent__._cast(_2376.RollingBearingElement)

    @property
    def rolling_bearing_element_load_case(
        self: "CastSelf",
    ) -> "RollingBearingElementLoadCase":
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
class RollingBearingElementLoadCase(_2376.RollingBearingElement):
    """RollingBearingElementLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROLLING_BEARING_ELEMENT_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_RollingBearingElementLoadCase":
        """Cast to another type.

        Returns:
            _Cast_RollingBearingElementLoadCase
        """
        return _Cast_RollingBearingElementLoadCase(self)
