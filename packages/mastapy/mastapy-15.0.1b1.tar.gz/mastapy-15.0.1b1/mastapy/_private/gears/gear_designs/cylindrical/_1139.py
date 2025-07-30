"""CylindricalGearSetFlankDesign"""

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

_CYLINDRICAL_GEAR_SET_FLANK_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "CylindricalGearSetFlankDesign"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CylindricalGearSetFlankDesign")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearSetFlankDesign._Cast_CylindricalGearSetFlankDesign",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearSetFlankDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearSetFlankDesign:
    """Special nested class for casting CylindricalGearSetFlankDesign to subclasses."""

    __parent__: "CylindricalGearSetFlankDesign"

    @property
    def cylindrical_gear_set_flank_design(
        self: "CastSelf",
    ) -> "CylindricalGearSetFlankDesign":
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
class CylindricalGearSetFlankDesign(_0.APIBase):
    """CylindricalGearSetFlankDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_SET_FLANK_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def base_helix_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BaseHelixAngle")

        if temp is None:
            return 0.0

        return temp

    @base_helix_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def base_helix_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "BaseHelixAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def flank_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FlankName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def minimum_total_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumTotalContactRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_transverse_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumTransverseContactRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_base_pitch(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalBasePitch")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_base_pitch_set_by_changing_normal_module(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "NormalBasePitchSetByChangingNormalModule"
        )

        if temp is None:
            return 0.0

        return temp

    @normal_base_pitch_set_by_changing_normal_module.setter
    @exception_bridge
    @enforce_parameter_types
    def normal_base_pitch_set_by_changing_normal_module(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "NormalBasePitchSetByChangingNormalModule",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def normal_base_pitch_set_by_changing_normal_pressure_angle(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "NormalBasePitchSetByChangingNormalPressureAngle"
        )

        if temp is None:
            return 0.0

        return temp

    @normal_base_pitch_set_by_changing_normal_pressure_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def normal_base_pitch_set_by_changing_normal_pressure_angle(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "NormalBasePitchSetByChangingNormalPressureAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def normal_pressure_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NormalPressureAngle")

        if temp is None:
            return 0.0

        return temp

    @normal_pressure_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def normal_pressure_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NormalPressureAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def transverse_base_pitch(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransverseBasePitch")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transverse_pressure_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransversePressureAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transverse_pressure_angle_normal_pressure_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TransversePressureAngleNormalPressureAngle"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearSetFlankDesign":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearSetFlankDesign
        """
        return _Cast_CylindricalGearSetFlankDesign(self)
