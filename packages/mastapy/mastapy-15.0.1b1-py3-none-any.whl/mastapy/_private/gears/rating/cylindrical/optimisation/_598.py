"""SafetyFactorOptimisationStepResultShortLength"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.cylindrical.optimisation import _595

_SAFETY_FACTOR_OPTIMISATION_STEP_RESULT_SHORT_LENGTH = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.Optimisation",
    "SafetyFactorOptimisationStepResultShortLength",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SafetyFactorOptimisationStepResultShortLength")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SafetyFactorOptimisationStepResultShortLength._Cast_SafetyFactorOptimisationStepResultShortLength",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SafetyFactorOptimisationStepResultShortLength",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SafetyFactorOptimisationStepResultShortLength:
    """Special nested class for casting SafetyFactorOptimisationStepResultShortLength to subclasses."""

    __parent__: "SafetyFactorOptimisationStepResultShortLength"

    @property
    def safety_factor_optimisation_step_result(
        self: "CastSelf",
    ) -> "_595.SafetyFactorOptimisationStepResult":
        return self.__parent__._cast(_595.SafetyFactorOptimisationStepResult)

    @property
    def safety_factor_optimisation_step_result_short_length(
        self: "CastSelf",
    ) -> "SafetyFactorOptimisationStepResultShortLength":
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
class SafetyFactorOptimisationStepResultShortLength(
    _595.SafetyFactorOptimisationStepResult
):
    """SafetyFactorOptimisationStepResultShortLength

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SAFETY_FACTOR_OPTIMISATION_STEP_RESULT_SHORT_LENGTH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Length")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_SafetyFactorOptimisationStepResultShortLength":
        """Cast to another type.

        Returns:
            _Cast_SafetyFactorOptimisationStepResultShortLength
        """
        return _Cast_SafetyFactorOptimisationStepResultShortLength(self)
