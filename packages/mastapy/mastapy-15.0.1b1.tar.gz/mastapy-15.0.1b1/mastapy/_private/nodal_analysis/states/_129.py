"""NodeVectorState"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.states import _127

_NODE_VECTOR_STATE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.States", "NodeVectorState"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.states import _128

    Self = TypeVar("Self", bound="NodeVectorState")
    CastSelf = TypeVar("CastSelf", bound="NodeVectorState._Cast_NodeVectorState")


__docformat__ = "restructuredtext en"
__all__ = ("NodeVectorState",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NodeVectorState:
    """Special nested class for casting NodeVectorState to subclasses."""

    __parent__: "NodeVectorState"

    @property
    def entity_vector_state(self: "CastSelf") -> "_127.EntityVectorState":
        return self.__parent__._cast(_127.EntityVectorState)

    @property
    def node_scalar_state(self: "CastSelf") -> "_128.NodeScalarState":
        from mastapy._private.nodal_analysis.states import _128

        return self.__parent__._cast(_128.NodeScalarState)

    @property
    def node_vector_state(self: "CastSelf") -> "NodeVectorState":
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
class NodeVectorState(_127.EntityVectorState):
    """NodeVectorState

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NODE_VECTOR_STATE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_NodeVectorState":
        """Cast to another type.

        Returns:
            _Cast_NodeVectorState
        """
        return _Cast_NodeVectorState(self)
