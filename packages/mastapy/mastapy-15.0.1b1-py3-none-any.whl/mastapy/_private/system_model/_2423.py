"""MASTASettings"""

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

_MASTA_SETTINGS = python_net_import("SMT.MastaAPI.SystemModel", "MASTASettings")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings import _2082, _2083, _2096, _2102
    from mastapy._private.bearings.bearing_results.rolling import _2182
    from mastapy._private.bolts import _1654, _1656, _1661
    from mastapy._private.cycloidal import _1642, _1649
    from mastapy._private.electric_machines import _1405, _1419, _1438, _1453
    from mastapy._private.gears import _405, _406, _433
    from mastapy._private.gears.gear_designs import _1044, _1046, _1049, _1055
    from mastapy._private.gears.gear_designs.cylindrical import (
        _1121,
        _1125,
        _1126,
        _1131,
        _1142,
    )
    from mastapy._private.gears.gear_set_pareto_optimiser import (
        _1024,
        _1025,
        _1028,
        _1029,
        _1031,
        _1032,
        _1034,
        _1035,
        _1037,
        _1038,
        _1039,
        _1040,
    )
    from mastapy._private.gears.ltca.cylindrical import _958
    from mastapy._private.gears.manufacturing.bevel import _903
    from mastapy._private.gears.manufacturing.cylindrical import _718, _729
    from mastapy._private.gears.manufacturing.cylindrical.cutters import (
        _808,
        _814,
        _819,
        _820,
    )
    from mastapy._private.gears.materials import (
        _678,
        _680,
        _682,
        _683,
        _686,
        _690,
        _699,
        _700,
        _709,
    )
    from mastapy._private.gears.rating.cylindrical import _543, _544, _559, _560
    from mastapy._private.materials import _333, _336, _343, _357, _360, _361
    from mastapy._private.nodal_analysis import _51, _52, _71
    from mastapy._private.nodal_analysis.geometry_modeller_link import _238
    from mastapy._private.shafts import _25, _41, _42
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6900,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _6054,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5744
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4929
    from mastapy._private.system_model.analyses_and_results.power_flows import _4386
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _4130,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3337,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _3069,
    )
    from mastapy._private.system_model.drawing import _2473
    from mastapy._private.system_model.optimization import _2439, _2448
    from mastapy._private.system_model.optimization.machine_learning import _2456
    from mastapy._private.system_model.part_model import _2675, _2701
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set import (
        _2802,
    )
    from mastapy._private.utility import _1788
    from mastapy._private.utility.cad_export import _2034
    from mastapy._private.utility.databases import _2026
    from mastapy._private.utility.scripting import _1934
    from mastapy._private.utility.units_and_measurements import _1798

    Self = TypeVar("Self", bound="MASTASettings")
    CastSelf = TypeVar("CastSelf", bound="MASTASettings._Cast_MASTASettings")


