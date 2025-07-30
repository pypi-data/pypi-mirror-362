"""LinearBacklashSpecification"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_LINEAR_BACKLASH_SPECIFICATION = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "LinearBacklashSpecification"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1150

    Self = TypeVar("Self", bound="LinearBacklashSpecification")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LinearBacklashSpecification._Cast_LinearBacklashSpecification",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LinearBacklashSpecification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LinearBacklashSpecification:
    """Special nested class for casting LinearBacklashSpecification to subclasses."""

    __parent__: "LinearBacklashSpecification"

    @property
    def linear_backlash_specification(
        self: "CastSelf",
    ) -> "LinearBacklashSpecification":
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
class LinearBacklashSpecification(_0.APIBase):
    """LinearBacklashSpecification

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LINEAR_BACKLASH_SPECIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def flank_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FlankName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def circumferential_backlash_pitch_circle(
        self: "Self",
    ) -> "_1150.CylindricalMeshLinearBacklashSpecification":
        """mastapy.gears.gear_designs.cylindrical.CylindricalMeshLinearBacklashSpecification

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CircumferentialBacklashPitchCircle"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def circumferential_backlash_reference_circle(
        self: "Self",
    ) -> "_1150.CylindricalMeshLinearBacklashSpecification":
        """mastapy.gears.gear_designs.cylindrical.CylindricalMeshLinearBacklashSpecification

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CircumferentialBacklashReferenceCircle"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def normal_backlash(
        self: "Self",
    ) -> "_1150.CylindricalMeshLinearBacklashSpecification":
        """mastapy.gears.gear_designs.cylindrical.CylindricalMeshLinearBacklashSpecification

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalBacklash")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def radial_backlash(
        self: "Self",
    ) -> "_1150.CylindricalMeshLinearBacklashSpecification":
        """mastapy.gears.gear_designs.cylindrical.CylindricalMeshLinearBacklashSpecification

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RadialBacklash")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def linear_backlash(
        self: "Self",
    ) -> "List[_1150.CylindricalMeshLinearBacklashSpecification]":
        """List[mastapy.gears.gear_designs.cylindrical.CylindricalMeshLinearBacklashSpecification]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LinearBacklash")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_LinearBacklashSpecification":
        """Cast to another type.

        Returns:
            _Cast_LinearBacklashSpecification
        """
        return _Cast_LinearBacklashSpecification(self)
