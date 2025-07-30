"""PlanetarySocketManufactureError"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_PLANETARY_SOCKET_MANUFACTURE_ERROR = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "PlanetarySocketManufactureError",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.static_loads import _7807

    Self = TypeVar("Self", bound="PlanetarySocketManufactureError")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PlanetarySocketManufactureError._Cast_PlanetarySocketManufactureError",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlanetarySocketManufactureError",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlanetarySocketManufactureError:
    """Special nested class for casting PlanetarySocketManufactureError to subclasses."""

    __parent__: "PlanetarySocketManufactureError"

    @property
    def planetary_socket_manufacture_error(
        self: "CastSelf",
    ) -> "PlanetarySocketManufactureError":
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
class PlanetarySocketManufactureError(_0.APIBase):
    """PlanetarySocketManufactureError

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLANETARY_SOCKET_MANUFACTURE_ERROR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def socket_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SocketName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def planet_manufacture_errors(self: "Self") -> "List[_7807.PlanetManufactureError]":
        """List[mastapy.system_model.analyses_and_results.static_loads.PlanetManufactureError]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PlanetManufactureErrors")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_PlanetarySocketManufactureError":
        """Cast to another type.

        Returns:
            _Cast_PlanetarySocketManufactureError
        """
        return _Cast_PlanetarySocketManufactureError(self)
