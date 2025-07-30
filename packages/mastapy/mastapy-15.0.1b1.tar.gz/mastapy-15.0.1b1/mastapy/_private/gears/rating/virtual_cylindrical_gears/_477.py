"""KlingelnbergVirtualCylindricalGear"""

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
from mastapy._private.gears.rating.virtual_cylindrical_gears import _479

_KLINGELNBERG_VIRTUAL_CYLINDRICAL_GEAR = python_net_import(
    "SMT.MastaAPI.Gears.Rating.VirtualCylindricalGears",
    "KlingelnbergVirtualCylindricalGear",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating.virtual_cylindrical_gears import _475, _476, _480

    Self = TypeVar("Self", bound="KlingelnbergVirtualCylindricalGear")
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergVirtualCylindricalGear._Cast_KlingelnbergVirtualCylindricalGear",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergVirtualCylindricalGear",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergVirtualCylindricalGear:
    """Special nested class for casting KlingelnbergVirtualCylindricalGear to subclasses."""

    __parent__: "KlingelnbergVirtualCylindricalGear"

    @property
    def virtual_cylindrical_gear(self: "CastSelf") -> "_479.VirtualCylindricalGear":
        return self.__parent__._cast(_479.VirtualCylindricalGear)

    @property
    def virtual_cylindrical_gear_basic(
        self: "CastSelf",
    ) -> "_480.VirtualCylindricalGearBasic":
        from mastapy._private.gears.rating.virtual_cylindrical_gears import _480

        return self.__parent__._cast(_480.VirtualCylindricalGearBasic)

    @property
    def klingelnberg_hypoid_virtual_cylindrical_gear(
        self: "CastSelf",
    ) -> "_475.KlingelnbergHypoidVirtualCylindricalGear":
        from mastapy._private.gears.rating.virtual_cylindrical_gears import _475

        return self.__parent__._cast(_475.KlingelnbergHypoidVirtualCylindricalGear)

    @property
    def klingelnberg_spiral_bevel_virtual_cylindrical_gear(
        self: "CastSelf",
    ) -> "_476.KlingelnbergSpiralBevelVirtualCylindricalGear":
        from mastapy._private.gears.rating.virtual_cylindrical_gears import _476

        return self.__parent__._cast(_476.KlingelnbergSpiralBevelVirtualCylindricalGear)

    @property
    def klingelnberg_virtual_cylindrical_gear(
        self: "CastSelf",
    ) -> "KlingelnbergVirtualCylindricalGear":
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
class KlingelnbergVirtualCylindricalGear(_479.VirtualCylindricalGear):
    """KlingelnbergVirtualCylindricalGear

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _KLINGELNBERG_VIRTUAL_CYLINDRICAL_GEAR

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
    def face_contact_ratio_transverse_for_virtual_cylindrical_gears(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "FaceContactRatioTransverseForVirtualCylindricalGears"
        )

        if temp is None:
            return 0.0

        return temp

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
    def outside_diameter_of_virtual_cylindrical_gear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "OutsideDiameterOfVirtualCylindricalGear"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def virtual_number_of_teeth_normal(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VirtualNumberOfTeethNormal")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def virtual_number_of_teeth_transverse(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VirtualNumberOfTeethTransverse")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_KlingelnbergVirtualCylindricalGear":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergVirtualCylindricalGear
        """
        return _Cast_KlingelnbergVirtualCylindricalGear(self)
