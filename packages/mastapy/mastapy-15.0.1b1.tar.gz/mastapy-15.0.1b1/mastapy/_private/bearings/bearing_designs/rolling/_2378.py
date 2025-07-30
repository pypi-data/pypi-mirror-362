"""SKFSealFrictionalMomentConstants"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import (
    constructor,
    conversion,
    overridable_enum_runtime,
    utility,
)
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
from mastapy._private.bearings import _2101

_SKF_SEAL_FRICTIONAL_MOMENT_CONSTANTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling", "SKFSealFrictionalMomentConstants"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    Self = TypeVar("Self", bound="SKFSealFrictionalMomentConstants")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SKFSealFrictionalMomentConstants._Cast_SKFSealFrictionalMomentConstants",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SKFSealFrictionalMomentConstants",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SKFSealFrictionalMomentConstants:
    """Special nested class for casting SKFSealFrictionalMomentConstants to subclasses."""

    __parent__: "SKFSealFrictionalMomentConstants"

    @property
    def skf_seal_frictional_moment_constants(
        self: "CastSelf",
    ) -> "SKFSealFrictionalMomentConstants":
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
class SKFSealFrictionalMomentConstants(_0.APIBase):
    """SKFSealFrictionalMomentConstants

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SKF_SEAL_FRICTIONAL_MOMENT_CONSTANTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def ks1(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "KS1")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @ks1.setter
    @exception_bridge
    @enforce_parameter_types
    def ks1(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "KS1", value)

    @property
    @exception_bridge
    def ks2(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "KS2")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @ks2.setter
    @exception_bridge
    @enforce_parameter_types
    def ks2(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "KS2", value)

    @property
    @exception_bridge
    def seal_counterface_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "SealCounterfaceDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @seal_counterface_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def seal_counterface_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "SealCounterfaceDiameter", value)

    @property
    @exception_bridge
    def seal_location(self: "Self") -> "overridable.Overridable_SealLocation":
        """Overridable[mastapy.bearings.SealLocation]"""
        temp = pythonnet_property_get(self.wrapped, "SealLocation")

        if temp is None:
            return None

        value = overridable.Overridable_SealLocation.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @seal_location.setter
    @exception_bridge
    @enforce_parameter_types
    def seal_location(
        self: "Self",
        value: "Union[_2101.SealLocation, Tuple[_2101.SealLocation, bool]]",
    ) -> None:
        wrapper_type = overridable.Overridable_SealLocation.wrapper_type()
        enclosed_type = overridable.Overridable_SealLocation.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(self.wrapped, "SealLocation", value)

    @property
    @exception_bridge
    def beta(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Beta")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @beta.setter
    @exception_bridge
    @enforce_parameter_types
    def beta(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Beta", value)

    @property
    def cast_to(self: "Self") -> "_Cast_SKFSealFrictionalMomentConstants":
        """Cast to another type.

        Returns:
            _Cast_SKFSealFrictionalMomentConstants
        """
        return _Cast_SKFSealFrictionalMomentConstants(self)
