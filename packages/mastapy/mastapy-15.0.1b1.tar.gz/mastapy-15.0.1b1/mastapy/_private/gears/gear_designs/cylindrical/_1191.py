"""SurfaceRoughness"""

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
from mastapy._private.utility import _1779

_SURFACE_ROUGHNESS = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "SurfaceRoughness"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    Self = TypeVar("Self", bound="SurfaceRoughness")
    CastSelf = TypeVar("CastSelf", bound="SurfaceRoughness._Cast_SurfaceRoughness")


__docformat__ = "restructuredtext en"
__all__ = ("SurfaceRoughness",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SurfaceRoughness:
    """Special nested class for casting SurfaceRoughness to subclasses."""

    __parent__: "SurfaceRoughness"

    @property
    def independent_reportable_properties_base(
        self: "CastSelf",
    ) -> "_1779.IndependentReportablePropertiesBase":
        pass

        return self.__parent__._cast(_1779.IndependentReportablePropertiesBase)

    @property
    def surface_roughness(self: "CastSelf") -> "SurfaceRoughness":
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
class SurfaceRoughness(_1779.IndependentReportablePropertiesBase["SurfaceRoughness"]):
    """SurfaceRoughness

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SURFACE_ROUGHNESS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def fillet_roughness_rz(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FilletRoughnessRz")

        if temp is None:
            return 0.0

        return temp

    @fillet_roughness_rz.setter
    @exception_bridge
    @enforce_parameter_types
    def fillet_roughness_rz(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FilletRoughnessRz",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def flank_roughness_ra(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FlankRoughnessRa")

        if temp is None:
            return 0.0

        return temp

    @flank_roughness_ra.setter
    @exception_bridge
    @enforce_parameter_types
    def flank_roughness_ra(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FlankRoughnessRa", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def flank_roughness_rz(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FlankRoughnessRz")

        if temp is None:
            return 0.0

        return temp

    @flank_roughness_rz.setter
    @exception_bridge
    @enforce_parameter_types
    def flank_roughness_rz(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FlankRoughnessRz", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def flank_roughness_in_cla(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "FlankRoughnessInCLA")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @flank_roughness_in_cla.setter
    @exception_bridge
    @enforce_parameter_types
    def flank_roughness_in_cla(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "FlankRoughnessInCLA", value)

    @property
    @exception_bridge
    def flank_roughness_in_rms(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "FlankRoughnessInRMS")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @flank_roughness_in_rms.setter
    @exception_bridge
    @enforce_parameter_types
    def flank_roughness_in_rms(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "FlankRoughnessInRMS", value)

    @property
    @exception_bridge
    def is_flank_roughness_in_ra_estimated(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsFlankRoughnessInRaEstimated")

        if temp is None:
            return False

        return temp

    @is_flank_roughness_in_ra_estimated.setter
    @exception_bridge
    @enforce_parameter_types
    def is_flank_roughness_in_ra_estimated(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IsFlankRoughnessInRaEstimated",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def is_flank_roughness_in_rz_estimated(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsFlankRoughnessInRzEstimated")

        if temp is None:
            return False

        return temp

    @is_flank_roughness_in_rz_estimated.setter
    @exception_bridge
    @enforce_parameter_types
    def is_flank_roughness_in_rz_estimated(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IsFlankRoughnessInRzEstimated",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_SurfaceRoughness":
        """Cast to another type.

        Returns:
            _Cast_SurfaceRoughness
        """
        return _Cast_SurfaceRoughness(self)
