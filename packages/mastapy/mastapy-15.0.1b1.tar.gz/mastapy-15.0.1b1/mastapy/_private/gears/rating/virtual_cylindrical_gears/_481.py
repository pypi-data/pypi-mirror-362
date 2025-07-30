"""VirtualCylindricalGearISO10300MethodB1"""

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

_VIRTUAL_CYLINDRICAL_GEAR_ISO10300_METHOD_B1 = python_net_import(
    "SMT.MastaAPI.Gears.Rating.VirtualCylindricalGears",
    "VirtualCylindricalGearISO10300MethodB1",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating.virtual_cylindrical_gears import _480

    Self = TypeVar("Self", bound="VirtualCylindricalGearISO10300MethodB1")
    CastSelf = TypeVar(
        "CastSelf",
        bound="VirtualCylindricalGearISO10300MethodB1._Cast_VirtualCylindricalGearISO10300MethodB1",
    )


__docformat__ = "restructuredtext en"
__all__ = ("VirtualCylindricalGearISO10300MethodB1",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_VirtualCylindricalGearISO10300MethodB1:
    """Special nested class for casting VirtualCylindricalGearISO10300MethodB1 to subclasses."""

    __parent__: "VirtualCylindricalGearISO10300MethodB1"

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
    def virtual_cylindrical_gear_iso10300_method_b1(
        self: "CastSelf",
    ) -> "VirtualCylindricalGearISO10300MethodB1":
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
class VirtualCylindricalGearISO10300MethodB1(_479.VirtualCylindricalGear):
    """VirtualCylindricalGearISO10300MethodB1

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _VIRTUAL_CYLINDRICAL_GEAR_ISO10300_METHOD_B1

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def base_diameter_of_virtual_cylindrical_gear_in_normal_section(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BaseDiameterOfVirtualCylindricalGearInNormalSection"
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
    def reference_diameter_in_normal_section(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReferenceDiameterInNormalSection")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def root_diameter_of_virtual_cylindrical_gear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RootDiameterOfVirtualCylindricalGear"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tip_diameter_of_virtual_cylindrical_gear_in_normal_section(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TipDiameterOfVirtualCylindricalGearInNormalSection"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transverse_module(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransverseModule")

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
    @exception_bridge
    def virtual_spur_gear_number_of_teeth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VirtualSpurGearNumberOfTeeth")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_VirtualCylindricalGearISO10300MethodB1":
        """Cast to another type.

        Returns:
            _Cast_VirtualCylindricalGearISO10300MethodB1
        """
        return _Cast_VirtualCylindricalGearISO10300MethodB1(self)
