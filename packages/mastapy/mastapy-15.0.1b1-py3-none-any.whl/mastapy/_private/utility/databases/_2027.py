"""NamedDatabase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility.databases import _2029, _2031

_NAMED_DATABASE = python_net_import("SMT.MastaAPI.Utility.Databases", "NamedDatabase")

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.bearings import _2083
    from mastapy._private.bearings.bearing_results.rolling import _2182
    from mastapy._private.bolts import _1652, _1654, _1656, _1661
    from mastapy._private.cycloidal import _1642, _1649
    from mastapy._private.electric_machines import _1405, _1419, _1438, _1453
    from mastapy._private.gears import _433
    from mastapy._private.gears.gear_designs import _1044, _1046, _1049
    from mastapy._private.gears.gear_designs.cylindrical import _1125, _1131
    from mastapy._private.gears.gear_set_pareto_optimiser import (
        _1022,
        _1024,
        _1025,
        _1027,
        _1028,
        _1029,
        _1030,
        _1031,
        _1032,
        _1033,
        _1034,
        _1035,
        _1037,
        _1038,
        _1039,
        _1040,
    )
    from mastapy._private.gears.manufacturing.bevel import _903
    from mastapy._private.gears.manufacturing.cylindrical import _713, _718, _729
    from mastapy._private.gears.manufacturing.cylindrical.cutters import (
        _808,
        _814,
        _819,
        _820,
    )
    from mastapy._private.gears.materials import (
        _676,
        _678,
        _680,
        _682,
        _683,
        _685,
        _686,
        _689,
        _699,
        _700,
        _709,
    )
    from mastapy._private.gears.rating.cylindrical import _544, _560
    from mastapy._private.materials import _333, _336, _343, _357, _359, _361
    from mastapy._private.math_utility.optimisation import _1723, _1736
    from mastapy._private.nodal_analysis import _52
    from mastapy._private.shafts import _25, _42
    from mastapy._private.system_model.optimization import _2439, _2448
    from mastapy._private.system_model.optimization.machine_learning import _2456
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set import (
        _2802,
    )
    from mastapy._private.utility.databases import _2023, _2028

    Self = TypeVar("Self", bound="NamedDatabase")
    CastSelf = TypeVar("CastSelf", bound="NamedDatabase._Cast_NamedDatabase")

TValue = TypeVar("TValue", bound="_2028.NamedDatabaseItem")

__docformat__ = "restructuredtext en"
__all__ = ("NamedDatabase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NamedDatabase:
    """Special nested class for casting NamedDatabase to subclasses."""

    __parent__: "NamedDatabase"

    @property
    def sql_database(self: "CastSelf") -> "_2031.SQLDatabase":
        return self.__parent__._cast(_2031.SQLDatabase)

    @property
    def database(self: "CastSelf") -> "_2023.Database":
        from mastapy._private.utility.databases import _2023

        return self.__parent__._cast(_2023.Database)

    @property
    def shaft_material_database(self: "CastSelf") -> "_25.ShaftMaterialDatabase":
        from mastapy._private.shafts import _25

        return self.__parent__._cast(_25.ShaftMaterialDatabase)

    @property
    def shaft_settings_database(self: "CastSelf") -> "_42.ShaftSettingsDatabase":
        from mastapy._private.shafts import _42

        return self.__parent__._cast(_42.ShaftSettingsDatabase)

    @property
    def analysis_settings_database(self: "CastSelf") -> "_52.AnalysisSettingsDatabase":
        from mastapy._private.nodal_analysis import _52

        return self.__parent__._cast(_52.AnalysisSettingsDatabase)

    @property
    def bearing_material_database(self: "CastSelf") -> "_333.BearingMaterialDatabase":
        from mastapy._private.materials import _333

        return self.__parent__._cast(_333.BearingMaterialDatabase)

    @property
    def component_material_database(
        self: "CastSelf",
    ) -> "_336.ComponentMaterialDatabase":
        from mastapy._private.materials import _336

        return self.__parent__._cast(_336.ComponentMaterialDatabase)

    @property
    def fluid_database(self: "CastSelf") -> "_343.FluidDatabase":
        from mastapy._private.materials import _343

        return self.__parent__._cast(_343.FluidDatabase)

    @property
    def lubrication_detail_database(
        self: "CastSelf",
    ) -> "_357.LubricationDetailDatabase":
        from mastapy._private.materials import _357

        return self.__parent__._cast(_357.LubricationDetailDatabase)

    @property
    def material_database(self: "CastSelf") -> "_359.MaterialDatabase":
        from mastapy._private.materials import _359

        return self.__parent__._cast(_359.MaterialDatabase)

    @property
    def materials_settings_database(
        self: "CastSelf",
    ) -> "_361.MaterialsSettingsDatabase":
        from mastapy._private.materials import _361

        return self.__parent__._cast(_361.MaterialsSettingsDatabase)

    @property
    def pocketing_power_loss_coefficients_database(
        self: "CastSelf",
    ) -> "_433.PocketingPowerLossCoefficientsDatabase":
        from mastapy._private.gears import _433

        return self.__parent__._cast(_433.PocketingPowerLossCoefficientsDatabase)

    @property
    def cylindrical_gear_design_and_rating_settings_database(
        self: "CastSelf",
    ) -> "_544.CylindricalGearDesignAndRatingSettingsDatabase":
        from mastapy._private.gears.rating.cylindrical import _544

        return self.__parent__._cast(
            _544.CylindricalGearDesignAndRatingSettingsDatabase
        )

    @property
    def cylindrical_plastic_gear_rating_settings_database(
        self: "CastSelf",
    ) -> "_560.CylindricalPlasticGearRatingSettingsDatabase":
        from mastapy._private.gears.rating.cylindrical import _560

        return self.__parent__._cast(_560.CylindricalPlasticGearRatingSettingsDatabase)

    @property
    def bevel_gear_abstract_material_database(
        self: "CastSelf",
    ) -> "_676.BevelGearAbstractMaterialDatabase":
        from mastapy._private.gears.materials import _676

        return self.__parent__._cast(_676.BevelGearAbstractMaterialDatabase)

    @property
    def bevel_gear_iso_material_database(
        self: "CastSelf",
    ) -> "_678.BevelGearISOMaterialDatabase":
        from mastapy._private.gears.materials import _678

        return self.__parent__._cast(_678.BevelGearISOMaterialDatabase)

    @property
    def bevel_gear_material_database(
        self: "CastSelf",
    ) -> "_680.BevelGearMaterialDatabase":
        from mastapy._private.gears.materials import _680

        return self.__parent__._cast(_680.BevelGearMaterialDatabase)

    @property
    def cylindrical_gear_agma_material_database(
        self: "CastSelf",
    ) -> "_682.CylindricalGearAGMAMaterialDatabase":
        from mastapy._private.gears.materials import _682

        return self.__parent__._cast(_682.CylindricalGearAGMAMaterialDatabase)

    @property
    def cylindrical_gear_iso_material_database(
        self: "CastSelf",
    ) -> "_683.CylindricalGearISOMaterialDatabase":
        from mastapy._private.gears.materials import _683

        return self.__parent__._cast(_683.CylindricalGearISOMaterialDatabase)

    @property
    def cylindrical_gear_material_database(
        self: "CastSelf",
    ) -> "_685.CylindricalGearMaterialDatabase":
        from mastapy._private.gears.materials import _685

        return self.__parent__._cast(_685.CylindricalGearMaterialDatabase)

    @property
    def cylindrical_gear_plastic_material_database(
        self: "CastSelf",
    ) -> "_686.CylindricalGearPlasticMaterialDatabase":
        from mastapy._private.gears.materials import _686

        return self.__parent__._cast(_686.CylindricalGearPlasticMaterialDatabase)

    @property
    def gear_material_database(self: "CastSelf") -> "_689.GearMaterialDatabase":
        from mastapy._private.gears.materials import _689

        return self.__parent__._cast(_689.GearMaterialDatabase)

    @property
    def isotr1417912001_coefficient_of_friction_constants_database(
        self: "CastSelf",
    ) -> "_699.ISOTR1417912001CoefficientOfFrictionConstantsDatabase":
        from mastapy._private.gears.materials import _699

        return self.__parent__._cast(
            _699.ISOTR1417912001CoefficientOfFrictionConstantsDatabase
        )

    @property
    def klingelnberg_conical_gear_material_database(
        self: "CastSelf",
    ) -> "_700.KlingelnbergConicalGearMaterialDatabase":
        from mastapy._private.gears.materials import _700

        return self.__parent__._cast(_700.KlingelnbergConicalGearMaterialDatabase)

    @property
    def raw_material_database(self: "CastSelf") -> "_709.RawMaterialDatabase":
        from mastapy._private.gears.materials import _709

        return self.__parent__._cast(_709.RawMaterialDatabase)

    @property
    def cylindrical_cutter_database(
        self: "CastSelf",
    ) -> "_713.CylindricalCutterDatabase":
        from mastapy._private.gears.manufacturing.cylindrical import _713

        return self.__parent__._cast(_713.CylindricalCutterDatabase)

    @property
    def cylindrical_hob_database(self: "CastSelf") -> "_718.CylindricalHobDatabase":
        from mastapy._private.gears.manufacturing.cylindrical import _718

        return self.__parent__._cast(_718.CylindricalHobDatabase)

    @property
    def cylindrical_shaper_database(
        self: "CastSelf",
    ) -> "_729.CylindricalShaperDatabase":
        from mastapy._private.gears.manufacturing.cylindrical import _729

        return self.__parent__._cast(_729.CylindricalShaperDatabase)

    @property
    def cylindrical_formed_wheel_grinder_database(
        self: "CastSelf",
    ) -> "_808.CylindricalFormedWheelGrinderDatabase":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _808

        return self.__parent__._cast(_808.CylindricalFormedWheelGrinderDatabase)

    @property
    def cylindrical_gear_plunge_shaver_database(
        self: "CastSelf",
    ) -> "_814.CylindricalGearPlungeShaverDatabase":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _814

        return self.__parent__._cast(_814.CylindricalGearPlungeShaverDatabase)

    @property
    def cylindrical_gear_shaver_database(
        self: "CastSelf",
    ) -> "_819.CylindricalGearShaverDatabase":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _819

        return self.__parent__._cast(_819.CylindricalGearShaverDatabase)

    @property
    def cylindrical_worm_grinder_database(
        self: "CastSelf",
    ) -> "_820.CylindricalWormGrinderDatabase":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _820

        return self.__parent__._cast(_820.CylindricalWormGrinderDatabase)

    @property
    def manufacturing_machine_database(
        self: "CastSelf",
    ) -> "_903.ManufacturingMachineDatabase":
        from mastapy._private.gears.manufacturing.bevel import _903

        return self.__parent__._cast(_903.ManufacturingMachineDatabase)

    @property
    def micro_geometry_design_space_search_strategy_database(
        self: "CastSelf",
    ) -> "_1022.MicroGeometryDesignSpaceSearchStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1022

        return self.__parent__._cast(
            _1022.MicroGeometryDesignSpaceSearchStrategyDatabase
        )

    @property
    def micro_geometry_gear_set_design_space_search_strategy_database(
        self: "CastSelf",
    ) -> "_1024.MicroGeometryGearSetDesignSpaceSearchStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1024

        return self.__parent__._cast(
            _1024.MicroGeometryGearSetDesignSpaceSearchStrategyDatabase
        )

    @property
    def micro_geometry_gear_set_duty_cycle_design_space_search_strategy_database(
        self: "CastSelf",
    ) -> "_1025.MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1025

        return self.__parent__._cast(
            _1025.MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase
        )

    @property
    def pareto_conical_rating_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1027.ParetoConicalRatingOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1027

        return self.__parent__._cast(
            _1027.ParetoConicalRatingOptimisationStrategyDatabase
        )

    @property
    def pareto_cylindrical_gear_set_duty_cycle_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1028.ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1028

        return self.__parent__._cast(
            _1028.ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase
        )

    @property
    def pareto_cylindrical_gear_set_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1029.ParetoCylindricalGearSetOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1029

        return self.__parent__._cast(
            _1029.ParetoCylindricalGearSetOptimisationStrategyDatabase
        )

    @property
    def pareto_cylindrical_rating_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1030.ParetoCylindricalRatingOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1030

        return self.__parent__._cast(
            _1030.ParetoCylindricalRatingOptimisationStrategyDatabase
        )

    @property
    def pareto_face_gear_set_duty_cycle_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1031.ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1031

        return self.__parent__._cast(
            _1031.ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase
        )

    @property
    def pareto_face_gear_set_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1032.ParetoFaceGearSetOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1032

        return self.__parent__._cast(
            _1032.ParetoFaceGearSetOptimisationStrategyDatabase
        )

    @property
    def pareto_face_rating_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1033.ParetoFaceRatingOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1033

        return self.__parent__._cast(_1033.ParetoFaceRatingOptimisationStrategyDatabase)

    @property
    def pareto_hypoid_gear_set_duty_cycle_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1034.ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1034

        return self.__parent__._cast(
            _1034.ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase
        )

    @property
    def pareto_hypoid_gear_set_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1035.ParetoHypoidGearSetOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1035

        return self.__parent__._cast(
            _1035.ParetoHypoidGearSetOptimisationStrategyDatabase
        )

    @property
    def pareto_spiral_bevel_gear_set_duty_cycle_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1037.ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1037

        return self.__parent__._cast(
            _1037.ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase
        )

    @property
    def pareto_spiral_bevel_gear_set_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1038.ParetoSpiralBevelGearSetOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1038

        return self.__parent__._cast(
            _1038.ParetoSpiralBevelGearSetOptimisationStrategyDatabase
        )

    @property
    def pareto_straight_bevel_gear_set_duty_cycle_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1039.ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1039

        return self.__parent__._cast(
            _1039.ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase
        )

    @property
    def pareto_straight_bevel_gear_set_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1040.ParetoStraightBevelGearSetOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1040

        return self.__parent__._cast(
            _1040.ParetoStraightBevelGearSetOptimisationStrategyDatabase
        )

    @property
    def bevel_hypoid_gear_design_settings_database(
        self: "CastSelf",
    ) -> "_1044.BevelHypoidGearDesignSettingsDatabase":
        from mastapy._private.gears.gear_designs import _1044

        return self.__parent__._cast(_1044.BevelHypoidGearDesignSettingsDatabase)

    @property
    def bevel_hypoid_gear_rating_settings_database(
        self: "CastSelf",
    ) -> "_1046.BevelHypoidGearRatingSettingsDatabase":
        from mastapy._private.gears.gear_designs import _1046

        return self.__parent__._cast(_1046.BevelHypoidGearRatingSettingsDatabase)

    @property
    def design_constraint_collection_database(
        self: "CastSelf",
    ) -> "_1049.DesignConstraintCollectionDatabase":
        from mastapy._private.gears.gear_designs import _1049

        return self.__parent__._cast(_1049.DesignConstraintCollectionDatabase)

    @property
    def cylindrical_gear_design_constraints_database(
        self: "CastSelf",
    ) -> "_1125.CylindricalGearDesignConstraintsDatabase":
        from mastapy._private.gears.gear_designs.cylindrical import _1125

        return self.__parent__._cast(_1125.CylindricalGearDesignConstraintsDatabase)

    @property
    def cylindrical_gear_micro_geometry_settings_database(
        self: "CastSelf",
    ) -> "_1131.CylindricalGearMicroGeometrySettingsDatabase":
        from mastapy._private.gears.gear_designs.cylindrical import _1131

        return self.__parent__._cast(_1131.CylindricalGearMicroGeometrySettingsDatabase)

    @property
    def general_electric_machine_material_database(
        self: "CastSelf",
    ) -> "_1405.GeneralElectricMachineMaterialDatabase":
        from mastapy._private.electric_machines import _1405

        return self.__parent__._cast(_1405.GeneralElectricMachineMaterialDatabase)

    @property
    def magnet_material_database(self: "CastSelf") -> "_1419.MagnetMaterialDatabase":
        from mastapy._private.electric_machines import _1419

        return self.__parent__._cast(_1419.MagnetMaterialDatabase)

    @property
    def stator_rotor_material_database(
        self: "CastSelf",
    ) -> "_1438.StatorRotorMaterialDatabase":
        from mastapy._private.electric_machines import _1438

        return self.__parent__._cast(_1438.StatorRotorMaterialDatabase)

    @property
    def winding_material_database(self: "CastSelf") -> "_1453.WindingMaterialDatabase":
        from mastapy._private.electric_machines import _1453

        return self.__parent__._cast(_1453.WindingMaterialDatabase)

    @property
    def cycloidal_disc_material_database(
        self: "CastSelf",
    ) -> "_1642.CycloidalDiscMaterialDatabase":
        from mastapy._private.cycloidal import _1642

        return self.__parent__._cast(_1642.CycloidalDiscMaterialDatabase)

    @property
    def ring_pins_material_database(
        self: "CastSelf",
    ) -> "_1649.RingPinsMaterialDatabase":
        from mastapy._private.cycloidal import _1649

        return self.__parent__._cast(_1649.RingPinsMaterialDatabase)

    @property
    def bolted_joint_material_database(
        self: "CastSelf",
    ) -> "_1652.BoltedJointMaterialDatabase":
        from mastapy._private.bolts import _1652

        return self.__parent__._cast(_1652.BoltedJointMaterialDatabase)

    @property
    def bolt_geometry_database(self: "CastSelf") -> "_1654.BoltGeometryDatabase":
        from mastapy._private.bolts import _1654

        return self.__parent__._cast(_1654.BoltGeometryDatabase)

    @property
    def bolt_material_database(self: "CastSelf") -> "_1656.BoltMaterialDatabase":
        from mastapy._private.bolts import _1656

        return self.__parent__._cast(_1656.BoltMaterialDatabase)

    @property
    def clamped_section_material_database(
        self: "CastSelf",
    ) -> "_1661.ClampedSectionMaterialDatabase":
        from mastapy._private.bolts import _1661

        return self.__parent__._cast(_1661.ClampedSectionMaterialDatabase)

    @property
    def design_space_search_strategy_database(
        self: "CastSelf",
    ) -> "_1723.DesignSpaceSearchStrategyDatabase":
        from mastapy._private.math_utility.optimisation import _1723

        return self.__parent__._cast(_1723.DesignSpaceSearchStrategyDatabase)

    @property
    def pareto_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1736.ParetoOptimisationStrategyDatabase":
        from mastapy._private.math_utility.optimisation import _1736

        return self.__parent__._cast(_1736.ParetoOptimisationStrategyDatabase)

    @property
    def bearing_settings_database(self: "CastSelf") -> "_2083.BearingSettingsDatabase":
        from mastapy._private.bearings import _2083

        return self.__parent__._cast(_2083.BearingSettingsDatabase)

    @property
    def iso14179_settings_database(
        self: "CastSelf",
    ) -> "_2182.ISO14179SettingsDatabase":
        from mastapy._private.bearings.bearing_results.rolling import _2182

        return self.__parent__._cast(_2182.ISO14179SettingsDatabase)

    @property
    def conical_gear_optimization_strategy_database(
        self: "CastSelf",
    ) -> "_2439.ConicalGearOptimizationStrategyDatabase":
        from mastapy._private.system_model.optimization import _2439

        return self.__parent__._cast(_2439.ConicalGearOptimizationStrategyDatabase)

    @property
    def optimization_strategy_database(
        self: "CastSelf",
    ) -> "_2448.OptimizationStrategyDatabase":
        from mastapy._private.system_model.optimization import _2448

        return self.__parent__._cast(_2448.OptimizationStrategyDatabase)

    @property
    def cylindrical_gear_flank_optimisation_parameters_database(
        self: "CastSelf",
    ) -> "_2456.CylindricalGearFlankOptimisationParametersDatabase":
        from mastapy._private.system_model.optimization.machine_learning import _2456

        return self.__parent__._cast(
            _2456.CylindricalGearFlankOptimisationParametersDatabase
        )

    @property
    def supercharger_rotor_set_database(
        self: "CastSelf",
    ) -> "_2802.SuperchargerRotorSetDatabase":
        from mastapy._private.system_model.part_model.gears.supercharger_rotor_set import (
            _2802,
        )

        return self.__parent__._cast(_2802.SuperchargerRotorSetDatabase)

    @property
    def named_database(self: "CastSelf") -> "NamedDatabase":
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
class NamedDatabase(_2031.SQLDatabase[_2029.NamedKey, TValue]):
    """NamedDatabase

    This is a mastapy class.

    Generic Types:
        TValue
    """

    TYPE: ClassVar["Type"] = _NAMED_DATABASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @exception_bridge
    @enforce_parameter_types
    def create(self: "Self", name: "str") -> "TValue":
        """TValue

        Args:
            name (str)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "Create", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def duplicate(
        self: "Self", new_name: "str", item: "_2028.NamedDatabaseItem"
    ) -> "_2028.NamedDatabaseItem":
        """mastapy.utility.databases.NamedDatabaseItem

        Args:
            new_name (str)
            item (mastapy.utility.databases.NamedDatabaseItem)
        """
        new_name = str(new_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "Duplicate",
            new_name if new_name else "",
            item.wrapped if item else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def get_value(self: "Self", name: "str") -> "TValue":
        """TValue

        Args:
            name (str)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "GetValue", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def rename(
        self: "Self", item: "_2028.NamedDatabaseItem", new_name: "str"
    ) -> "bool":
        """bool

        Args:
            item (mastapy.utility.databases.NamedDatabaseItem)
            new_name (str)
        """
        new_name = str(new_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "Rename",
            item.wrapped if item else None,
            new_name if new_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_NamedDatabase":
        """Cast to another type.

        Returns:
            _Cast_NamedDatabase
        """
        return _Cast_NamedDatabase(self)
