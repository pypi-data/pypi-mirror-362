"""Material"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility.databases import _2028

_MATERIAL = python_net_import("SMT.MastaAPI.Materials", "Material")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bolts import _1651, _1655
    from mastapy._private.cycloidal import _1641, _1648
    from mastapy._private.detailed_rigid_connectors.splines import _1601
    from mastapy._private.electric_machines import _1404, _1418, _1437, _1452
    from mastapy._private.gears.materials import (
        _674,
        _677,
        _679,
        _684,
        _688,
        _696,
        _701,
        _705,
    )
    from mastapy._private.materials import _332, _347, _363
    from mastapy._private.shafts import _24

    Self = TypeVar("Self", bound="Material")
    CastSelf = TypeVar("CastSelf", bound="Material._Cast_Material")


__docformat__ = "restructuredtext en"
__all__ = ("Material",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Material:
    """Special nested class for casting Material to subclasses."""

    __parent__: "Material"

    @property
    def named_database_item(self: "CastSelf") -> "_2028.NamedDatabaseItem":
        return self.__parent__._cast(_2028.NamedDatabaseItem)

    @property
    def shaft_material(self: "CastSelf") -> "_24.ShaftMaterial":
        from mastapy._private.shafts import _24

        return self.__parent__._cast(_24.ShaftMaterial)

    @property
    def bearing_material(self: "CastSelf") -> "_332.BearingMaterial":
        from mastapy._private.materials import _332

        return self.__parent__._cast(_332.BearingMaterial)

    @property
    def agma_cylindrical_gear_material(
        self: "CastSelf",
    ) -> "_674.AGMACylindricalGearMaterial":
        from mastapy._private.gears.materials import _674

        return self.__parent__._cast(_674.AGMACylindricalGearMaterial)

    @property
    def bevel_gear_iso_material(self: "CastSelf") -> "_677.BevelGearISOMaterial":
        from mastapy._private.gears.materials import _677

        return self.__parent__._cast(_677.BevelGearISOMaterial)

    @property
    def bevel_gear_material(self: "CastSelf") -> "_679.BevelGearMaterial":
        from mastapy._private.gears.materials import _679

        return self.__parent__._cast(_679.BevelGearMaterial)

    @property
    def cylindrical_gear_material(self: "CastSelf") -> "_684.CylindricalGearMaterial":
        from mastapy._private.gears.materials import _684

        return self.__parent__._cast(_684.CylindricalGearMaterial)

    @property
    def gear_material(self: "CastSelf") -> "_688.GearMaterial":
        from mastapy._private.gears.materials import _688

        return self.__parent__._cast(_688.GearMaterial)

    @property
    def iso_cylindrical_gear_material(
        self: "CastSelf",
    ) -> "_696.ISOCylindricalGearMaterial":
        from mastapy._private.gears.materials import _696

        return self.__parent__._cast(_696.ISOCylindricalGearMaterial)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_material(
        self: "CastSelf",
    ) -> "_701.KlingelnbergCycloPalloidConicalGearMaterial":
        from mastapy._private.gears.materials import _701

        return self.__parent__._cast(_701.KlingelnbergCycloPalloidConicalGearMaterial)

    @property
    def plastic_cylindrical_gear_material(
        self: "CastSelf",
    ) -> "_705.PlasticCylindricalGearMaterial":
        from mastapy._private.gears.materials import _705

        return self.__parent__._cast(_705.PlasticCylindricalGearMaterial)

    @property
    def general_electric_machine_material(
        self: "CastSelf",
    ) -> "_1404.GeneralElectricMachineMaterial":
        from mastapy._private.electric_machines import _1404

        return self.__parent__._cast(_1404.GeneralElectricMachineMaterial)

    @property
    def magnet_material(self: "CastSelf") -> "_1418.MagnetMaterial":
        from mastapy._private.electric_machines import _1418

        return self.__parent__._cast(_1418.MagnetMaterial)

    @property
    def stator_rotor_material(self: "CastSelf") -> "_1437.StatorRotorMaterial":
        from mastapy._private.electric_machines import _1437

        return self.__parent__._cast(_1437.StatorRotorMaterial)

    @property
    def winding_material(self: "CastSelf") -> "_1452.WindingMaterial":
        from mastapy._private.electric_machines import _1452

        return self.__parent__._cast(_1452.WindingMaterial)

    @property
    def spline_material(self: "CastSelf") -> "_1601.SplineMaterial":
        from mastapy._private.detailed_rigid_connectors.splines import _1601

        return self.__parent__._cast(_1601.SplineMaterial)

    @property
    def cycloidal_disc_material(self: "CastSelf") -> "_1641.CycloidalDiscMaterial":
        from mastapy._private.cycloidal import _1641

        return self.__parent__._cast(_1641.CycloidalDiscMaterial)

    @property
    def ring_pins_material(self: "CastSelf") -> "_1648.RingPinsMaterial":
        from mastapy._private.cycloidal import _1648

        return self.__parent__._cast(_1648.RingPinsMaterial)

    @property
    def bolted_joint_material(self: "CastSelf") -> "_1651.BoltedJointMaterial":
        from mastapy._private.bolts import _1651

        return self.__parent__._cast(_1651.BoltedJointMaterial)

    @property
    def bolt_material(self: "CastSelf") -> "_1655.BoltMaterial":
        from mastapy._private.bolts import _1655

        return self.__parent__._cast(_1655.BoltMaterial)

    @property
    def material(self: "CastSelf") -> "Material":
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
class Material(_2028.NamedDatabaseItem):
    """Material

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MATERIAL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def coefficient_of_thermal_expansion(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CoefficientOfThermalExpansion")

        if temp is None:
            return 0.0

        return temp

    @coefficient_of_thermal_expansion.setter
    @exception_bridge
    @enforce_parameter_types
    def coefficient_of_thermal_expansion(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CoefficientOfThermalExpansion",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def cost_per_unit_mass(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CostPerUnitMass")

        if temp is None:
            return 0.0

        return temp

    @cost_per_unit_mass.setter
    @exception_bridge
    @enforce_parameter_types
    def cost_per_unit_mass(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "CostPerUnitMass", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def density(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Density")

        if temp is None:
            return 0.0

        return temp

    @density.setter
    @exception_bridge
    @enforce_parameter_types
    def density(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Density", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def hardness_type(self: "Self") -> "_347.HardnessType":
        """mastapy.materials.HardnessType"""
        temp = pythonnet_property_get(self.wrapped, "HardnessType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Materials.HardnessType")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials._347", "HardnessType"
        )(value)

    @hardness_type.setter
    @exception_bridge
    @enforce_parameter_types
    def hardness_type(self: "Self", value: "_347.HardnessType") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.Materials.HardnessType")
        pythonnet_property_set(self.wrapped, "HardnessType", value)

    @property
    @exception_bridge
    def heat_conductivity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "HeatConductivity")

        if temp is None:
            return 0.0

        return temp

    @heat_conductivity.setter
    @exception_bridge
    @enforce_parameter_types
    def heat_conductivity(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "HeatConductivity", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def material_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaterialName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def maximum_allowable_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumAllowableTemperature")

        if temp is None:
            return 0.0

        return temp

    @maximum_allowable_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_allowable_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumAllowableTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def modulus_of_elasticity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ModulusOfElasticity")

        if temp is None:
            return 0.0

        return temp

    @modulus_of_elasticity.setter
    @exception_bridge
    @enforce_parameter_types
    def modulus_of_elasticity(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ModulusOfElasticity",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def plane_strain_modulus(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PlaneStrainModulus")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def poissons_ratio(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PoissonsRatio")

        if temp is None:
            return 0.0

        return temp

    @poissons_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def poissons_ratio(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "PoissonsRatio", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def shear_fatigue_strength(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShearFatigueStrength")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def shear_modulus(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShearModulus")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def shear_yield_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShearYieldStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def specific_heat(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpecificHeat")

        if temp is None:
            return 0.0

        return temp

    @specific_heat.setter
    @exception_bridge
    @enforce_parameter_types
    def specific_heat(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "SpecificHeat", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def standard(self: "Self") -> "_363.MaterialStandards":
        """mastapy.materials.MaterialStandards

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Standard")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Materials.MaterialStandards"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials._363", "MaterialStandards"
        )(value)

    @property
    @exception_bridge
    def surface_hardness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SurfaceHardness")

        if temp is None:
            return 0.0

        return temp

    @surface_hardness.setter
    @exception_bridge
    @enforce_parameter_types
    def surface_hardness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "SurfaceHardness", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def surface_hardness_range_max_in_hb(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SurfaceHardnessRangeMaxInHB")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def surface_hardness_range_max_in_hrc(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SurfaceHardnessRangeMaxInHRC")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def surface_hardness_range_max_in_hv(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SurfaceHardnessRangeMaxInHV")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def surface_hardness_range_min_in_hb(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SurfaceHardnessRangeMinInHB")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def surface_hardness_range_min_in_hrc(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SurfaceHardnessRangeMinInHRC")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def surface_hardness_range_min_in_hv(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SurfaceHardnessRangeMinInHV")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tensile_yield_strength(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TensileYieldStrength")

        if temp is None:
            return 0.0

        return temp

    @tensile_yield_strength.setter
    @exception_bridge
    @enforce_parameter_types
    def tensile_yield_strength(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TensileYieldStrength",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def ultimate_tensile_strength(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "UltimateTensileStrength")

        if temp is None:
            return 0.0

        return temp

    @ultimate_tensile_strength.setter
    @exception_bridge
    @enforce_parameter_types
    def ultimate_tensile_strength(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UltimateTensileStrength",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_Material":
        """Cast to another type.

        Returns:
            _Cast_Material
        """
        return _Cast_Material(self)
