"""FlankMicroGeometry"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_FLANK_MICRO_GEOMETRY = python_net_import(
    "SMT.MastaAPI.Gears.MicroGeometry", "FlankMicroGeometry"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears import _426
    from mastapy._private.gears.gear_designs import _1051
    from mastapy._private.gears.gear_designs.conical.micro_geometry import _1293
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1208
    from mastapy._private.utility.scripting import _1936

    Self = TypeVar("Self", bound="FlankMicroGeometry")
    CastSelf = TypeVar("CastSelf", bound="FlankMicroGeometry._Cast_FlankMicroGeometry")


__docformat__ = "restructuredtext en"
__all__ = ("FlankMicroGeometry",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FlankMicroGeometry:
    """Special nested class for casting FlankMicroGeometry to subclasses."""

    __parent__: "FlankMicroGeometry"

    @property
    def cylindrical_gear_flank_micro_geometry(
        self: "CastSelf",
    ) -> "_1208.CylindricalGearFlankMicroGeometry":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1208

        return self.__parent__._cast(_1208.CylindricalGearFlankMicroGeometry)

    @property
    def conical_gear_flank_micro_geometry(
        self: "CastSelf",
    ) -> "_1293.ConicalGearFlankMicroGeometry":
        from mastapy._private.gears.gear_designs.conical.micro_geometry import _1293

        return self.__parent__._cast(_1293.ConicalGearFlankMicroGeometry)

    @property
    def flank_micro_geometry(self: "CastSelf") -> "FlankMicroGeometry":
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
class FlankMicroGeometry(_0.APIBase):
    """FlankMicroGeometry

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FLANK_MICRO_GEOMETRY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def micro_geometry_input_type(self: "Self") -> "_426.MicroGeometryInputTypes":
        """mastapy.gears.MicroGeometryInputTypes"""
        temp = pythonnet_property_get(self.wrapped, "MicroGeometryInputType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.MicroGeometryInputTypes"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears._426", "MicroGeometryInputTypes"
        )(value)

    @micro_geometry_input_type.setter
    @exception_bridge
    @enforce_parameter_types
    def micro_geometry_input_type(
        self: "Self", value: "_426.MicroGeometryInputTypes"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.MicroGeometryInputTypes"
        )
        pythonnet_property_set(self.wrapped, "MicroGeometryInputType", value)

    @property
    @exception_bridge
    def modification_chart(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModificationChart")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def gear_design(self: "Self") -> "_1051.GearDesign":
        """mastapy.gears.gear_designs.GearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def user_specified_data(self: "Self") -> "_1936.UserSpecifiedData":
        """mastapy.utility.scripting.UserSpecifiedData

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UserSpecifiedData")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_FlankMicroGeometry":
        """Cast to another type.

        Returns:
            _Cast_FlankMicroGeometry
        """
        return _Cast_FlankMicroGeometry(self)
