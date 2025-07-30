"""Implementations of 'ListWithSelectedItem' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, mixins
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.ltca.cylindrical import _960

_ARRAY = python_net_import("System", "Array")
_LIST_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Property", "ListWithSelectedItem"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar(
        "Self", bound="ListWithSelectedItem_CylindricalGearMeshLoadDistributionAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ListWithSelectedItem_CylindricalGearMeshLoadDistributionAnalysis",)


class ListWithSelectedItem_CylindricalGearMeshLoadDistributionAnalysis(
    _960.CylindricalGearMeshLoadDistributionAnalysis, mixins.ListWithSelectedItemMixin
):
    """ListWithSelectedItem_CylindricalGearMeshLoadDistributionAnalysis

    A specific implementation of 'ListWithSelectedItem' for 'CylindricalGearMeshLoadDistributionAnalysis' types.
    """

    __qualname__ = "CylindricalGearMeshLoadDistributionAnalysis"

    def __init__(self: "Self", instance_to_wrap: "Any") -> None:
        super().__init__(instance_to_wrap.SelectedValue)
        object.__setattr__(self, "enclosing", instance_to_wrap)

    @classmethod
    def wrapper_type(
        cls: "Type[ListWithSelectedItem_CylindricalGearMeshLoadDistributionAnalysis]",
    ) -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(
        cls: "Type[ListWithSelectedItem_CylindricalGearMeshLoadDistributionAnalysis]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _960.CylindricalGearMeshLoadDistributionAnalysis.TYPE

    @property
    @exception_bridge
    def selected_value(
        self: "Self",
    ) -> "_960.CylindricalGearMeshLoadDistributionAnalysis":
        """mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadDistributionAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.enclosing, "SelectedValue")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def available_values(
        self: "Self",
    ) -> "List[_960.CylindricalGearMeshLoadDistributionAnalysis]":
        """List[mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadDistributionAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.enclosing, "AvailableValues")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def invalid_properties(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.enclosing, "InvalidProperties")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def read_only_properties(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.enclosing, "ReadOnlyProperties")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def all_properties_are_read_only(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.enclosing, "AllPropertiesAreReadOnly")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def all_properties_are_invalid(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.enclosing, "AllPropertiesAreInvalid")

        if temp is None:
            return False

        return temp
