"""NodeInformation"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_NODE_INFORMATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Reporting",
    "NodeInformation",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis import _78

    Self = TypeVar("Self", bound="NodeInformation")
    CastSelf = TypeVar("CastSelf", bound="NodeInformation._Cast_NodeInformation")


__docformat__ = "restructuredtext en"
__all__ = ("NodeInformation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NodeInformation:
    """Special nested class for casting NodeInformation to subclasses."""

    __parent__: "NodeInformation"

    @property
    def node_information(self: "CastSelf") -> "NodeInformation":
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
class NodeInformation(_0.APIBase):
    """NodeInformation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NODE_INFORMATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def node_id(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NodeID")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def parts_using_node(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PartsUsingNode")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def node_info(self: "Self") -> "_78.LocalNodeInfo":
        """mastapy.nodal_analysis.LocalNodeInfo

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NodeInfo")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_NodeInformation":
        """Cast to another type.

        Returns:
            _Cast_NodeInformation
        """
        return _Cast_NodeInformation(self)
