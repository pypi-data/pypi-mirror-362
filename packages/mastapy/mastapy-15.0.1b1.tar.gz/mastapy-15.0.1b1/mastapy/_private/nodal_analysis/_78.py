"""LocalNodeInfo"""

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

_LOCAL_NODE_INFO = python_net_import("SMT.MastaAPI.NodalAnalysis", "LocalNodeInfo")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="LocalNodeInfo")
    CastSelf = TypeVar("CastSelf", bound="LocalNodeInfo._Cast_LocalNodeInfo")


__docformat__ = "restructuredtext en"
__all__ = ("LocalNodeInfo",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LocalNodeInfo:
    """Special nested class for casting LocalNodeInfo to subclasses."""

    __parent__: "LocalNodeInfo"

    @property
    def local_node_info(self: "CastSelf") -> "LocalNodeInfo":
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
class LocalNodeInfo(_0.APIBase):
    """LocalNodeInfo

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOCAL_NODE_INFO

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def first_degrees_of_freedom_index(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FirstDegreesOfFreedomIndex")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_degrees_of_freedom(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfDegreesOfFreedom")

        if temp is None:
            return 0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_LocalNodeInfo":
        """Cast to another type.

        Returns:
            _Cast_LocalNodeInfo
        """
        return _Cast_LocalNodeInfo(self)
