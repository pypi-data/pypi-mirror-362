"""GearSetOptimiserCandidate"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private.gears.gear_set_pareto_optimiser import _1010
from mastapy._private.gears.rating import _445

_GEAR_SET_OPTIMISER_CANDIDATE = python_net_import(
    "SMT.MastaAPI.Gears.GearSetParetoOptimiser", "GearSetOptimiserCandidate"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="GearSetOptimiserCandidate")
    CastSelf = TypeVar(
        "CastSelf", bound="GearSetOptimiserCandidate._Cast_GearSetOptimiserCandidate"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearSetOptimiserCandidate",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetOptimiserCandidate:
    """Special nested class for casting GearSetOptimiserCandidate to subclasses."""

    __parent__: "GearSetOptimiserCandidate"

    @property
    def design_space_search_candidate_base(
        self: "CastSelf",
    ) -> "_1010.DesignSpaceSearchCandidateBase":
        pass

        return self.__parent__._cast(_1010.DesignSpaceSearchCandidateBase)

    @property
    def gear_set_optimiser_candidate(self: "CastSelf") -> "GearSetOptimiserCandidate":
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
class GearSetOptimiserCandidate(
    _1010.DesignSpaceSearchCandidateBase[
        _445.AbstractGearSetRating, "GearSetOptimiserCandidate"
    ]
):
    """GearSetOptimiserCandidate

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_OPTIMISER_CANDIDATE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def candidate(self: "Self") -> "_445.AbstractGearSetRating":
        """mastapy.gears.rating.AbstractGearSetRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Candidate")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    def add_design(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddDesign")

    @property
    def cast_to(self: "Self") -> "_Cast_GearSetOptimiserCandidate":
        """Cast to another type.

        Returns:
            _Cast_GearSetOptimiserCandidate
        """
        return _Cast_GearSetOptimiserCandidate(self)
