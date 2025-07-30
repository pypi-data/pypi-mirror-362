"""BevelVirtualCylindricalGearSetISO10300MethodB2"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.rating.virtual_cylindrical_gears import _485

_BEVEL_VIRTUAL_CYLINDRICAL_GEAR_SET_ISO10300_METHOD_B2 = python_net_import(
    "SMT.MastaAPI.Gears.Rating.VirtualCylindricalGears",
    "BevelVirtualCylindricalGearSetISO10300MethodB2",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating.virtual_cylindrical_gears import _483

    Self = TypeVar("Self", bound="BevelVirtualCylindricalGearSetISO10300MethodB2")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelVirtualCylindricalGearSetISO10300MethodB2._Cast_BevelVirtualCylindricalGearSetISO10300MethodB2",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelVirtualCylindricalGearSetISO10300MethodB2",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelVirtualCylindricalGearSetISO10300MethodB2:
    """Special nested class for casting BevelVirtualCylindricalGearSetISO10300MethodB2 to subclasses."""

    __parent__: "BevelVirtualCylindricalGearSetISO10300MethodB2"

    @property
    def virtual_cylindrical_gear_set_iso10300_method_b2(
        self: "CastSelf",
    ) -> "_485.VirtualCylindricalGearSetISO10300MethodB2":
        return self.__parent__._cast(_485.VirtualCylindricalGearSetISO10300MethodB2)

    @property
    def virtual_cylindrical_gear_set(
        self: "CastSelf",
    ) -> "_483.VirtualCylindricalGearSet":
        pass

        from mastapy._private.gears.rating.virtual_cylindrical_gears import _483

        return self.__parent__._cast(_483.VirtualCylindricalGearSet)

    @property
    def bevel_virtual_cylindrical_gear_set_iso10300_method_b2(
        self: "CastSelf",
    ) -> "BevelVirtualCylindricalGearSetISO10300MethodB2":
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
class BevelVirtualCylindricalGearSetISO10300MethodB2(
    _485.VirtualCylindricalGearSetISO10300MethodB2
):
    """BevelVirtualCylindricalGearSetISO10300MethodB2

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_VIRTUAL_CYLINDRICAL_GEAR_SET_ISO10300_METHOD_B2

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_BevelVirtualCylindricalGearSetISO10300MethodB2":
        """Cast to another type.

        Returns:
            _Cast_BevelVirtualCylindricalGearSetISO10300MethodB2
        """
        return _Cast_BevelVirtualCylindricalGearSetISO10300MethodB2(self)
