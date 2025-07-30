"""GeometricConstantsForRollingFrictionalMoments"""

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

_GEOMETRIC_CONSTANTS_FOR_ROLLING_FRICTIONAL_MOMENTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling",
    "GeometricConstantsForRollingFrictionalMoments",
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    Self = TypeVar("Self", bound="GeometricConstantsForRollingFrictionalMoments")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GeometricConstantsForRollingFrictionalMoments._Cast_GeometricConstantsForRollingFrictionalMoments",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GeometricConstantsForRollingFrictionalMoments",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GeometricConstantsForRollingFrictionalMoments:
    """Special nested class for casting GeometricConstantsForRollingFrictionalMoments to subclasses."""

    __parent__: "GeometricConstantsForRollingFrictionalMoments"

    @property
    def geometric_constants_for_rolling_frictional_moments(
        self: "CastSelf",
    ) -> "GeometricConstantsForRollingFrictionalMoments":
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
class GeometricConstantsForRollingFrictionalMoments(_0.APIBase):
    """GeometricConstantsForRollingFrictionalMoments

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEOMETRIC_CONSTANTS_FOR_ROLLING_FRICTIONAL_MOMENTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def r1(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "R1")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @r1.setter
    @exception_bridge
    @enforce_parameter_types
    def r1(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "R1", value)

    @property
    @exception_bridge
    def r2(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "R2")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @r2.setter
    @exception_bridge
    @enforce_parameter_types
    def r2(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "R2", value)

    @property
    @exception_bridge
    def r3(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "R3")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @r3.setter
    @exception_bridge
    @enforce_parameter_types
    def r3(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "R3", value)

    @property
    @exception_bridge
    def r4(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "R4")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @r4.setter
    @exception_bridge
    @enforce_parameter_types
    def r4(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "R4", value)

    @property
    def cast_to(self: "Self") -> "_Cast_GeometricConstantsForRollingFrictionalMoments":
        """Cast to another type.

        Returns:
            _Cast_GeometricConstantsForRollingFrictionalMoments
        """
        return _Cast_GeometricConstantsForRollingFrictionalMoments(self)
