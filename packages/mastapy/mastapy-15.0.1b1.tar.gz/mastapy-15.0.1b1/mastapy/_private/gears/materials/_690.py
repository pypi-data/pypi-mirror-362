"""GearMaterialExpertSystemFactorSettings"""

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
from mastapy._private.utility import _1786

_GEAR_MATERIAL_EXPERT_SYSTEM_FACTOR_SETTINGS = python_net_import(
    "SMT.MastaAPI.Gears.Materials", "GearMaterialExpertSystemFactorSettings"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility import _1787

    Self = TypeVar("Self", bound="GearMaterialExpertSystemFactorSettings")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearMaterialExpertSystemFactorSettings._Cast_GearMaterialExpertSystemFactorSettings",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearMaterialExpertSystemFactorSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMaterialExpertSystemFactorSettings:
    """Special nested class for casting GearMaterialExpertSystemFactorSettings to subclasses."""

    __parent__: "GearMaterialExpertSystemFactorSettings"

    @property
    def per_machine_settings(self: "CastSelf") -> "_1786.PerMachineSettings":
        return self.__parent__._cast(_1786.PerMachineSettings)

    @property
    def persistent_singleton(self: "CastSelf") -> "_1787.PersistentSingleton":
        from mastapy._private.utility import _1787

        return self.__parent__._cast(_1787.PersistentSingleton)

    @property
    def gear_material_expert_system_factor_settings(
        self: "CastSelf",
    ) -> "GearMaterialExpertSystemFactorSettings":
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
class GearMaterialExpertSystemFactorSettings(_1786.PerMachineSettings):
    """GearMaterialExpertSystemFactorSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MATERIAL_EXPERT_SYSTEM_FACTOR_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def maximum_damage(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumDamage")

        if temp is None:
            return 0.0

        return temp

    @maximum_damage.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_damage(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "MaximumDamage", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def maximum_safety_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @maximum_safety_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_safety_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumSafetyFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def minimum_damage(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MinimumDamage")

        if temp is None:
            return 0.0

        return temp

    @minimum_damage.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_damage(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "MinimumDamage", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def minimum_safety_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MinimumSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @minimum_safety_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_safety_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumSafetyFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_GearMaterialExpertSystemFactorSettings":
        """Cast to another type.

        Returns:
            _Cast_GearMaterialExpertSystemFactorSettings
        """
        return _Cast_GearMaterialExpertSystemFactorSettings(self)
