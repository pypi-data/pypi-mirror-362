"""RingPinsMaterial"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.materials import _358

_RING_PINS_MATERIAL = python_net_import("SMT.MastaAPI.Cycloidal", "RingPinsMaterial")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.databases import _2028

    Self = TypeVar("Self", bound="RingPinsMaterial")
    CastSelf = TypeVar("CastSelf", bound="RingPinsMaterial._Cast_RingPinsMaterial")


__docformat__ = "restructuredtext en"
__all__ = ("RingPinsMaterial",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RingPinsMaterial:
    """Special nested class for casting RingPinsMaterial to subclasses."""

    __parent__: "RingPinsMaterial"

    @property
    def material(self: "CastSelf") -> "_358.Material":
        return self.__parent__._cast(_358.Material)

    @property
    def named_database_item(self: "CastSelf") -> "_2028.NamedDatabaseItem":
        from mastapy._private.utility.databases import _2028

        return self.__parent__._cast(_2028.NamedDatabaseItem)

    @property
    def ring_pins_material(self: "CastSelf") -> "RingPinsMaterial":
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
class RingPinsMaterial(_358.Material):
    """RingPinsMaterial

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RING_PINS_MATERIAL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_RingPinsMaterial":
        """Cast to another type.

        Returns:
            _Cast_RingPinsMaterial
        """
        return _Cast_RingPinsMaterial(self)
