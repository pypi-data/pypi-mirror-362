"""MicroGeometryDesignSpaceSearchStrategyDatabase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.math_utility.optimisation import _1723

_MICRO_GEOMETRY_DESIGN_SPACE_SEARCH_STRATEGY_DATABASE = python_net_import(
    "SMT.MastaAPI.Gears.GearSetParetoOptimiser",
    "MicroGeometryDesignSpaceSearchStrategyDatabase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_set_pareto_optimiser import _1024, _1025
    from mastapy._private.utility.databases import _2023, _2027, _2031

    Self = TypeVar("Self", bound="MicroGeometryDesignSpaceSearchStrategyDatabase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MicroGeometryDesignSpaceSearchStrategyDatabase._Cast_MicroGeometryDesignSpaceSearchStrategyDatabase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MicroGeometryDesignSpaceSearchStrategyDatabase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MicroGeometryDesignSpaceSearchStrategyDatabase:
    """Special nested class for casting MicroGeometryDesignSpaceSearchStrategyDatabase to subclasses."""

    __parent__: "MicroGeometryDesignSpaceSearchStrategyDatabase"

    @property
    def design_space_search_strategy_database(
        self: "CastSelf",
    ) -> "_1723.DesignSpaceSearchStrategyDatabase":
        return self.__parent__._cast(_1723.DesignSpaceSearchStrategyDatabase)

    @property
    def named_database(self: "CastSelf") -> "_2027.NamedDatabase":
        pass

        from mastapy._private.utility.databases import _2027

        return self.__parent__._cast(_2027.NamedDatabase)

    @property
    def sql_database(self: "CastSelf") -> "_2031.SQLDatabase":
        pass

        from mastapy._private.utility.databases import _2031

        return self.__parent__._cast(_2031.SQLDatabase)

    @property
    def database(self: "CastSelf") -> "_2023.Database":
        pass

        from mastapy._private.utility.databases import _2023

        return self.__parent__._cast(_2023.Database)

    @property
    def micro_geometry_gear_set_design_space_search_strategy_database(
        self: "CastSelf",
    ) -> "_1024.MicroGeometryGearSetDesignSpaceSearchStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1024

        return self.__parent__._cast(
            _1024.MicroGeometryGearSetDesignSpaceSearchStrategyDatabase
        )

    @property
    def micro_geometry_gear_set_duty_cycle_design_space_search_strategy_database(
        self: "CastSelf",
    ) -> "_1025.MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1025

        return self.__parent__._cast(
            _1025.MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase
        )

    @property
    def micro_geometry_design_space_search_strategy_database(
        self: "CastSelf",
    ) -> "MicroGeometryDesignSpaceSearchStrategyDatabase":
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
class MicroGeometryDesignSpaceSearchStrategyDatabase(
    _1723.DesignSpaceSearchStrategyDatabase
):
    """MicroGeometryDesignSpaceSearchStrategyDatabase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MICRO_GEOMETRY_DESIGN_SPACE_SEARCH_STRATEGY_DATABASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_MicroGeometryDesignSpaceSearchStrategyDatabase":
        """Cast to another type.

        Returns:
            _Cast_MicroGeometryDesignSpaceSearchStrategyDatabase
        """
        return _Cast_MicroGeometryDesignSpaceSearchStrategyDatabase(self)
