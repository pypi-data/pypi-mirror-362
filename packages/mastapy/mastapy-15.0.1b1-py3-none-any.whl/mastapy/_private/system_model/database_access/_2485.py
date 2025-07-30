"""Databases"""

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

_DATABASES = python_net_import("SMT.MastaAPI.SystemModel.DatabaseAccess", "Databases")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings import _2096
    from mastapy._private.bolts import _1654, _1656, _1661
    from mastapy._private.electric_machines import _1419, _1438, _1453
    from mastapy._private.gears.gear_set_pareto_optimiser import (
        _1024,
        _1025,
        _1028,
        _1029,
        _1034,
        _1035,
        _1037,
        _1038,
        _1039,
        _1040,
    )
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
        _700,
        _709,
    )
    from mastapy._private.materials import _333, _336, _357
    from mastapy._private.shafts import _25
    from mastapy._private.system_model.optimization import _2439, _2448
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set import (
        _2802,
    )

    Self = TypeVar("Self", bound="Databases")
    CastSelf = TypeVar("CastSelf", bound="Databases._Cast_Databases")


__docformat__ = "restructuredtext en"
__all__ = ("Databases",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Databases:
    """Special nested class for casting Databases to subclasses."""

    __parent__: "Databases"

    @property
    def databases(self: "CastSelf") -> "Databases":
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
class Databases(_0.APIBase):
    """Databases

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DATABASES

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def bevel_gear_iso_material_database(
        self: "Self",
    ) -> "_678.BevelGearISOMaterialDatabase":
        """mastapy.gears.materials.BevelGearISOMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelGearIsoMaterialDatabase")

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
    def stator_and_rotor_material_database(
        self: "Self",
    ) -> "_1438.StatorRotorMaterialDatabase":
        """mastapy.electric_machines.StatorRotorMaterialDatabase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StatorAndRotorMaterialDatabase")

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
    def cast_to(self: "Self") -> "_Cast_Databases":
        """Cast to another type.

        Returns:
            _Cast_Databases
        """
        return _Cast_Databases(self)
