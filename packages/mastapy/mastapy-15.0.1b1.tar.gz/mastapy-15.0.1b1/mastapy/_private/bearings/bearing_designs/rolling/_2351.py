"""BallBearingShoulderDefinition"""

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

_BALL_BEARING_SHOULDER_DEFINITION = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling", "BallBearingShoulderDefinition"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    Self = TypeVar("Self", bound="BallBearingShoulderDefinition")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BallBearingShoulderDefinition._Cast_BallBearingShoulderDefinition",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BallBearingShoulderDefinition",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BallBearingShoulderDefinition:
    """Special nested class for casting BallBearingShoulderDefinition to subclasses."""

    __parent__: "BallBearingShoulderDefinition"

    @property
    def ball_bearing_shoulder_definition(
        self: "CastSelf",
    ) -> "BallBearingShoulderDefinition":
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
class BallBearingShoulderDefinition(_0.APIBase):
    """BallBearingShoulderDefinition

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BALL_BEARING_SHOULDER_DEFINITION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def chamfer(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Chamfer")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @chamfer.setter
    @exception_bridge
    @enforce_parameter_types
    def chamfer(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Chamfer", value)

    @property
    @exception_bridge
    def diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Diameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def diameter(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Diameter", value)

    @property
    @exception_bridge
    def height(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Height")

        if temp is None:
            return 0.0

        return temp

    @height.setter
    @exception_bridge
    @enforce_parameter_types
    def height(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Height", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_BallBearingShoulderDefinition":
        """Cast to another type.

        Returns:
            _Cast_BallBearingShoulderDefinition
        """
        return _Cast_BallBearingShoulderDefinition(self)
