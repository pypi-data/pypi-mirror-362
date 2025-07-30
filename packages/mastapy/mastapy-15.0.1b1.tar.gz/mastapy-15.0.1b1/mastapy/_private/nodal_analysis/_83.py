"""NodalMatrixEditorWrapper"""

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
from mastapy._private.utility.units_and_measurements import _1802

_NODAL_MATRIX_EDITOR_WRAPPER = python_net_import(
    "SMT.MastaAPI.NodalAnalysis", "NodalMatrixEditorWrapper"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.nodal_analysis import _84, _85

    Self = TypeVar("Self", bound="NodalMatrixEditorWrapper")
    CastSelf = TypeVar(
        "CastSelf", bound="NodalMatrixEditorWrapper._Cast_NodalMatrixEditorWrapper"
    )


__docformat__ = "restructuredtext en"
__all__ = ("NodalMatrixEditorWrapper",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NodalMatrixEditorWrapper:
    """Special nested class for casting NodalMatrixEditorWrapper to subclasses."""

    __parent__: "NodalMatrixEditorWrapper"

    @property
    def nodal_matrix_editor_wrapper_concept_coupling_stiffness(
        self: "CastSelf",
    ) -> "_85.NodalMatrixEditorWrapperConceptCouplingStiffness":
        from mastapy._private.nodal_analysis import _85

        return self.__parent__._cast(
            _85.NodalMatrixEditorWrapperConceptCouplingStiffness
        )

    @property
    def nodal_matrix_editor_wrapper(self: "CastSelf") -> "NodalMatrixEditorWrapper":
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
class NodalMatrixEditorWrapper(_0.APIBase):
    """NodalMatrixEditorWrapper

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NODAL_MATRIX_EDITOR_WRAPPER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def distance_units(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_Unit":
        """ListWithSelectedItem[mastapy.utility.units_and_measurements.Unit]"""
        temp = pythonnet_property_get(self.wrapped, "DistanceUnits")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_Unit",
        )(temp)

    @distance_units.setter
    @exception_bridge
    @enforce_parameter_types
    def distance_units(self: "Self", value: "_1802.Unit") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "DistanceUnits", value)

    @property
    @exception_bridge
    def force_units(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_Unit":
        """ListWithSelectedItem[mastapy.utility.units_and_measurements.Unit]"""
        temp = pythonnet_property_get(self.wrapped, "ForceUnits")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_Unit",
        )(temp)

    @force_units.setter
    @exception_bridge
    @enforce_parameter_types
    def force_units(self: "Self", value: "_1802.Unit") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "ForceUnits", value)

    @property
    @exception_bridge
    def columns(self: "Self") -> "List[_84.NodalMatrixEditorWrapperColumn]":
        """List[mastapy.nodal_analysis.NodalMatrixEditorWrapperColumn]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Columns")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_NodalMatrixEditorWrapper":
        """Cast to another type.

        Returns:
            _Cast_NodalMatrixEditorWrapper
        """
        return _Cast_NodalMatrixEditorWrapper(self)
