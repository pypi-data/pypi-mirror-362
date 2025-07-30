"""Bearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    overridable_enum_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import enum_with_selected_value, overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_get_with_method,
    pythonnet_property_set,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings import _2080
from mastapy._private.bearings.bearing_results import _2148, _2167
from mastapy._private.bearings.tolerances import _2106
from mastapy._private.materials.efficiency import _382
from mastapy._private.system_model.part_model import _2673

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_ARRAY = python_net_import("System", "Array")
_BEARING = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Bearing")

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.bearings import _2072, _2076, _2089
    from mastapy._private.bearings.bearing_designs import _2340
    from mastapy._private.bearings.bearing_results import _2166
    from mastapy._private.bearings.bearing_results.rolling import _2279
    from mastapy._private.bearings.tolerances import (
        _2107,
        _2109,
        _2110,
        _2115,
        _2116,
        _2120,
        _2123,
        _2125,
        _2127,
    )
    from mastapy._private.materials import _356
    from mastapy._private.math_utility.measured_vectors import _1748
    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.part_model import (
        _2663,
        _2665,
        _2666,
        _2670,
        _2671,
        _2693,
        _2698,
        _2704,
    )
    from mastapy._private.system_model.part_model.shaft_model import _2714
    from mastapy._private.utility import _1791
    from mastapy._private.utility.report import _1981

    Self = TypeVar("Self", bound="Bearing")
    CastSelf = TypeVar("CastSelf", bound="Bearing._Cast_Bearing")


__docformat__ = "restructuredtext en"
__all__ = ("Bearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Bearing:
    """Special nested class for casting Bearing to subclasses."""

    __parent__: "Bearing"

    @property
    def connector(self: "CastSelf") -> "_2673.Connector":
        return self.__parent__._cast(_2673.Connector)

    @property
    def mountable_component(self: "CastSelf") -> "_2693.MountableComponent":
        from mastapy._private.system_model.part_model import _2693

        return self.__parent__._cast(_2693.MountableComponent)

    @property
    def component(self: "CastSelf") -> "_2670.Component":
        from mastapy._private.system_model.part_model import _2670

        return self.__parent__._cast(_2670.Component)

    @property
    def part(self: "CastSelf") -> "_2698.Part":
        from mastapy._private.system_model.part_model import _2698

        return self.__parent__._cast(_2698.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2414.DesignEntity":
        from mastapy._private.system_model import _2414

        return self.__parent__._cast(_2414.DesignEntity)

    @property
    def bearing(self: "CastSelf") -> "Bearing":
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
class Bearing(_2673.Connector):
    """Bearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def axial_displacement_preload(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AxialDisplacementPreload")

        if temp is None:
            return 0.0

        return temp

    @axial_displacement_preload.setter
    @exception_bridge
    @enforce_parameter_types
    def axial_displacement_preload(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AxialDisplacementPreload",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def axial_force_preload(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AxialForcePreload")

        if temp is None:
            return 0.0

        return temp

    @axial_force_preload.setter
    @exception_bridge
    @enforce_parameter_types
    def axial_force_preload(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AxialForcePreload",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def axial_internal_clearance(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "AxialInternalClearance")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @axial_internal_clearance.setter
    @exception_bridge
    @enforce_parameter_types
    def axial_internal_clearance(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "AxialInternalClearance", value)

    @property
    @exception_bridge
    def axial_stiffness_at_mounting_points(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AxialStiffnessAtMountingPoints")

        if temp is None:
            return 0.0

        return temp

    @axial_stiffness_at_mounting_points.setter
    @exception_bridge
    @enforce_parameter_types
    def axial_stiffness_at_mounting_points(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AxialStiffnessAtMountingPoints",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def bearing_life_adjustment_factor_for_operating_conditions(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "BearingLifeAdjustmentFactorForOperatingConditions"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @bearing_life_adjustment_factor_for_operating_conditions.setter
    @exception_bridge
    @enforce_parameter_types
    def bearing_life_adjustment_factor_for_operating_conditions(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "BearingLifeAdjustmentFactorForOperatingConditions", value
        )

    @property
    @exception_bridge
    def bearing_life_adjustment_factor_for_special_bearing_properties(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "BearingLifeAdjustmentFactorForSpecialBearingProperties"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @bearing_life_adjustment_factor_for_special_bearing_properties.setter
    @exception_bridge
    @enforce_parameter_types
    def bearing_life_adjustment_factor_for_special_bearing_properties(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped,
            "BearingLifeAdjustmentFactorForSpecialBearingProperties",
            value,
        )

    @property
    @exception_bridge
    def bearing_life_modification_factor(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "BearingLifeModificationFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @bearing_life_modification_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def bearing_life_modification_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "BearingLifeModificationFactor", value)

    @property
    @exception_bridge
    def bearing_tolerance_class(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_BearingToleranceClass":
        """EnumWithSelectedValue[mastapy.bearings.tolerances.BearingToleranceClass]"""
        temp = pythonnet_property_get(self.wrapped, "BearingToleranceClass")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_BearingToleranceClass.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @bearing_tolerance_class.setter
    @exception_bridge
    @enforce_parameter_types
    def bearing_tolerance_class(
        self: "Self", value: "_2106.BearingToleranceClass"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_BearingToleranceClass.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "BearingToleranceClass", value)

    @property
    @exception_bridge
    def bearing_tolerance_definition(
        self: "Self",
    ) -> "_2107.BearingToleranceDefinitionOptions":
        """mastapy.bearings.tolerances.BearingToleranceDefinitionOptions"""
        temp = pythonnet_property_get(self.wrapped, "BearingToleranceDefinition")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.Tolerances.BearingToleranceDefinitionOptions"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings.tolerances._2107",
            "BearingToleranceDefinitionOptions",
        )(value)

    @bearing_tolerance_definition.setter
    @exception_bridge
    @enforce_parameter_types
    def bearing_tolerance_definition(
        self: "Self", value: "_2107.BearingToleranceDefinitionOptions"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Bearings.Tolerances.BearingToleranceDefinitionOptions"
        )
        pythonnet_property_set(self.wrapped, "BearingToleranceDefinition", value)

    @property
    @exception_bridge
    def coefficient_of_friction(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CoefficientOfFriction")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @coefficient_of_friction.setter
    @exception_bridge
    @enforce_parameter_types
    def coefficient_of_friction(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CoefficientOfFriction", value)

    @property
    @exception_bridge
    def damping_options(self: "Self") -> "_2076.BearingDampingMatrixOption":
        """mastapy.bearings.BearingDampingMatrixOption"""
        temp = pythonnet_property_get(self.wrapped, "DampingOptions")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.BearingDampingMatrixOption"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings._2076", "BearingDampingMatrixOption"
        )(value)

    @damping_options.setter
    @exception_bridge
    @enforce_parameter_types
    def damping_options(
        self: "Self", value: "_2076.BearingDampingMatrixOption"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Bearings.BearingDampingMatrixOption"
        )
        pythonnet_property_set(self.wrapped, "DampingOptions", value)

    @property
    @exception_bridge
    def diameter_of_contact_on_inner_race_at_nominal_contact_angle(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DiameterOfContactOnInnerRaceAtNominalContactAngle"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def diameter_of_contact_on_left_race(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DiameterOfContactOnLeftRace")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def diameter_of_contact_on_outer_race_at_nominal_contact_angle(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DiameterOfContactOnOuterRaceAtNominalContactAngle"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def diameter_of_contact_on_right_race(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DiameterOfContactOnRightRace")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def difference_between_inner_diameter_and_diameter_of_connected_component_at_inner_connection(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "DifferenceBetweenInnerDiameterAndDiameterOfConnectedComponentAtInnerConnection",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def difference_between_outer_diameter_and_diameter_of_connected_component_at_outer_connection(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "DifferenceBetweenOuterDiameterAndDiameterOfConnectedComponentAtOuterConnection",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def efficiency_rating_method(
        self: "Self",
    ) -> "overridable.Overridable_BearingEfficiencyRatingMethod":
        """Overridable[mastapy.materials.efficiency.BearingEfficiencyRatingMethod]"""
        temp = pythonnet_property_get(self.wrapped, "EfficiencyRatingMethod")

        if temp is None:
            return None

        value = overridable.Overridable_BearingEfficiencyRatingMethod.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @efficiency_rating_method.setter
    @exception_bridge
    @enforce_parameter_types
    def efficiency_rating_method(
        self: "Self",
        value: "Union[_382.BearingEfficiencyRatingMethod, Tuple[_382.BearingEfficiencyRatingMethod, bool]]",
    ) -> None:
        wrapper_type = (
            overridable.Overridable_BearingEfficiencyRatingMethod.wrapper_type()
        )
        enclosed_type = (
            overridable.Overridable_BearingEfficiencyRatingMethod.implicit_type()
        )
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(self.wrapped, "EfficiencyRatingMethod", value)

    @property
    @exception_bridge
    def feed_flow_rate(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "FeedFlowRate")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @feed_flow_rate.setter
    @exception_bridge
    @enforce_parameter_types
    def feed_flow_rate(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "FeedFlowRate", value)

    @property
    @exception_bridge
    def feed_pressure(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "FeedPressure")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @feed_pressure.setter
    @exception_bridge
    @enforce_parameter_types
    def feed_pressure(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "FeedPressure", value)

    @property
    @exception_bridge
    def first_element_angle(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "FirstElementAngle")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @first_element_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def first_element_angle(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "FirstElementAngle", value)

    @property
    @exception_bridge
    def force_at_zero_displacement_input_method(
        self: "Self",
    ) -> "_2665.BearingF0InputMethod":
        """mastapy.system_model.part_model.BearingF0InputMethod"""
        temp = pythonnet_property_get(
            self.wrapped, "ForceAtZeroDisplacementInputMethod"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.SystemModel.PartModel.BearingF0InputMethod"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.part_model._2665", "BearingF0InputMethod"
        )(value)

    @force_at_zero_displacement_input_method.setter
    @exception_bridge
    @enforce_parameter_types
    def force_at_zero_displacement_input_method(
        self: "Self", value: "_2665.BearingF0InputMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.SystemModel.PartModel.BearingF0InputMethod"
        )
        pythonnet_property_set(
            self.wrapped, "ForceAtZeroDisplacementInputMethod", value
        )

    @property
    @exception_bridge
    def has_radial_mounting_clearance(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "HasRadialMountingClearance")

        if temp is None:
            return False

        return temp

    @has_radial_mounting_clearance.setter
    @exception_bridge
    @enforce_parameter_types
    def has_radial_mounting_clearance(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "HasRadialMountingClearance",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def include_fitting_details(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeFittingDetails")

        if temp is None:
            return False

        return temp

    @include_fitting_details.setter
    @exception_bridge
    @enforce_parameter_types
    def include_fitting_details(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeFittingDetails",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def inner_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "InnerDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @inner_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def inner_diameter(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "InnerDiameter", value)

    @property
    @exception_bridge
    def inner_fitting_chart(self: "Self") -> "_1981.SimpleChartDefinition":
        """mastapy.utility.report.SimpleChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerFittingChart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def inner_node_position_from_centre(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerNodePositionFromCentre")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def is_internal_clearance_adjusted_after_fitting(
        self: "Self",
    ) -> "overridable.Overridable_bool":
        """Overridable[bool]"""
        temp = pythonnet_property_get(
            self.wrapped, "IsInternalClearanceAdjustedAfterFitting"
        )

        if temp is None:
            return False

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_bool"
        )(temp)

    @is_internal_clearance_adjusted_after_fitting.setter
    @exception_bridge
    @enforce_parameter_types
    def is_internal_clearance_adjusted_after_fitting(
        self: "Self", value: "Union[bool, Tuple[bool, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else False, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "IsInternalClearanceAdjustedAfterFitting", value
        )

    @property
    @exception_bridge
    def journal_bearing_type(self: "Self") -> "_2089.JournalBearingType":
        """mastapy.bearings.JournalBearingType"""
        temp = pythonnet_property_get(self.wrapped, "JournalBearingType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.JournalBearingType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings._2089", "JournalBearingType"
        )(value)

    @journal_bearing_type.setter
    @exception_bridge
    @enforce_parameter_types
    def journal_bearing_type(self: "Self", value: "_2089.JournalBearingType") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Bearings.JournalBearingType"
        )
        pythonnet_property_set(self.wrapped, "JournalBearingType", value)

    @property
    @exception_bridge
    def left_node_position_from_centre(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeftNodePositionFromCentre")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Length")

        if temp is None:
            return 0.0

        return temp

    @length.setter
    @exception_bridge
    @enforce_parameter_types
    def length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Length", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def lubrication_detail(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "LubricationDetail", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @lubrication_detail.setter
    @exception_bridge
    @enforce_parameter_types
    def lubrication_detail(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "LubricationDetail",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def maximum_bearing_life_modification_factor(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumBearingLifeModificationFactor"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @maximum_bearing_life_modification_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_bearing_life_modification_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "MaximumBearingLifeModificationFactor", value
        )

    @property
    @exception_bridge
    def model(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_BearingModel":
        """EnumWithSelectedValue[mastapy.bearings.BearingModel]"""
        temp = pythonnet_property_get(self.wrapped, "Model")

        if temp is None:
            return None

        value = (
            enum_with_selected_value.EnumWithSelectedValue_BearingModel.wrapped_type()
        )
        return enum_with_selected_value_runtime.create(temp, value)

    @model.setter
    @exception_bridge
    @enforce_parameter_types
    def model(self: "Self", value: "_2080.BearingModel") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = (
            enum_with_selected_value.EnumWithSelectedValue_BearingModel.implicit_type()
        )
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "Model", value)

    @property
    @exception_bridge
    def offset_of_contact_on_inner_race_at_nominal_contact_angle(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "OffsetOfContactOnInnerRaceAtNominalContactAngle"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def offset_of_contact_on_left_race(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OffsetOfContactOnLeftRace")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def offset_of_contact_on_outer_race_at_nominal_contact_angle(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "OffsetOfContactOnOuterRaceAtNominalContactAngle"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def offset_of_contact_on_right_race(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OffsetOfContactOnRightRace")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def orientation(self: "Self") -> "_2166.Orientations":
        """mastapy.bearings.bearing_results.Orientations"""
        temp = pythonnet_property_get(self.wrapped, "Orientation")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.BearingResults.Orientations"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings.bearing_results._2166", "Orientations"
        )(value)

    @orientation.setter
    @exception_bridge
    @enforce_parameter_types
    def orientation(self: "Self", value: "_2166.Orientations") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Bearings.BearingResults.Orientations"
        )
        pythonnet_property_set(self.wrapped, "Orientation", value)

    @property
    @exception_bridge
    def outer_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "OuterDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @outer_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_diameter(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "OuterDiameter", value)

    @property
    @exception_bridge
    def outer_fitting_chart(self: "Self") -> "_1981.SimpleChartDefinition":
        """mastapy.utility.report.SimpleChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterFittingChart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def outer_node_position_from_centre(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterNodePositionFromCentre")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def override_design_lubrication_detail(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "OverrideDesignLubricationDetail")

        if temp is None:
            return False

        return temp

    @override_design_lubrication_detail.setter
    @exception_bridge
    @enforce_parameter_types
    def override_design_lubrication_detail(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OverrideDesignLubricationDetail",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def percentage_difference_between_inner_diameter_and_diameter_of_connected_component_at_inner_connection(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "PercentageDifferenceBetweenInnerDiameterAndDiameterOfConnectedComponentAtInnerConnection",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def percentage_difference_between_outer_diameter_and_diameter_of_connected_component_at_outer_connection(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "PercentageDifferenceBetweenOuterDiameterAndDiameterOfConnectedComponentAtOuterConnection",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def permissible_axial_load_calculation_method(
        self: "Self",
    ) -> "overridable.Overridable_CylindricalRollerMaxAxialLoadMethod":
        """Overridable[mastapy.bearings.bearing_results.CylindricalRollerMaxAxialLoadMethod]"""
        temp = pythonnet_property_get(
            self.wrapped, "PermissibleAxialLoadCalculationMethod"
        )

        if temp is None:
            return None

        value = (
            overridable.Overridable_CylindricalRollerMaxAxialLoadMethod.wrapped_type()
        )
        return overridable_enum_runtime.create(temp, value)

    @permissible_axial_load_calculation_method.setter
    @exception_bridge
    @enforce_parameter_types
    def permissible_axial_load_calculation_method(
        self: "Self",
        value: "Union[_2148.CylindricalRollerMaxAxialLoadMethod, Tuple[_2148.CylindricalRollerMaxAxialLoadMethod, bool]]",
    ) -> None:
        wrapper_type = (
            overridable.Overridable_CylindricalRollerMaxAxialLoadMethod.wrapper_type()
        )
        enclosed_type = (
            overridable.Overridable_CylindricalRollerMaxAxialLoadMethod.implicit_type()
        )
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "PermissibleAxialLoadCalculationMethod", value
        )

    @property
    @exception_bridge
    def permissible_track_truncation(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "PermissibleTrackTruncation")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @permissible_track_truncation.setter
    @exception_bridge
    @enforce_parameter_types
    def permissible_track_truncation(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "PermissibleTrackTruncation", value)

    @property
    @exception_bridge
    def preload(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_PreloadType":
        """EnumWithSelectedValue[mastapy.bearings.bearing_results.PreloadType]"""
        temp = pythonnet_property_get(self.wrapped, "Preload")

        if temp is None:
            return None

        value = (
            enum_with_selected_value.EnumWithSelectedValue_PreloadType.wrapped_type()
        )
        return enum_with_selected_value_runtime.create(temp, value)

    @preload.setter
    @exception_bridge
    @enforce_parameter_types
    def preload(self: "Self", value: "_2167.PreloadType") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = (
            enum_with_selected_value.EnumWithSelectedValue_PreloadType.implicit_type()
        )
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "Preload", value)

    @property
    @exception_bridge
    def preload_spring_initial_compression(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PreloadSpringInitialCompression")

        if temp is None:
            return 0.0

        return temp

    @preload_spring_initial_compression.setter
    @exception_bridge
    @enforce_parameter_types
    def preload_spring_initial_compression(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PreloadSpringInitialCompression",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def preload_spring_max_travel(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PreloadSpringMaxTravel")

        if temp is None:
            return 0.0

        return temp

    @preload_spring_max_travel.setter
    @exception_bridge
    @enforce_parameter_types
    def preload_spring_max_travel(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PreloadSpringMaxTravel",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def preload_spring_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PreloadSpringStiffness")

        if temp is None:
            return 0.0

        return temp

    @preload_spring_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def preload_spring_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PreloadSpringStiffness",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def preload_spring_on_outer(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "PreloadSpringOnOuter")

        if temp is None:
            return False

        return temp

    @preload_spring_on_outer.setter
    @exception_bridge
    @enforce_parameter_types
    def preload_spring_on_outer(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PreloadSpringOnOuter",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def preload_is_from_left(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "PreloadIsFromLeft")

        if temp is None:
            return False

        return temp

    @preload_is_from_left.setter
    @exception_bridge
    @enforce_parameter_types
    def preload_is_from_left(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PreloadIsFromLeft",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def radial_internal_clearance(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RadialInternalClearance")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @radial_internal_clearance.setter
    @exception_bridge
    @enforce_parameter_types
    def radial_internal_clearance(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RadialInternalClearance", value)

    @property
    @exception_bridge
    def right_node_position_from_centre(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RightNodePositionFromCentre")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def system_includes_oil_pump(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemIncludesOilPump")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def use_design_iso14179_settings(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseDesignISO14179Settings")

        if temp is None:
            return False

        return temp

    @use_design_iso14179_settings.setter
    @exception_bridge
    @enforce_parameter_types
    def use_design_iso14179_settings(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseDesignISO14179Settings",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def axial_internal_clearance_tolerance(
        self: "Self",
    ) -> "_2663.AxialInternalClearanceTolerance":
        """mastapy.system_model.part_model.AxialInternalClearanceTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AxialInternalClearanceTolerance")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def detail(self: "Self") -> "_2340.BearingDesign":
        """mastapy.bearings.bearing_designs.BearingDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Detail")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def displacement_for_stiffness_operating_point(
        self: "Self",
    ) -> "_1748.VectorWithLinearAndAngularComponents":
        """mastapy.math_utility.measured_vectors.VectorWithLinearAndAngularComponents

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DisplacementForStiffnessOperatingPoint"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def force_at_zero_displacement(
        self: "Self",
    ) -> "_1748.VectorWithLinearAndAngularComponents":
        """mastapy.math_utility.measured_vectors.VectorWithLinearAndAngularComponents

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceAtZeroDisplacement")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def force_for_stiffness_operating_point(
        self: "Self",
    ) -> "_1748.VectorWithLinearAndAngularComponents":
        """mastapy.math_utility.measured_vectors.VectorWithLinearAndAngularComponents

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceForStiffnessOperatingPoint")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def friction_coefficients(
        self: "Self",
    ) -> "_2279.RollingBearingFrictionCoefficients":
        """mastapy.bearings.bearing_results.rolling.RollingBearingFrictionCoefficients

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrictionCoefficients")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def inner_mounting_sleeve_bore_tolerance(
        self: "Self",
    ) -> "_2116.OuterSupportTolerance":
        """mastapy.bearings.tolerances.OuterSupportTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerMountingSleeveBoreTolerance")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def inner_mounting_sleeve_outer_diameter_tolerance(
        self: "Self",
    ) -> "_2110.InnerSupportTolerance":
        """mastapy.bearings.tolerances.InnerSupportTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "InnerMountingSleeveOuterDiameterTolerance"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def inner_support_detail(self: "Self") -> "_2123.SupportDetail":
        """mastapy.bearings.tolerances.SupportDetail

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerSupportDetail")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def left_support_detail(self: "Self") -> "_2123.SupportDetail":
        """mastapy.bearings.tolerances.SupportDetail

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeftSupportDetail")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def outer_mounting_sleeve_bore_tolerance(
        self: "Self",
    ) -> "_2116.OuterSupportTolerance":
        """mastapy.bearings.tolerances.OuterSupportTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterMountingSleeveBoreTolerance")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def outer_mounting_sleeve_outer_diameter_tolerance(
        self: "Self",
    ) -> "_2110.InnerSupportTolerance":
        """mastapy.bearings.tolerances.InnerSupportTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "OuterMountingSleeveOuterDiameterTolerance"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def outer_support_detail(self: "Self") -> "_2123.SupportDetail":
        """mastapy.bearings.tolerances.SupportDetail

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterSupportDetail")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def overridden_lubrication_detail(self: "Self") -> "_356.LubricationDetail":
        """mastapy.materials.LubricationDetail

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OverriddenLubricationDetail")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def radial_internal_clearance_tolerance(
        self: "Self",
    ) -> "_2704.RadialInternalClearanceTolerance":
        """mastapy.system_model.part_model.RadialInternalClearanceTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RadialInternalClearanceTolerance")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def right_support_detail(self: "Self") -> "_2123.SupportDetail":
        """mastapy.bearings.tolerances.SupportDetail

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RightSupportDetail")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def ring_tolerance_inner(self: "Self") -> "_2109.InnerRingTolerance":
        """mastapy.bearings.tolerances.InnerRingTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RingToleranceInner")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def ring_tolerance_left(self: "Self") -> "_2120.RingTolerance":
        """mastapy.bearings.tolerances.RingTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RingToleranceLeft")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def ring_tolerance_outer(self: "Self") -> "_2115.OuterRingTolerance":
        """mastapy.bearings.tolerances.OuterRingTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RingToleranceOuter")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def ring_tolerance_right(self: "Self") -> "_2120.RingTolerance":
        """mastapy.bearings.tolerances.RingTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RingToleranceRight")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def skf_loss_moment_multipliers(self: "Self") -> "_1791.SKFLossMomentMultipliers":
        """mastapy.utility.SKFLossMomentMultipliers

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SKFLossMomentMultipliers")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def simple_bearing_detail_property(self: "Self") -> "_2340.BearingDesign":
        """mastapy.bearings.bearing_designs.BearingDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SimpleBearingDetailProperty")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def support_tolerance_inner(self: "Self") -> "_2110.InnerSupportTolerance":
        """mastapy.bearings.tolerances.InnerSupportTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SupportToleranceInner")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def support_tolerance_left(self: "Self") -> "_2125.SupportTolerance":
        """mastapy.bearings.tolerances.SupportTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SupportToleranceLeft")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def support_tolerance_outer(self: "Self") -> "_2116.OuterSupportTolerance":
        """mastapy.bearings.tolerances.OuterSupportTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SupportToleranceOuter")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def support_tolerance_right(self: "Self") -> "_2125.SupportTolerance":
        """mastapy.bearings.tolerances.SupportTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SupportToleranceRight")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def mounting(self: "Self") -> "List[_2666.BearingRaceMountingOptions]":
        """List[mastapy.system_model.part_model.BearingRaceMountingOptions]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Mounting")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def tolerance_combinations(self: "Self") -> "List[_2127.ToleranceCombination]":
        """List[mastapy.bearings.tolerances.ToleranceCombination]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToleranceCombinations")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def is_radial_bearing(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsRadialBearing")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def specified_stiffness_for_linear_bearing_in_local_coordinate_system(
        self: "Self",
    ) -> "List[List[float]]":
        """List[List[float]]"""
        temp = pythonnet_property_get(
            self.wrapped, "SpecifiedStiffnessForLinearBearingInLocalCoordinateSystem"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_list_float_2d(temp)

        if value is None:
            return None

        return value

    @specified_stiffness_for_linear_bearing_in_local_coordinate_system.setter
    @exception_bridge
    @enforce_parameter_types
    def specified_stiffness_for_linear_bearing_in_local_coordinate_system(
        self: "Self", value: "List[List[float]]"
    ) -> None:
        value = conversion.mp_to_pn_list_float_2d(value)
        pythonnet_property_set(
            self.wrapped,
            "SpecifiedStiffnessForLinearBearingInLocalCoordinateSystem",
            value,
        )

    @exception_bridge
    @enforce_parameter_types
    def try_attach_right_side_to(
        self: "Self", shaft: "_2714.Shaft", offset: "float" = float("nan")
    ) -> "_2671.ComponentsConnectedResult":
        """mastapy.system_model.part_model.ComponentsConnectedResult

        Args:
            shaft (mastapy.system_model.part_model.shaft_model.Shaft)
            offset (float, optional)
        """
        offset = float(offset)
        method_result = pythonnet_method_call(
            self.wrapped,
            "TryAttachRightSideTo",
            shaft.wrapped if shaft else None,
            offset if offset else 0.0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def set_detail_from_catalogue(
        self: "Self", catalogue: "_2072.BearingCatalog", designation: "str"
    ) -> None:
        """Method does not return.

        Args:
            catalogue (mastapy.bearings.BearingCatalog)
            designation (str)
        """
        catalogue = conversion.mp_to_pn_enum(
            catalogue, "SMT.MastaAPI.Bearings.BearingCatalog"
        )
        designation = str(designation)
        pythonnet_method_call(
            self.wrapped,
            "SetDetailFromCatalogue",
            catalogue,
            designation if designation else "",
        )

    @exception_bridge
    @enforce_parameter_types
    def try_attach_left_side_to(
        self: "Self", shaft: "_2714.Shaft", offset: "float" = float("nan")
    ) -> "_2671.ComponentsConnectedResult":
        """mastapy.system_model.part_model.ComponentsConnectedResult

        Args:
            shaft (mastapy.system_model.part_model.shaft_model.Shaft)
            offset (float, optional)
        """
        offset = float(offset)
        method_result = pythonnet_method_call(
            self.wrapped,
            "TryAttachLeftSideTo",
            shaft.wrapped if shaft else None,
            offset if offset else 0.0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_Bearing":
        """Cast to another type.

        Returns:
            _Cast_Bearing
        """
        return _Cast_Bearing(self)
