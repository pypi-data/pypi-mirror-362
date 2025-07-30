"""GearSetParetoOptimiser"""

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
from mastapy._private.gears.gear_set_pareto_optimiser import _1009, _1014
from mastapy._private.gears.rating import _445

_GEAR_SET_PARETO_OPTIMISER = python_net_import(
    "SMT.MastaAPI.Gears.GearSetParetoOptimiser", "GearSetParetoOptimiser"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs import _1054
    from mastapy._private.gears.gear_set_pareto_optimiser import (
        _1008,
        _1011,
        _1016,
        _1042,
        _1043,
    )

    Self = TypeVar("Self", bound="GearSetParetoOptimiser")
    CastSelf = TypeVar(
        "CastSelf", bound="GearSetParetoOptimiser._Cast_GearSetParetoOptimiser"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearSetParetoOptimiser",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetParetoOptimiser:
    """Special nested class for casting GearSetParetoOptimiser to subclasses."""

    __parent__: "GearSetParetoOptimiser"

    @property
    def design_space_search_base(self: "CastSelf") -> "_1009.DesignSpaceSearchBase":
        return self.__parent__._cast(_1009.DesignSpaceSearchBase)

    @property
    def cylindrical_gear_set_pareto_optimiser(
        self: "CastSelf",
    ) -> "_1008.CylindricalGearSetParetoOptimiser":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1008

        return self.__parent__._cast(_1008.CylindricalGearSetParetoOptimiser)

    @property
    def face_gear_set_pareto_optimiser(
        self: "CastSelf",
    ) -> "_1011.FaceGearSetParetoOptimiser":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1011

        return self.__parent__._cast(_1011.FaceGearSetParetoOptimiser)

    @property
    def hypoid_gear_set_pareto_optimiser(
        self: "CastSelf",
    ) -> "_1016.HypoidGearSetParetoOptimiser":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1016

        return self.__parent__._cast(_1016.HypoidGearSetParetoOptimiser)

    @property
    def spiral_bevel_gear_set_pareto_optimiser(
        self: "CastSelf",
    ) -> "_1042.SpiralBevelGearSetParetoOptimiser":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1042

        return self.__parent__._cast(_1042.SpiralBevelGearSetParetoOptimiser)

    @property
    def straight_bevel_gear_set_pareto_optimiser(
        self: "CastSelf",
    ) -> "_1043.StraightBevelGearSetParetoOptimiser":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1043

        return self.__parent__._cast(_1043.StraightBevelGearSetParetoOptimiser)

    @property
    def gear_set_pareto_optimiser(self: "CastSelf") -> "GearSetParetoOptimiser":
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
class GearSetParetoOptimiser(
    _1009.DesignSpaceSearchBase[
        _445.AbstractGearSetRating, _1014.GearSetOptimiserCandidate
    ]
):
    """GearSetParetoOptimiser

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_PARETO_OPTIMISER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def number_of_designs_with_gears_which_cannot_be_manufactured_from_cutters(
        self: "Self",
    ) -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfDesignsWithGearsWhichCannotBeManufacturedFromCutters"
        )

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def remove_candidates_which_cannot_be_manufactured_with_cutters_from_database(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped,
            "RemoveCandidatesWhichCannotBeManufacturedWithCuttersFromDatabase",
        )

        if temp is None:
            return False

        return temp

    @remove_candidates_which_cannot_be_manufactured_with_cutters_from_database.setter
    @exception_bridge
    @enforce_parameter_types
    def remove_candidates_which_cannot_be_manufactured_with_cutters_from_database(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "RemoveCandidatesWhichCannotBeManufacturedWithCuttersFromDatabase",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def remove_candidates_with_warnings(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "RemoveCandidatesWithWarnings")

        if temp is None:
            return False

        return temp

    @remove_candidates_with_warnings.setter
    @exception_bridge
    @enforce_parameter_types
    def remove_candidates_with_warnings(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RemoveCandidatesWithWarnings",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def selected_candidate_geometry(self: "Self") -> "_1054.GearSetDesign":
        """mastapy.gears.gear_designs.GearSetDesign

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
    def all_candidate_gear_sets(self: "Self") -> "List[_1054.GearSetDesign]":
        """List[mastapy.gears.gear_designs.GearSetDesign]

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
    def candidate_gear_sets(self: "Self") -> "List[_1054.GearSetDesign]":
        """List[mastapy.gears.gear_designs.GearSetDesign]

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

    @exception_bridge
    def add_chart(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddChart")

    @exception_bridge
    def reset_charts(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ResetCharts")

    @property
    def cast_to(self: "Self") -> "_Cast_GearSetParetoOptimiser":
        """Cast to another type.

        Returns:
            _Cast_GearSetParetoOptimiser
        """
        return _Cast_GearSetParetoOptimiser(self)
