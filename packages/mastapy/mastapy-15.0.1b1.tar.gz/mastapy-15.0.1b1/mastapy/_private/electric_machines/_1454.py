"""Windings"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import list_with_selected_item, overridable
from mastapy._private._internal.list_with_selected_item import (
    promote_to_list_with_selected_item,
)
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_get_with_method,
    pythonnet_property_set,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_WINDINGS = python_net_import("SMT.MastaAPI.ElectricMachines", "Windings")

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.electric_machines import (
        _1376,
        _1383,
        _1400,
        _1426,
        _1433,
        _1434,
        _1450,
        _1451,
        _1455,
        _1456,
        _1457,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses import _1546
    from mastapy._private.math_utility import _1697
    from mastapy._private.utility_gui.charts import _2070

    Self = TypeVar("Self", bound="Windings")
    CastSelf = TypeVar("CastSelf", bound="Windings._Cast_Windings")


__docformat__ = "restructuredtext en"
__all__ = ("Windings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Windings:
    """Special nested class for casting Windings to subclasses."""

    __parent__: "Windings"

    @property
    def windings(self: "CastSelf") -> "Windings":
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
class Windings(_0.APIBase):
    """Windings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WINDINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def awg_selector(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_int":
        """ListWithSelectedItem[int]"""
        temp = pythonnet_property_get(self.wrapped, "AWGSelector")

        if temp is None:
            return 0

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_int",
        )(temp)

    @awg_selector.setter
    @exception_bridge
    @enforce_parameter_types
    def awg_selector(self: "Self", value: "int") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_int.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "AWGSelector", value)

    @property
    @exception_bridge
    def double_layer_winding_slot_positions(
        self: "Self",
    ) -> "_1383.DoubleLayerWindingSlotPositions":
        """mastapy.electric_machines.DoubleLayerWindingSlotPositions"""
        temp = pythonnet_property_get(self.wrapped, "DoubleLayerWindingSlotPositions")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.ElectricMachines.DoubleLayerWindingSlotPositions"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines._1383",
            "DoubleLayerWindingSlotPositions",
        )(value)

    @double_layer_winding_slot_positions.setter
    @exception_bridge
    @enforce_parameter_types
    def double_layer_winding_slot_positions(
        self: "Self", value: "_1383.DoubleLayerWindingSlotPositions"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.ElectricMachines.DoubleLayerWindingSlotPositions"
        )
        pythonnet_property_set(self.wrapped, "DoubleLayerWindingSlotPositions", value)

    @property
    @exception_bridge
    def end_winding_inductance_rosa_and_grover(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EndWindingInductanceRosaAndGrover")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def end_winding_inductance_method(
        self: "Self",
    ) -> "_1546.EndWindingInductanceMethod":
        """mastapy.electric_machines.load_cases_and_analyses.EndWindingInductanceMethod"""
        temp = pythonnet_property_get(self.wrapped, "EndWindingInductanceMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses.EndWindingInductanceMethod",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines.load_cases_and_analyses._1546",
            "EndWindingInductanceMethod",
        )(value)

    @end_winding_inductance_method.setter
    @exception_bridge
    @enforce_parameter_types
    def end_winding_inductance_method(
        self: "Self", value: "_1546.EndWindingInductanceMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses.EndWindingInductanceMethod",
        )
        pythonnet_property_set(self.wrapped, "EndWindingInductanceMethod", value)

    @property
    @exception_bridge
    def end_winding_pole_pitch_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EndWindingPolePitchFactor")

        if temp is None:
            return 0.0

        return temp

    @end_winding_pole_pitch_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def end_winding_pole_pitch_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EndWindingPolePitchFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def factor_for_phase_circle_size(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "FactorForPhaseCircleSize")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @factor_for_phase_circle_size.setter
    @exception_bridge
    @enforce_parameter_types
    def factor_for_phase_circle_size(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "FactorForPhaseCircleSize", value)

    @property
    @exception_bridge
    def fill_factor_specification_method(
        self: "Self",
    ) -> "_1400.FillFactorSpecificationMethod":
        """mastapy.electric_machines.FillFactorSpecificationMethod"""
        temp = pythonnet_property_get(self.wrapped, "FillFactorSpecificationMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.ElectricMachines.FillFactorSpecificationMethod"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines._1400", "FillFactorSpecificationMethod"
        )(value)

    @fill_factor_specification_method.setter
    @exception_bridge
    @enforce_parameter_types
    def fill_factor_specification_method(
        self: "Self", value: "_1400.FillFactorSpecificationMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.ElectricMachines.FillFactorSpecificationMethod"
        )
        pythonnet_property_set(self.wrapped, "FillFactorSpecificationMethod", value)

    @property
    @exception_bridge
    def iec60228_wire_gauge_selector(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_float":
        """ListWithSelectedItem[float]"""
        temp = pythonnet_property_get(self.wrapped, "IEC60228WireGaugeSelector")

        if temp is None:
            return 0.0

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_float",
        )(temp)

    @iec60228_wire_gauge_selector.setter
    @exception_bridge
    @enforce_parameter_types
    def iec60228_wire_gauge_selector(self: "Self", value: "float") -> None:
        generic_type = (
            list_with_selected_item.ListWithSelectedItem_float.implicit_type()
        )
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "IEC60228WireGaugeSelector", value)

    @property
    @exception_bridge
    def include_individual_conductors(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeIndividualConductors")

        if temp is None:
            return False

        return temp

    @include_individual_conductors.setter
    @exception_bridge
    @enforce_parameter_types
    def include_individual_conductors(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeIndividualConductors",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def mmf(self: "Self") -> "_2070.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MMF")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def mass(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Mass")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def material_cost(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaterialCost")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_length_per_turn(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanLengthPerTurn")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def number_of_coils_per_parallel_path(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfCoilsPerParallelPath")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_coils_per_phase(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfCoilsPerPhase")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_coils_per_phase_per_parallel_path(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfCoilsPerPhasePerParallelPath"
        )

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_electrical_orders_for_mmf_chart(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfElectricalOrdersForMMFChart"
        )

        if temp is None:
            return 0

        return temp

    @number_of_electrical_orders_for_mmf_chart.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_electrical_orders_for_mmf_chart(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfElectricalOrdersForMMFChart",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def number_of_parallel_paths(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfParallelPaths")

        if temp is None:
            return 0

        return temp

    @number_of_parallel_paths.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_parallel_paths(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfParallelPaths",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def number_of_strands_per_turn(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfStrandsPerTurn")

        if temp is None:
            return 0

        return temp

    @number_of_strands_per_turn.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_strands_per_turn(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfStrandsPerTurn",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def number_of_turns(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfTurns")

        if temp is None:
            return 0

        return temp

    @number_of_turns.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_turns(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfTurns", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def number_of_turns_per_phase(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfTurnsPerPhase")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_winding_layers(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfWindingLayers")

        if temp is None:
            return 0

        return temp

    @number_of_winding_layers.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_winding_layers(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfWindingLayers",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def overall_fill_factor_windings(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OverallFillFactorWindings")

        if temp is None:
            return 0.0

        return temp

    @overall_fill_factor_windings.setter
    @exception_bridge
    @enforce_parameter_types
    def overall_fill_factor_windings(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OverallFillFactorWindings",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def overall_winding_material_area(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OverallWindingMaterialArea")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def single_double_layer_windings(
        self: "Self",
    ) -> "_1433.SingleOrDoubleLayerWindings":
        """mastapy.electric_machines.SingleOrDoubleLayerWindings"""
        temp = pythonnet_property_get(self.wrapped, "SingleDoubleLayerWindings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.ElectricMachines.SingleOrDoubleLayerWindings"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines._1433", "SingleOrDoubleLayerWindings"
        )(value)

    @single_double_layer_windings.setter
    @exception_bridge
    @enforce_parameter_types
    def single_double_layer_windings(
        self: "Self", value: "_1433.SingleOrDoubleLayerWindings"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.ElectricMachines.SingleOrDoubleLayerWindings"
        )
        pythonnet_property_set(self.wrapped, "SingleDoubleLayerWindings", value)

    @property
    @exception_bridge
    def throw_for_automated_winding_generation(
        self: "Self",
    ) -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(
            self.wrapped, "ThrowForAutomatedWindingGeneration"
        )

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @throw_for_automated_winding_generation.setter
    @exception_bridge
    @enforce_parameter_types
    def throw_for_automated_winding_generation(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "ThrowForAutomatedWindingGeneration", value
        )

    @property
    @exception_bridge
    def total_length_of_conductors_in_phase(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalLengthOfConductorsInPhase")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_slot_area(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalSlotArea")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def user_specified_end_winding_inductance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "UserSpecifiedEndWindingInductance")

        if temp is None:
            return 0.0

        return temp

    @user_specified_end_winding_inductance.setter
    @exception_bridge
    @enforce_parameter_types
    def user_specified_end_winding_inductance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UserSpecifiedEndWindingInductance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def winding_connection(self: "Self") -> "_1451.WindingConnection":
        """mastapy.electric_machines.WindingConnection"""
        temp = pythonnet_property_get(self.wrapped, "WindingConnection")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.ElectricMachines.WindingConnection"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines._1451", "WindingConnection"
        )(value)

    @winding_connection.setter
    @exception_bridge
    @enforce_parameter_types
    def winding_connection(self: "Self", value: "_1451.WindingConnection") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.ElectricMachines.WindingConnection"
        )
        pythonnet_property_set(self.wrapped, "WindingConnection", value)

    @property
    @exception_bridge
    def winding_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WindingFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def winding_material_database(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "WindingMaterialDatabase", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @winding_material_database.setter
    @exception_bridge
    @enforce_parameter_types
    def winding_material_database(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "WindingMaterialDatabase",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def winding_material_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WindingMaterialDiameter")

        if temp is None:
            return 0.0

        return temp

    @winding_material_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def winding_material_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "WindingMaterialDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def winding_type(self: "Self") -> "_1456.WindingType":
        """mastapy.electric_machines.WindingType"""
        temp = pythonnet_property_get(self.wrapped, "WindingType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.ElectricMachines.WindingType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines._1456", "WindingType"
        )(value)

    @winding_type.setter
    @exception_bridge
    @enforce_parameter_types
    def winding_type(self: "Self", value: "_1456.WindingType") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.ElectricMachines.WindingType"
        )
        pythonnet_property_set(self.wrapped, "WindingType", value)

    @property
    @exception_bridge
    def wire_size_specification_method(
        self: "Self",
    ) -> "_1457.WireSizeSpecificationMethod":
        """mastapy.electric_machines.WireSizeSpecificationMethod"""
        temp = pythonnet_property_get(self.wrapped, "WireSizeSpecificationMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.ElectricMachines.WireSizeSpecificationMethod"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines._1457", "WireSizeSpecificationMethod"
        )(value)

    @wire_size_specification_method.setter
    @exception_bridge
    @enforce_parameter_types
    def wire_size_specification_method(
        self: "Self", value: "_1457.WireSizeSpecificationMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.ElectricMachines.WireSizeSpecificationMethod"
        )
        pythonnet_property_set(self.wrapped, "WireSizeSpecificationMethod", value)

    @property
    @exception_bridge
    def mmf_fourier_series_electrical(self: "Self") -> "_1697.FourierSeries":
        """mastapy.math_utility.FourierSeries

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MMFFourierSeriesElectrical")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def mmf_fourier_series_mechanical(self: "Self") -> "_1697.FourierSeries":
        """mastapy.math_utility.FourierSeries

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MMFFourierSeriesMechanical")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def windings_viewer(self: "Self") -> "_1455.WindingsViewer":
        """mastapy.electric_machines.WindingsViewer

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WindingsViewer")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def coils(self: "Self") -> "List[_1376.Coil]":
        """List[mastapy.electric_machines.Coil]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Coils")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def conductors(self: "Self") -> "List[_1450.WindingConductor]":
        """List[mastapy.electric_machines.WindingConductor]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Conductors")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def phases(self: "Self") -> "List[_1426.Phase]":
        """List[mastapy.electric_machines.Phase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Phases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def slot_section_details(self: "Self") -> "List[_1434.SlotSectionDetail]":
        """List[mastapy.electric_machines.SlotSectionDetail]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SlotSectionDetails")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

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
    def generate_default_winding_configuration_coils(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "GenerateDefaultWindingConfigurationCoils")

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
    def cast_to(self: "Self") -> "_Cast_Windings":
        """Cast to another type.

        Returns:
            _Cast_Windings
        """
        return _Cast_Windings(self)
