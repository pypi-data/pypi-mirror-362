"""NamedDatabaseItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_NAMED_DATABASE_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Databases", "NamedDatabaseItem"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.bearings import _2084
    from mastapy._private.bearings.bearing_results.rolling import _2181
    from mastapy._private.bolts import _1651, _1653, _1655
    from mastapy._private.cycloidal import _1641, _1648
    from mastapy._private.detailed_rigid_connectors.splines import _1601
    from mastapy._private.electric_machines import _1404, _1418, _1437, _1452
    from mastapy._private.gears import _432
    from mastapy._private.gears.gear_designs import _1045, _1047, _1050
    from mastapy._private.gears.gear_designs.cylindrical import _1124, _1132
    from mastapy._private.gears.manufacturing.bevel import _902
    from mastapy._private.gears.manufacturing.cylindrical.cutters import (
        _809,
        _810,
        _811,
        _812,
        _813,
        _815,
        _816,
        _817,
        _818,
        _821,
    )
    from mastapy._private.gears.materials import (
        _674,
        _677,
        _679,
        _684,
        _688,
        _696,
        _698,
        _701,
        _705,
        _708,
    )
    from mastapy._private.gears.rating.cylindrical import _545, _561
    from mastapy._private.materials import _332, _342, _356, _358, _362
    from mastapy._private.math_utility.optimisation import _1733
    from mastapy._private.nodal_analysis import _53
    from mastapy._private.shafts import _24, _43, _46
    from mastapy._private.system_model.optimization import _2437, _2440, _2446, _2447
    from mastapy._private.system_model.optimization.machine_learning import _2455
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set import (
        _2801,
    )
    from mastapy._private.utility import _1775
    from mastapy._private.utility.databases import _2029

    Self = TypeVar("Self", bound="NamedDatabaseItem")
    CastSelf = TypeVar("CastSelf", bound="NamedDatabaseItem._Cast_NamedDatabaseItem")


__docformat__ = "restructuredtext en"
__all__ = ("NamedDatabaseItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NamedDatabaseItem:
    """Special nested class for casting NamedDatabaseItem to subclasses."""

    __parent__: "NamedDatabaseItem"

    @property
    def shaft_material(self: "CastSelf") -> "_24.ShaftMaterial":
        from mastapy._private.shafts import _24

        return self.__parent__._cast(_24.ShaftMaterial)

    @property
    def shaft_settings_item(self: "CastSelf") -> "_43.ShaftSettingsItem":
        from mastapy._private.shafts import _43

        return self.__parent__._cast(_43.ShaftSettingsItem)

    @property
    def simple_shaft_definition(self: "CastSelf") -> "_46.SimpleShaftDefinition":
        from mastapy._private.shafts import _46

        return self.__parent__._cast(_46.SimpleShaftDefinition)

    @property
    def analysis_settings_item(self: "CastSelf") -> "_53.AnalysisSettingsItem":
        from mastapy._private.nodal_analysis import _53

        return self.__parent__._cast(_53.AnalysisSettingsItem)

    @property
    def bearing_material(self: "CastSelf") -> "_332.BearingMaterial":
        from mastapy._private.materials import _332

        return self.__parent__._cast(_332.BearingMaterial)

    @property
    def fluid(self: "CastSelf") -> "_342.Fluid":
        from mastapy._private.materials import _342

        return self.__parent__._cast(_342.Fluid)

    @property
    def lubrication_detail(self: "CastSelf") -> "_356.LubricationDetail":
        from mastapy._private.materials import _356

        return self.__parent__._cast(_356.LubricationDetail)

    @property
    def material(self: "CastSelf") -> "_358.Material":
        from mastapy._private.materials import _358

        return self.__parent__._cast(_358.Material)

    @property
    def materials_settings_item(self: "CastSelf") -> "_362.MaterialsSettingsItem":
        from mastapy._private.materials import _362

        return self.__parent__._cast(_362.MaterialsSettingsItem)

    @property
    def pocketing_power_loss_coefficients(
        self: "CastSelf",
    ) -> "_432.PocketingPowerLossCoefficients":
        from mastapy._private.gears import _432

        return self.__parent__._cast(_432.PocketingPowerLossCoefficients)

    @property
    def cylindrical_gear_design_and_rating_settings_item(
        self: "CastSelf",
    ) -> "_545.CylindricalGearDesignAndRatingSettingsItem":
        from mastapy._private.gears.rating.cylindrical import _545

        return self.__parent__._cast(_545.CylindricalGearDesignAndRatingSettingsItem)

    @property
    def cylindrical_plastic_gear_rating_settings_item(
        self: "CastSelf",
    ) -> "_561.CylindricalPlasticGearRatingSettingsItem":
        from mastapy._private.gears.rating.cylindrical import _561

        return self.__parent__._cast(_561.CylindricalPlasticGearRatingSettingsItem)

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
    def isotr1417912001_coefficient_of_friction_constants(
        self: "CastSelf",
    ) -> "_698.ISOTR1417912001CoefficientOfFrictionConstants":
        from mastapy._private.gears.materials import _698

        return self.__parent__._cast(_698.ISOTR1417912001CoefficientOfFrictionConstants)

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
    def raw_material(self: "CastSelf") -> "_708.RawMaterial":
        from mastapy._private.gears.materials import _708

        return self.__parent__._cast(_708.RawMaterial)

    @property
    def cylindrical_gear_abstract_cutter_design(
        self: "CastSelf",
    ) -> "_809.CylindricalGearAbstractCutterDesign":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _809

        return self.__parent__._cast(_809.CylindricalGearAbstractCutterDesign)

    @property
    def cylindrical_gear_form_grinding_wheel(
        self: "CastSelf",
    ) -> "_810.CylindricalGearFormGrindingWheel":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _810

        return self.__parent__._cast(_810.CylindricalGearFormGrindingWheel)

    @property
    def cylindrical_gear_grinding_worm(
        self: "CastSelf",
    ) -> "_811.CylindricalGearGrindingWorm":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _811

        return self.__parent__._cast(_811.CylindricalGearGrindingWorm)

    @property
    def cylindrical_gear_hob_design(
        self: "CastSelf",
    ) -> "_812.CylindricalGearHobDesign":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _812

        return self.__parent__._cast(_812.CylindricalGearHobDesign)

    @property
    def cylindrical_gear_plunge_shaver(
        self: "CastSelf",
    ) -> "_813.CylindricalGearPlungeShaver":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _813

        return self.__parent__._cast(_813.CylindricalGearPlungeShaver)

    @property
    def cylindrical_gear_rack_design(
        self: "CastSelf",
    ) -> "_815.CylindricalGearRackDesign":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _815

        return self.__parent__._cast(_815.CylindricalGearRackDesign)

    @property
    def cylindrical_gear_real_cutter_design(
        self: "CastSelf",
    ) -> "_816.CylindricalGearRealCutterDesign":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _816

        return self.__parent__._cast(_816.CylindricalGearRealCutterDesign)

    @property
    def cylindrical_gear_shaper(self: "CastSelf") -> "_817.CylindricalGearShaper":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _817

        return self.__parent__._cast(_817.CylindricalGearShaper)

    @property
    def cylindrical_gear_shaver(self: "CastSelf") -> "_818.CylindricalGearShaver":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _818

        return self.__parent__._cast(_818.CylindricalGearShaver)

    @property
    def involute_cutter_design(self: "CastSelf") -> "_821.InvoluteCutterDesign":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _821

        return self.__parent__._cast(_821.InvoluteCutterDesign)

    @property
    def manufacturing_machine(self: "CastSelf") -> "_902.ManufacturingMachine":
        from mastapy._private.gears.manufacturing.bevel import _902

        return self.__parent__._cast(_902.ManufacturingMachine)

    @property
    def bevel_hypoid_gear_design_settings_item(
        self: "CastSelf",
    ) -> "_1045.BevelHypoidGearDesignSettingsItem":
        from mastapy._private.gears.gear_designs import _1045

        return self.__parent__._cast(_1045.BevelHypoidGearDesignSettingsItem)

    @property
    def bevel_hypoid_gear_rating_settings_item(
        self: "CastSelf",
    ) -> "_1047.BevelHypoidGearRatingSettingsItem":
        from mastapy._private.gears.gear_designs import _1047

        return self.__parent__._cast(_1047.BevelHypoidGearRatingSettingsItem)

    @property
    def design_constraints_collection(
        self: "CastSelf",
    ) -> "_1050.DesignConstraintsCollection":
        from mastapy._private.gears.gear_designs import _1050

        return self.__parent__._cast(_1050.DesignConstraintsCollection)

    @property
    def cylindrical_gear_design_constraints(
        self: "CastSelf",
    ) -> "_1124.CylindricalGearDesignConstraints":
        from mastapy._private.gears.gear_designs.cylindrical import _1124

        return self.__parent__._cast(_1124.CylindricalGearDesignConstraints)

    @property
    def cylindrical_gear_micro_geometry_settings_item(
        self: "CastSelf",
    ) -> "_1132.CylindricalGearMicroGeometrySettingsItem":
        from mastapy._private.gears.gear_designs.cylindrical import _1132

        return self.__parent__._cast(_1132.CylindricalGearMicroGeometrySettingsItem)

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
    def bolt_geometry(self: "CastSelf") -> "_1653.BoltGeometry":
        from mastapy._private.bolts import _1653

        return self.__parent__._cast(_1653.BoltGeometry)

    @property
    def bolt_material(self: "CastSelf") -> "_1655.BoltMaterial":
        from mastapy._private.bolts import _1655

        return self.__parent__._cast(_1655.BoltMaterial)

    @property
    def pareto_optimisation_strategy(
        self: "CastSelf",
    ) -> "_1733.ParetoOptimisationStrategy":
        from mastapy._private.math_utility.optimisation import _1733

        return self.__parent__._cast(_1733.ParetoOptimisationStrategy)

    @property
    def bearing_settings_item(self: "CastSelf") -> "_2084.BearingSettingsItem":
        from mastapy._private.bearings import _2084

        return self.__parent__._cast(_2084.BearingSettingsItem)

    @property
    def iso14179_settings(self: "CastSelf") -> "_2181.ISO14179Settings":
        from mastapy._private.bearings.bearing_results.rolling import _2181

        return self.__parent__._cast(_2181.ISO14179Settings)

    @property
    def conical_gear_optimisation_strategy(
        self: "CastSelf",
    ) -> "_2437.ConicalGearOptimisationStrategy":
        from mastapy._private.system_model.optimization import _2437

        return self.__parent__._cast(_2437.ConicalGearOptimisationStrategy)

    @property
    def cylindrical_gear_optimisation_strategy(
        self: "CastSelf",
    ) -> "_2440.CylindricalGearOptimisationStrategy":
        from mastapy._private.system_model.optimization import _2440

        return self.__parent__._cast(_2440.CylindricalGearOptimisationStrategy)

    @property
    def optimization_strategy(self: "CastSelf") -> "_2446.OptimizationStrategy":
        from mastapy._private.system_model.optimization import _2446

        return self.__parent__._cast(_2446.OptimizationStrategy)

    @property
    def optimization_strategy_base(
        self: "CastSelf",
    ) -> "_2447.OptimizationStrategyBase":
        from mastapy._private.system_model.optimization import _2447

        return self.__parent__._cast(_2447.OptimizationStrategyBase)

    @property
    def cylindrical_gear_flank_optimisation_parameters(
        self: "CastSelf",
    ) -> "_2455.CylindricalGearFlankOptimisationParameters":
        from mastapy._private.system_model.optimization.machine_learning import _2455

        return self.__parent__._cast(_2455.CylindricalGearFlankOptimisationParameters)

    @property
    def supercharger_rotor_set(self: "CastSelf") -> "_2801.SuperchargerRotorSet":
        from mastapy._private.system_model.part_model.gears.supercharger_rotor_set import (
            _2801,
        )

        return self.__parent__._cast(_2801.SuperchargerRotorSet)

    @property
    def named_database_item(self: "CastSelf") -> "NamedDatabaseItem":
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
class NamedDatabaseItem(_0.APIBase):
    """NamedDatabaseItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NAMED_DATABASE_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def comment(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Comment")

        if temp is None:
            return ""

        return temp

    @comment.setter
    @exception_bridge
    @enforce_parameter_types
    def comment(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Comment", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def no_history(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NoHistory")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def history(self: "Self") -> "_1775.FileHistory":
        """mastapy.utility.FileHistory

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "History")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def database_key(self: "Self") -> "_2029.NamedKey":
        """mastapy.utility.databases.NamedKey"""
        temp = pythonnet_property_get(self.wrapped, "DatabaseKey")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @database_key.setter
    @exception_bridge
    @enforce_parameter_types
    def database_key(self: "Self", value: "_2029.NamedKey") -> None:
        pythonnet_property_set(self.wrapped, "DatabaseKey", value.wrapped)

    @property
    @exception_bridge
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @exception_bridge
    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputDefaultReportTo", file_path)

    @exception_bridge
    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportTo", file_path)

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportAsTextTo", file_path)

    @exception_bridge
    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_NamedDatabaseItem":
        """Cast to another type.

        Returns:
            _Cast_NamedDatabaseItem
        """
        return _Cast_NamedDatabaseItem(self)
