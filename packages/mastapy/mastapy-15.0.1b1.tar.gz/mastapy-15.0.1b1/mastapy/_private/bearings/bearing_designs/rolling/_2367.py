"""GeometricConstantsForSlidingFrictionalMoments"""

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

_GEOMETRIC_CONSTANTS_FOR_SLIDING_FRICTIONAL_MOMENTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling",
    "GeometricConstantsForSlidingFrictionalMoments",
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    Self = TypeVar("Self", bound="GeometricConstantsForSlidingFrictionalMoments")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GeometricConstantsForSlidingFrictionalMoments._Cast_GeometricConstantsForSlidingFrictionalMoments",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GeometricConstantsForSlidingFrictionalMoments",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GeometricConstantsForSlidingFrictionalMoments:
    """Special nested class for casting GeometricConstantsForSlidingFrictionalMoments to subclasses."""

    __parent__: "GeometricConstantsForSlidingFrictionalMoments"

    @property
    def geometric_constants_for_sliding_frictional_moments(
        self: "CastSelf",
    ) -> "GeometricConstantsForSlidingFrictionalMoments":
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
class GeometricConstantsForSlidingFrictionalMoments(_0.APIBase):
    """GeometricConstantsForSlidingFrictionalMoments

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEOMETRIC_CONSTANTS_FOR_SLIDING_FRICTIONAL_MOMENTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def s1(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "S1")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @s1.setter
    @exception_bridge
    @enforce_parameter_types
    def s1(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "S1", value)

    @property
    @exception_bridge
    def s2(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "S2")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @s2.setter
    @exception_bridge
    @enforce_parameter_types
    def s2(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "S2", value)

    @property
    @exception_bridge
    def s3(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "S3")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @s3.setter
    @exception_bridge
    @enforce_parameter_types
    def s3(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "S3", value)

    @property
    @exception_bridge
    def s4(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "S4")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @s4.setter
    @exception_bridge
    @enforce_parameter_types
    def s4(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "S4", value)

    @property
    @exception_bridge
    def s5(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "S5")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @s5.setter
    @exception_bridge
    @enforce_parameter_types
    def s5(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "S5", value)

    @property
    def cast_to(self: "Self") -> "_Cast_GeometricConstantsForSlidingFrictionalMoments":
        """Cast to another type.

        Returns:
            _Cast_GeometricConstantsForSlidingFrictionalMoments
        """
        return _Cast_GeometricConstantsForSlidingFrictionalMoments(self)
