"""OperatingViscosity"""

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

_OPERATING_VISCOSITY = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule", "OperatingViscosity"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="OperatingViscosity")
    CastSelf = TypeVar("CastSelf", bound="OperatingViscosity._Cast_OperatingViscosity")


__docformat__ = "restructuredtext en"
__all__ = ("OperatingViscosity",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_OperatingViscosity:
    """Special nested class for casting OperatingViscosity to subclasses."""

    __parent__: "OperatingViscosity"

    @property
    def operating_viscosity(self: "CastSelf") -> "OperatingViscosity":
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
class OperatingViscosity(_0.APIBase):
    """OperatingViscosity

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _OPERATING_VISCOSITY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def actual(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Actual")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def rated(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Rated")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def rated_at_40_degrees_c(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RatedAt40DegreesC")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_OperatingViscosity":
        """Cast to another type.

        Returns:
            _Cast_OperatingViscosity
        """
        return _Cast_OperatingViscosity(self)
