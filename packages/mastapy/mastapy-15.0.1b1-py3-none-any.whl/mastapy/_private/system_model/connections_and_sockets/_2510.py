"""PlanetarySocketBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.connections_and_sockets import _2497

_PLANETARY_SOCKET_BASE = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "PlanetarySocketBase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears import _430
    from mastapy._private.system_model.connections_and_sockets import _2509, _2517
    from mastapy._private.system_model.connections_and_sockets.cycloidal import _2560

    Self = TypeVar("Self", bound="PlanetarySocketBase")
    CastSelf = TypeVar(
        "CastSelf", bound="PlanetarySocketBase._Cast_PlanetarySocketBase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlanetarySocketBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlanetarySocketBase:
    """Special nested class for casting PlanetarySocketBase to subclasses."""

    __parent__: "PlanetarySocketBase"

    @property
    def cylindrical_socket(self: "CastSelf") -> "_2497.CylindricalSocket":
        return self.__parent__._cast(_2497.CylindricalSocket)

    @property
    def socket(self: "CastSelf") -> "_2517.Socket":
        from mastapy._private.system_model.connections_and_sockets import _2517

        return self.__parent__._cast(_2517.Socket)

    @property
    def planetary_socket(self: "CastSelf") -> "_2509.PlanetarySocket":
        from mastapy._private.system_model.connections_and_sockets import _2509

        return self.__parent__._cast(_2509.PlanetarySocket)

    @property
    def cycloidal_disc_planetary_bearing_socket(
        self: "CastSelf",
    ) -> "_2560.CycloidalDiscPlanetaryBearingSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2560,
        )

        return self.__parent__._cast(_2560.CycloidalDiscPlanetaryBearingSocket)

    @property
    def planetary_socket_base(self: "CastSelf") -> "PlanetarySocketBase":
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
class PlanetarySocketBase(_2497.CylindricalSocket):
    """PlanetarySocketBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLANETARY_SOCKET_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def draw_on_lower_half_of_2d(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "DrawOnLowerHalfOf2D")

        if temp is None:
            return False

        return temp

    @draw_on_lower_half_of_2d.setter
    @exception_bridge
    @enforce_parameter_types
    def draw_on_lower_half_of_2d(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DrawOnLowerHalfOf2D",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def draw_on_upper_half_of_2d(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "DrawOnUpperHalfOf2D")

        if temp is None:
            return False

        return temp

    @draw_on_upper_half_of_2d.setter
    @exception_bridge
    @enforce_parameter_types
    def draw_on_upper_half_of_2d(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DrawOnUpperHalfOf2D",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def editable_name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "EditableName")

        if temp is None:
            return ""

        return temp

    @editable_name.setter
    @exception_bridge
    @enforce_parameter_types
    def editable_name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "EditableName", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def planetary_load_sharing_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PlanetaryLoadSharingFactor")

        if temp is None:
            return 0.0

        return temp

    @planetary_load_sharing_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def planetary_load_sharing_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PlanetaryLoadSharingFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Width")

        if temp is None:
            return 0.0

        return temp

    @width.setter
    @exception_bridge
    @enforce_parameter_types
    def width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Width", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def planetary_details(self: "Self") -> "_430.PlanetaryDetail":
        """mastapy.gears.PlanetaryDetail

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PlanetaryDetails")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_PlanetarySocketBase":
        """Cast to another type.

        Returns:
            _Cast_PlanetarySocketBase
        """
        return _Cast_PlanetarySocketBase(self)
