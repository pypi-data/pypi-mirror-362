"""GearMaterialExpertSystemMaterialDetails"""

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

_GEAR_MATERIAL_EXPERT_SYSTEM_MATERIAL_DETAILS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears.Materials",
    "GearMaterialExpertSystemMaterialDetails",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="GearMaterialExpertSystemMaterialDetails")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearMaterialExpertSystemMaterialDetails._Cast_GearMaterialExpertSystemMaterialDetails",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearMaterialExpertSystemMaterialDetails",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMaterialExpertSystemMaterialDetails:
    """Special nested class for casting GearMaterialExpertSystemMaterialDetails to subclasses."""

    __parent__: "GearMaterialExpertSystemMaterialDetails"

    @property
    def gear_material_expert_system_material_details(
        self: "CastSelf",
    ) -> "GearMaterialExpertSystemMaterialDetails":
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
class GearMaterialExpertSystemMaterialDetails(_0.APIBase):
    """GearMaterialExpertSystemMaterialDetails

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MATERIAL_EXPERT_SYSTEM_MATERIAL_DETAILS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def bar_length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BarLength")

        if temp is None:
            return 0.0

        return temp

    @bar_length.setter
    @exception_bridge
    @enforce_parameter_types
    def bar_length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "BarLength", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_GearMaterialExpertSystemMaterialDetails":
        """Cast to another type.

        Returns:
            _Cast_GearMaterialExpertSystemMaterialDetails
        """
        return _Cast_GearMaterialExpertSystemMaterialDetails(self)
