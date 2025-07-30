"""GearSetOptimisationResult"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_GEAR_SET_OPTIMISATION_RESULT = python_net_import(
    "SMT.MastaAPI.Gears", "GearSetOptimisationResult"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs import _1054
    from mastapy._private.gears.rating import _445
    from mastapy._private.math_utility.optimisation import _1726

    Self = TypeVar("Self", bound="GearSetOptimisationResult")
    CastSelf = TypeVar(
        "CastSelf", bound="GearSetOptimisationResult._Cast_GearSetOptimisationResult"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearSetOptimisationResult",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetOptimisationResult:
    """Special nested class for casting GearSetOptimisationResult to subclasses."""

    __parent__: "GearSetOptimisationResult"

    @property
    def gear_set_optimisation_result(self: "CastSelf") -> "GearSetOptimisationResult":
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
class GearSetOptimisationResult(_0.APIBase):
    """GearSetOptimisationResult

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_OPTIMISATION_RESULT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def gear_set(self: "Self") -> "_1054.GearSetDesign":
        """mastapy.gears.gear_designs.GearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSet")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def is_optimized(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsOptimized")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def optimisation_history(self: "Self") -> "_1726.OptimisationHistory":
        """mastapy.math_utility.optimisation.OptimisationHistory"""
        temp = pythonnet_property_get(self.wrapped, "OptimisationHistory")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @optimisation_history.setter
    @exception_bridge
    @enforce_parameter_types
    def optimisation_history(self: "Self", value: "_1726.OptimisationHistory") -> None:
        pythonnet_property_set(self.wrapped, "OptimisationHistory", value.wrapped)

    @property
    @exception_bridge
    def rating(self: "Self") -> "_445.AbstractGearSetRating":
        """mastapy.gears.rating.AbstractGearSetRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Rating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_GearSetOptimisationResult":
        """Cast to another type.

        Returns:
            _Cast_GearSetOptimisationResult
        """
        return _Cast_GearSetOptimisationResult(self)
