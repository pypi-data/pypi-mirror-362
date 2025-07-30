"""ProfilePointFilletStressConcentrationFactors"""

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

_PROFILE_POINT_FILLET_STRESS_CONCENTRATION_FACTORS = python_net_import(
    "SMT.MastaAPI.Shafts", "ProfilePointFilletStressConcentrationFactors"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    Self = TypeVar("Self", bound="ProfilePointFilletStressConcentrationFactors")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ProfilePointFilletStressConcentrationFactors._Cast_ProfilePointFilletStressConcentrationFactors",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ProfilePointFilletStressConcentrationFactors",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ProfilePointFilletStressConcentrationFactors:
    """Special nested class for casting ProfilePointFilletStressConcentrationFactors to subclasses."""

    __parent__: "ProfilePointFilletStressConcentrationFactors"

    @property
    def profile_point_fillet_stress_concentration_factors(
        self: "CastSelf",
    ) -> "ProfilePointFilletStressConcentrationFactors":
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
class ProfilePointFilletStressConcentrationFactors(_0.APIBase):
    """ProfilePointFilletStressConcentrationFactors

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PROFILE_POINT_FILLET_STRESS_CONCENTRATION_FACTORS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def bending(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Bending")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @bending.setter
    @exception_bridge
    @enforce_parameter_types
    def bending(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Bending", value)

    @property
    @exception_bridge
    def tension(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Tension")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @tension.setter
    @exception_bridge
    @enforce_parameter_types
    def tension(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Tension", value)

    @property
    @exception_bridge
    def torsion(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Torsion")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @torsion.setter
    @exception_bridge
    @enforce_parameter_types
    def torsion(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Torsion", value)

    @property
    def cast_to(self: "Self") -> "_Cast_ProfilePointFilletStressConcentrationFactors":
        """Cast to another type.

        Returns:
            _Cast_ProfilePointFilletStressConcentrationFactors
        """
        return _Cast_ProfilePointFilletStressConcentrationFactors(self)
