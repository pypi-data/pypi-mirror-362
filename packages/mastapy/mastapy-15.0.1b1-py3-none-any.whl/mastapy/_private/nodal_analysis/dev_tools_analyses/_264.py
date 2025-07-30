"""ElementEdgeGroup"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.fe_tools.vis_tools_global import _1353
from mastapy._private.nodal_analysis.dev_tools_analyses import _267

_ELEMENT_EDGE_GROUP = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses", "ElementEdgeGroup"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ElementEdgeGroup")
    CastSelf = TypeVar("CastSelf", bound="ElementEdgeGroup._Cast_ElementEdgeGroup")


__docformat__ = "restructuredtext en"
__all__ = ("ElementEdgeGroup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElementEdgeGroup:
    """Special nested class for casting ElementEdgeGroup to subclasses."""

    __parent__: "ElementEdgeGroup"

    @property
    def fe_entity_group(self: "CastSelf") -> "_267.FEEntityGroup":
        return self.__parent__._cast(_267.FEEntityGroup)

    @property
    def element_edge_group(self: "CastSelf") -> "ElementEdgeGroup":
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
class ElementEdgeGroup(_267.FEEntityGroup[_1353.ElementEdge]):
    """ElementEdgeGroup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELEMENT_EDGE_GROUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ElementEdgeGroup":
        """Cast to another type.

        Returns:
            _Cast_ElementEdgeGroup
        """
        return _Cast_ElementEdgeGroup(self)
