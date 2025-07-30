"""ShaftBow"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private._math.vector_3d import Vector3D

_SHAFT_BOW = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.ShaftModel", "ShaftBow"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="ShaftBow")
    CastSelf = TypeVar("CastSelf", bound="ShaftBow._Cast_ShaftBow")


__docformat__ = "restructuredtext en"
__all__ = ("ShaftBow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftBow:
    """Special nested class for casting ShaftBow to subclasses."""

    __parent__: "ShaftBow"

    @property
    def shaft_bow(self: "CastSelf") -> "ShaftBow":
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
class ShaftBow(_0.APIBase):
    """ShaftBow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_BOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def linear_displacement(self: "Self") -> "List[Vector3D]":
        """List[Vector3D]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LinearDisplacement")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, Vector3D)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftBow":
        """Cast to another type.

        Returns:
            _Cast_ShaftBow
        """
        return _Cast_ShaftBow(self)
