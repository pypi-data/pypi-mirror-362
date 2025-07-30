"""GearMeshForTE"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility.modal_analysis.gears import _1999

_GEAR_MESH_FOR_TE = python_net_import(
    "SMT.MastaAPI.Utility.ModalAnalysis.Gears", "GearMeshForTE"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.utility.modal_analysis.gears import _1995

    Self = TypeVar("Self", bound="GearMeshForTE")
    CastSelf = TypeVar("CastSelf", bound="GearMeshForTE._Cast_GearMeshForTE")


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshForTE",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMeshForTE:
    """Special nested class for casting GearMeshForTE to subclasses."""

    __parent__: "GearMeshForTE"

    @property
    def order_for_te(self: "CastSelf") -> "_1999.OrderForTE":
        return self.__parent__._cast(_1999.OrderForTE)

    @property
    def gear_mesh_for_te(self: "CastSelf") -> "GearMeshForTE":
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
class GearMeshForTE(_1999.OrderForTE):
    """GearMeshForTE

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESH_FOR_TE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def number_of_teeth(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfTeeth")

        if temp is None:
            return ""

        return temp

    @number_of_teeth.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_teeth(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfTeeth", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def attached_gears(self: "Self") -> "List[_1995.GearOrderForTE]":
        """List[mastapy.utility.modal_analysis.gears.GearOrderForTE]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AttachedGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_GearMeshForTE":
        """Cast to another type.

        Returns:
            _Cast_GearMeshForTE
        """
        return _Cast_GearMeshForTE(self)
