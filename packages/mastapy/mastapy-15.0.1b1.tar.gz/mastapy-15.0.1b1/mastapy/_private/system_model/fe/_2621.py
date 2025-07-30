"""IndependentMASTACreatedRigidlyConnectedNodeGroup"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.fe import _2619

_INDEPENDENT_MASTA_CREATED_RIGIDLY_CONNECTED_NODE_GROUP = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "IndependentMASTACreatedRigidlyConnectedNodeGroup"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="IndependentMASTACreatedRigidlyConnectedNodeGroup")
    CastSelf = TypeVar(
        "CastSelf",
        bound="IndependentMASTACreatedRigidlyConnectedNodeGroup._Cast_IndependentMASTACreatedRigidlyConnectedNodeGroup",
    )


__docformat__ = "restructuredtext en"
__all__ = ("IndependentMASTACreatedRigidlyConnectedNodeGroup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_IndependentMASTACreatedRigidlyConnectedNodeGroup:
    """Special nested class for casting IndependentMASTACreatedRigidlyConnectedNodeGroup to subclasses."""

    __parent__: "IndependentMASTACreatedRigidlyConnectedNodeGroup"

    @property
    def independent_masta_created_constrained_nodes(
        self: "CastSelf",
    ) -> "_2619.IndependentMASTACreatedConstrainedNodes":
        return self.__parent__._cast(_2619.IndependentMASTACreatedConstrainedNodes)

    @property
    def independent_masta_created_rigidly_connected_node_group(
        self: "CastSelf",
    ) -> "IndependentMASTACreatedRigidlyConnectedNodeGroup":
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
class IndependentMASTACreatedRigidlyConnectedNodeGroup(
    _2619.IndependentMASTACreatedConstrainedNodes
):
    """IndependentMASTACreatedRigidlyConnectedNodeGroup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INDEPENDENT_MASTA_CREATED_RIGIDLY_CONNECTED_NODE_GROUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_IndependentMASTACreatedRigidlyConnectedNodeGroup":
        """Cast to another type.

        Returns:
            _Cast_IndependentMASTACreatedRigidlyConnectedNodeGroup
        """
        return _Cast_IndependentMASTACreatedRigidlyConnectedNodeGroup(self)
