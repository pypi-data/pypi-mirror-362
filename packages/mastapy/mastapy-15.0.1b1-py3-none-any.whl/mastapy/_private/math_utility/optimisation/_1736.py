"""ParetoOptimisationStrategyDatabase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.math_utility.optimisation import _1723

_PARETO_OPTIMISATION_STRATEGY_DATABASE = python_net_import(
    "SMT.MastaAPI.MathUtility.Optimisation", "ParetoOptimisationStrategyDatabase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_set_pareto_optimiser import (
        _1027,
        _1028,
        _1029,
        _1030,
        _1031,
        _1032,
        _1033,
        _1034,
        _1035,
        _1037,
        _1038,
        _1039,
        _1040,
    )
    from mastapy._private.utility.databases import _2023, _2027, _2031

    Self = TypeVar("Self", bound="ParetoOptimisationStrategyDatabase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ParetoOptimisationStrategyDatabase._Cast_ParetoOptimisationStrategyDatabase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ParetoOptimisationStrategyDatabase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ParetoOptimisationStrategyDatabase:
    """Special nested class for casting ParetoOptimisationStrategyDatabase to subclasses."""

    __parent__: "ParetoOptimisationStrategyDatabase"

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
    def pareto_conical_rating_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1027.ParetoConicalRatingOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1027

        return self.__parent__._cast(
            _1027.ParetoConicalRatingOptimisationStrategyDatabase
        )

    @property
    def pareto_cylindrical_gear_set_duty_cycle_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1028.ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1028

        return self.__parent__._cast(
            _1028.ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase
        )

    @property
    def pareto_cylindrical_gear_set_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1029.ParetoCylindricalGearSetOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1029

        return self.__parent__._cast(
            _1029.ParetoCylindricalGearSetOptimisationStrategyDatabase
        )

    @property
    def pareto_cylindrical_rating_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1030.ParetoCylindricalRatingOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1030

        return self.__parent__._cast(
            _1030.ParetoCylindricalRatingOptimisationStrategyDatabase
        )

    @property
    def pareto_face_gear_set_duty_cycle_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1031.ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1031

        return self.__parent__._cast(
            _1031.ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase
        )

    @property
    def pareto_face_gear_set_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1032.ParetoFaceGearSetOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1032

        return self.__parent__._cast(
            _1032.ParetoFaceGearSetOptimisationStrategyDatabase
        )

    @property
    def pareto_face_rating_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1033.ParetoFaceRatingOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1033

        return self.__parent__._cast(_1033.ParetoFaceRatingOptimisationStrategyDatabase)

    @property
    def pareto_hypoid_gear_set_duty_cycle_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1034.ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1034

        return self.__parent__._cast(
            _1034.ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase
        )

    @property
    def pareto_hypoid_gear_set_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1035.ParetoHypoidGearSetOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1035

        return self.__parent__._cast(
            _1035.ParetoHypoidGearSetOptimisationStrategyDatabase
        )

    @property
    def pareto_spiral_bevel_gear_set_duty_cycle_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1037.ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1037

        return self.__parent__._cast(
            _1037.ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase
        )

    @property
    def pareto_spiral_bevel_gear_set_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1038.ParetoSpiralBevelGearSetOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1038

        return self.__parent__._cast(
            _1038.ParetoSpiralBevelGearSetOptimisationStrategyDatabase
        )

    @property
    def pareto_straight_bevel_gear_set_duty_cycle_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1039.ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1039

        return self.__parent__._cast(
            _1039.ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase
        )

    @property
    def pareto_straight_bevel_gear_set_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1040.ParetoStraightBevelGearSetOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1040

        return self.__parent__._cast(
            _1040.ParetoStraightBevelGearSetOptimisationStrategyDatabase
        )

    @property
    def pareto_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "ParetoOptimisationStrategyDatabase":
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
class ParetoOptimisationStrategyDatabase(_1723.DesignSpaceSearchStrategyDatabase):
    """ParetoOptimisationStrategyDatabase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PARETO_OPTIMISATION_STRATEGY_DATABASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ParetoOptimisationStrategyDatabase":
        """Cast to another type.

        Returns:
            _Cast_ParetoOptimisationStrategyDatabase
        """
        return _Cast_ParetoOptimisationStrategyDatabase(self)