__docformat__ = "restructuredtext en"
__all__ = ("MASTASettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MASTASettings:
    """Special nested class for casting MASTASettings to subclasses."""

    __parent__: "MASTASettings"

    @property
    def masta_settings(self: "CastSelf") -> "MASTASettings":
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
class MASTASettings(_0.APIBase):
    """MASTASettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MASTA_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def iso14179_settings_database(self: "Self") -> "_2182.ISO14179SettingsDatabase":
        """mastapy.bearings.bearing_results.rolling.ISO14179SettingsDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISO14179SettingsDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def bearing_settings(self: "Self") -> "_2082.BearingSettings":
        """mastapy.bearings.BearingSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BearingSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def bearing_settings_database(self: "Self") -> "_2083.BearingSettingsDatabase":
        """mastapy.bearings.BearingSettingsDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BearingSettingsDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def rolling_bearing_database(self: "Self") -> "_2096.RollingBearingDatabase":
        """mastapy.bearings.RollingBearingDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RollingBearingDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def skf_settings(self: "Self") -> "_2102.SKFSettings":
        """mastapy.bearings.SKFSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SKFSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def bolt_geometry_database(self: "Self") -> "_1654.BoltGeometryDatabase":
        """mastapy.bolts.BoltGeometryDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BoltGeometryDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def bolt_material_database(self: "Self") -> "_1656.BoltMaterialDatabase":
        """mastapy.bolts.BoltMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BoltMaterialDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def clamped_section_material_database(
        self: "Self",
    ) -> "_1661.ClampedSectionMaterialDatabase":
        """mastapy.bolts.ClampedSectionMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ClampedSectionMaterialDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cycloidal_disc_material_database(
        self: "Self",
    ) -> "_1642.CycloidalDiscMaterialDatabase":
        """mastapy.cycloidal.CycloidalDiscMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CycloidalDiscMaterialDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def ring_pins_material_database(self: "Self") -> "_1649.RingPinsMaterialDatabase":
        """mastapy.cycloidal.RingPinsMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RingPinsMaterialDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def general_electric_machine_material_database(
        self: "Self",
    ) -> "_1405.GeneralElectricMachineMaterialDatabase":
        """mastapy.electric_machines.GeneralElectricMachineMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GeneralElectricMachineMaterialDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def magnet_material_database(self: "Self") -> "_1419.MagnetMaterialDatabase":
        """mastapy.electric_machines.MagnetMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MagnetMaterialDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def stator_rotor_material_database(
        self: "Self",
    ) -> "_1438.StatorRotorMaterialDatabase":
        """mastapy.electric_machines.StatorRotorMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StatorRotorMaterialDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def winding_material_database(self: "Self") -> "_1453.WindingMaterialDatabase":
        """mastapy.electric_machines.WindingMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WindingMaterialDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def bevel_hypoid_gear_design_settings(
        self: "Self",
    ) -> "_405.BevelHypoidGearDesignSettings":
        """mastapy.gears.BevelHypoidGearDesignSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelHypoidGearDesignSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def bevel_hypoid_gear_rating_settings(
        self: "Self",
    ) -> "_406.BevelHypoidGearRatingSettings":
        """mastapy.gears.BevelHypoidGearRatingSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelHypoidGearRatingSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def bevel_hypoid_gear_design_settings_database(
        self: "Self",
    ) -> "_1044.BevelHypoidGearDesignSettingsDatabase":
        """mastapy.gears.gear_designs.BevelHypoidGearDesignSettingsDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BevelHypoidGearDesignSettingsDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def bevel_hypoid_gear_rating_settings_database(
        self: "Self",
    ) -> "_1046.BevelHypoidGearRatingSettingsDatabase":
        """mastapy.gears.gear_designs.BevelHypoidGearRatingSettingsDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BevelHypoidGearRatingSettingsDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_gear_defaults(self: "Self") -> "_1121.CylindricalGearDefaults":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearDefaults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearDefaults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_gear_design_constraints_database(
        self: "Self",
    ) -> "_1125.CylindricalGearDesignConstraintsDatabase":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearDesignConstraintsDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalGearDesignConstraintsDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_gear_design_constraint_settings(
        self: "Self",
    ) -> "_1126.CylindricalGearDesignConstraintSettings":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearDesignConstraintSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalGearDesignConstraintSettings"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_gear_micro_geometry_settings_database(
        self: "Self",
    ) -> "_1131.CylindricalGearMicroGeometrySettingsDatabase":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearMicroGeometrySettingsDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalGearMicroGeometrySettingsDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_gear_set_micro_geometry_settings(
        self: "Self",
    ) -> "_1142.CylindricalGearSetMicroGeometrySettings":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearSetMicroGeometrySettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalGearSetMicroGeometrySettings"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def design_constraint_collection_database(
        self: "Self",
    ) -> "_1049.DesignConstraintCollectionDatabase":
        """mastapy.gears.gear_designs.DesignConstraintCollectionDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DesignConstraintCollectionDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def selected_design_constraints_collection(
        self: "Self",
    ) -> "_1055.SelectedDesignConstraintsCollection":
        """mastapy.gears.gear_designs.SelectedDesignConstraintsCollection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SelectedDesignConstraintsCollection"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def micro_geometry_gear_set_design_space_search_strategy_database(
        self: "Self",
    ) -> "_1024.MicroGeometryGearSetDesignSpaceSearchStrategyDatabase":
        """mastapy.gears.gear_set_pareto_optimiser.MicroGeometryGearSetDesignSpaceSearchStrategyDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MicroGeometryGearSetDesignSpaceSearchStrategyDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def micro_geometry_gear_set_duty_cycle_design_space_search_strategy_database(
        self: "Self",
    ) -> "_1025.MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase":
        """mastapy.gears.gear_set_pareto_optimiser.MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase",
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def pareto_cylindrical_gear_set_duty_cycle_optimisation_strategy_database(
        self: "Self",
    ) -> "_1028.ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase":
        """mastapy.gears.gear_set_pareto_optimiser.ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase",
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def pareto_cylindrical_gear_set_optimisation_strategy_database(
        self: "Self",
    ) -> "_1029.ParetoCylindricalGearSetOptimisationStrategyDatabase":
        """mastapy.gears.gear_set_pareto_optimiser.ParetoCylindricalGearSetOptimisationStrategyDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ParetoCylindricalGearSetOptimisationStrategyDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def pareto_face_gear_set_duty_cycle_optimisation_strategy_database(
        self: "Self",
    ) -> "_1031.ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase":
        """mastapy.gears.gear_set_pareto_optimiser.ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def pareto_face_gear_set_optimisation_strategy_database(
        self: "Self",
    ) -> "_1032.ParetoFaceGearSetOptimisationStrategyDatabase":
        """mastapy.gears.gear_set_pareto_optimiser.ParetoFaceGearSetOptimisationStrategyDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ParetoFaceGearSetOptimisationStrategyDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def pareto_hypoid_gear_set_duty_cycle_optimisation_strategy_database(
        self: "Self",
    ) -> "_1034.ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase":
        """mastapy.gears.gear_set_pareto_optimiser.ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def pareto_hypoid_gear_set_optimisation_strategy_database(
        self: "Self",
    ) -> "_1035.ParetoHypoidGearSetOptimisationStrategyDatabase":
        """mastapy.gears.gear_set_pareto_optimiser.ParetoHypoidGearSetOptimisationStrategyDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ParetoHypoidGearSetOptimisationStrategyDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def pareto_spiral_bevel_gear_set_duty_cycle_optimisation_strategy_database(
        self: "Self",
    ) -> "_1037.ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase":
        """mastapy.gears.gear_set_pareto_optimiser.ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase",
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def pareto_spiral_bevel_gear_set_optimisation_strategy_database(
        self: "Self",
    ) -> "_1038.ParetoSpiralBevelGearSetOptimisationStrategyDatabase":
        """mastapy.gears.gear_set_pareto_optimiser.ParetoSpiralBevelGearSetOptimisationStrategyDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ParetoSpiralBevelGearSetOptimisationStrategyDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def pareto_straight_bevel_gear_set_duty_cycle_optimisation_strategy_database(
        self: "Self",
    ) -> "_1039.ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase":
        """mastapy.gears.gear_set_pareto_optimiser.ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase",
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def pareto_straight_bevel_gear_set_optimisation_strategy_database(
        self: "Self",
    ) -> "_1040.ParetoStraightBevelGearSetOptimisationStrategyDatabase":
        """mastapy.gears.gear_set_pareto_optimiser.ParetoStraightBevelGearSetOptimisationStrategyDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ParetoStraightBevelGearSetOptimisationStrategyDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_gear_fe_settings(self: "Self") -> "_958.CylindricalGearFESettings":
        """mastapy.gears.ltca.cylindrical.CylindricalGearFESettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearFESettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def manufacturing_machine_database(
        self: "Self",
    ) -> "_903.ManufacturingMachineDatabase":
        """mastapy.gears.manufacturing.bevel.ManufacturingMachineDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ManufacturingMachineDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_formed_wheel_grinder_database(
        self: "Self",
    ) -> "_808.CylindricalFormedWheelGrinderDatabase":
        """mastapy.gears.manufacturing.cylindrical.cutters.CylindricalFormedWheelGrinderDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalFormedWheelGrinderDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_gear_plunge_shaver_database(
        self: "Self",
    ) -> "_814.CylindricalGearPlungeShaverDatabase":
        """mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearPlungeShaverDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalGearPlungeShaverDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_gear_shaver_database(
        self: "Self",
    ) -> "_819.CylindricalGearShaverDatabase":
        """mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearShaverDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearShaverDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_worm_grinder_database(
        self: "Self",
    ) -> "_820.CylindricalWormGrinderDatabase":
        """mastapy.gears.manufacturing.cylindrical.cutters.CylindricalWormGrinderDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalWormGrinderDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_hob_database(self: "Self") -> "_718.CylindricalHobDatabase":
        """mastapy.gears.manufacturing.cylindrical.CylindricalHobDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalHobDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_shaper_database(self: "Self") -> "_729.CylindricalShaperDatabase":
        """mastapy.gears.manufacturing.cylindrical.CylindricalShaperDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalShaperDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def bevel_gear_iso_material_database(
        self: "Self",
    ) -> "_678.BevelGearISOMaterialDatabase":
        """mastapy.gears.materials.BevelGearISOMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelGearISOMaterialDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def bevel_gear_material_database(self: "Self") -> "_680.BevelGearMaterialDatabase":
        """mastapy.gears.materials.BevelGearMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelGearMaterialDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_gear_agma_material_database(
        self: "Self",
    ) -> "_682.CylindricalGearAGMAMaterialDatabase":
        """mastapy.gears.materials.CylindricalGearAGMAMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalGearAGMAMaterialDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_gear_iso_material_database(
        self: "Self",
    ) -> "_683.CylindricalGearISOMaterialDatabase":
        """mastapy.gears.materials.CylindricalGearISOMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalGearISOMaterialDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_gear_plastic_material_database(
        self: "Self",
    ) -> "_686.CylindricalGearPlasticMaterialDatabase":
        """mastapy.gears.materials.CylindricalGearPlasticMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalGearPlasticMaterialDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear_material_expert_system_factor_settings(
        self: "Self",
    ) -> "_690.GearMaterialExpertSystemFactorSettings":
        """mastapy.gears.materials.GearMaterialExpertSystemFactorSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GearMaterialExpertSystemFactorSettings"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def isotr1417912001_coefficient_of_friction_constants_database(
        self: "Self",
    ) -> "_699.ISOTR1417912001CoefficientOfFrictionConstantsDatabase":
        """mastapy.gears.materials.ISOTR1417912001CoefficientOfFrictionConstantsDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISOTR1417912001CoefficientOfFrictionConstantsDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def klingelnberg_conical_gear_material_database(
        self: "Self",
    ) -> "_700.KlingelnbergConicalGearMaterialDatabase":
        """mastapy.gears.materials.KlingelnbergConicalGearMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergConicalGearMaterialDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def raw_material_database(self: "Self") -> "_709.RawMaterialDatabase":
        """mastapy.gears.materials.RawMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RawMaterialDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def pocketing_power_loss_coefficients_database(
        self: "Self",
    ) -> "_433.PocketingPowerLossCoefficientsDatabase":
        """mastapy.gears.PocketingPowerLossCoefficientsDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PocketingPowerLossCoefficientsDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_gear_design_and_rating_settings(
        self: "Self",
    ) -> "_543.CylindricalGearDesignAndRatingSettings":
        """mastapy.gears.rating.cylindrical.CylindricalGearDesignAndRatingSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalGearDesignAndRatingSettings"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_gear_design_and_rating_settings_database(
        self: "Self",
    ) -> "_544.CylindricalGearDesignAndRatingSettingsDatabase":
        """mastapy.gears.rating.cylindrical.CylindricalGearDesignAndRatingSettingsDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalGearDesignAndRatingSettingsDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_plastic_gear_rating_settings(
        self: "Self",
    ) -> "_559.CylindricalPlasticGearRatingSettings":
        """mastapy.gears.rating.cylindrical.CylindricalPlasticGearRatingSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalPlasticGearRatingSettings"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_plastic_gear_rating_settings_database(
        self: "Self",
    ) -> "_560.CylindricalPlasticGearRatingSettingsDatabase":
        """mastapy.gears.rating.cylindrical.CylindricalPlasticGearRatingSettingsDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalPlasticGearRatingSettingsDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def critical_speed_analysis_draw_style(
        self: "Self",
    ) -> "_6900.CriticalSpeedAnalysisDrawStyle":
        """mastapy.system_model.analyses_and_results.critical_speed_analyses.CriticalSpeedAnalysisDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CriticalSpeedAnalysisDrawStyle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def harmonic_analysis_draw_style(self: "Self") -> "_6054.HarmonicAnalysisDrawStyle":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.HarmonicAnalysisDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HarmonicAnalysisDrawStyle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def mbd_analysis_draw_style(self: "Self") -> "_5744.MBDAnalysisDrawStyle":
        """mastapy.system_model.analyses_and_results.mbd_analyses.MBDAnalysisDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MBDAnalysisDrawStyle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def modal_analysis_draw_style(self: "Self") -> "_4929.ModalAnalysisDrawStyle":
        """mastapy.system_model.analyses_and_results.modal_analyses.ModalAnalysisDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModalAnalysisDrawStyle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def power_flow_draw_style(self: "Self") -> "_4386.PowerFlowDrawStyle":
        """mastapy.system_model.analyses_and_results.power_flows.PowerFlowDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerFlowDrawStyle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def stability_analysis_draw_style(
        self: "Self",
    ) -> "_4130.StabilityAnalysisDrawStyle":
        """mastapy.system_model.analyses_and_results.stability_analyses.StabilityAnalysisDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StabilityAnalysisDrawStyle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def steady_state_synchronous_response_draw_style(
        self: "Self",
    ) -> "_3337.SteadyStateSynchronousResponseDrawStyle":
        """mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.SteadyStateSynchronousResponseDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SteadyStateSynchronousResponseDrawStyle"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def system_deflection_draw_style(self: "Self") -> "_3069.SystemDeflectionDrawStyle":
        """mastapy.system_model.analyses_and_results.system_deflections.SystemDeflectionDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionDrawStyle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def model_view_options_draw_style(
        self: "Self",
    ) -> "_2473.ModelViewOptionsDrawStyle":
        """mastapy.system_model.drawing.ModelViewOptionsDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModelViewOptionsDrawStyle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def conical_gear_optimization_strategy_database(
        self: "Self",
    ) -> "_2439.ConicalGearOptimizationStrategyDatabase":
        """mastapy.system_model.optimization.ConicalGearOptimizationStrategyDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ConicalGearOptimizationStrategyDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_gear_flank_optimisation_parameters_database(
        self: "Self",
    ) -> "_2456.CylindricalGearFlankOptimisationParametersDatabase":
        """mastapy.system_model.optimization.machine_learning.CylindricalGearFlankOptimisationParametersDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalGearFlankOptimisationParametersDatabase"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def optimization_strategy_database(
        self: "Self",
    ) -> "_2448.OptimizationStrategyDatabase":
        """mastapy.system_model.optimization.OptimizationStrategyDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OptimizationStrategyDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def supercharger_rotor_set_database(
        self: "Self",
    ) -> "_2802.SuperchargerRotorSetDatabase":
        """mastapy.system_model.part_model.gears.supercharger_rotor_set.SuperchargerRotorSetDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SuperchargerRotorSetDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def planet_carrier_settings(self: "Self") -> "_2701.PlanetCarrierSettings":
        """mastapy.system_model.part_model.PlanetCarrierSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PlanetCarrierSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def default_export_settings(self: "Self") -> "_2675.DefaultExportSettings":
        """mastapy.system_model.part_model.DefaultExportSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DefaultExportSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def bearing_material_database(self: "Self") -> "_333.BearingMaterialDatabase":
        """mastapy.materials.BearingMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BearingMaterialDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def component_material_database(self: "Self") -> "_336.ComponentMaterialDatabase":
        """mastapy.materials.ComponentMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentMaterialDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def fluid_database(self: "Self") -> "_343.FluidDatabase":
        """mastapy.materials.FluidDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FluidDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def lubrication_detail_database(self: "Self") -> "_357.LubricationDetailDatabase":
        """mastapy.materials.LubricationDetailDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LubricationDetailDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def materials_settings(self: "Self") -> "_360.MaterialsSettings":
        """mastapy.materials.MaterialsSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaterialsSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def materials_settings_database(self: "Self") -> "_361.MaterialsSettingsDatabase":
        """mastapy.materials.MaterialsSettingsDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaterialsSettingsDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def analysis_settings(self: "Self") -> "_51.AnalysisSettings":
        """mastapy.nodal_analysis.AnalysisSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AnalysisSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def analysis_settings_database(self: "Self") -> "_52.AnalysisSettingsDatabase":
        """mastapy.nodal_analysis.AnalysisSettingsDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AnalysisSettingsDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def fe_user_settings(self: "Self") -> "_71.FEUserSettings":
        """mastapy.nodal_analysis.FEUserSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FEUserSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def geometry_modeller_settings(self: "Self") -> "_238.GeometryModellerSettings":
        """mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GeometryModellerSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def shaft_material_database(self: "Self") -> "_25.ShaftMaterialDatabase":
        """mastapy.shafts.ShaftMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftMaterialDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def shaft_settings(self: "Self") -> "_41.ShaftSettings":
        """mastapy.shafts.ShaftSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def shaft_settings_database(self: "Self") -> "_42.ShaftSettingsDatabase":
        """mastapy.shafts.ShaftSettingsDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftSettingsDatabase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cad_export_settings(self: "Self") -> "_2034.CADExportSettings":
        """mastapy.utility.cad_export.CADExportSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CADExportSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def database_settings(self: "Self") -> "_2026.DatabaseSettings":
        """mastapy.utility.databases.DatabaseSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DatabaseSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def program_settings(self: "Self") -> "_1788.ProgramSettings":
        """mastapy.utility.ProgramSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProgramSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def scripting_setup(self: "Self") -> "_1934.ScriptingSetup":
        """mastapy.utility.scripting.ScriptingSetup

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ScriptingSetup")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def measurement_settings(self: "Self") -> "_1798.MeasurementSettings":
        """mastapy.utility.units_and_measurements.MeasurementSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeasurementSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_MASTASettings":
        """Cast to another type.

        Returns:
            _Cast_MASTASettings
        """
        return _Cast_MASTASettings(self)
