"""NodeScalarState"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.states import _129

_NODE_SCALAR_STATE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.States", "NodeScalarState"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.states import _127

    Self = TypeVar("Self", bound="NodeScalarState")
    CastSelf = TypeVar("CastSelf", bound="NodeScalarState._Cast_NodeScalarState")


__docformat__ = "restructuredtext en"
__all__ = ("NodeScalarState",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NodeScalarState:
    """Special nested class for casting NodeScalarState to subclasses."""

    __parent__: "NodeScalarState"

    @property
    def node_vector_state(self: "CastSelf") -> "_129.NodeVectorState":
        return self.__parent__._cast(_129.NodeVectorState)

    @property
    def entity_vector_state(self: "CastSelf") -> "_127.EntityVectorState":
        from mastapy._private.nodal_analysis.states import _127

        return self.__parent__._cast(_127.EntityVectorState)

    @property
    def node_scalar_state(self: "CastSelf") -> "NodeScalarState":
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
class NodeScalarState(_129.NodeVectorState):
    """NodeScalarState

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NODE_SCALAR_STATE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_NodeScalarState":
        """Cast to another type.

        Returns:
            _Cast_NodeScalarState
        """
        return _Cast_NodeScalarState(self)
