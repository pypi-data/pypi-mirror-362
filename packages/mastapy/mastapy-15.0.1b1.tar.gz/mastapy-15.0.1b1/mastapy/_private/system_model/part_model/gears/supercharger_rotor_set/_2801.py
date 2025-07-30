"""SuperchargerRotorSet"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

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
from mastapy._private.utility.databases import _2028

_SUPERCHARGER_ROTOR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears.SuperchargerRotorSet",
    "SuperchargerRotorSet",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set import (
        _2793,
        _2794,
        _2795,
        _2796,
        _2797,
        _2798,
        _2803,
    )
    from mastapy._private.utility_gui.charts import _2068

    Self = TypeVar("Self", bound="SuperchargerRotorSet")
    CastSelf = TypeVar(
        "CastSelf", bound="SuperchargerRotorSet._Cast_SuperchargerRotorSet"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SuperchargerRotorSet",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SuperchargerRotorSet:
    """Special nested class for casting SuperchargerRotorSet to subclasses."""

    __parent__: "SuperchargerRotorSet"

    @property
    def named_database_item(self: "CastSelf") -> "_2028.NamedDatabaseItem":
        return self.__parent__._cast(_2028.NamedDatabaseItem)

    @property
    def supercharger_rotor_set(self: "CastSelf") -> "SuperchargerRotorSet":
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
class SuperchargerRotorSet(_2028.NamedDatabaseItem):
    """SuperchargerRotorSet

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SUPERCHARGER_ROTOR_SET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def axial_reaction_force(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AxialReactionForce")

        if temp is None:
            return 0.0

        return temp

    @axial_reaction_force.setter
    @exception_bridge
    @enforce_parameter_types
    def axial_reaction_force(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AxialReactionForce",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def dynamic_load_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DynamicLoadFactor")

        if temp is None:
            return 0.0

        return temp

    @dynamic_load_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def dynamic_load_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DynamicLoadFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def lateral_reaction_force(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LateralReactionForce")

        if temp is None:
            return 0.0

        return temp

    @lateral_reaction_force.setter
    @exception_bridge
    @enforce_parameter_types
    def lateral_reaction_force(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LateralReactionForce",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def lateral_reaction_moment(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LateralReactionMoment")

        if temp is None:
            return 0.0

        return temp

    @lateral_reaction_moment.setter
    @exception_bridge
    @enforce_parameter_types
    def lateral_reaction_moment(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LateralReactionMoment",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def selected_file_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SelectedFileName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def supercharger_map_chart(self: "Self") -> "_2068.ThreeDChartDefinition":
        """mastapy.utility_gui.charts.ThreeDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SuperchargerMapChart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def vertical_reaction_force(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "VerticalReactionForce")

        if temp is None:
            return 0.0

        return temp

    @vertical_reaction_force.setter
    @exception_bridge
    @enforce_parameter_types
    def vertical_reaction_force(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "VerticalReactionForce",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def vertical_reaction_moment(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "VerticalReactionMoment")

        if temp is None:
            return 0.0

        return temp

    @vertical_reaction_moment.setter
    @exception_bridge
    @enforce_parameter_types
    def vertical_reaction_moment(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "VerticalReactionMoment",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def y_variable_for_imported_data(self: "Self") -> "_2803.YVariableForImportedData":
        """mastapy.system_model.part_model.gears.supercharger_rotor_set.YVariableForImportedData"""
        temp = pythonnet_property_get(self.wrapped, "YVariableForImportedData")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.PartModel.Gears.SuperchargerRotorSet.YVariableForImportedData",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.part_model.gears.supercharger_rotor_set._2803",
            "YVariableForImportedData",
        )(value)

    @y_variable_for_imported_data.setter
    @exception_bridge
    @enforce_parameter_types
    def y_variable_for_imported_data(
        self: "Self", value: "_2803.YVariableForImportedData"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.PartModel.Gears.SuperchargerRotorSet.YVariableForImportedData",
        )
        pythonnet_property_set(self.wrapped, "YVariableForImportedData", value)

    @property
    @exception_bridge
    def boost_pressure(self: "Self") -> "_2793.BoostPressureInputOptions":
        """mastapy.system_model.part_model.gears.supercharger_rotor_set.BoostPressureInputOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BoostPressure")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def file(self: "Self") -> "_2796.RotorSetDataInputFileOptions":
        """mastapy.system_model.part_model.gears.supercharger_rotor_set.RotorSetDataInputFileOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "File")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def input_power(self: "Self") -> "_2794.InputPowerInputOptions":
        """mastapy.system_model.part_model.gears.supercharger_rotor_set.InputPowerInputOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InputPower")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def pressure_ratio(self: "Self") -> "_2795.PressureRatioInputOptions":
        """mastapy.system_model.part_model.gears.supercharger_rotor_set.PressureRatioInputOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PressureRatio")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def rotor_speed(self: "Self") -> "_2798.RotorSpeedInputOptions":
        """mastapy.system_model.part_model.gears.supercharger_rotor_set.RotorSpeedInputOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RotorSpeed")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def measured_points(self: "Self") -> "List[_2797.RotorSetMeasuredPoint]":
        """List[mastapy.system_model.part_model.gears.supercharger_rotor_set.RotorSetMeasuredPoint]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeasuredPoints")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    def select_different_file(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SelectDifferentFile")

    @property
    def cast_to(self: "Self") -> "_Cast_SuperchargerRotorSet":
        """Cast to another type.

        Returns:
            _Cast_SuperchargerRotorSet
        """
        return _Cast_SuperchargerRotorSet(self)
