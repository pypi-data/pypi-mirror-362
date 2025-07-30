"""DesignStateOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

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
from mastapy._private.system_model.analyses_and_results.load_case_groups import _5953
from mastapy._private.utility_gui import _2050

_DESIGN_STATE_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.DutyCycleDefinition",
    "DesignStateOptions",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model import _2418

    Self = TypeVar("Self", bound="DesignStateOptions")
    CastSelf = TypeVar("CastSelf", bound="DesignStateOptions._Cast_DesignStateOptions")


__docformat__ = "restructuredtext en"
__all__ = ("DesignStateOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DesignStateOptions:
    """Special nested class for casting DesignStateOptions to subclasses."""

    __parent__: "DesignStateOptions"

    @property
    def column_input_options(self: "CastSelf") -> "_2050.ColumnInputOptions":
        return self.__parent__._cast(_2050.ColumnInputOptions)

    @property
    def design_state_options(self: "CastSelf") -> "DesignStateOptions":
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
class DesignStateOptions(_2050.ColumnInputOptions):
    """DesignStateOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DESIGN_STATE_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def create_new_design_state(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "CreateNewDesignState")

        if temp is None:
            return False

        return temp

    @create_new_design_state.setter
    @exception_bridge
    @enforce_parameter_types
    def create_new_design_state(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CreateNewDesignState",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def design_state(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_DesignState":
        """ListWithSelectedItem[mastapy.system_model.analyses_and_results.load_case_groups.DesignState]"""
        temp = pythonnet_property_get(self.wrapped, "DesignState")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_DesignState",
        )(temp)

    @design_state.setter
    @exception_bridge
    @enforce_parameter_types
    def design_state(self: "Self", value: "_5953.DesignState") -> None:
        generic_type = (
            list_with_selected_item.ListWithSelectedItem_DesignState.implicit_type()
        )
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "DesignState", value)

    @property
    @exception_bridge
    def design_state_destinations(
        self: "Self",
    ) -> "List[_2418.DutyCycleImporterDesignEntityMatch[_5953.DesignState]]":
        """List[mastapy.system_model.DutyCycleImporterDesignEntityMatch[mastapy.system_model.analyses_and_results.load_case_groups.DesignState]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DesignStateDestinations")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_DesignStateOptions":
        """Cast to another type.

        Returns:
            _Cast_DesignStateOptions
        """
        return _Cast_DesignStateOptions(self)
