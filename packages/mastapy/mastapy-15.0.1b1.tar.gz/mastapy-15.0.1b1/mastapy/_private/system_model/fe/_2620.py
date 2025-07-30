"""IndependentMASTACreatedConstrainedNodesWithSelectionComponents"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)

_INDEPENDENT_MASTA_CREATED_CONSTRAINED_NODES_WITH_SELECTION_COMPONENTS = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.FE",
        "IndependentMASTACreatedConstrainedNodesWithSelectionComponents",
    )
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.fe import _2619

    Self = TypeVar(
        "Self", bound="IndependentMASTACreatedConstrainedNodesWithSelectionComponents"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="IndependentMASTACreatedConstrainedNodesWithSelectionComponents._Cast_IndependentMASTACreatedConstrainedNodesWithSelectionComponents",
    )


__docformat__ = "restructuredtext en"
__all__ = ("IndependentMASTACreatedConstrainedNodesWithSelectionComponents",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_IndependentMASTACreatedConstrainedNodesWithSelectionComponents:
    """Special nested class for casting IndependentMASTACreatedConstrainedNodesWithSelectionComponents to subclasses."""

    __parent__: "IndependentMASTACreatedConstrainedNodesWithSelectionComponents"

    @property
    def independent_masta_created_constrained_nodes_with_selection_components(
        self: "CastSelf",
    ) -> "IndependentMASTACreatedConstrainedNodesWithSelectionComponents":
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
class IndependentMASTACreatedConstrainedNodesWithSelectionComponents(_0.APIBase):
    """IndependentMASTACreatedConstrainedNodesWithSelectionComponents

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _INDEPENDENT_MASTA_CREATED_CONSTRAINED_NODES_WITH_SELECTION_COMPONENTS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def node(self: "Self") -> "_2619.IndependentMASTACreatedConstrainedNodes":
        """mastapy.system_model.fe.IndependentMASTACreatedConstrainedNodes

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Node")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    def select(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Select")

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_IndependentMASTACreatedConstrainedNodesWithSelectionComponents":
        """Cast to another type.

        Returns:
            _Cast_IndependentMASTACreatedConstrainedNodesWithSelectionComponents
        """
        return _Cast_IndependentMASTACreatedConstrainedNodesWithSelectionComponents(
            self
        )
