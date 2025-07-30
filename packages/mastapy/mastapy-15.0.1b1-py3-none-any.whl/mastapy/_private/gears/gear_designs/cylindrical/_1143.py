"""CylindricalGearSetOptimisationWrapper"""

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

_CYLINDRICAL_GEAR_SET_OPTIMISATION_WRAPPER = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical",
    "CylindricalGearSetOptimisationWrapper",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CylindricalGearSetOptimisationWrapper")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearSetOptimisationWrapper._Cast_CylindricalGearSetOptimisationWrapper",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearSetOptimisationWrapper",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearSetOptimisationWrapper:
    """Special nested class for casting CylindricalGearSetOptimisationWrapper to subclasses."""

    __parent__: "CylindricalGearSetOptimisationWrapper"

    @property
    def cylindrical_gear_set_optimisation_wrapper(
        self: "CastSelf",
    ) -> "CylindricalGearSetOptimisationWrapper":
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
class CylindricalGearSetOptimisationWrapper(_0.APIBase):
    """CylindricalGearSetOptimisationWrapper

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_SET_OPTIMISATION_WRAPPER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def face_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FaceWidth")

        if temp is None:
            return 0.0

        return temp

    @face_width.setter
    @exception_bridge
    @enforce_parameter_types
    def face_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FaceWidth", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def face_width_with_constant_axial_contact_ratio(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "FaceWidthWithConstantAxialContactRatio"
        )

        if temp is None:
            return 0.0

        return temp

    @face_width_with_constant_axial_contact_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def face_width_with_constant_axial_contact_ratio(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "FaceWidthWithConstantAxialContactRatio",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def helix_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "HelixAngle")

        if temp is None:
            return 0.0

        return temp

    @helix_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def helix_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "HelixAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def helix_angle_fixed_transverse_profile(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "HelixAngleFixedTransverseProfile")

        if temp is None:
            return 0.0

        return temp

    @helix_angle_fixed_transverse_profile.setter
    @exception_bridge
    @enforce_parameter_types
    def helix_angle_fixed_transverse_profile(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "HelixAngleFixedTransverseProfile",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def normal_module(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NormalModule")

        if temp is None:
            return 0.0

        return temp

    @normal_module.setter
    @exception_bridge
    @enforce_parameter_types
    def normal_module(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "NormalModule", float(value) if value is not None else 0.0
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
    def planet_diameter_with_adjusted_face_width_to_maintain_mass(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "PlanetDiameterWithAdjustedFaceWidthToMaintainMass"
        )

        if temp is None:
            return 0.0

        return temp

    @planet_diameter_with_adjusted_face_width_to_maintain_mass.setter
    @exception_bridge
    @enforce_parameter_types
    def planet_diameter_with_adjusted_face_width_to_maintain_mass(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "PlanetDiameterWithAdjustedFaceWidthToMaintainMass",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def root_gear_profile_shift_coefficient(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RootGearProfileShiftCoefficient")

        if temp is None:
            return 0.0

        return temp

    @root_gear_profile_shift_coefficient.setter
    @exception_bridge
    @enforce_parameter_types
    def root_gear_profile_shift_coefficient(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RootGearProfileShiftCoefficient",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def root_gear_profile_shift_coefficient_with_fixed_tip_and_root_diameters(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "RootGearProfileShiftCoefficientWithFixedTipAndRootDiameters"
        )

        if temp is None:
            return 0.0

        return temp

    @root_gear_profile_shift_coefficient_with_fixed_tip_and_root_diameters.setter
    @exception_bridge
    @enforce_parameter_types
    def root_gear_profile_shift_coefficient_with_fixed_tip_and_root_diameters(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "RootGearProfileShiftCoefficientWithFixedTipAndRootDiameters",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearSetOptimisationWrapper":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearSetOptimisationWrapper
        """
        return _Cast_CylindricalGearSetOptimisationWrapper(self)
