"""ActiveCylindricalGearSetDesignSelection"""

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
from mastapy._private.system_model.part_model.gears import _2748

_ACTIVE_CYLINDRICAL_GEAR_SET_DESIGN_SELECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears",
    "ActiveCylindricalGearSetDesignSelection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.part_model.configurations import _2865

    Self = TypeVar("Self", bound="ActiveCylindricalGearSetDesignSelection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ActiveCylindricalGearSetDesignSelection._Cast_ActiveCylindricalGearSetDesignSelection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ActiveCylindricalGearSetDesignSelection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ActiveCylindricalGearSetDesignSelection:
    """Special nested class for casting ActiveCylindricalGearSetDesignSelection to subclasses."""

    __parent__: "ActiveCylindricalGearSetDesignSelection"

    @property
    def active_gear_set_design_selection(
        self: "CastSelf",
    ) -> "_2748.ActiveGearSetDesignSelection":
        return self.__parent__._cast(_2748.ActiveGearSetDesignSelection)

    @property
    def part_detail_selection(self: "CastSelf") -> "_2865.PartDetailSelection":
        pass

        from mastapy._private.system_model.part_model.configurations import _2865

        return self.__parent__._cast(_2865.PartDetailSelection)

    @property
    def active_cylindrical_gear_set_design_selection(
        self: "CastSelf",
    ) -> "ActiveCylindricalGearSetDesignSelection":
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
class ActiveCylindricalGearSetDesignSelection(_2748.ActiveGearSetDesignSelection):
    """ActiveCylindricalGearSetDesignSelection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ACTIVE_CYLINDRICAL_GEAR_SET_DESIGN_SELECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def micro_geometry_selection(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "MicroGeometrySelection")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @micro_geometry_selection.setter
    @exception_bridge
    @enforce_parameter_types
    def micro_geometry_selection(self: "Self", value: "str") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "MicroGeometrySelection", value)

    @property
    def cast_to(self: "Self") -> "_Cast_ActiveCylindricalGearSetDesignSelection":
        """Cast to another type.

        Returns:
            _Cast_ActiveCylindricalGearSetDesignSelection
        """
        return _Cast_ActiveCylindricalGearSetDesignSelection(self)
