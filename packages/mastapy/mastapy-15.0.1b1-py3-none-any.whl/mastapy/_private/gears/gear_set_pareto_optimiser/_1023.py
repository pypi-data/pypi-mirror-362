"""MicroGeometryGearSetDesignSpaceSearch"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get_with_method,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_set_pareto_optimiser import _1019

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_MICRO_GEOMETRY_GEAR_SET_DESIGN_SPACE_SEARCH = python_net_import(
    "SMT.MastaAPI.Gears.GearSetParetoOptimiser", "MicroGeometryGearSetDesignSpaceSearch"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_set_pareto_optimiser import _1009

    Self = TypeVar("Self", bound="MicroGeometryGearSetDesignSpaceSearch")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MicroGeometryGearSetDesignSpaceSearch._Cast_MicroGeometryGearSetDesignSpaceSearch",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MicroGeometryGearSetDesignSpaceSearch",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MicroGeometryGearSetDesignSpaceSearch:
    """Special nested class for casting MicroGeometryGearSetDesignSpaceSearch to subclasses."""

    __parent__: "MicroGeometryGearSetDesignSpaceSearch"

    @property
    def micro_geometry_design_space_search(
        self: "CastSelf",
    ) -> "_1019.MicroGeometryDesignSpaceSearch":
        return self.__parent__._cast(_1019.MicroGeometryDesignSpaceSearch)

    @property
    def design_space_search_base(self: "CastSelf") -> "_1009.DesignSpaceSearchBase":
        pass

        from mastapy._private.gears.gear_set_pareto_optimiser import _1009

        return self.__parent__._cast(_1009.DesignSpaceSearchBase)

    @property
    def micro_geometry_gear_set_design_space_search(
        self: "CastSelf",
    ) -> "MicroGeometryGearSetDesignSpaceSearch":
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
class MicroGeometryGearSetDesignSpaceSearch(_1019.MicroGeometryDesignSpaceSearch):
    """MicroGeometryGearSetDesignSpaceSearch

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MICRO_GEOMETRY_GEAR_SET_DESIGN_SPACE_SEARCH

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
    def cast_to(self: "Self") -> "_Cast_MicroGeometryGearSetDesignSpaceSearch":
        """Cast to another type.

        Returns:
            _Cast_MicroGeometryGearSetDesignSpaceSearch
        """
        return _Cast_MicroGeometryGearSetDesignSpaceSearch(self)
