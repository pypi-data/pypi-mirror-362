"""GuideDxfModel"""

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
from mastapy._private.system_model.part_model import _2670
from mastapy._private.utility.units_and_measurements import _1802

_GUIDE_DXF_MODEL = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "GuideDxfModel"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.part_model import _2698

    Self = TypeVar("Self", bound="GuideDxfModel")
    CastSelf = TypeVar("CastSelf", bound="GuideDxfModel._Cast_GuideDxfModel")


__docformat__ = "restructuredtext en"
__all__ = ("GuideDxfModel",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GuideDxfModel:
    """Special nested class for casting GuideDxfModel to subclasses."""

    __parent__: "GuideDxfModel"

    @property
    def component(self: "CastSelf") -> "_2670.Component":
        return self.__parent__._cast(_2670.Component)

    @property
    def part(self: "CastSelf") -> "_2698.Part":
        from mastapy._private.system_model.part_model import _2698

        return self.__parent__._cast(_2698.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2414.DesignEntity":
        from mastapy._private.system_model import _2414

        return self.__parent__._cast(_2414.DesignEntity)

    @property
    def guide_dxf_model(self: "CastSelf") -> "GuideDxfModel":
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
class GuideDxfModel(_2670.Component):
    """GuideDxfModel

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GUIDE_DXF_MODEL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def length_unit(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_Unit":
        """ListWithSelectedItem[mastapy.utility.units_and_measurements.Unit]"""
        temp = pythonnet_property_get(self.wrapped, "LengthUnit")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_Unit",
        )(temp)

    @length_unit.setter
    @exception_bridge
    @enforce_parameter_types
    def length_unit(self: "Self", value: "_1802.Unit") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "LengthUnit", value)

    @property
    @exception_bridge
    def memory_usage(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MemoryUsage")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def scale_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ScaleFactor")

        if temp is None:
            return 0.0

        return temp

    @scale_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def scale_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ScaleFactor", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_GuideDxfModel":
        """Cast to another type.

        Returns:
            _Cast_GuideDxfModel
        """
        return _Cast_GuideDxfModel(self)
