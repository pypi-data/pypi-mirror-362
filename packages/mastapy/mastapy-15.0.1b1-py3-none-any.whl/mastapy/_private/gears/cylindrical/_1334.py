"""PointsWithWorstResults"""

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
)

_POINTS_WITH_WORST_RESULTS = python_net_import(
    "SMT.MastaAPI.Gears.Cylindrical", "PointsWithWorstResults"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.ltca.cylindrical import _962

    Self = TypeVar("Self", bound="PointsWithWorstResults")
    CastSelf = TypeVar(
        "CastSelf", bound="PointsWithWorstResults._Cast_PointsWithWorstResults"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PointsWithWorstResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PointsWithWorstResults:
    """Special nested class for casting PointsWithWorstResults to subclasses."""

    __parent__: "PointsWithWorstResults"

    @property
    def points_with_worst_results(self: "CastSelf") -> "PointsWithWorstResults":
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
class PointsWithWorstResults(_0.APIBase):
    """PointsWithWorstResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _POINTS_WITH_WORST_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def coefficient_of_friction(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CoefficientOfFriction")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def depth_of_max_shear_stress(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DepthOfMaxShearStress")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def force_per_unit_length(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForcePerUnitLength")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gap_between_loaded_flanks_transverse(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GapBetweenLoadedFlanksTransverse")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gap_between_unloaded_flanks_transverse(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GapBetweenUnloadedFlanksTransverse"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear_a_depth_of_maximum_material_exposure_iso633642019(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GearADepthOfMaximumMaterialExposureISO633642019"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear_a_maximum_material_exposure_iso633642019(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GearAMaximumMaterialExposureISO633642019"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear_b_depth_of_maximum_material_exposure_iso633642019(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GearBDepthOfMaximumMaterialExposureISO633642019"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear_b_maximum_material_exposure_iso633642019(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GearBMaximumMaterialExposureISO633642019"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def hertzian_contact_half_width(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HertzianContactHalfWidth")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def lubrication_state_d_value(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LubricationStateDValue")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def max_pressure(self: "Self") -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaxPressure")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def max_shear_stress(self: "Self") -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaxShearStress")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def micropitting_contact_temperature_isotr1514412010(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MicropittingContactTemperatureISOTR1514412010"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def micropitting_contact_temperature_isotr1514412014(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MicropittingContactTemperatureISOTR1514412014"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def micropitting_contact_temperature_isots6336222018(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MicropittingContactTemperatureISOTS6336222018"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def micropitting_flash_temperature_isotr1514412010(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MicropittingFlashTemperatureISOTR1514412010"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def micropitting_flash_temperature_isotr1514412014(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MicropittingFlashTemperatureISOTR1514412014"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def micropitting_flash_temperature_isots6336222018(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MicropittingFlashTemperatureISOTS6336222018"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def micropitting_safety_factor_isotr1514412010(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MicropittingSafetyFactorISOTR1514412010"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def micropitting_safety_factor_isotr1514412014(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MicropittingSafetyFactorISOTR1514412014"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def micropitting_safety_factor_isots6336222018(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MicropittingSafetyFactorISOTS6336222018"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def minimum_lubricant_film_thickness_dowson(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumLubricantFilmThicknessDowson"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def minimum_lubricant_film_thickness_isotr1514412010(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumLubricantFilmThicknessISOTR1514412010"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def minimum_lubricant_film_thickness_isotr1514412014(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumLubricantFilmThicknessISOTR1514412014"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def minimum_lubricant_film_thickness_isots6336222018(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumLubricantFilmThicknessISOTS6336222018"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def pressure_velocity_pv(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PressureVelocityPV")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def scuffing_contact_temperature_agma925a03(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingContactTemperatureAGMA925A03"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def scuffing_contact_temperature_agma925b22(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingContactTemperatureAGMA925B22"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def scuffing_contact_temperature_din399041987(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingContactTemperatureDIN399041987"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def scuffing_contact_temperature_isotr1398912000(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingContactTemperatureISOTR1398912000"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def scuffing_contact_temperature_isots6336202017(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingContactTemperatureISOTS6336202017"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def scuffing_contact_temperature_isots6336202022(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingContactTemperatureISOTS6336202022"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def scuffing_flash_temperature_agma925a03(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingFlashTemperatureAGMA925A03"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def scuffing_flash_temperature_agma925b22(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingFlashTemperatureAGMA925B22"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def scuffing_flash_temperature_din399041987(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingFlashTemperatureDIN399041987"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def scuffing_flash_temperature_isotr1398912000(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingFlashTemperatureISOTR1398912000"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def scuffing_flash_temperature_isots6336202017(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingFlashTemperatureISOTS6336202017"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def scuffing_flash_temperature_isots6336202022(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingFlashTemperatureISOTS6336202022"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def scuffing_safety_factor_agma925a03(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ScuffingSafetyFactorAGMA925A03")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def scuffing_safety_factor_agma925b22(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ScuffingSafetyFactorAGMA925B22")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def scuffing_safety_factor_din399041987(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ScuffingSafetyFactorDIN399041987")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def scuffing_safety_factor_isotr1398912000(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingSafetyFactorISOTR1398912000"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def scuffing_safety_factor_isots6336202017(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingSafetyFactorISOTS6336202017"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def scuffing_safety_factor_isots6336202022(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ScuffingSafetyFactorISOTS6336202022"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def sliding_power_loss(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SlidingPowerLoss")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def sliding_velocity(self: "Self") -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SlidingVelocity")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def specific_lubricant_film_thickness_isotr1514412010(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SpecificLubricantFilmThicknessISOTR1514412010"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def specific_lubricant_film_thickness_isotr1514412014(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SpecificLubricantFilmThicknessISOTR1514412014"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def specific_lubricant_film_thickness_isots6336222018(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SpecificLubricantFilmThicknessISOTS6336222018"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def total_deflection_for_mesh(
        self: "Self",
    ) -> "_962.CylindricalGearMeshLoadedContactPoint":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalDeflectionForMesh")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_PointsWithWorstResults":
        """Cast to another type.

        Returns:
            _Cast_PointsWithWorstResults
        """
        return _Cast_PointsWithWorstResults(self)
