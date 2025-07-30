"""TorqueConverterLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import enum_with_selected_value
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5796
from mastapy._private.system_model.analyses_and_results.static_loads import _7722

_TORQUE_CONVERTER_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "TorqueConverterLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility import _1718
    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7675,
        _7799,
        _7823,
    )
    from mastapy._private.system_model.part_model.couplings import _2853

    Self = TypeVar("Self", bound="TorqueConverterLoadCase")
    CastSelf = TypeVar(
        "CastSelf", bound="TorqueConverterLoadCase._Cast_TorqueConverterLoadCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("TorqueConverterLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TorqueConverterLoadCase:
    """Special nested class for casting TorqueConverterLoadCase to subclasses."""

    __parent__: "TorqueConverterLoadCase"

    @property
    def coupling_load_case(self: "CastSelf") -> "_7722.CouplingLoadCase":
        return self.__parent__._cast(_7722.CouplingLoadCase)

    @property
    def specialised_assembly_load_case(
        self: "CastSelf",
    ) -> "_7823.SpecialisedAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7823,
        )

        return self.__parent__._cast(_7823.SpecialisedAssemblyLoadCase)

    @property
    def abstract_assembly_load_case(
        self: "CastSelf",
    ) -> "_7675.AbstractAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7675,
        )

        return self.__parent__._cast(_7675.AbstractAssemblyLoadCase)

    @property
    def part_load_case(self: "CastSelf") -> "_7799.PartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7799,
        )

        return self.__parent__._cast(_7799.PartLoadCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2898.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2898

        return self.__parent__._cast(_2898.PartAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2894.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2894

        return self.__parent__._cast(_2894.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2892.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2892

        return self.__parent__._cast(_2892.DesignEntityAnalysis)

    @property
    def torque_converter_load_case(self: "CastSelf") -> "TorqueConverterLoadCase":
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
class TorqueConverterLoadCase(_7722.CouplingLoadCase):
    """TorqueConverterLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TORQUE_CONVERTER_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def initial_lock_up_clutch_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InitialLockUpClutchTemperature")

        if temp is None:
            return 0.0

        return temp

    @initial_lock_up_clutch_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def initial_lock_up_clutch_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "InitialLockUpClutchTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def initially_locked(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "InitiallyLocked")

        if temp is None:
            return False

        return temp

    @initially_locked.setter
    @exception_bridge
    @enforce_parameter_types
    def initially_locked(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "InitiallyLocked", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def lock_up_clutch_pressure_for_no_torque_converter_operation(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "LockUpClutchPressureForNoTorqueConverterOperation"
        )

        if temp is None:
            return 0.0

        return temp

    @lock_up_clutch_pressure_for_no_torque_converter_operation.setter
    @exception_bridge
    @enforce_parameter_types
    def lock_up_clutch_pressure_for_no_torque_converter_operation(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "LockUpClutchPressureForNoTorqueConverterOperation",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def lock_up_clutch_pressure_time_profile(
        self: "Self",
    ) -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "LockUpClutchPressureTimeProfile")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @lock_up_clutch_pressure_time_profile.setter
    @exception_bridge
    @enforce_parameter_types
    def lock_up_clutch_pressure_time_profile(
        self: "Self", value: "_1718.Vector2DListAccessor"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "LockUpClutchPressureTimeProfile", value.wrapped
        )

    @property
    @exception_bridge
    def lock_up_clutch_rule(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_TorqueConverterLockupRule":
        """EnumWithSelectedValue[mastapy.system_model.analyses_and_results.mbd_analyses.TorqueConverterLockupRule]"""
        temp = pythonnet_property_get(self.wrapped, "LockUpClutchRule")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_TorqueConverterLockupRule.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @lock_up_clutch_rule.setter
    @exception_bridge
    @enforce_parameter_types
    def lock_up_clutch_rule(
        self: "Self", value: "_5796.TorqueConverterLockupRule"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_TorqueConverterLockupRule.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "LockUpClutchRule", value)

    @property
    @exception_bridge
    def locking_speed_ratio_threshold(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LockingSpeedRatioThreshold")

        if temp is None:
            return 0.0

        return temp

    @locking_speed_ratio_threshold.setter
    @exception_bridge
    @enforce_parameter_types
    def locking_speed_ratio_threshold(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LockingSpeedRatioThreshold",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def time_for_full_clutch_pressure(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TimeForFullClutchPressure")

        if temp is None:
            return 0.0

        return temp

    @time_for_full_clutch_pressure.setter
    @exception_bridge
    @enforce_parameter_types
    def time_for_full_clutch_pressure(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TimeForFullClutchPressure",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def time_to_change_locking_state(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TimeToChangeLockingState")

        if temp is None:
            return 0.0

        return temp

    @time_to_change_locking_state.setter
    @exception_bridge
    @enforce_parameter_types
    def time_to_change_locking_state(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TimeToChangeLockingState",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def transient_time_to_change_locking_status(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "TransientTimeToChangeLockingStatus"
        )

        if temp is None:
            return 0.0

        return temp

    @transient_time_to_change_locking_status.setter
    @exception_bridge
    @enforce_parameter_types
    def transient_time_to_change_locking_status(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TransientTimeToChangeLockingStatus",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def vehicle_speed_to_unlock(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "VehicleSpeedToUnlock")

        if temp is None:
            return 0.0

        return temp

    @vehicle_speed_to_unlock.setter
    @exception_bridge
    @enforce_parameter_types
    def vehicle_speed_to_unlock(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "VehicleSpeedToUnlock",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def assembly_design(self: "Self") -> "_2853.TorqueConverter":
        """mastapy.system_model.part_model.couplings.TorqueConverter

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_TorqueConverterLoadCase":
        """Cast to another type.

        Returns:
            _Cast_TorqueConverterLoadCase
        """
        return _Cast_TorqueConverterLoadCase(self)
