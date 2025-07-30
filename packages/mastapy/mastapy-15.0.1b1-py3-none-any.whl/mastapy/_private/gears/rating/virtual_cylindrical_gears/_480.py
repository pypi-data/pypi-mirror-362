"""VirtualCylindricalGearBasic"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_VIRTUAL_CYLINDRICAL_GEAR_BASIC = python_net_import(
    "SMT.MastaAPI.Gears.Rating.VirtualCylindricalGears", "VirtualCylindricalGearBasic"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating.virtual_cylindrical_gears import (
        _469,
        _472,
        _475,
        _476,
        _477,
        _479,
        _481,
        _482,
    )

    Self = TypeVar("Self", bound="VirtualCylindricalGearBasic")
    CastSelf = TypeVar(
        "CastSelf",
        bound="VirtualCylindricalGearBasic._Cast_VirtualCylindricalGearBasic",
    )


__docformat__ = "restructuredtext en"
__all__ = ("VirtualCylindricalGearBasic",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_VirtualCylindricalGearBasic:
    """Special nested class for casting VirtualCylindricalGearBasic to subclasses."""

    __parent__: "VirtualCylindricalGearBasic"

    @property
    def bevel_virtual_cylindrical_gear_iso10300_method_b2(
        self: "CastSelf",
    ) -> "_469.BevelVirtualCylindricalGearISO10300MethodB2":
        from mastapy._private.gears.rating.virtual_cylindrical_gears import _469

        return self.__parent__._cast(_469.BevelVirtualCylindricalGearISO10300MethodB2)

    @property
    def hypoid_virtual_cylindrical_gear_iso10300_method_b2(
        self: "CastSelf",
    ) -> "_472.HypoidVirtualCylindricalGearISO10300MethodB2":
        from mastapy._private.gears.rating.virtual_cylindrical_gears import _472

        return self.__parent__._cast(_472.HypoidVirtualCylindricalGearISO10300MethodB2)

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
    ) -> "_477.KlingelnbergVirtualCylindricalGear":
        from mastapy._private.gears.rating.virtual_cylindrical_gears import _477

        return self.__parent__._cast(_477.KlingelnbergVirtualCylindricalGear)

    @property
    def virtual_cylindrical_gear(self: "CastSelf") -> "_479.VirtualCylindricalGear":
        from mastapy._private.gears.rating.virtual_cylindrical_gears import _479

        return self.__parent__._cast(_479.VirtualCylindricalGear)

    @property
    def virtual_cylindrical_gear_iso10300_method_b1(
        self: "CastSelf",
    ) -> "_481.VirtualCylindricalGearISO10300MethodB1":
        from mastapy._private.gears.rating.virtual_cylindrical_gears import _481

        return self.__parent__._cast(_481.VirtualCylindricalGearISO10300MethodB1)

    @property
    def virtual_cylindrical_gear_iso10300_method_b2(
        self: "CastSelf",
    ) -> "_482.VirtualCylindricalGearISO10300MethodB2":
        from mastapy._private.gears.rating.virtual_cylindrical_gears import _482

        return self.__parent__._cast(_482.VirtualCylindricalGearISO10300MethodB2)

    @property
    def virtual_cylindrical_gear_basic(
        self: "CastSelf",
    ) -> "VirtualCylindricalGearBasic":
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
class VirtualCylindricalGearBasic(_0.APIBase):
    """VirtualCylindricalGearBasic

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _VIRTUAL_CYLINDRICAL_GEAR_BASIC

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def helix_angle_at_base_circle_of_virtual_cylindrical_gears(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HelixAngleAtBaseCircleOfVirtualCylindricalGears"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def helix_angle_of_virtual_cylindrical_gears(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HelixAngleOfVirtualCylindricalGears"
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
    def normal_module(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalModule")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def reference_diameter_of_virtual_cylindrical_gear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ReferenceDiameterOfVirtualCylindricalGear"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tip_diameter_of_virtual_cylindrical_gear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TipDiameterOfVirtualCylindricalGear"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tip_radius_of_virtual_cylindrical_gear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TipRadiusOfVirtualCylindricalGear")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_VirtualCylindricalGearBasic":
        """Cast to another type.

        Returns:
            _Cast_VirtualCylindricalGearBasic
        """
        return _Cast_VirtualCylindricalGearBasic(self)
