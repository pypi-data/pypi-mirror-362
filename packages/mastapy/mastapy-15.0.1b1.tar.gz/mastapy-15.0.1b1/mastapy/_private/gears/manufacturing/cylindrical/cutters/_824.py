"""MutableFillet"""

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
from mastapy._private.gears.manufacturing.cylindrical.cutters import _822

_MUTABLE_FILLET = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters", "MutableFillet"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical.cutters import _806

    Self = TypeVar("Self", bound="MutableFillet")
    CastSelf = TypeVar("CastSelf", bound="MutableFillet._Cast_MutableFillet")


__docformat__ = "restructuredtext en"
__all__ = ("MutableFillet",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MutableFillet:
    """Special nested class for casting MutableFillet to subclasses."""

    __parent__: "MutableFillet"

    @property
    def mutable_common(self: "CastSelf") -> "_822.MutableCommon":
        return self.__parent__._cast(_822.MutableCommon)

    @property
    def curve_in_linked_list(self: "CastSelf") -> "_806.CurveInLinkedList":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _806

        return self.__parent__._cast(_806.CurveInLinkedList)

    @property
    def mutable_fillet(self: "CastSelf") -> "MutableFillet":
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
class MutableFillet(_822.MutableCommon):
    """MutableFillet

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MUTABLE_FILLET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def height(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Height")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def offset(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Offset")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Radius")

        if temp is None:
            return 0.0

        return temp

    @radius.setter
    @exception_bridge
    @enforce_parameter_types
    def radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Radius", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_MutableFillet":
        """Cast to another type.

        Returns:
            _Cast_MutableFillet
        """
        return _Cast_MutableFillet(self)
