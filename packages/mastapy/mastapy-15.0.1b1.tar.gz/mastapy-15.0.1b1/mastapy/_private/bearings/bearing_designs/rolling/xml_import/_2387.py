"""AbstractXmlVariableAssignment"""

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

_ABSTRACT_XML_VARIABLE_ASSIGNMENT = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling.XmlImport",
    "AbstractXmlVariableAssignment",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_designs.rolling.xml_import import _2391

    Self = TypeVar("Self", bound="AbstractXmlVariableAssignment")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractXmlVariableAssignment._Cast_AbstractXmlVariableAssignment",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractXmlVariableAssignment",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractXmlVariableAssignment:
    """Special nested class for casting AbstractXmlVariableAssignment to subclasses."""

    __parent__: "AbstractXmlVariableAssignment"

    @property
    def xml_variable_assignment(self: "CastSelf") -> "_2391.XMLVariableAssignment":
        from mastapy._private.bearings.bearing_designs.rolling.xml_import import _2391

        return self.__parent__._cast(_2391.XMLVariableAssignment)

    @property
    def abstract_xml_variable_assignment(
        self: "CastSelf",
    ) -> "AbstractXmlVariableAssignment":
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
class AbstractXmlVariableAssignment(_0.APIBase):
    """AbstractXmlVariableAssignment

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_XML_VARIABLE_ASSIGNMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def definitions(self: "Self") -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "Definitions")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @definitions.setter
    @exception_bridge
    @enforce_parameter_types
    def definitions(self: "Self", value: "str") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "Definitions", value)

    @property
    @exception_bridge
    def description(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Description")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def variable_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VariableName")

        if temp is None:
            return ""

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractXmlVariableAssignment":
        """Cast to another type.

        Returns:
            _Cast_AbstractXmlVariableAssignment
        """
        return _Cast_AbstractXmlVariableAssignment(self)
