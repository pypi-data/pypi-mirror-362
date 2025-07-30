"""EaseOffBasedTCA"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.manufacturing.bevel import _875

_EASE_OFF_BASED_TCA = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel", "EaseOffBasedTCA"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="EaseOffBasedTCA")
    CastSelf = TypeVar("CastSelf", bound="EaseOffBasedTCA._Cast_EaseOffBasedTCA")


__docformat__ = "restructuredtext en"
__all__ = ("EaseOffBasedTCA",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_EaseOffBasedTCA:
    """Special nested class for casting EaseOffBasedTCA to subclasses."""

    __parent__: "EaseOffBasedTCA"

    @property
    def abstract_tca(self: "CastSelf") -> "_875.AbstractTCA":
        return self.__parent__._cast(_875.AbstractTCA)

    @property
    def ease_off_based_tca(self: "CastSelf") -> "EaseOffBasedTCA":
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
class EaseOffBasedTCA(_875.AbstractTCA):
    """EaseOffBasedTCA

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _EASE_OFF_BASED_TCA

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def current_ease_off_optimisation_wheel_u(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CurrentEaseOffOptimisationWheelU")

        if temp is None:
            return 0.0

        return temp

    @current_ease_off_optimisation_wheel_u.setter
    @exception_bridge
    @enforce_parameter_types
    def current_ease_off_optimisation_wheel_u(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CurrentEaseOffOptimisationWheelU",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def current_ease_off_optimisation_wheel_v(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CurrentEaseOffOptimisationWheelV")

        if temp is None:
            return 0.0

        return temp

    @current_ease_off_optimisation_wheel_v.setter
    @exception_bridge
    @enforce_parameter_types
    def current_ease_off_optimisation_wheel_v(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CurrentEaseOffOptimisationWheelV",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_EaseOffBasedTCA":
        """Cast to another type.

        Returns:
            _Cast_EaseOffBasedTCA
        """
        return _Cast_EaseOffBasedTCA(self)
