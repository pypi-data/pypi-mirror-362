"""ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.gear_set_pareto_optimiser import _1033

_PARETO_FACE_GEAR_SET_DUTY_CYCLE_OPTIMISATION_STRATEGY_DATABASE = python_net_import(
    "SMT.MastaAPI.Gears.GearSetParetoOptimiser",
    "ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility.optimisation import _1723, _1736
    from mastapy._private.utility.databases import _2023, _2027, _2031

    Self = TypeVar(
        "Self", bound="ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase._Cast_ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase:
    """Special nested class for casting ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase to subclasses."""

    __parent__: "ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase"

    @property
    def pareto_face_rating_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1033.ParetoFaceRatingOptimisationStrategyDatabase":
        return self.__parent__._cast(_1033.ParetoFaceRatingOptimisationStrategyDatabase)

    @property
    def pareto_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1736.ParetoOptimisationStrategyDatabase":
        from mastapy._private.math_utility.optimisation import _1736

        return self.__parent__._cast(_1736.ParetoOptimisationStrategyDatabase)

    @property
    def design_space_search_strategy_database(
        self: "CastSelf",
    ) -> "_1723.DesignSpaceSearchStrategyDatabase":
        from mastapy._private.math_utility.optimisation import _1723

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
    def pareto_face_gear_set_duty_cycle_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase":
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
class ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase(
    _1033.ParetoFaceRatingOptimisationStrategyDatabase
):
    """ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _PARETO_FACE_GEAR_SET_DUTY_CYCLE_OPTIMISATION_STRATEGY_DATABASE
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase":
        """Cast to another type.

        Returns:
            _Cast_ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase
        """
        return _Cast_ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase(self)
