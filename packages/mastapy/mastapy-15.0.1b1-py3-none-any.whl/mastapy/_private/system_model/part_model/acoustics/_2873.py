"""FEPartInputSurfaceOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import list_with_selected_item
from mastapy._private._internal.list_with_selected_item import (
    promote_to_list_with_selected_item,
)
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.nodal_analysis.component_mode_synthesis import _310
from mastapy._private.system_model.fe import _2605

_FE_PART_INPUT_SURFACE_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Acoustics", "FEPartInputSurfaceOptions"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FEPartInputSurfaceOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="FEPartInputSurfaceOptions._Cast_FEPartInputSurfaceOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("FEPartInputSurfaceOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FEPartInputSurfaceOptions:
    """Special nested class for casting FEPartInputSurfaceOptions to subclasses."""

    __parent__: "FEPartInputSurfaceOptions"

    @property
    def fe_part_input_surface_options(self: "CastSelf") -> "FEPartInputSurfaceOptions":
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
class FEPartInputSurfaceOptions(_0.APIBase):
    """FEPartInputSurfaceOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_PART_INPUT_SURFACE_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def fe_substructure(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_FESubstructure":
        """ListWithSelectedItem[mastapy.system_model.fe.FESubstructure]"""
        temp = pythonnet_property_get(self.wrapped, "FESubstructure")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_FESubstructure",
        )(temp)

    @fe_substructure.setter
    @exception_bridge
    @enforce_parameter_types
    def fe_substructure(self: "Self", value: "_2605.FESubstructure") -> None:
        generic_type = (
            list_with_selected_item.ListWithSelectedItem_FESubstructure.implicit_type()
        )
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "FESubstructure", value)

    @property
    @exception_bridge
    def is_included(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsIncluded")

        if temp is None:
            return False

        return temp

    @is_included.setter
    @exception_bridge
    @enforce_parameter_types
    def is_included(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "IsIncluded", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def surfaces(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_CMSElementFaceGroup":
        """ListWithSelectedItem[mastapy.nodal_analysis.component_mode_synthesis.CMSElementFaceGroup]"""
        temp = pythonnet_property_get(self.wrapped, "Surfaces")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_CMSElementFaceGroup",
        )(temp)

    @surfaces.setter
    @exception_bridge
    @enforce_parameter_types
    def surfaces(self: "Self", value: "_310.CMSElementFaceGroup") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_CMSElementFaceGroup.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "Surfaces", value)

    @property
    def cast_to(self: "Self") -> "_Cast_FEPartInputSurfaceOptions":
        """Cast to another type.

        Returns:
            _Cast_FEPartInputSurfaceOptions
        """
        return _Cast_FEPartInputSurfaceOptions(self)
