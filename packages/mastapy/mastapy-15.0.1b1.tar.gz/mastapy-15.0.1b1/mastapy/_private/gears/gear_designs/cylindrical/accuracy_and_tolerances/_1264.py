"""OverridableTolerance"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_OVERRIDABLE_TOLERANCE = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.AccuracyAndTolerances",
    "OverridableTolerance",
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    Self = TypeVar("Self", bound="OverridableTolerance")
    CastSelf = TypeVar(
        "CastSelf", bound="OverridableTolerance._Cast_OverridableTolerance"
    )


__docformat__ = "restructuredtext en"
__all__ = ("OverridableTolerance",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_OverridableTolerance:
    """Special nested class for casting OverridableTolerance to subclasses."""

    __parent__: "OverridableTolerance"

    @property
    def overridable_tolerance(self: "CastSelf") -> "OverridableTolerance":
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
class OverridableTolerance(_0.APIBase):
    """OverridableTolerance

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _OVERRIDABLE_TOLERANCE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def standard_value(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StandardValue")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def value(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Value")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @value.setter
    @exception_bridge
    @enforce_parameter_types
    def value(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Value", value)

    @property
    def cast_to(self: "Self") -> "_Cast_OverridableTolerance":
        """Cast to another type.

        Returns:
            _Cast_OverridableTolerance
        """
        return _Cast_OverridableTolerance(self)
