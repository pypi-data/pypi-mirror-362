"""CylindricalGearMeshLoadedContactPoint"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.ltca import _947

_CYLINDRICAL_GEAR_MESH_LOADED_CONTACT_POINT = python_net_import(
    "SMT.MastaAPI.Gears.LTCA.Cylindrical", "CylindricalGearMeshLoadedContactPoint"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1135
    from mastapy._private.gears.rating.cylindrical.iso6336 import _617
    from mastapy._private.materials import _356

    Self = TypeVar("Self", bound="CylindricalGearMeshLoadedContactPoint")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearMeshLoadedContactPoint._Cast_CylindricalGearMeshLoadedContactPoint",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearMeshLoadedContactPoint",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearMeshLoadedContactPoint:
    """Special nested class for casting CylindricalGearMeshLoadedContactPoint to subclasses."""

    __parent__: "CylindricalGearMeshLoadedContactPoint"

    @property
    def gear_mesh_loaded_contact_point(
        self: "CastSelf",
    ) -> "_947.GearMeshLoadedContactPoint":
        return self.__parent__._cast(_947.GearMeshLoadedContactPoint)

    @property
    def cylindrical_gear_mesh_loaded_contact_point(
        self: "CastSelf",
    ) -> "CylindricalGearMeshLoadedContactPoint":
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
class CylindricalGearMeshLoadedContactPoint(_947.GearMeshLoadedContactPoint):
    """CylindricalGearMeshLoadedContactPoint

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_MESH_LOADED_CONTACT_POINT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def coefficient_of_friction(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CoefficientOfFriction")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def depth_of_maximum_material_exposure_gear_aiso633642019(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DepthOfMaximumMaterialExposureGearAISO633642019"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def depth_of_maximum_material_exposure_gear_biso633642019(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DepthOfMaximumMaterialExposureGearBISO633642019"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def face_width_position_gear_a(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceWidthPositionGearA")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def face_width_position_gear_b(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceWidthPositionGearB")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def is_gear_a_tip_contact_point(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsGearATipContactPoint")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def is_gear_b_tip_contact_point(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsGearBTipContactPoint")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def is_tip_contact_point(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsTipContactPoint")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def lubrication_state_d_value(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LubricationStateDValue")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_material_exposure_gear_aiso633642019(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumMaterialExposureGearAISO633642019"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_material_exposure_gear_biso633642019(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumMaterialExposureGearBISO633642019"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def micropitting_contact_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MicropittingContactTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def micropitting_flash_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MicropittingFlashTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def micropitting_minimum_lubricant_film_thickness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MicropittingMinimumLubricantFilmThickness"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def micropitting_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MicropittingSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def micropitting_specific_lubricant_film_thickness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MicropittingSpecificLubricantFilmThickness"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_lubricant_film_thickness_dowson(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumLubricantFilmThicknessDowson"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pressure_velocity_pv(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PressureVelocityPV")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def scuffing_contact_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ScuffingContactTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def scuffing_contact_temperature_agma925a03(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingContactTemperatureAGMA925A03"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def scuffing_contact_temperature_agma925b22(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingContactTemperatureAGMA925B22"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def scuffing_contact_temperature_din399041987(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingContactTemperatureDIN399041987"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def scuffing_flash_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ScuffingFlashTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def scuffing_flash_temperature_agma925a03(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingFlashTemperatureAGMA925A03"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def scuffing_flash_temperature_agma925b22(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingFlashTemperatureAGMA925B22"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def scuffing_flash_temperature_din399041987(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingFlashTemperatureDIN399041987"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def scuffing_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ScuffingSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def scuffing_safety_factor_agma925a03(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ScuffingSafetyFactorAGMA925A03")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def scuffing_safety_factor_agma925b22(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ScuffingSafetyFactorAGMA925B22")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def scuffing_safety_factor_din399041987(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ScuffingSafetyFactorDIN399041987")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sliding_power_loss(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SlidingPowerLoss")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sliding_velocity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SlidingVelocity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_a_profile_measurement(
        self: "Self",
    ) -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearAProfileMeasurement")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear_b_profile_measurement(
        self: "Self",
    ) -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearBProfileMeasurement")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def lubrication_detail(self: "Self") -> "_356.LubricationDetail":
        """mastapy.materials.LubricationDetail

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LubricationDetail")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def tooth_flank_fracture_analysis_gear_a(
        self: "Self",
    ) -> "_617.ToothFlankFractureAnalysisContactPointMethodA":
        """mastapy.gears.rating.cylindrical.iso6336.ToothFlankFractureAnalysisContactPointMethodA

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothFlankFractureAnalysisGearA")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def tooth_flank_fracture_analysis_gear_b(
        self: "Self",
    ) -> "_617.ToothFlankFractureAnalysisContactPointMethodA":
        """mastapy.gears.rating.cylindrical.iso6336.ToothFlankFractureAnalysisContactPointMethodA

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothFlankFractureAnalysisGearB")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearMeshLoadedContactPoint":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearMeshLoadedContactPoint
        """
        return _Cast_CylindricalGearMeshLoadedContactPoint(self)
