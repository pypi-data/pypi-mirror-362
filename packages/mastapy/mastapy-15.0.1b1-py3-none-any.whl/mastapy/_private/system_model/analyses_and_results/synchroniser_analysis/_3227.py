"""SynchroniserShift"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import list_with_selected_item
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
from mastapy._private.system_model.analyses_and_results.load_case_groups import _5953

_SYNCHRONISER_SHIFT = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SynchroniserAnalysis",
    "SynchroniserShift",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.system_model.part_model.couplings import _2850, _2852

    Self = TypeVar("Self", bound="SynchroniserShift")
    CastSelf = TypeVar("CastSelf", bound="SynchroniserShift._Cast_SynchroniserShift")


__docformat__ = "restructuredtext en"
__all__ = ("SynchroniserShift",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SynchroniserShift:
    """Special nested class for casting SynchroniserShift to subclasses."""

    __parent__: "SynchroniserShift"

    @property
    def synchroniser_shift(self: "CastSelf") -> "SynchroniserShift":
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
class SynchroniserShift(_0.APIBase):
    """SynchroniserShift

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SYNCHRONISER_SHIFT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def clutch_inertia(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ClutchInertia")

        if temp is None:
            return 0.0

        return temp

    @clutch_inertia.setter
    @exception_bridge
    @enforce_parameter_types
    def clutch_inertia(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ClutchInertia", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def cone_normal_pressure_when_all_cones_take_equal_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ConeNormalPressureWhenAllConesTakeEqualForce"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def cone_torque_index_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConeTorqueIndexTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def downstream_component(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DownstreamComponent")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def engine_power_load_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EnginePowerLoadName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def final_design_state(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_DesignState":
        """ListWithSelectedItem[mastapy.system_model.analyses_and_results.load_case_groups.DesignState]"""
        temp = pythonnet_property_get(self.wrapped, "FinalDesignState")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_DesignState",
        )(temp)

    @final_design_state.setter
    @exception_bridge
    @enforce_parameter_types
    def final_design_state(self: "Self", value: "_5953.DesignState") -> None:
        generic_type = (
            list_with_selected_item.ListWithSelectedItem_DesignState.implicit_type()
        )
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "FinalDesignState", value)

    @property
    @exception_bridge
    def final_synchronised_speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FinalSynchronisedSpeed")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def frictional_energy_per_area_for_shift_time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "FrictionalEnergyPerAreaForShiftTime"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def frictional_work(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrictionalWork")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hand_ball_force(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "HandBallForce")

        if temp is None:
            return 0.0

        return temp

    @hand_ball_force.setter
    @exception_bridge
    @enforce_parameter_types
    def hand_ball_force(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "HandBallForce", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def hand_ball_impulse(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HandBallImpulse")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def indexing_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IndexingTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def initial_design_state(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_DesignState":
        """ListWithSelectedItem[mastapy.system_model.analyses_and_results.load_case_groups.DesignState]"""
        temp = pythonnet_property_get(self.wrapped, "InitialDesignState")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_DesignState",
        )(temp)

    @initial_design_state.setter
    @exception_bridge
    @enforce_parameter_types
    def initial_design_state(self: "Self", value: "_5953.DesignState") -> None:
        generic_type = (
            list_with_selected_item.ListWithSelectedItem_DesignState.implicit_type()
        )
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "InitialDesignState", value)

    @property
    @exception_bridge
    def initial_downstream_component_speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InitialDownstreamComponentSpeed")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def initial_engine_speed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InitialEngineSpeed")

        if temp is None:
            return 0.0

        return temp

    @initial_engine_speed.setter
    @exception_bridge
    @enforce_parameter_types
    def initial_engine_speed(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "InitialEngineSpeed",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def initial_upstream_component_speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InitialUpstreamComponentSpeed")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_cone_normal_pressure(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumConeNormalPressure")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_frictional_power_for_shift_time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanFrictionalPowerForShiftTime")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_frictional_power_per_area_for_shift_time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MeanFrictionalPowerPerAreaForShiftTime"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @name.setter
    @exception_bridge
    @enforce_parameter_types
    def name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Name", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def shift_mechanism_efficiency(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ShiftMechanismEfficiency")

        if temp is None:
            return 0.0

        return temp

    @shift_mechanism_efficiency.setter
    @exception_bridge
    @enforce_parameter_types
    def shift_mechanism_efficiency(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShiftMechanismEfficiency",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def shift_mechanism_ratio(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ShiftMechanismRatio")

        if temp is None:
            return 0.0

        return temp

    @shift_mechanism_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def shift_mechanism_ratio(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShiftMechanismRatio",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def shift_time(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ShiftTime")

        if temp is None:
            return 0.0

        return temp

    @shift_time.setter
    @exception_bridge
    @enforce_parameter_types
    def shift_time(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ShiftTime", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def sleeve_axial_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SleeveAxialForce")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sleeve_impulse(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SleeveImpulse")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def slipping_velocity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SlippingVelocity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def synchronisation_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SynchronisationTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def time_specified(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "TimeSpecified")

        if temp is None:
            return False

        return temp

    @time_specified.setter
    @exception_bridge
    @enforce_parameter_types
    def time_specified(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "TimeSpecified", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def total_normal_force_on_cones(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalNormalForceOnCones")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def upstream_component(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UpstreamComponent")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def upstream_inertia(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UpstreamInertia")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def cone(self: "Self") -> "_2850.SynchroniserHalf":
        """mastapy.system_model.part_model.couplings.SynchroniserHalf

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Cone")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def sleeve(self: "Self") -> "_2852.SynchroniserSleeve":
        """mastapy.system_model.part_model.couplings.SynchroniserSleeve

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Sleeve")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

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
    def cast_to(self: "Self") -> "_Cast_SynchroniserShift":
        """Cast to another type.

        Returns:
            _Cast_SynchroniserShift
        """
        return _Cast_SynchroniserShift(self)
