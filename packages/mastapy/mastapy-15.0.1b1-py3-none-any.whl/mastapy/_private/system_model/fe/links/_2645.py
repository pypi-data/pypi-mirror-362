"""FELinkWithSelection"""

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

_FE_LINK_WITH_SELECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.FE.Links", "FELinkWithSelection"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.fe.links import _2643

    Self = TypeVar("Self", bound="FELinkWithSelection")
    CastSelf = TypeVar(
        "CastSelf", bound="FELinkWithSelection._Cast_FELinkWithSelection"
    )


__docformat__ = "restructuredtext en"
__all__ = ("FELinkWithSelection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FELinkWithSelection:
    """Special nested class for casting FELinkWithSelection to subclasses."""

    __parent__: "FELinkWithSelection"

    @property
    def fe_link_with_selection(self: "CastSelf") -> "FELinkWithSelection":
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
class FELinkWithSelection(_0.APIBase):
    """FELinkWithSelection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_LINK_WITH_SELECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def link(self: "Self") -> "_2643.FELink":
        """mastapy.system_model.fe.links.FELink

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Link")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    def add_selected_nodes(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddSelectedNodes")

    @exception_bridge
    def delete_all_nodes(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "DeleteAllNodes")

    @exception_bridge
    def select_component(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SelectComponent")

    @property
    def cast_to(self: "Self") -> "_Cast_FELinkWithSelection":
        """Cast to another type.

        Returns:
            _Cast_FELinkWithSelection
        """
        return _Cast_FELinkWithSelection(self)
