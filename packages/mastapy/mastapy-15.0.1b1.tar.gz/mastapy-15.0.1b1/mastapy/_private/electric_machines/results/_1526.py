"""NonLinearDQModel"""

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
from mastapy._private.electric_machines.results import _1507

_NON_LINEAR_DQ_MODEL = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Results", "NonLinearDQModel"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.electric_machines.results import _1527
    from mastapy._private.utility_gui.charts import _2068, _2070

    Self = TypeVar("Self", bound="NonLinearDQModel")
    CastSelf = TypeVar("CastSelf", bound="NonLinearDQModel._Cast_NonLinearDQModel")


__docformat__ = "restructuredtext en"
__all__ = ("NonLinearDQModel",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NonLinearDQModel:
    """Special nested class for casting NonLinearDQModel to subclasses."""

    __parent__: "NonLinearDQModel"

    @property
    def electric_machine_dq_model(self: "CastSelf") -> "_1507.ElectricMachineDQModel":
        return self.__parent__._cast(_1507.ElectricMachineDQModel)

    @property
    def non_linear_dq_model(self: "CastSelf") -> "NonLinearDQModel":
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
class NonLinearDQModel(_1507.ElectricMachineDQModel):
    """NonLinearDQModel

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NON_LINEAR_DQ_MODEL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def ac_winding_loss_per_frequency_exponent_map(
        self: "Self",
    ) -> "_2068.ThreeDChartDefinition":
        """mastapy.utility_gui.charts.ThreeDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ACWindingLossPerFrequencyExponentMap"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def alignment_torque_map_at_reference_temperatures(
        self: "Self",
    ) -> "_2068.ThreeDChartDefinition":
        """mastapy.utility_gui.charts.ThreeDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AlignmentTorqueMapAtReferenceTemperatures"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def d_axis_armature_flux_linkage_map(self: "Self") -> "_2068.ThreeDChartDefinition":
        """mastapy.utility_gui.charts.ThreeDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DAxisArmatureFluxLinkageMap")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def d_axis_flux_linkage_map(self: "Self") -> "_2068.ThreeDChartDefinition":
        """mastapy.utility_gui.charts.ThreeDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DAxisFluxLinkageMap")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def magnet_loss_per_frequency_2_map(self: "Self") -> "_2068.ThreeDChartDefinition":
        """mastapy.utility_gui.charts.ThreeDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MagnetLossPerFrequency2Map")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

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
    def number_of_current_angle_values(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfCurrentAngleValues")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_current_values(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfCurrentValues")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def q_axis_armature_flux_linkage_map(self: "Self") -> "_2068.ThreeDChartDefinition":
        """mastapy.utility_gui.charts.ThreeDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "QAxisArmatureFluxLinkageMap")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def q_axis_flux_linkage_map(self: "Self") -> "_2068.ThreeDChartDefinition":
        """mastapy.utility_gui.charts.ThreeDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "QAxisFluxLinkageMap")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def reluctance_torque_map_at_reference_temperatures(
        self: "Self",
    ) -> "_2068.ThreeDChartDefinition":
        """mastapy.utility_gui.charts.ThreeDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ReluctanceTorqueMapAtReferenceTemperatures"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def rotor_eddy_current_loss_per_frequency_exponent_map(
        self: "Self",
    ) -> "_2068.ThreeDChartDefinition":
        """mastapy.utility_gui.charts.ThreeDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RotorEddyCurrentLossPerFrequencyExponentMap"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def rotor_excess_loss_per_frequency_exponent_map(
        self: "Self",
    ) -> "_2068.ThreeDChartDefinition":
        """mastapy.utility_gui.charts.ThreeDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RotorExcessLossPerFrequencyExponentMap"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def rotor_hysteresis_loss_per_frequency_exponent_map(
        self: "Self",
    ) -> "_2068.ThreeDChartDefinition":
        """mastapy.utility_gui.charts.ThreeDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RotorHysteresisLossPerFrequencyExponentMap"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def stator_eddy_current_loss_per_frequency_exponent_map(
        self: "Self",
    ) -> "_2068.ThreeDChartDefinition":
        """mastapy.utility_gui.charts.ThreeDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StatorEddyCurrentLossPerFrequencyExponentMap"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def stator_excess_loss_per_frequency_exponent_map(
        self: "Self",
    ) -> "_2068.ThreeDChartDefinition":
        """mastapy.utility_gui.charts.ThreeDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StatorExcessLossPerFrequencyExponentMap"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def stator_hysteresis_loss_per_frequency_exponent_map(
        self: "Self",
    ) -> "_2068.ThreeDChartDefinition":
        """mastapy.utility_gui.charts.ThreeDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StatorHysteresisLossPerFrequencyExponentMap"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def time_taken_to_generate_non_linear_dq_model(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TimeTakenToGenerateNonLinearDQModel"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def torque_map_at_reference_temperatures(
        self: "Self",
    ) -> "_2068.ThreeDChartDefinition":
        """mastapy.utility_gui.charts.ThreeDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorqueMapAtReferenceTemperatures")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def torque_at_max_current_and_reference_temperatures(
        self: "Self",
    ) -> "_2070.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TorqueAtMaxCurrentAndReferenceTemperatures"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def non_linear_dq_model_generator_settings(
        self: "Self",
    ) -> "_1527.NonLinearDQModelGeneratorSettings":
        """mastapy.electric_machines.results.NonLinearDQModelGeneratorSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NonLinearDQModelGeneratorSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_NonLinearDQModel":
        """Cast to another type.

        Returns:
            _Cast_NonLinearDQModel
        """
        return _Cast_NonLinearDQModel(self)
