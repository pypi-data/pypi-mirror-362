"""RollerBearingFujiwaraKawaseProfile"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

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
from mastapy._private.bearings.roller_bearing_profiles import _2139

_ROLLER_BEARING_FUJIWARA_KAWASE_PROFILE = python_net_import(
    "SMT.MastaAPI.Bearings.RollerBearingProfiles", "RollerBearingFujiwaraKawaseProfile"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.bearings.roller_bearing_profiles import _2141

    Self = TypeVar("Self", bound="RollerBearingFujiwaraKawaseProfile")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RollerBearingFujiwaraKawaseProfile._Cast_RollerBearingFujiwaraKawaseProfile",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RollerBearingFujiwaraKawaseProfile",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RollerBearingFujiwaraKawaseProfile:
    """Special nested class for casting RollerBearingFujiwaraKawaseProfile to subclasses."""

    __parent__: "RollerBearingFujiwaraKawaseProfile"

    @property
    def roller_bearing_load_dependent_profile(
        self: "CastSelf",
    ) -> "_2139.RollerBearingLoadDependentProfile":
        return self.__parent__._cast(_2139.RollerBearingLoadDependentProfile)

    @property
    def roller_bearing_profile(self: "CastSelf") -> "_2141.RollerBearingProfile":
        from mastapy._private.bearings.roller_bearing_profiles import _2141

        return self.__parent__._cast(_2141.RollerBearingProfile)

    @property
    def roller_bearing_fujiwara_kawase_profile(
        self: "CastSelf",
    ) -> "RollerBearingFujiwaraKawaseProfile":
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
class RollerBearingFujiwaraKawaseProfile(_2139.RollerBearingLoadDependentProfile):
    """RollerBearingFujiwaraKawaseProfile

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROLLER_BEARING_FUJIWARA_KAWASE_PROFILE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def end_drop(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "EndDrop")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @end_drop.setter
    @exception_bridge
    @enforce_parameter_types
    def end_drop(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "EndDrop", value)

    @property
    @exception_bridge
    def length_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LengthFactor")

        if temp is None:
            return 0.0

        return temp

    @length_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def length_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "LengthFactor", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def load_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LoadFactor")

        if temp is None:
            return 0.0

        return temp

    @load_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def load_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "LoadFactor", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_RollerBearingFujiwaraKawaseProfile":
        """Cast to another type.

        Returns:
            _Cast_RollerBearingFujiwaraKawaseProfile
        """
        return _Cast_RollerBearingFujiwaraKawaseProfile(self)
