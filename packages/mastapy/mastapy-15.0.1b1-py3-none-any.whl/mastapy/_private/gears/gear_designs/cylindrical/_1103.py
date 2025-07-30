"""BacklashSpecification"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.gear_designs.cylindrical import _1180

_BACKLASH_SPECIFICATION = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "BacklashSpecification"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1147, _1168

    Self = TypeVar("Self", bound="BacklashSpecification")
    CastSelf = TypeVar(
        "CastSelf", bound="BacklashSpecification._Cast_BacklashSpecification"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BacklashSpecification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BacklashSpecification:
    """Special nested class for casting BacklashSpecification to subclasses."""

    __parent__: "BacklashSpecification"

    @property
    def relative_values_specification(
        self: "CastSelf",
    ) -> "_1180.RelativeValuesSpecification":
        pass

        return self.__parent__._cast(_1180.RelativeValuesSpecification)

    @property
    def backlash_specification(self: "CastSelf") -> "BacklashSpecification":
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
class BacklashSpecification(_1180.RelativeValuesSpecification["BacklashSpecification"]):
    """BacklashSpecification

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BACKLASH_SPECIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def left_flank(self: "Self") -> "_1168.LinearBacklashSpecification":
        """mastapy.gears.gear_designs.cylindrical.LinearBacklashSpecification

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeftFlank")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def right_flank(self: "Self") -> "_1168.LinearBacklashSpecification":
        """mastapy.gears.gear_designs.cylindrical.LinearBacklashSpecification

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RightFlank")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def angular_backlash(self: "Self") -> "List[_1147.CylindricalMeshAngularBacklash]":
        """List[mastapy.gears.gear_designs.cylindrical.CylindricalMeshAngularBacklash]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AngularBacklash")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def flanks(self: "Self") -> "List[_1168.LinearBacklashSpecification]":
        """List[mastapy.gears.gear_designs.cylindrical.LinearBacklashSpecification]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Flanks")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def both_flanks(self: "Self") -> "_1168.LinearBacklashSpecification":
        """mastapy.gears.gear_designs.cylindrical.LinearBacklashSpecification

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BothFlanks")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_BacklashSpecification":
        """Cast to another type.

        Returns:
            _Cast_BacklashSpecification
        """
        return _Cast_BacklashSpecification(self)
