"""HoleInFaceGroup"""

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
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_HOLE_IN_FACE_GROUP = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Acoustics", "HoleInFaceGroup"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="HoleInFaceGroup")
    CastSelf = TypeVar("CastSelf", bound="HoleInFaceGroup._Cast_HoleInFaceGroup")


__docformat__ = "restructuredtext en"
__all__ = ("HoleInFaceGroup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HoleInFaceGroup:
    """Special nested class for casting HoleInFaceGroup to subclasses."""

    __parent__: "HoleInFaceGroup"

    @property
    def hole_in_face_group(self: "CastSelf") -> "HoleInFaceGroup":
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
class HoleInFaceGroup(_0.APIBase):
    """HoleInFaceGroup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HOLE_IN_FACE_GROUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def hole_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HoleDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hole_id(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HoleID")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def included(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "Included")

        if temp is None:
            return False

        return temp

    @included.setter
    @exception_bridge
    @enforce_parameter_types
    def included(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "Included", bool(value) if value is not None else False
        )

    @property
    def cast_to(self: "Self") -> "_Cast_HoleInFaceGroup":
        """Cast to another type.

        Returns:
            _Cast_HoleInFaceGroup
        """
        return _Cast_HoleInFaceGroup(self)
