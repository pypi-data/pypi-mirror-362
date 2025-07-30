"""Shaft"""

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
    pythonnet_property_get,
    pythonnet_property_get_with_method,
    pythonnet_property_set,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model import _2660, _2682

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_SHAFT = python_net_import("SMT.MastaAPI.SystemModel.PartModel.ShaftModel", "Shaft")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.shafts import _46
    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.fe import _2605
    from mastapy._private.system_model.part_model import (
        _2661,
        _2670,
        _2683,
        _2693,
        _2698,
    )

    Self = TypeVar("Self", bound="Shaft")
    CastSelf = TypeVar("CastSelf", bound="Shaft._Cast_Shaft")


__docformat__ = "restructuredtext en"
__all__ = ("Shaft",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Shaft:
    """Special nested class for casting Shaft to subclasses."""

    __parent__: "Shaft"

    @property
    def abstract_shaft(self: "CastSelf") -> "_2660.AbstractShaft":
        return self.__parent__._cast(_2660.AbstractShaft)

    @property
    def abstract_shaft_or_housing(self: "CastSelf") -> "_2661.AbstractShaftOrHousing":
        from mastapy._private.system_model.part_model import _2661

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
    def shaft(self: "CastSelf") -> "Shaft":
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
class Shaft(_2660.AbstractShaft):
    """Shaft

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def active_design(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "ActiveDesign", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @active_design.setter
    @exception_bridge
    @enforce_parameter_types
    def active_design(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "ActiveDesign",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def cad_model(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_GuideDxfModel":
        """ListWithSelectedItem[mastapy.system_model.part_model.GuideDxfModel]"""
        temp = pythonnet_property_get(self.wrapped, "CADModel")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_GuideDxfModel",
        )(temp)

    @cad_model.setter
    @exception_bridge
    @enforce_parameter_types
    def cad_model(self: "Self", value: "_2682.GuideDxfModel") -> None:
        generic_type = (
            list_with_selected_item.ListWithSelectedItem_GuideDxfModel.implicit_type()
        )
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "CADModel", value)

    @property
    @exception_bridge
    def has_guide_image(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "HasGuideImage")

        if temp is None:
            return False

        return temp

    @has_guide_image.setter
    @exception_bridge
    @enforce_parameter_types
    def has_guide_image(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "HasGuideImage", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def is_replaced_by_fe(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsReplacedByFE")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def left_side_offset(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LeftSideOffset")

        if temp is None:
            return 0.0

        return temp

    @left_side_offset.setter
    @exception_bridge
    @enforce_parameter_types
    def left_side_offset(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "LeftSideOffset", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Length")

        if temp is None:
            return 0.0

        return temp

    @length.setter
    @exception_bridge
    @enforce_parameter_types
    def length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Length", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def mass_of_shaft_body(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MassOfShaftBody")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def polar_inertia_of_shaft_body(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PolarInertiaOfShaftBody")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def position_fixed(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "PositionFixed")

        if temp is None:
            return False

        return temp

    @position_fixed.setter
    @exception_bridge
    @enforce_parameter_types
    def position_fixed(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "PositionFixed", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def rotation_about_axis_for_all_mounted_components(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "RotationAboutAxisForAllMountedComponents"
        )

        if temp is None:
            return 0.0

        return temp

    @rotation_about_axis_for_all_mounted_components.setter
    @exception_bridge
    @enforce_parameter_types
    def rotation_about_axis_for_all_mounted_components(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "RotationAboutAxisForAllMountedComponents",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def stress_to_yield_strength_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StressToYieldStrengthFactor")

        if temp is None:
            return 0.0

        return temp

    @stress_to_yield_strength_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def stress_to_yield_strength_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StressToYieldStrengthFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def uses_cad_guide(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UsesCADGuide")

        if temp is None:
            return False

        return temp

    @uses_cad_guide.setter
    @exception_bridge
    @enforce_parameter_types
    def uses_cad_guide(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "UsesCADGuide", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def active_definition(self: "Self") -> "_46.SimpleShaftDefinition":
        """mastapy.shafts.SimpleShaftDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveDefinition")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def guide_image(self: "Self") -> "_2683.GuideImage":
        """mastapy.system_model.part_model.GuideImage

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GuideImage")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def fe_substructure_replacing_this(self: "Self") -> "_2605.FESubstructure":
        """mastapy.system_model.fe.FESubstructure

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FESubstructureReplacingThis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    def import_shaft(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ImportShaft")

    @exception_bridge
    @enforce_parameter_types
    def add_section(
        self: "Self",
        start_offset: "float",
        end_offset: "float",
        start_outer: "float",
        start_inner: "float",
        end_outer: "float",
        end_inner: "float",
    ) -> None:
        """Method does not return.

        Args:
            start_offset (float)
            end_offset (float)
            start_outer (float)
            start_inner (float)
            end_outer (float)
            end_inner (float)
        """
        start_offset = float(start_offset)
        end_offset = float(end_offset)
        start_outer = float(start_outer)
        start_inner = float(start_inner)
        end_outer = float(end_outer)
        end_inner = float(end_inner)
        pythonnet_method_call(
            self.wrapped,
            "AddSection",
            start_offset if start_offset else 0.0,
            end_offset if end_offset else 0.0,
            start_outer if start_outer else 0.0,
            start_inner if start_inner else 0.0,
            end_outer if end_outer else 0.0,
            end_inner if end_inner else 0.0,
        )

    @exception_bridge
    @enforce_parameter_types
    def mount_component(
        self: "Self", component: "_2693.MountableComponent", offset: "float"
    ) -> None:
        """Method does not return.

        Args:
            component (mastapy.system_model.part_model.MountableComponent)
            offset (float)
        """
        offset = float(offset)
        pythonnet_method_call(
            self.wrapped,
            "MountComponent",
            component.wrapped if component else None,
            offset if offset else 0.0,
        )

    @exception_bridge
    @enforce_parameter_types
    def read_rxf(self: "Self", file_name: "PathLike") -> None:
        """Method does not return.

        Args:
            file_name (PathLike)
        """
        file_name = str(file_name)
        pythonnet_method_call(self.wrapped, "ReadRXF", file_name)

    @exception_bridge
    def remove_all_sections(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "RemoveAllSections")

    @exception_bridge
    def remove_duplications(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "RemoveDuplications")

    @property
    def cast_to(self: "Self") -> "_Cast_Shaft":
        """Cast to another type.

        Returns:
            _Cast_Shaft
        """
        return _Cast_Shaft(self)
