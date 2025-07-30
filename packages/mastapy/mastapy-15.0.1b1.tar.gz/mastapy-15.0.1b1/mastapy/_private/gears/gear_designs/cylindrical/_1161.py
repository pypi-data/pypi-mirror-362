"""HardenedMaterialProperties"""

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
from mastapy._private.utility import _1779

_HARDENED_MATERIAL_PROPERTIES = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "HardenedMaterialProperties"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="HardenedMaterialProperties")
    CastSelf = TypeVar(
        "CastSelf", bound="HardenedMaterialProperties._Cast_HardenedMaterialProperties"
    )


__docformat__ = "restructuredtext en"
__all__ = ("HardenedMaterialProperties",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HardenedMaterialProperties:
    """Special nested class for casting HardenedMaterialProperties to subclasses."""

    __parent__: "HardenedMaterialProperties"

    @property
    def independent_reportable_properties_base(
        self: "CastSelf",
    ) -> "_1779.IndependentReportablePropertiesBase":
        pass

        return self.__parent__._cast(_1779.IndependentReportablePropertiesBase)

    @property
    def hardened_material_properties(self: "CastSelf") -> "HardenedMaterialProperties":
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
class HardenedMaterialProperties(
    _1779.IndependentReportablePropertiesBase["HardenedMaterialProperties"]
):
    """HardenedMaterialProperties

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HARDENED_MATERIAL_PROPERTIES

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def critical_stress(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CriticalStress")

        if temp is None:
            return 0.0

        return temp

    @critical_stress.setter
    @exception_bridge
    @enforce_parameter_types
    def critical_stress(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "CriticalStress", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def fatigue_sensitivity_to_normal_stress(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FatigueSensitivityToNormalStress")

        if temp is None:
            return 0.0

        return temp

    @fatigue_sensitivity_to_normal_stress.setter
    @exception_bridge
    @enforce_parameter_types
    def fatigue_sensitivity_to_normal_stress(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FatigueSensitivityToNormalStress",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_HardenedMaterialProperties":
        """Cast to another type.

        Returns:
            _Cast_HardenedMaterialProperties
        """
        return _Cast_HardenedMaterialProperties(self)
