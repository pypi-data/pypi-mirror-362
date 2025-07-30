"""KlingelnbergVirtualCylindricalGearSet"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.virtual_cylindrical_gears import _477, _483

_KLINGELNBERG_VIRTUAL_CYLINDRICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.Gears.Rating.VirtualCylindricalGears",
    "KlingelnbergVirtualCylindricalGearSet",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="KlingelnbergVirtualCylindricalGearSet")
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergVirtualCylindricalGearSet._Cast_KlingelnbergVirtualCylindricalGearSet",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergVirtualCylindricalGearSet",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergVirtualCylindricalGearSet:
    """Special nested class for casting KlingelnbergVirtualCylindricalGearSet to subclasses."""

    __parent__: "KlingelnbergVirtualCylindricalGearSet"

    @property
    def virtual_cylindrical_gear_set(
        self: "CastSelf",
    ) -> "_483.VirtualCylindricalGearSet":
        return self.__parent__._cast(_483.VirtualCylindricalGearSet)

    @property
    def klingelnberg_virtual_cylindrical_gear_set(
        self: "CastSelf",
    ) -> "KlingelnbergVirtualCylindricalGearSet":
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
class KlingelnbergVirtualCylindricalGearSet(
    _483.VirtualCylindricalGearSet[_477.KlingelnbergVirtualCylindricalGear]
):
    """KlingelnbergVirtualCylindricalGearSet

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _KLINGELNBERG_VIRTUAL_CYLINDRICAL_GEAR_SET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def effective_face_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EffectiveFaceWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def length_of_path_of_contact_of_virtual_cylindrical_gear_in_transverse_section(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "LengthOfPathOfContactOfVirtualCylindricalGearInTransverseSection",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_contact_ratio_transverse_for_virtual_cylindrical_gears(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TotalContactRatioTransverseForVirtualCylindricalGears"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def virtual_transmission_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VirtualTransmissionRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_KlingelnbergVirtualCylindricalGearSet":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergVirtualCylindricalGearSet
        """
        return _Cast_KlingelnbergVirtualCylindricalGearSet(self)
