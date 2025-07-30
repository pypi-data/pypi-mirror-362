"""NodeGroup"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.dev_tools_analyses import _268

_NODE_GROUP = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses", "NodeGroup"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.component_mode_synthesis import _313
    from mastapy._private.nodal_analysis.dev_tools_analyses import _267

    Self = TypeVar("Self", bound="NodeGroup")
    CastSelf = TypeVar("CastSelf", bound="NodeGroup._Cast_NodeGroup")


__docformat__ = "restructuredtext en"
__all__ = ("NodeGroup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NodeGroup:
    """Special nested class for casting NodeGroup to subclasses."""

    __parent__: "NodeGroup"

    @property
    def fe_entity_group_integer(self: "CastSelf") -> "_268.FEEntityGroupInteger":
        return self.__parent__._cast(_268.FEEntityGroupInteger)

    @property
    def fe_entity_group(self: "CastSelf") -> "_267.FEEntityGroup":
        from mastapy._private.nodal_analysis.dev_tools_analyses import _267

        return self.__parent__._cast(_267.FEEntityGroup)

    @property
    def cms_node_group(self: "CastSelf") -> "_313.CMSNodeGroup":
        from mastapy._private.nodal_analysis.component_mode_synthesis import _313

        return self.__parent__._cast(_313.CMSNodeGroup)

    @property
    def node_group(self: "CastSelf") -> "NodeGroup":
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
class NodeGroup(_268.FEEntityGroupInteger):
    """NodeGroup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NODE_GROUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_NodeGroup":
        """Cast to another type.

        Returns:
            _Cast_NodeGroup
        """
        return _Cast_NodeGroup(self)
