"""ModelViewOptionsDrawStyle"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, overridable_enum_runtime, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import list_with_selected_item_and_image
from mastapy._private._internal.list_with_selected_item import (
    promote_to_list_with_selected_item,
)
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.geometry import _396
from mastapy._private.nodal_analysis import _62

_MODEL_VIEW_OPTIONS_DRAW_STYLE = python_net_import(
    "SMT.MastaAPI.SystemModel.Drawing", "ModelViewOptionsDrawStyle"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.geometry import _397

    Self = TypeVar("Self", bound="ModelViewOptionsDrawStyle")
    CastSelf = TypeVar(
        "CastSelf", bound="ModelViewOptionsDrawStyle._Cast_ModelViewOptionsDrawStyle"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ModelViewOptionsDrawStyle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ModelViewOptionsDrawStyle:
    """Special nested class for casting ModelViewOptionsDrawStyle to subclasses."""

    __parent__: "ModelViewOptionsDrawStyle"

    @property
    def draw_style(self: "CastSelf") -> "_396.DrawStyle":
        return self.__parent__._cast(_396.DrawStyle)

    @property
    def draw_style_base(self: "CastSelf") -> "_397.DrawStyleBase":
        from mastapy._private.geometry import _397

        return self.__parent__._cast(_397.DrawStyleBase)

    @property
    def model_view_options_draw_style(self: "CastSelf") -> "ModelViewOptionsDrawStyle":
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
class ModelViewOptionsDrawStyle(_396.DrawStyle):
    """ModelViewOptionsDrawStyle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MODEL_VIEW_OPTIONS_DRAW_STYLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def mesh(
        self: "Self",
    ) -> "list_with_selected_item_and_image.ListWithSelectedItemAndImage_FEMeshElementEntityOption":
        """ListWithSelectedItemAndImage[mastapy.nodal_analysis.FEMeshElementEntityOption]"""
        temp = pythonnet_property_get(self.wrapped, "Mesh")

        if temp is None:
            return None

        value = list_with_selected_item_and_image.ListWithSelectedItemAndImage_FEMeshElementEntityOption.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @mesh.setter
    @exception_bridge
    @enforce_parameter_types
    def mesh(self: "Self", value: "_62.FEMeshElementEntityOption") -> None:
        generic_type = list_with_selected_item_and_image.ListWithSelectedItemAndImage_FEMeshElementEntityOption.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "Mesh", value)

    @property
    @exception_bridge
    def rigid_elements(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "RigidElements")

        if temp is None:
            return False

        return temp

    @rigid_elements.setter
    @exception_bridge
    @enforce_parameter_types
    def rigid_elements(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "RigidElements", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def show_bearing_rings_which_are_in_f_es(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowBearingRingsWhichAreInFEs")

        if temp is None:
            return False

        return temp

    @show_bearing_rings_which_are_in_f_es.setter
    @exception_bridge
    @enforce_parameter_types
    def show_bearing_rings_which_are_in_f_es(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowBearingRingsWhichAreInFEs",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def show_nodes(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowNodes")

        if temp is None:
            return False

        return temp

    @show_nodes.setter
    @exception_bridge
    @enforce_parameter_types
    def show_nodes(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ShowNodes", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def show_part_coordinate_system(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowPartCoordinateSystem")

        if temp is None:
            return False

        return temp

    @show_part_coordinate_system.setter
    @exception_bridge
    @enforce_parameter_types
    def show_part_coordinate_system(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowPartCoordinateSystem",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def show_part_labels(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowPartLabels")

        if temp is None:
            return False

        return temp

    @show_part_labels.setter
    @exception_bridge
    @enforce_parameter_types
    def show_part_labels(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ShowPartLabels", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def solid_3d_shafts(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "Solid3DShafts")

        if temp is None:
            return False

        return temp

    @solid_3d_shafts.setter
    @exception_bridge
    @enforce_parameter_types
    def solid_3d_shafts(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "Solid3DShafts", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def solid_components(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "SolidComponents")

        if temp is None:
            return False

        return temp

    @solid_components.setter
    @exception_bridge
    @enforce_parameter_types
    def solid_components(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "SolidComponents", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def solid_housing(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "SolidHousing")

        if temp is None:
            return False

        return temp

    @solid_housing.setter
    @exception_bridge
    @enforce_parameter_types
    def solid_housing(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "SolidHousing", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def transparent_model(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "TransparentModel")

        if temp is None:
            return False

        return temp

    @transparent_model.setter
    @exception_bridge
    @enforce_parameter_types
    def transparent_model(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TransparentModel",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ModelViewOptionsDrawStyle":
        """Cast to another type.

        Returns:
            _Cast_ModelViewOptionsDrawStyle
        """
        return _Cast_ModelViewOptionsDrawStyle(self)
