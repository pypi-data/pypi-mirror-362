"""ShaftProfileFromImport"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private.nodal_analysis.geometry_modeller_link import _243

_SHAFT_PROFILE_FROM_IMPORT = python_net_import(
    "SMT.MastaAPI.Shafts", "ShaftProfileFromImport"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.shafts import _32

    Self = TypeVar("Self", bound="ShaftProfileFromImport")
    CastSelf = TypeVar(
        "CastSelf", bound="ShaftProfileFromImport._Cast_ShaftProfileFromImport"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftProfileFromImport",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftProfileFromImport:
    """Special nested class for casting ShaftProfileFromImport to subclasses."""

    __parent__: "ShaftProfileFromImport"

    @property
    def profile_from_import(self: "CastSelf") -> "_243.ProfileFromImport":
        return self.__parent__._cast(_243.ProfileFromImport)

    @property
    def shaft_profile_from_import(self: "CastSelf") -> "ShaftProfileFromImport":
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
class ShaftProfileFromImport(_243.ProfileFromImport):
    """ShaftProfileFromImport

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_PROFILE_FROM_IMPORT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def inner_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Length")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def outer_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def moniker(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Moniker")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def profile_loops(self: "Self") -> "List[_32.ShaftProfileLoop]":
        """List[mastapy.shafts.ShaftProfileLoop]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProfileLoops")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def window_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WindowName")

        if temp is None:
            return ""

        return temp

    @exception_bridge
    def update_profile_for_masta(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "UpdateProfileForMASTA")

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftProfileFromImport":
        """Cast to another type.

        Returns:
            _Cast_ShaftProfileFromImport
        """
        return _Cast_ShaftProfileFromImport(self)
