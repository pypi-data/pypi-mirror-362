"""FEPart"""

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
    pythonnet_method_call,
    pythonnet_method_call_overload,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.fe import _2605
from mastapy._private.system_model.part_model import _2661

_STRING = python_net_import("System", "String")
_FE_PART = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "FEPart")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility import _1683
    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.part_model import _2670, _2698

    Self = TypeVar("Self", bound="FEPart")
    CastSelf = TypeVar("CastSelf", bound="FEPart._Cast_FEPart")


__docformat__ = "restructuredtext en"
__all__ = ("FEPart",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FEPart:
    """Special nested class for casting FEPart to subclasses."""

    __parent__: "FEPart"

    @property
    def abstract_shaft_or_housing(self: "CastSelf") -> "_2661.AbstractShaftOrHousing":
        return self.__parent__._cast(_2661.AbstractShaftOrHousing)

    @property
    def component(self: "CastSelf") -> "_2670.Component":
        from mastapy._private.system_model.part_model import _2670

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
    def fe_part(self: "CastSelf") -> "FEPart":
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
class FEPart(_2661.AbstractShaftOrHousing):
    """FEPart

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_PART

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def three_d_node_size(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ThreeDNodeSize")

        if temp is None:
            return 0.0

        return temp

    @three_d_node_size.setter
    @exception_bridge
    @enforce_parameter_types
    def three_d_node_size(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ThreeDNodeSize", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def default_fe_substructure(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_FESubstructure":
        """ListWithSelectedItem[mastapy.system_model.fe.FESubstructure]"""
        temp = pythonnet_property_get(self.wrapped, "DefaultFESubstructure")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_FESubstructure",
        )(temp)

    @default_fe_substructure.setter
    @exception_bridge
    @enforce_parameter_types
    def default_fe_substructure(self: "Self", value: "_2605.FESubstructure") -> None:
        generic_type = (
            list_with_selected_item.ListWithSelectedItem_FESubstructure.implicit_type()
        )
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "DefaultFESubstructure", value)

    @property
    @exception_bridge
    def knows_scalar_mass(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "KnowsScalarMass")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def local_coordinate_system(self: "Self") -> "_1683.CoordinateSystem3D":
        """mastapy.math_utility.CoordinateSystem3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LocalCoordinateSystem")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    def create_fe_substructure(self: "Self") -> "_2605.FESubstructure":
        """mastapy.system_model.fe.FESubstructure"""
        method_result = pythonnet_method_call(self.wrapped, "CreateFESubstructure")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def create_fe_substructure_with_name(
        self: "Self", name: "str"
    ) -> "_2605.FESubstructure":
        """mastapy.system_model.fe.FESubstructure

        Args:
            name (str)
        """
        name = str(name)
        method_result = pythonnet_method_call_overload(
            self.wrapped, "CreateFESubstructure", [_STRING], name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def remove_fe_substructure(
        self: "Self", fe_substructure: "_2605.FESubstructure"
    ) -> "bool":
        """bool

        Args:
            fe_substructure (mastapy.system_model.fe.FESubstructure)
        """
        method_result = pythonnet_method_call(
            self.wrapped,
            "RemoveFESubstructure",
            fe_substructure.wrapped if fe_substructure else None,
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def select_fe_substructure(
        self: "Self", fe_substructure: "_2605.FESubstructure"
    ) -> None:
        """Method does not return.

        Args:
            fe_substructure (mastapy.system_model.fe.FESubstructure)
        """
        pythonnet_method_call(
            self.wrapped,
            "SelectFESubstructure",
            fe_substructure.wrapped if fe_substructure else None,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_FEPart":
        """Cast to another type.

        Returns:
            _Cast_FEPart
        """
        return _Cast_FEPart(self)
