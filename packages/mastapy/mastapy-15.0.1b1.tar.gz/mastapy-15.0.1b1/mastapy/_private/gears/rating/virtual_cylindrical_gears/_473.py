"""HypoidVirtualCylindricalGearSetISO10300MethodB1"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.rating.virtual_cylindrical_gears import _484

_HYPOID_VIRTUAL_CYLINDRICAL_GEAR_SET_ISO10300_METHOD_B1 = python_net_import(
    "SMT.MastaAPI.Gears.Rating.VirtualCylindricalGears",
    "HypoidVirtualCylindricalGearSetISO10300MethodB1",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating.virtual_cylindrical_gears import _483

    Self = TypeVar("Self", bound="HypoidVirtualCylindricalGearSetISO10300MethodB1")
    CastSelf = TypeVar(
        "CastSelf",
        bound="HypoidVirtualCylindricalGearSetISO10300MethodB1._Cast_HypoidVirtualCylindricalGearSetISO10300MethodB1",
    )


__docformat__ = "restructuredtext en"
__all__ = ("HypoidVirtualCylindricalGearSetISO10300MethodB1",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HypoidVirtualCylindricalGearSetISO10300MethodB1:
    """Special nested class for casting HypoidVirtualCylindricalGearSetISO10300MethodB1 to subclasses."""

    __parent__: "HypoidVirtualCylindricalGearSetISO10300MethodB1"

    @property
    def virtual_cylindrical_gear_set_iso10300_method_b1(
        self: "CastSelf",
    ) -> "_484.VirtualCylindricalGearSetISO10300MethodB1":
        return self.__parent__._cast(_484.VirtualCylindricalGearSetISO10300MethodB1)

    @property
    def virtual_cylindrical_gear_set(
        self: "CastSelf",
    ) -> "_483.VirtualCylindricalGearSet":
        pass

        from mastapy._private.gears.rating.virtual_cylindrical_gears import _483

        return self.__parent__._cast(_483.VirtualCylindricalGearSet)

    @property
    def hypoid_virtual_cylindrical_gear_set_iso10300_method_b1(
        self: "CastSelf",
    ) -> "HypoidVirtualCylindricalGearSetISO10300MethodB1":
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
class HypoidVirtualCylindricalGearSetISO10300MethodB1(
    _484.VirtualCylindricalGearSetISO10300MethodB1
):
    """HypoidVirtualCylindricalGearSetISO10300MethodB1

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HYPOID_VIRTUAL_CYLINDRICAL_GEAR_SET_ISO10300_METHOD_B1

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_HypoidVirtualCylindricalGearSetISO10300MethodB1":
        """Cast to another type.

        Returns:
            _Cast_HypoidVirtualCylindricalGearSetISO10300MethodB1
        """
        return _Cast_HypoidVirtualCylindricalGearSetISO10300MethodB1(self)
