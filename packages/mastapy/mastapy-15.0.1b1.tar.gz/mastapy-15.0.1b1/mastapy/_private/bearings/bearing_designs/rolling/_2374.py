"""RollerRibDetail"""

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

_ROLLER_RIB_DETAIL = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling", "RollerRibDetail"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    Self = TypeVar("Self", bound="RollerRibDetail")
    CastSelf = TypeVar("CastSelf", bound="RollerRibDetail._Cast_RollerRibDetail")


__docformat__ = "restructuredtext en"
__all__ = ("RollerRibDetail",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RollerRibDetail:
    """Special nested class for casting RollerRibDetail to subclasses."""

    __parent__: "RollerRibDetail"

    @property
    def roller_rib_detail(self: "CastSelf") -> "RollerRibDetail":
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
class RollerRibDetail(_0.APIBase):
    """RollerRibDetail

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROLLER_RIB_DETAIL

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
    def height_above_race(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HeightAboveRace")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def layback_angle(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "LaybackAngle")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @layback_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def layback_angle(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "LaybackAngle", value)

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
    @exception_bridge
    def nominal_contact_height_above_race(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalContactHeightAboveRace")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def present(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "Present")

        if temp is None:
            return False

        return temp

    @present.setter
    @exception_bridge
    @enforce_parameter_types
    def present(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "Present", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def undercut_axial_angle(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "UndercutAxialAngle")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @undercut_axial_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def undercut_axial_angle(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "UndercutAxialAngle", value)

    @property
    @exception_bridge
    def undercut_axial_start_offset(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "UndercutAxialStartOffset")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @undercut_axial_start_offset.setter
    @exception_bridge
    @enforce_parameter_types
    def undercut_axial_start_offset(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "UndercutAxialStartOffset", value)

    @property
    @exception_bridge
    def undercut_radial_angle(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "UndercutRadialAngle")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @undercut_radial_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def undercut_radial_angle(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "UndercutRadialAngle", value)

    @property
    @exception_bridge
    def undercut_radial_start_offset(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "UndercutRadialStartOffset")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @undercut_radial_start_offset.setter
    @exception_bridge
    @enforce_parameter_types
    def undercut_radial_start_offset(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "UndercutRadialStartOffset", value)

    @property
    @exception_bridge
    def undercut_radius(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "UndercutRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @undercut_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def undercut_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "UndercutRadius", value)

    @property
    def cast_to(self: "Self") -> "_Cast_RollerRibDetail":
        """Cast to another type.

        Returns:
            _Cast_RollerRibDetail
        """
        return _Cast_RollerRibDetail(self)
