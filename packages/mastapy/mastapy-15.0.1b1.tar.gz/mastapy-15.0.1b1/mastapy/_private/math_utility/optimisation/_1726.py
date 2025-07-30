"""OptimisationHistory"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_OPTIMISATION_HISTORY = python_net_import(
    "SMT.MastaAPI.MathUtility.Optimisation", "OptimisationHistory"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.math_utility.optimisation import _1729

    Self = TypeVar("Self", bound="OptimisationHistory")
    CastSelf = TypeVar(
        "CastSelf", bound="OptimisationHistory._Cast_OptimisationHistory"
    )


__docformat__ = "restructuredtext en"
__all__ = ("OptimisationHistory",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_OptimisationHistory:
    """Special nested class for casting OptimisationHistory to subclasses."""

    __parent__: "OptimisationHistory"

    @property
    def optimisation_history(self: "CastSelf") -> "OptimisationHistory":
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
class OptimisationHistory(_0.APIBase):
    """OptimisationHistory

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _OPTIMISATION_HISTORY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def input_history(self: "Self") -> "List[_1729.OptimizationVariable]":
        """List[mastapy.math_utility.optimisation.OptimizationVariable]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InputHistory")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def input_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InputNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def target_history(self: "Self") -> "List[_1729.OptimizationVariable]":
        """List[mastapy.math_utility.optimisation.OptimizationVariable]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TargetHistory")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def target_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TargetNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @exception_bridge
    @enforce_parameter_types
    def add_input_history(self: "Self", value: "_1729.OptimizationVariable") -> None:
        """Method does not return.

        Args:
            value (mastapy.math_utility.optimisation.OptimizationVariable)
        """
        pythonnet_method_call(
            self.wrapped, "AddInputHistory", value.wrapped if value else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_target_history(self: "Self", value: "_1729.OptimizationVariable") -> None:
        """Method does not return.

        Args:
            value (mastapy.math_utility.optimisation.OptimizationVariable)
        """
        pythonnet_method_call(
            self.wrapped, "AddTargetHistory", value.wrapped if value else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_OptimisationHistory":
        """Cast to another type.

        Returns:
            _Cast_OptimisationHistory
        """
        return _Cast_OptimisationHistory(self)
