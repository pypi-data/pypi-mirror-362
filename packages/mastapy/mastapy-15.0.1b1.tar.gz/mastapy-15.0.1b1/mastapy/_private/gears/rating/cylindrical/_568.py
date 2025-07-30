"""MicroPittingResultsRow"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_MICRO_PITTING_RESULTS_ROW = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical", "MicroPittingResultsRow"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1135

    Self = TypeVar("Self", bound="MicroPittingResultsRow")
    CastSelf = TypeVar(
        "CastSelf", bound="MicroPittingResultsRow._Cast_MicroPittingResultsRow"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MicroPittingResultsRow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MicroPittingResultsRow:
    """Special nested class for casting MicroPittingResultsRow to subclasses."""

    __parent__: "MicroPittingResultsRow"

    @property
    def micro_pitting_results_row(self: "CastSelf") -> "MicroPittingResultsRow":
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
class MicroPittingResultsRow(_0.APIBase):
    """MicroPittingResultsRow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MICRO_PITTING_RESULTS_ROW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def contact_point(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ContactPoint")

        if temp is None:
            return 0.0

        return temp

    @contact_point.setter
    @exception_bridge
    @enforce_parameter_types
    def contact_point(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ContactPoint", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def dynamic_viscosity_of_the_lubricant_at_contact_temperature(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "DynamicViscosityOfTheLubricantAtContactTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @dynamic_viscosity_of_the_lubricant_at_contact_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def dynamic_viscosity_of_the_lubricant_at_contact_temperature(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "DynamicViscosityOfTheLubricantAtContactTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def kinematic_viscosity_of_lubricant_at_contact_temperature(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "KinematicViscosityOfLubricantAtContactTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @kinematic_viscosity_of_lubricant_at_contact_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def kinematic_viscosity_of_lubricant_at_contact_temperature(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "KinematicViscosityOfLubricantAtContactTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def load_sharing_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LoadSharingFactor")

        if temp is None:
            return 0.0

        return temp

    @load_sharing_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def load_sharing_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LoadSharingFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def local_contact_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LocalContactTemperature")

        if temp is None:
            return 0.0

        return temp

    @local_contact_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def local_contact_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LocalContactTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def local_flash_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LocalFlashTemperature")

        if temp is None:
            return 0.0

        return temp

    @local_flash_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def local_flash_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LocalFlashTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def local_hertzian_contact_stress(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LocalHertzianContactStress")

        if temp is None:
            return 0.0

        return temp

    @local_hertzian_contact_stress.setter
    @exception_bridge
    @enforce_parameter_types
    def local_hertzian_contact_stress(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LocalHertzianContactStress",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def local_load_parameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LocalLoadParameter")

        if temp is None:
            return 0.0

        return temp

    @local_load_parameter.setter
    @exception_bridge
    @enforce_parameter_types
    def local_load_parameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LocalLoadParameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def local_lubricant_film_thickness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LocalLubricantFilmThickness")

        if temp is None:
            return 0.0

        return temp

    @local_lubricant_film_thickness.setter
    @exception_bridge
    @enforce_parameter_types
    def local_lubricant_film_thickness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LocalLubricantFilmThickness",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def local_sliding_parameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LocalSlidingParameter")

        if temp is None:
            return 0.0

        return temp

    @local_sliding_parameter.setter
    @exception_bridge
    @enforce_parameter_types
    def local_sliding_parameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LocalSlidingParameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def local_sliding_velocity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LocalSlidingVelocity")

        if temp is None:
            return 0.0

        return temp

    @local_sliding_velocity.setter
    @exception_bridge
    @enforce_parameter_types
    def local_sliding_velocity(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LocalSlidingVelocity",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def local_velocity_parameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LocalVelocityParameter")

        if temp is None:
            return 0.0

        return temp

    @local_velocity_parameter.setter
    @exception_bridge
    @enforce_parameter_types
    def local_velocity_parameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LocalVelocityParameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def lubricant_density_at_contact_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "LubricantDensityAtContactTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @lubricant_density_at_contact_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def lubricant_density_at_contact_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LubricantDensityAtContactTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def mesh(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Mesh")

        if temp is None:
            return ""

        return temp

    @mesh.setter
    @exception_bridge
    @enforce_parameter_types
    def mesh(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Mesh", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def normal_relative_radius_of_curvature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NormalRelativeRadiusOfCurvature")

        if temp is None:
            return 0.0

        return temp

    @normal_relative_radius_of_curvature.setter
    @exception_bridge
    @enforce_parameter_types
    def normal_relative_radius_of_curvature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NormalRelativeRadiusOfCurvature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def pinion_flank_radius_of_curvature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PinionFlankRadiusOfCurvature")

        if temp is None:
            return 0.0

        return temp

    @pinion_flank_radius_of_curvature.setter
    @exception_bridge
    @enforce_parameter_types
    def pinion_flank_radius_of_curvature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PinionFlankRadiusOfCurvature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def point_of_mesh(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PointOfMesh")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def pressure_viscosity_coefficient_at_contact_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "PressureViscosityCoefficientAtContactTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @pressure_viscosity_coefficient_at_contact_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def pressure_viscosity_coefficient_at_contact_temperature(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "PressureViscosityCoefficientAtContactTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def sum_of_tangential_velocities(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SumOfTangentialVelocities")

        if temp is None:
            return 0.0

        return temp

    @sum_of_tangential_velocities.setter
    @exception_bridge
    @enforce_parameter_types
    def sum_of_tangential_velocities(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SumOfTangentialVelocities",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def transverse_relative_radius_of_curvature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "TransverseRelativeRadiusOfCurvature"
        )

        if temp is None:
            return 0.0

        return temp

    @transverse_relative_radius_of_curvature.setter
    @exception_bridge
    @enforce_parameter_types
    def transverse_relative_radius_of_curvature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TransverseRelativeRadiusOfCurvature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def wheel_flank_radius_of_curvature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WheelFlankRadiusOfCurvature")

        if temp is None:
            return 0.0

        return temp

    @wheel_flank_radius_of_curvature.setter
    @exception_bridge
    @enforce_parameter_types
    def wheel_flank_radius_of_curvature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "WheelFlankRadiusOfCurvature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def position_on_pinion(self: "Self") -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PositionOnPinion")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def position_on_wheel(self: "Self") -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PositionOnWheel")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_MicroPittingResultsRow":
        """Cast to another type.

        Returns:
            _Cast_MicroPittingResultsRow
        """
        return _Cast_MicroPittingResultsRow(self)
