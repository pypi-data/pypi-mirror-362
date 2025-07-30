"""ElectricMachineHarmonicLoadDataBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import (
    enum_with_selected_value,
    list_with_selected_item,
)
from mastapy._private._internal.list_with_selected_item import (
    promote_to_list_with_selected_item,
)
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.electric_machines import _1431
from mastapy._private.electric_machines.harmonic_load_data import (
    _1563,
    _1566,
    _1567,
    _1568,
)

_ELECTRIC_MACHINE_HARMONIC_LOAD_DATA_BASE = python_net_import(
    "SMT.MastaAPI.ElectricMachines.HarmonicLoadData",
    "ElectricMachineHarmonicLoadDataBase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.electric_machines.harmonic_load_data import (
        _1564,
        _1570,
        _1571,
    )
    from mastapy._private.electric_machines.results import _1505
    from mastapy._private.math_utility import _1705
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7740,
        _7741,
        _7742,
        _7743,
        _7744,
        _7745,
        _7746,
    )
    from mastapy._private.utility_gui.charts import _2065, _2069

    Self = TypeVar("Self", bound="ElectricMachineHarmonicLoadDataBase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElectricMachineHarmonicLoadDataBase._Cast_ElectricMachineHarmonicLoadDataBase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineHarmonicLoadDataBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineHarmonicLoadDataBase:
    """Special nested class for casting ElectricMachineHarmonicLoadDataBase to subclasses."""

    __parent__: "ElectricMachineHarmonicLoadDataBase"

    @property
    def speed_dependent_harmonic_load_data(
        self: "CastSelf",
    ) -> "_1568.SpeedDependentHarmonicLoadData":
        return self.__parent__._cast(_1568.SpeedDependentHarmonicLoadData)

    @property
    def harmonic_load_data_base(self: "CastSelf") -> "_1564.HarmonicLoadDataBase":
        from mastapy._private.electric_machines.harmonic_load_data import _1564

        return self.__parent__._cast(_1564.HarmonicLoadDataBase)

    @property
    def dynamic_force_results(self: "CastSelf") -> "_1505.DynamicForceResults":
        from mastapy._private.electric_machines.results import _1505

        return self.__parent__._cast(_1505.DynamicForceResults)

    @property
    def electric_machine_harmonic_load_data(
        self: "CastSelf",
    ) -> "_7740.ElectricMachineHarmonicLoadData":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7740,
        )

        return self.__parent__._cast(_7740.ElectricMachineHarmonicLoadData)

    @property
    def electric_machine_harmonic_load_data_from_excel(
        self: "CastSelf",
    ) -> "_7741.ElectricMachineHarmonicLoadDataFromExcel":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7741,
        )

        return self.__parent__._cast(_7741.ElectricMachineHarmonicLoadDataFromExcel)

    @property
    def electric_machine_harmonic_load_data_from_flux(
        self: "CastSelf",
    ) -> "_7742.ElectricMachineHarmonicLoadDataFromFlux":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7742,
        )

        return self.__parent__._cast(_7742.ElectricMachineHarmonicLoadDataFromFlux)

    @property
    def electric_machine_harmonic_load_data_from_jmag(
        self: "CastSelf",
    ) -> "_7743.ElectricMachineHarmonicLoadDataFromJMAG":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7743,
        )

        return self.__parent__._cast(_7743.ElectricMachineHarmonicLoadDataFromJMAG)

    @property
    def electric_machine_harmonic_load_data_from_masta(
        self: "CastSelf",
    ) -> "_7744.ElectricMachineHarmonicLoadDataFromMASTA":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7744,
        )

        return self.__parent__._cast(_7744.ElectricMachineHarmonicLoadDataFromMASTA)

    @property
    def electric_machine_harmonic_load_data_from_motor_cad(
        self: "CastSelf",
    ) -> "_7745.ElectricMachineHarmonicLoadDataFromMotorCAD":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7745,
        )

        return self.__parent__._cast(_7745.ElectricMachineHarmonicLoadDataFromMotorCAD)

    @property
    def electric_machine_harmonic_load_data_from_motor_packages(
        self: "CastSelf",
    ) -> "_7746.ElectricMachineHarmonicLoadDataFromMotorPackages":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7746,
        )

        return self.__parent__._cast(
            _7746.ElectricMachineHarmonicLoadDataFromMotorPackages
        )

    @property
    def electric_machine_harmonic_load_data_base(
        self: "CastSelf",
    ) -> "ElectricMachineHarmonicLoadDataBase":
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
class ElectricMachineHarmonicLoadDataBase(_1568.SpeedDependentHarmonicLoadData):
    """ElectricMachineHarmonicLoadDataBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELECTRIC_MACHINE_HARMONIC_LOAD_DATA_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def compare_torque_ripple_and_stator_torque_reaction_derived_from_stator_tangential_loads(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped,
            "CompareTorqueRippleAndStatorTorqueReactionDerivedFromStatorTangentialLoads",
        )

        if temp is None:
            return False

        return temp

    @compare_torque_ripple_and_stator_torque_reaction_derived_from_stator_tangential_loads.setter
    @exception_bridge
    @enforce_parameter_types
    def compare_torque_ripple_and_stator_torque_reaction_derived_from_stator_tangential_loads(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "CompareTorqueRippleAndStatorTorqueReactionDerivedFromStatorTangentialLoads",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def data_type_for_force_moment_distribution_and_temporal_spatial_harmonics_charts(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType":
        """EnumWithSelectedValue[mastapy.electric_machines.harmonic_load_data.HarmonicLoadDataType]"""
        temp = pythonnet_property_get(
            self.wrapped,
            "DataTypeForForceMomentDistributionAndTemporalSpatialHarmonicsCharts",
        )

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @data_type_for_force_moment_distribution_and_temporal_spatial_harmonics_charts.setter
    @exception_bridge
    @enforce_parameter_types
    def data_type_for_force_moment_distribution_and_temporal_spatial_harmonics_charts(
        self: "Self", value: "_1566.HarmonicLoadDataType"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(
            self.wrapped,
            "DataTypeForForceMomentDistributionAndTemporalSpatialHarmonicsCharts",
            value,
        )

    @property
    @exception_bridge
    def display_interpolated_data(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "DisplayInterpolatedData")

        if temp is None:
            return False

        return temp

    @display_interpolated_data.setter
    @exception_bridge
    @enforce_parameter_types
    def display_interpolated_data(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DisplayInterpolatedData",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def display_option_for_slice_data(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ForceDisplayOption":
        """EnumWithSelectedValue[mastapy.electric_machines.harmonic_load_data.ForceDisplayOption]"""
        temp = pythonnet_property_get(self.wrapped, "DisplayOptionForSliceData")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ForceDisplayOption.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @display_option_for_slice_data.setter
    @exception_bridge
    @enforce_parameter_types
    def display_option_for_slice_data(
        self: "Self", value: "_1563.ForceDisplayOption"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ForceDisplayOption.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "DisplayOptionForSliceData", value)

    @property
    @exception_bridge
    def force_distribution_3d(self: "Self") -> "_2069.ThreeDVectorChartDefinition":
        """mastapy.utility_gui.charts.ThreeDVectorChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceDistribution3D")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def force_moment_distribution(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceMomentDistribution")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def invert_axis(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "InvertAxis")

        if temp is None:
            return False

        return temp

    @invert_axis.setter
    @exception_bridge
    @enforce_parameter_types
    def invert_axis(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "InvertAxis", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def plot_as_vectors(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "PlotAsVectors")

        if temp is None:
            return False

        return temp

    @plot_as_vectors.setter
    @exception_bridge
    @enforce_parameter_types
    def plot_as_vectors(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "PlotAsVectors", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def rotor_x_force_amplitude_cut_off(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RotorXForceAmplitudeCutOff")

        if temp is None:
            return 0.0

        return temp

    @rotor_x_force_amplitude_cut_off.setter
    @exception_bridge
    @enforce_parameter_types
    def rotor_x_force_amplitude_cut_off(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RotorXForceAmplitudeCutOff",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def rotor_y_force_amplitude_cut_off(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RotorYForceAmplitudeCutOff")

        if temp is None:
            return 0.0

        return temp

    @rotor_y_force_amplitude_cut_off.setter
    @exception_bridge
    @enforce_parameter_types
    def rotor_y_force_amplitude_cut_off(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RotorYForceAmplitudeCutOff",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def selected_tooth(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_SimpleElectricMachineTooth":
        """ListWithSelectedItem[mastapy.electric_machines.harmonic_load_data.SimpleElectricMachineTooth]"""
        temp = pythonnet_property_get(self.wrapped, "SelectedTooth")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_SimpleElectricMachineTooth",
        )(temp)

    @selected_tooth.setter
    @exception_bridge
    @enforce_parameter_types
    def selected_tooth(self: "Self", value: "_1567.SimpleElectricMachineTooth") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_SimpleElectricMachineTooth.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "SelectedTooth", value)

    @property
    @exception_bridge
    def show_all_forces(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowAllForces")

        if temp is None:
            return False

        return temp

    @show_all_forces.setter
    @exception_bridge
    @enforce_parameter_types
    def show_all_forces(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ShowAllForces", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def show_all_teeth(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowAllTeeth")

        if temp is None:
            return False

        return temp

    @show_all_teeth.setter
    @exception_bridge
    @enforce_parameter_types
    def show_all_teeth(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ShowAllTeeth", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def slice(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_RotorSkewSlice":
        """ListWithSelectedItem[mastapy.electric_machines.RotorSkewSlice]"""
        temp = pythonnet_property_get(self.wrapped, "Slice")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_RotorSkewSlice",
        )(temp)

    @slice.setter
    @exception_bridge
    @enforce_parameter_types
    def slice(self: "Self", value: "_1431.RotorSkewSlice") -> None:
        generic_type = (
            list_with_selected_item.ListWithSelectedItem_RotorSkewSlice.implicit_type()
        )
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "Slice", value)

    @property
    @exception_bridge
    def speed_to_view(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpeedToView")

        if temp is None:
            return 0.0

        return temp

    @speed_to_view.setter
    @exception_bridge
    @enforce_parameter_types
    def speed_to_view(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "SpeedToView", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def stator_axial_loads_amplitude_cut_off(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StatorAxialLoadsAmplitudeCutOff")

        if temp is None:
            return 0.0

        return temp

    @stator_axial_loads_amplitude_cut_off.setter
    @exception_bridge
    @enforce_parameter_types
    def stator_axial_loads_amplitude_cut_off(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StatorAxialLoadsAmplitudeCutOff",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def stator_radial_loads_amplitude_cut_off(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StatorRadialLoadsAmplitudeCutOff")

        if temp is None:
            return 0.0

        return temp

    @stator_radial_loads_amplitude_cut_off.setter
    @exception_bridge
    @enforce_parameter_types
    def stator_radial_loads_amplitude_cut_off(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StatorRadialLoadsAmplitudeCutOff",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def stator_tangential_loads_amplitude_cut_off(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "StatorTangentialLoadsAmplitudeCutOff"
        )

        if temp is None:
            return 0.0

        return temp

    @stator_tangential_loads_amplitude_cut_off.setter
    @exception_bridge
    @enforce_parameter_types
    def stator_tangential_loads_amplitude_cut_off(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StatorTangentialLoadsAmplitudeCutOff",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def stator_tooth_moments_amplitude_cut_off(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StatorToothMomentsAmplitudeCutOff")

        if temp is None:
            return 0.0

        return temp

    @stator_tooth_moments_amplitude_cut_off.setter
    @exception_bridge
    @enforce_parameter_types
    def stator_tooth_moments_amplitude_cut_off(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StatorToothMomentsAmplitudeCutOff",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def sum_over_all_nodes(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "SumOverAllNodes")

        if temp is None:
            return False

        return temp

    @sum_over_all_nodes.setter
    @exception_bridge
    @enforce_parameter_types
    def sum_over_all_nodes(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "SumOverAllNodes", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def temporal_spatial_harmonics_chart(
        self: "Self",
    ) -> "_2065.ScatterChartDefinition":
        """mastapy.utility_gui.charts.ScatterChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TemporalSpatialHarmonicsChart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def torque_ripple_amplitude_cut_off(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TorqueRippleAmplitudeCutOff")

        if temp is None:
            return 0.0

        return temp

    @torque_ripple_amplitude_cut_off.setter
    @exception_bridge
    @enforce_parameter_types
    def torque_ripple_amplitude_cut_off(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TorqueRippleAmplitudeCutOff",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def use_log_scale_for_temporal_spatial_harmonics_chart(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseLogScaleForTemporalSpatialHarmonicsChart"
        )

        if temp is None:
            return False

        return temp

    @use_log_scale_for_temporal_spatial_harmonics_chart.setter
    @exception_bridge
    @enforce_parameter_types
    def use_log_scale_for_temporal_spatial_harmonics_chart(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseLogScaleForTemporalSpatialHarmonicsChart",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def rotor_x_force(self: "Self") -> "_1705.MultipleFourierSeriesInterpolator":
        """mastapy.math_utility.MultipleFourierSeriesInterpolator

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RotorXForce")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def rotor_y_force(self: "Self") -> "_1705.MultipleFourierSeriesInterpolator":
        """mastapy.math_utility.MultipleFourierSeriesInterpolator

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RotorYForce")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def stator_axial_loads(self: "Self") -> "_1570.StatorToothLoadInterpolator":
        """mastapy.electric_machines.harmonic_load_data.StatorToothLoadInterpolator

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StatorAxialLoads")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def stator_radial_loads(self: "Self") -> "_1570.StatorToothLoadInterpolator":
        """mastapy.electric_machines.harmonic_load_data.StatorToothLoadInterpolator

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StatorRadialLoads")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def stator_tangential_loads(self: "Self") -> "_1570.StatorToothLoadInterpolator":
        """mastapy.electric_machines.harmonic_load_data.StatorToothLoadInterpolator

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StatorTangentialLoads")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def stator_tooth_moments(self: "Self") -> "_1571.StatorToothMomentInterpolator":
        """mastapy.electric_machines.harmonic_load_data.StatorToothMomentInterpolator

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StatorToothMoments")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    @enforce_parameter_types
    def multiple_fourier_series_interpolator_for(
        self: "Self",
        harmonic_load_data_type: "_1566.HarmonicLoadDataType",
        slice_index: "int",
    ) -> "_1705.MultipleFourierSeriesInterpolator":
        """mastapy.math_utility.MultipleFourierSeriesInterpolator

        Args:
            harmonic_load_data_type (mastapy.electric_machines.harmonic_load_data.HarmonicLoadDataType)
            slice_index (int)
        """
        harmonic_load_data_type = conversion.mp_to_pn_enum(
            harmonic_load_data_type,
            "SMT.MastaAPI.ElectricMachines.HarmonicLoadData.HarmonicLoadDataType",
        )
        slice_index = int(slice_index)
        method_result = pythonnet_method_call(
            self.wrapped,
            "MultipleFourierSeriesInterpolatorFor",
            harmonic_load_data_type,
            slice_index if slice_index else 0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def stator_tooth_load_interpolator_for(
        self: "Self",
        harmonic_load_data_type: "_1566.HarmonicLoadDataType",
        slice_index: "int",
    ) -> "_1570.StatorToothLoadInterpolator":
        """mastapy.electric_machines.harmonic_load_data.StatorToothLoadInterpolator

        Args:
            harmonic_load_data_type (mastapy.electric_machines.harmonic_load_data.HarmonicLoadDataType)
            slice_index (int)
        """
        harmonic_load_data_type = conversion.mp_to_pn_enum(
            harmonic_load_data_type,
            "SMT.MastaAPI.ElectricMachines.HarmonicLoadData.HarmonicLoadDataType",
        )
        slice_index = int(slice_index)
        method_result = pythonnet_method_call(
            self.wrapped,
            "StatorToothLoadInterpolatorFor",
            harmonic_load_data_type,
            slice_index if slice_index else 0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def stator_tooth_moment_interpolator_for(
        self: "Self",
        harmonic_load_data_type: "_1566.HarmonicLoadDataType",
        slice_index: "int",
    ) -> "_1571.StatorToothMomentInterpolator":
        """mastapy.electric_machines.harmonic_load_data.StatorToothMomentInterpolator

        Args:
            harmonic_load_data_type (mastapy.electric_machines.harmonic_load_data.HarmonicLoadDataType)
            slice_index (int)
        """
        harmonic_load_data_type = conversion.mp_to_pn_enum(
            harmonic_load_data_type,
            "SMT.MastaAPI.ElectricMachines.HarmonicLoadData.HarmonicLoadDataType",
        )
        slice_index = int(slice_index)
        method_result = pythonnet_method_call(
            self.wrapped,
            "StatorToothMomentInterpolatorFor",
            harmonic_load_data_type,
            slice_index if slice_index else 0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ElectricMachineHarmonicLoadDataBase":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineHarmonicLoadDataBase
        """
        return _Cast_ElectricMachineHarmonicLoadDataBase(self)
