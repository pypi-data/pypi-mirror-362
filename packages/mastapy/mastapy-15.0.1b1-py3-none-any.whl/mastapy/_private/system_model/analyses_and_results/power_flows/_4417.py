"""ToothPassingHarmonic"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_TOOTH_PASSING_HARMONIC = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows", "ToothPassingHarmonic"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ToothPassingHarmonic")
    CastSelf = TypeVar(
        "CastSelf", bound="ToothPassingHarmonic._Cast_ToothPassingHarmonic"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ToothPassingHarmonic",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ToothPassingHarmonic:
    """Special nested class for casting ToothPassingHarmonic to subclasses."""

    __parent__: "ToothPassingHarmonic"

    @property
    def tooth_passing_harmonic(self: "CastSelf") -> "ToothPassingHarmonic":
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
class ToothPassingHarmonic(_0.APIBase):
    """ToothPassingHarmonic

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TOOTH_PASSING_HARMONIC

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def harmonic_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HarmonicName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def order(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Order")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tooth_passing_frequency_at_reference_speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ToothPassingFrequencyAtReferenceSpeed"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ToothPassingHarmonic":
        """Cast to another type.

        Returns:
            _Cast_ToothPassingHarmonic
        """
        return _Cast_ToothPassingHarmonic(self)
