"""FEEntityGroupWithSelection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

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

_FE_ENTITY_GROUP_WITH_SELECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "FEEntityGroupWithSelection"
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.system_model.fe import _2597, _2626

    Self = TypeVar("Self", bound="FEEntityGroupWithSelection")
    CastSelf = TypeVar(
        "CastSelf", bound="FEEntityGroupWithSelection._Cast_FEEntityGroupWithSelection"
    )

TGroup = TypeVar("TGroup")
TGroupContents = TypeVar("TGroupContents")

__docformat__ = "restructuredtext en"
__all__ = ("FEEntityGroupWithSelection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FEEntityGroupWithSelection:
    """Special nested class for casting FEEntityGroupWithSelection to subclasses."""

    __parent__: "FEEntityGroupWithSelection"

    @property
    def element_face_group_with_selection(
        self: "CastSelf",
    ) -> "_2597.ElementFaceGroupWithSelection":
        from mastapy._private.system_model.fe import _2597

        return self.__parent__._cast(_2597.ElementFaceGroupWithSelection)

    @property
    def node_group_with_selection(self: "CastSelf") -> "_2626.NodeGroupWithSelection":
        from mastapy._private.system_model.fe import _2626

        return self.__parent__._cast(_2626.NodeGroupWithSelection)

    @property
    def fe_entity_group_with_selection(
        self: "CastSelf",
    ) -> "FEEntityGroupWithSelection":
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
class FEEntityGroupWithSelection(_0.APIBase, Generic[TGroup, TGroupContents]):
    """FEEntityGroupWithSelection

    This is a mastapy class.

    Generic Types:
        TGroup
        TGroupContents
    """

    TYPE: ClassVar["Type"] = _FE_ENTITY_GROUP_WITH_SELECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def group(self: "Self") -> "TGroup":
        """TGroup

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Group")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    def add_selection_to_group(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddSelectionToGroup")

    @exception_bridge
    def delete_group(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "DeleteGroup")

    @exception_bridge
    def select_items(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SelectItems")

    @property
    def cast_to(self: "Self") -> "_Cast_FEEntityGroupWithSelection":
        """Cast to another type.

        Returns:
            _Cast_FEEntityGroupWithSelection
        """
        return _Cast_FEEntityGroupWithSelection(self)
