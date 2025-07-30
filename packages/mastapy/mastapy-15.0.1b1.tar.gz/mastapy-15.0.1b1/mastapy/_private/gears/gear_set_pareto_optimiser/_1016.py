"""HypoidGearSetParetoOptimiser"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_get_with_method,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_set_pareto_optimiser import _1015

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_HYPOID_GEAR_SET_PARETO_OPTIMISER = python_net_import(
    "SMT.MastaAPI.Gears.GearSetParetoOptimiser", "HypoidGearSetParetoOptimiser"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs.hypoid import _1091
    from mastapy._private.gears.gear_set_pareto_optimiser import _1009

    Self = TypeVar("Self", bound="HypoidGearSetParetoOptimiser")
    CastSelf = TypeVar(
        "CastSelf",
        bound="HypoidGearSetParetoOptimiser._Cast_HypoidGearSetParetoOptimiser",
    )


__docformat__ = "restructuredtext en"
__all__ = ("HypoidGearSetParetoOptimiser",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HypoidGearSetParetoOptimiser:
    """Special nested class for casting HypoidGearSetParetoOptimiser to subclasses."""

    __parent__: "HypoidGearSetParetoOptimiser"

    @property
    def gear_set_pareto_optimiser(self: "CastSelf") -> "_1015.GearSetParetoOptimiser":
        return self.__parent__._cast(_1015.GearSetParetoOptimiser)

    @property
    def design_space_search_base(self: "CastSelf") -> "_1009.DesignSpaceSearchBase":
        pass

        from mastapy._private.gears.gear_set_pareto_optimiser import _1009

        return self.__parent__._cast(_1009.DesignSpaceSearchBase)

    @property
    def hypoid_gear_set_pareto_optimiser(
        self: "CastSelf",
    ) -> "HypoidGearSetParetoOptimiser":
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
class HypoidGearSetParetoOptimiser(_1015.GearSetParetoOptimiser):
    """HypoidGearSetParetoOptimiser

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HYPOID_GEAR_SET_PARETO_OPTIMISER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def design_space_search_strategy(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "DesignSpaceSearchStrategy", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @design_space_search_strategy.setter
    @exception_bridge
    @enforce_parameter_types
    def design_space_search_strategy(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "DesignSpaceSearchStrategy",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def design_space_search_strategy_duty_cycle(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "DesignSpaceSearchStrategyDutyCycle", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @design_space_search_strategy_duty_cycle.setter
    @exception_bridge
    @enforce_parameter_types
    def design_space_search_strategy_duty_cycle(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "DesignSpaceSearchStrategyDutyCycle",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def selected_candidate_geometry(self: "Self") -> "_1091.HypoidGearSetDesign":
        """mastapy.gears.gear_designs.hypoid.HypoidGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SelectedCandidateGeometry")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def all_candidate_gear_sets(self: "Self") -> "List[_1091.HypoidGearSetDesign]":
        """List[mastapy.gears.gear_designs.hypoid.HypoidGearSetDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllCandidateGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def candidate_gear_sets(self: "Self") -> "List[_1091.HypoidGearSetDesign]":
        """List[mastapy.gears.gear_designs.hypoid.HypoidGearSetDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CandidateGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_HypoidGearSetParetoOptimiser":
        """Cast to another type.

        Returns:
            _Cast_HypoidGearSetParetoOptimiser
        """
        return _Cast_HypoidGearSetParetoOptimiser(self)
