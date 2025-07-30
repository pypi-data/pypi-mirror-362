"""ElementFaceGroupWithSelection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.fe_tools.vis_tools_global import _1354
from mastapy._private.nodal_analysis.component_mode_synthesis import _310
from mastapy._private.system_model.fe import _2599

_ELEMENT_FACE_GROUP_WITH_SELECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "ElementFaceGroupWithSelection"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ElementFaceGroupWithSelection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElementFaceGroupWithSelection._Cast_ElementFaceGroupWithSelection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElementFaceGroupWithSelection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElementFaceGroupWithSelection:
    """Special nested class for casting ElementFaceGroupWithSelection to subclasses."""

    __parent__: "ElementFaceGroupWithSelection"

    @property
    def fe_entity_group_with_selection(
        self: "CastSelf",
    ) -> "_2599.FEEntityGroupWithSelection":
        return self.__parent__._cast(_2599.FEEntityGroupWithSelection)

    @property
    def element_face_group_with_selection(
        self: "CastSelf",
    ) -> "ElementFaceGroupWithSelection":
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
class ElementFaceGroupWithSelection(
    _2599.FEEntityGroupWithSelection[_310.CMSElementFaceGroup, _1354.ElementFace]
):
    """ElementFaceGroupWithSelection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELEMENT_FACE_GROUP_WITH_SELECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def is_default_surface_group(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsDefaultSurfaceGroup")

        if temp is None:
            return False

        return temp

    @is_default_surface_group.setter
    @exception_bridge
    @enforce_parameter_types
    def is_default_surface_group(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IsDefaultSurfaceGroup",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ElementFaceGroupWithSelection":
        """Cast to another type.

        Returns:
            _Cast_ElementFaceGroupWithSelection
        """
        return _Cast_ElementFaceGroupWithSelection(self)
