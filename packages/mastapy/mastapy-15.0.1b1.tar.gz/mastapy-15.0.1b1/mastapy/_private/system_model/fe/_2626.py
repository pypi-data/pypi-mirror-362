"""NodeGroupWithSelection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.component_mode_synthesis import _313
from mastapy._private.system_model.fe import _2599

_NODE_GROUP_WITH_SELECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "NodeGroupWithSelection"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="NodeGroupWithSelection")
    CastSelf = TypeVar(
        "CastSelf", bound="NodeGroupWithSelection._Cast_NodeGroupWithSelection"
    )


__docformat__ = "restructuredtext en"
__all__ = ("NodeGroupWithSelection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NodeGroupWithSelection:
    """Special nested class for casting NodeGroupWithSelection to subclasses."""

    __parent__: "NodeGroupWithSelection"

    @property
    def fe_entity_group_with_selection(
        self: "CastSelf",
    ) -> "_2599.FEEntityGroupWithSelection":
        return self.__parent__._cast(_2599.FEEntityGroupWithSelection)

    @property
    def node_group_with_selection(self: "CastSelf") -> "NodeGroupWithSelection":
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
class NodeGroupWithSelection(_2599.FEEntityGroupWithSelection[_313.CMSNodeGroup, int]):
    """NodeGroupWithSelection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NODE_GROUP_WITH_SELECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_NodeGroupWithSelection":
        """Cast to another type.

        Returns:
            _Cast_NodeGroupWithSelection
        """
        return _Cast_NodeGroupWithSelection(self)
