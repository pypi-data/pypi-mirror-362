"""HarmonicValue"""

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

_HARMONIC_VALUE = python_net_import("SMT.MastaAPI.MathUtility", "HarmonicValue")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="HarmonicValue")
    CastSelf = TypeVar("CastSelf", bound="HarmonicValue._Cast_HarmonicValue")


__docformat__ = "restructuredtext en"
__all__ = ("HarmonicValue",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HarmonicValue:
    """Special nested class for casting HarmonicValue to subclasses."""

    __parent__: "HarmonicValue"

    @property
    def harmonic_value(self: "CastSelf") -> "HarmonicValue":
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
class HarmonicValue(_0.APIBase):
    """HarmonicValue

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HARMONIC_VALUE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def amplitude(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Amplitude")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def harmonic_index(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HarmonicIndex")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def phase(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Phase")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_HarmonicValue":
        """Cast to another type.

        Returns:
            _Cast_HarmonicValue
        """
        return _Cast_HarmonicValue(self)
