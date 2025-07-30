"""PermissibleAxialLoad"""

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

_PERMISSIBLE_AXIAL_LOAD = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule", "PermissibleAxialLoad"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="PermissibleAxialLoad")
    CastSelf = TypeVar(
        "CastSelf", bound="PermissibleAxialLoad._Cast_PermissibleAxialLoad"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PermissibleAxialLoad",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PermissibleAxialLoad:
    """Special nested class for casting PermissibleAxialLoad to subclasses."""

    __parent__: "PermissibleAxialLoad"

    @property
    def permissible_axial_load(self: "CastSelf") -> "PermissibleAxialLoad":
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
class PermissibleAxialLoad(_0.APIBase):
    """PermissibleAxialLoad

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PERMISSIBLE_AXIAL_LOAD

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def brief_periods(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BriefPeriods")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def continuous(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Continuous")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def peak_loads(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PeakLoads")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_PermissibleAxialLoad":
        """Cast to another type.

        Returns:
            _Cast_PermissibleAxialLoad
        """
        return _Cast_PermissibleAxialLoad(self)
