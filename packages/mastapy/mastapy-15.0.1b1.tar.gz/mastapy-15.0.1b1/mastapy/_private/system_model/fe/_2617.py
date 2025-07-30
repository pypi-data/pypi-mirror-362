"""GearMeshingOptions"""

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

_GEAR_MESHING_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "GearMeshingOptions"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.gears.fe_model import _1319

    Self = TypeVar("Self", bound="GearMeshingOptions")
    CastSelf = TypeVar("CastSelf", bound="GearMeshingOptions._Cast_GearMeshingOptions")


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshingOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMeshingOptions:
    """Special nested class for casting GearMeshingOptions to subclasses."""

    __parent__: "GearMeshingOptions"

    @property
    def gear_meshing_options(self: "CastSelf") -> "GearMeshingOptions":
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
class GearMeshingOptions(_0.APIBase):
    """GearMeshingOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESHING_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def mesh_teeth(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "MeshTeeth")

        if temp is None:
            return False

        return temp

    @mesh_teeth.setter
    @exception_bridge
    @enforce_parameter_types
    def mesh_teeth(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "MeshTeeth", bool(value) if value is not None else False
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
    @exception_bridge
    def offset_of_gear_centre_calculated_from_fe(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "OffsetOfGearCentreCalculatedFromFE"
        )

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def element_settings(self: "Self") -> "_1319.GearMeshingElementOptions":
        """mastapy.gears.fe_model.GearMeshingElementOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElementSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_GearMeshingOptions":
        """Cast to another type.

        Returns:
            _Cast_GearMeshingOptions
        """
        return _Cast_GearMeshingOptions(self)
