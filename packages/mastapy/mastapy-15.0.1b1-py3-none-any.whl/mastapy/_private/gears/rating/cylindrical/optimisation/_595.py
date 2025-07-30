"""SafetyFactorOptimisationStepResult"""

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
)

_SAFETY_FACTOR_OPTIMISATION_STEP_RESULT = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.Optimisation",
    "SafetyFactorOptimisationStepResult",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _459
    from mastapy._private.gears.rating.cylindrical.optimisation import _596, _597, _598

    Self = TypeVar("Self", bound="SafetyFactorOptimisationStepResult")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SafetyFactorOptimisationStepResult._Cast_SafetyFactorOptimisationStepResult",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SafetyFactorOptimisationStepResult",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SafetyFactorOptimisationStepResult:
    """Special nested class for casting SafetyFactorOptimisationStepResult to subclasses."""

    __parent__: "SafetyFactorOptimisationStepResult"

    @property
    def safety_factor_optimisation_step_result_angle(
        self: "CastSelf",
    ) -> "_596.SafetyFactorOptimisationStepResultAngle":
        from mastapy._private.gears.rating.cylindrical.optimisation import _596

        return self.__parent__._cast(_596.SafetyFactorOptimisationStepResultAngle)

    @property
    def safety_factor_optimisation_step_result_number(
        self: "CastSelf",
    ) -> "_597.SafetyFactorOptimisationStepResultNumber":
        from mastapy._private.gears.rating.cylindrical.optimisation import _597

        return self.__parent__._cast(_597.SafetyFactorOptimisationStepResultNumber)

    @property
    def safety_factor_optimisation_step_result_short_length(
        self: "CastSelf",
    ) -> "_598.SafetyFactorOptimisationStepResultShortLength":
        from mastapy._private.gears.rating.cylindrical.optimisation import _598

        return self.__parent__._cast(_598.SafetyFactorOptimisationStepResultShortLength)

    @property
    def safety_factor_optimisation_step_result(
        self: "CastSelf",
    ) -> "SafetyFactorOptimisationStepResult":
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
class SafetyFactorOptimisationStepResult(_0.APIBase):
    """SafetyFactorOptimisationStepResult

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SAFETY_FACTOR_OPTIMISATION_STEP_RESULT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def normalised_safety_factors(self: "Self") -> "_459.SafetyFactorResults":
        """mastapy.gears.rating.SafetyFactorResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalisedSafetyFactors")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def safety_factors(self: "Self") -> "_459.SafetyFactorResults":
        """mastapy.gears.rating.SafetyFactorResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SafetyFactors")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_SafetyFactorOptimisationStepResult":
        """Cast to another type.

        Returns:
            _Cast_SafetyFactorOptimisationStepResult
        """
        return _Cast_SafetyFactorOptimisationStepResult(self)
