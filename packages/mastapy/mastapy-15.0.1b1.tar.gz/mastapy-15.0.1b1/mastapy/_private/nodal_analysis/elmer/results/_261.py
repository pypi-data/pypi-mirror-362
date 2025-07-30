"""Data3D"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.nodal_analysis.elmer.results import _259

_DATA_3D = python_net_import("SMT.MastaAPI.NodalAnalysis.Elmer.Results", "Data3D")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="Data3D")
    CastSelf = TypeVar("CastSelf", bound="Data3D._Cast_Data3D")


__docformat__ = "restructuredtext en"
__all__ = ("Data3D",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Data3D:
    """Special nested class for casting Data3D to subclasses."""

    __parent__: "Data3D"

    @property
    def data(self: "CastSelf") -> "_259.Data":
        return self.__parent__._cast(_259.Data)

    @property
    def data_3d(self: "CastSelf") -> "Data3D":
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
class Data3D(_259.Data):
    """Data3D

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DATA_3D

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def x_data(self: "Self") -> "List[float]":
        """List[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "XData")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, float)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def y_data(self: "Self") -> "List[float]":
        """List[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "YData")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, float)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def z_data(self: "Self") -> "List[float]":
        """List[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ZData")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, float)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_Data3D":
        """Cast to another type.

        Returns:
            _Cast_Data3D
        """
        return _Cast_Data3D(self)
