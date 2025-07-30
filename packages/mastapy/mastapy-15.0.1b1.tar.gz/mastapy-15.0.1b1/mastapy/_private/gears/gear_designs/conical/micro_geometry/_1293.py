"""ConicalGearFlankMicroGeometry"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

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
from mastapy._private.gears.micro_geometry import _661

_CONICAL_GEAR_FLANK_MICRO_GEOMETRY = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Conical.MicroGeometry",
    "ConicalGearFlankMicroGeometry",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears import _426
    from mastapy._private.gears.gear_designs.conical import _1274
    from mastapy._private.gears.gear_designs.conical.micro_geometry import (
        _1292,
        _1294,
        _1295,
    )

    Self = TypeVar("Self", bound="ConicalGearFlankMicroGeometry")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearFlankMicroGeometry._Cast_ConicalGearFlankMicroGeometry",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearFlankMicroGeometry",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearFlankMicroGeometry:
    """Special nested class for casting ConicalGearFlankMicroGeometry to subclasses."""

    __parent__: "ConicalGearFlankMicroGeometry"

    @property
    def flank_micro_geometry(self: "CastSelf") -> "_661.FlankMicroGeometry":
        return self.__parent__._cast(_661.FlankMicroGeometry)

    @property
    def conical_gear_flank_micro_geometry(
        self: "CastSelf",
    ) -> "ConicalGearFlankMicroGeometry":
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
class ConicalGearFlankMicroGeometry(_661.FlankMicroGeometry):
    """ConicalGearFlankMicroGeometry

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_FLANK_MICRO_GEOMETRY

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
    def bias(self: "Self") -> "_1292.ConicalGearBiasModification":
        """mastapy.gears.gear_designs.conical.micro_geometry.ConicalGearBiasModification

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Bias")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def lead_relief(self: "Self") -> "_1294.ConicalGearLeadModification":
        """mastapy.gears.gear_designs.conical.micro_geometry.ConicalGearLeadModification

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeadRelief")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def profile_relief(self: "Self") -> "_1295.ConicalGearProfileModification":
        """mastapy.gears.gear_designs.conical.micro_geometry.ConicalGearProfileModification

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProfileRelief")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear_design(self: "Self") -> "_1274.ConicalGearDesign":
        """mastapy.gears.gear_designs.conical.ConicalGearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearFlankMicroGeometry":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearFlankMicroGeometry
        """
        return _Cast_ConicalGearFlankMicroGeometry(self)
