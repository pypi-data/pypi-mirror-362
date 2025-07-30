"""KlingelnbergSpiralBevelVirtualCylindricalGear"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.rating.virtual_cylindrical_gears import _477

_KLINGELNBERG_SPIRAL_BEVEL_VIRTUAL_CYLINDRICAL_GEAR = python_net_import(
    "SMT.MastaAPI.Gears.Rating.VirtualCylindricalGears",
    "KlingelnbergSpiralBevelVirtualCylindricalGear",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating.virtual_cylindrical_gears import _479, _480

    Self = TypeVar("Self", bound="KlingelnbergSpiralBevelVirtualCylindricalGear")
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergSpiralBevelVirtualCylindricalGear._Cast_KlingelnbergSpiralBevelVirtualCylindricalGear",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergSpiralBevelVirtualCylindricalGear",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergSpiralBevelVirtualCylindricalGear:
    """Special nested class for casting KlingelnbergSpiralBevelVirtualCylindricalGear to subclasses."""

    __parent__: "KlingelnbergSpiralBevelVirtualCylindricalGear"

    @property
    def klingelnberg_virtual_cylindrical_gear(
        self: "CastSelf",
    ) -> "_477.KlingelnbergVirtualCylindricalGear":
        return self.__parent__._cast(_477.KlingelnbergVirtualCylindricalGear)

    @property
    def virtual_cylindrical_gear(self: "CastSelf") -> "_479.VirtualCylindricalGear":
        from mastapy._private.gears.rating.virtual_cylindrical_gears import _479

        return self.__parent__._cast(_479.VirtualCylindricalGear)

    @property
    def virtual_cylindrical_gear_basic(
        self: "CastSelf",
    ) -> "_480.VirtualCylindricalGearBasic":
        from mastapy._private.gears.rating.virtual_cylindrical_gears import _480

        return self.__parent__._cast(_480.VirtualCylindricalGearBasic)

    @property
    def klingelnberg_spiral_bevel_virtual_cylindrical_gear(
        self: "CastSelf",
    ) -> "KlingelnbergSpiralBevelVirtualCylindricalGear":
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
class KlingelnbergSpiralBevelVirtualCylindricalGear(
    _477.KlingelnbergVirtualCylindricalGear
):
    """KlingelnbergSpiralBevelVirtualCylindricalGear

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _KLINGELNBERG_SPIRAL_BEVEL_VIRTUAL_CYLINDRICAL_GEAR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_KlingelnbergSpiralBevelVirtualCylindricalGear":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergSpiralBevelVirtualCylindricalGear
        """
        return _Cast_KlingelnbergSpiralBevelVirtualCylindricalGear(self)
