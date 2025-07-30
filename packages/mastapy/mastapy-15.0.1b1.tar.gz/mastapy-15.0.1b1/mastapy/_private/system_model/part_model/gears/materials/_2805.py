"""GearMaterialExpertSystemMaterialOptions"""

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

_GEAR_MATERIAL_EXPERT_SYSTEM_MATERIAL_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears.Materials",
    "GearMaterialExpertSystemMaterialOptions",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="GearMaterialExpertSystemMaterialOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearMaterialExpertSystemMaterialOptions._Cast_GearMaterialExpertSystemMaterialOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearMaterialExpertSystemMaterialOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMaterialExpertSystemMaterialOptions:
    """Special nested class for casting GearMaterialExpertSystemMaterialOptions to subclasses."""

    __parent__: "GearMaterialExpertSystemMaterialOptions"

    @property
    def gear_material_expert_system_material_options(
        self: "CastSelf",
    ) -> "GearMaterialExpertSystemMaterialOptions":
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
class GearMaterialExpertSystemMaterialOptions(_0.APIBase):
    """GearMaterialExpertSystemMaterialOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MATERIAL_EXPERT_SYSTEM_MATERIAL_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def maximum_damage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumDamage")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_damage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumDamage")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_GearMaterialExpertSystemMaterialOptions":
        """Cast to another type.

        Returns:
            _Cast_GearMaterialExpertSystemMaterialOptions
        """
        return _Cast_GearMaterialExpertSystemMaterialOptions(self)
