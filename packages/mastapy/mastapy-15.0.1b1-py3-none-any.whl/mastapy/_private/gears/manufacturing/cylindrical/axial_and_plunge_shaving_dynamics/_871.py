"""ShavingDynamicsCalculationForHobbedGears"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeVar

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
    pythonnet_property_get,
    pythonnet_property_get_with_method,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs.cylindrical import _1135
from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
    _869,
)

_REPORTING_OVERRIDABLE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "ReportingOverridable"
)
_SHAVING_DYNAMICS_CALCULATION_FOR_HOBBED_GEARS = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics",
    "ShavingDynamicsCalculationForHobbedGears",
)

if TYPE_CHECKING:
    from typing import Any, List, Type

    from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
        _856,
        _862,
        _864,
        _867,
        _868,
    )
    from mastapy._private.utility_gui.charts import _2070

    Self = TypeVar("Self", bound="ShavingDynamicsCalculationForHobbedGears")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ShavingDynamicsCalculationForHobbedGears._Cast_ShavingDynamicsCalculationForHobbedGears",
    )

T = TypeVar("T", bound="_868.ShavingDynamics")

__docformat__ = "restructuredtext en"
__all__ = ("ShavingDynamicsCalculationForHobbedGears",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShavingDynamicsCalculationForHobbedGears:
    """Special nested class for casting ShavingDynamicsCalculationForHobbedGears to subclasses."""

    __parent__: "ShavingDynamicsCalculationForHobbedGears"

    @property
    def shaving_dynamics_calculation(
        self: "CastSelf",
    ) -> "_869.ShavingDynamicsCalculation":
        return self.__parent__._cast(_869.ShavingDynamicsCalculation)

    @property
    def conventional_shaving_dynamics_calculation_for_hobbed_gears(
        self: "CastSelf",
    ) -> "_856.ConventionalShavingDynamicsCalculationForHobbedGears":
        from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
            _856,
        )

        return self.__parent__._cast(
            _856.ConventionalShavingDynamicsCalculationForHobbedGears
        )

    @property
    def plunge_shaving_dynamics_calculation_for_hobbed_gears(
        self: "CastSelf",
    ) -> "_862.PlungeShavingDynamicsCalculationForHobbedGears":
        from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
            _862,
        )

        return self.__parent__._cast(
            _862.PlungeShavingDynamicsCalculationForHobbedGears
        )

    @property
    def shaving_dynamics_calculation_for_hobbed_gears(
        self: "CastSelf",
    ) -> "ShavingDynamicsCalculationForHobbedGears":
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
class ShavingDynamicsCalculationForHobbedGears(_869.ShavingDynamicsCalculation[T]):
    """ShavingDynamicsCalculationForHobbedGears

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _SHAVING_DYNAMICS_CALCULATION_FOR_HOBBED_GEARS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def redressing_chart_maximum_start_and_end_of_shaving_profile(
        self: "Self",
    ) -> "_2070.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RedressingChartMaximumStartAndEndOfShavingProfile"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def redressing_chart_maximum_start_and_minimum_end_of_shaving_profile(
        self: "Self",
    ) -> "_2070.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RedressingChartMaximumStartAndMinimumEndOfShavingProfile"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def redressing_chart_minimum_start_and_end_of_shaving_profile(
        self: "Self",
    ) -> "_2070.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RedressingChartMinimumStartAndEndOfShavingProfile"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def redressing_chart_minimum_start_and_maximum_end_of_shaving_profile(
        self: "Self",
    ) -> "_2070.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RedressingChartMinimumStartAndMaximumEndOfShavingProfile"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def selected_redressing(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_T":
        """ListWithSelectedItem[T]"""
        temp = pythonnet_property_get(self.wrapped, "SelectedRedressing")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_T",
        )(temp)

    @selected_redressing.setter
    @exception_bridge
    @enforce_parameter_types
    def selected_redressing(self: "Self", value: "T") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_T.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "SelectedRedressing", value)

    @property
    @exception_bridge
    def maximum_end_of_shaving_profile(
        self: "Self",
    ) -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get_with_method(
            self.wrapped, "MaximumEndOfShavingProfile", "Value"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def maximum_start_of_shaving_profile(
        self: "Self",
    ) -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get_with_method(
            self.wrapped, "MaximumStartOfShavingProfile", "Value"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def minimum_end_of_shaving_profile(
        self: "Self",
    ) -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get_with_method(
            self.wrapped, "MinimumEndOfShavingProfile", "Value"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def minimum_start_of_shaving_profile(
        self: "Self",
    ) -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get_with_method(
            self.wrapped, "MinimumStartOfShavingProfile", "Value"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def redressing_at_maximum_start_and_end_of_shaving_profile(
        self: "Self",
    ) -> "_867.ShaverRedressing[T]":
        """mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics.ShaverRedressing[T]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RedressingAtMaximumStartAndEndOfShavingProfile"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[T](temp)

    @property
    @exception_bridge
    def redressing_at_maximum_start_and_minimum_end_of_shaving_profile(
        self: "Self",
    ) -> "_867.ShaverRedressing[T]":
        """mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics.ShaverRedressing[T]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RedressingAtMaximumStartAndMinimumEndOfShavingProfile"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[T](temp)

    @property
    @exception_bridge
    def redressing_at_minimum_start_and_end_of_shaving_profile(
        self: "Self",
    ) -> "_867.ShaverRedressing[T]":
        """mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics.ShaverRedressing[T]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RedressingAtMinimumStartAndEndOfShavingProfile"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[T](temp)

    @property
    @exception_bridge
    def redressing_at_minimum_start_and_maximum_end_of_shaving_profile(
        self: "Self",
    ) -> "_867.ShaverRedressing[T]":
        """mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics.ShaverRedressing[T]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RedressingAtMinimumStartAndMaximumEndOfShavingProfile"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[T](temp)

    @property
    @exception_bridge
    def redressing_settings(self: "Self") -> "List[_864.RedressingSettings[T]]":
        """List[mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics.RedressingSettings[T]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RedressingSettings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ShavingDynamicsCalculationForHobbedGears":
        """Cast to another type.

        Returns:
            _Cast_ShavingDynamicsCalculationForHobbedGears
        """
        return _Cast_ShavingDynamicsCalculationForHobbedGears(self)
