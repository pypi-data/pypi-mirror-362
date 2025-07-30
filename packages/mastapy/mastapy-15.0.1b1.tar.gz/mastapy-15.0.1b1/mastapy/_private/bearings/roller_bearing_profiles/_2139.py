"""RollerBearingLoadDependentProfile"""

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
from mastapy._private.bearings.roller_bearing_profiles import _2141

_ROLLER_BEARING_LOAD_DEPENDENT_PROFILE = python_net_import(
    "SMT.MastaAPI.Bearings.RollerBearingProfiles", "RollerBearingLoadDependentProfile"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.bearings.roller_bearing_profiles import _2137, _2138, _2140

    Self = TypeVar("Self", bound="RollerBearingLoadDependentProfile")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RollerBearingLoadDependentProfile._Cast_RollerBearingLoadDependentProfile",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RollerBearingLoadDependentProfile",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RollerBearingLoadDependentProfile:
    """Special nested class for casting RollerBearingLoadDependentProfile to subclasses."""

    __parent__: "RollerBearingLoadDependentProfile"

    @property
    def roller_bearing_profile(self: "CastSelf") -> "_2141.RollerBearingProfile":
        return self.__parent__._cast(_2141.RollerBearingProfile)

    @property
    def roller_bearing_fujiwara_kawase_profile(
        self: "CastSelf",
    ) -> "_2137.RollerBearingFujiwaraKawaseProfile":
        from mastapy._private.bearings.roller_bearing_profiles import _2137

        return self.__parent__._cast(_2137.RollerBearingFujiwaraKawaseProfile)

    @property
    def roller_bearing_johns_gohar_profile(
        self: "CastSelf",
    ) -> "_2138.RollerBearingJohnsGoharProfile":
        from mastapy._private.bearings.roller_bearing_profiles import _2138

        return self.__parent__._cast(_2138.RollerBearingJohnsGoharProfile)

    @property
    def roller_bearing_lundberg_profile(
        self: "CastSelf",
    ) -> "_2140.RollerBearingLundbergProfile":
        from mastapy._private.bearings.roller_bearing_profiles import _2140

        return self.__parent__._cast(_2140.RollerBearingLundbergProfile)

    @property
    def roller_bearing_load_dependent_profile(
        self: "CastSelf",
    ) -> "RollerBearingLoadDependentProfile":
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
class RollerBearingLoadDependentProfile(_2141.RollerBearingProfile):
    """RollerBearingLoadDependentProfile

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROLLER_BEARING_LOAD_DEPENDENT_PROFILE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def load(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Load")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @load.setter
    @exception_bridge
    @enforce_parameter_types
    def load(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Load", value)

    @property
    @exception_bridge
    def stress(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Stress")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @stress.setter
    @exception_bridge
    @enforce_parameter_types
    def stress(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Stress", value)

    @property
    @exception_bridge
    def use_bearing_dynamic_capacity(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseBearingDynamicCapacity")

        if temp is None:
            return False

        return temp

    @use_bearing_dynamic_capacity.setter
    @exception_bridge
    @enforce_parameter_types
    def use_bearing_dynamic_capacity(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseBearingDynamicCapacity",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_RollerBearingLoadDependentProfile":
        """Cast to another type.

        Returns:
            _Cast_RollerBearingLoadDependentProfile
        """
        return _Cast_RollerBearingLoadDependentProfile(self)
