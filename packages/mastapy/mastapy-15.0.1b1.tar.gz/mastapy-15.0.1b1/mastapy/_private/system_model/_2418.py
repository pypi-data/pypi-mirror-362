"""DutyCycleImporterDesignEntityMatch"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

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

_DUTY_CYCLE_IMPORTER_DESIGN_ENTITY_MATCH = python_net_import(
    "SMT.MastaAPI.SystemModel", "DutyCycleImporterDesignEntityMatch"
)

if TYPE_CHECKING:
    from typing import Any, Type

    Self = TypeVar("Self", bound="DutyCycleImporterDesignEntityMatch")
    CastSelf = TypeVar(
        "CastSelf",
        bound="DutyCycleImporterDesignEntityMatch._Cast_DutyCycleImporterDesignEntityMatch",
    )

T = TypeVar("T")

__docformat__ = "restructuredtext en"
__all__ = ("DutyCycleImporterDesignEntityMatch",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DutyCycleImporterDesignEntityMatch:
    """Special nested class for casting DutyCycleImporterDesignEntityMatch to subclasses."""

    __parent__: "DutyCycleImporterDesignEntityMatch"

    @property
    def duty_cycle_importer_design_entity_match(
        self: "CastSelf",
    ) -> "DutyCycleImporterDesignEntityMatch":
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
class DutyCycleImporterDesignEntityMatch(_0.APIBase, Generic[T]):
    """DutyCycleImporterDesignEntityMatch

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _DUTY_CYCLE_IMPORTER_DESIGN_ENTITY_MATCH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def destination(self: "Self") -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "Destination")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @destination.setter
    @exception_bridge
    @enforce_parameter_types
    def destination(self: "Self", value: "str") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "Destination", value)

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
    def cast_to(self: "Self") -> "_Cast_DutyCycleImporterDesignEntityMatch":
        """Cast to another type.

        Returns:
            _Cast_DutyCycleImporterDesignEntityMatch
        """
        return _Cast_DutyCycleImporterDesignEntityMatch(self)
