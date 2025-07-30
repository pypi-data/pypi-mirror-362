"""BearingRaceMountingOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import enum_with_selected_value, overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_get_with_method,
    pythonnet_property_set,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings.bearing_results import _2169, _2170

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_BEARING_RACE_MOUNTING_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "BearingRaceMountingOptions"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.materials import _332
    from mastapy._private.system_model.part_model import _2685, _2697

    Self = TypeVar("Self", bound="BearingRaceMountingOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="BearingRaceMountingOptions._Cast_BearingRaceMountingOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BearingRaceMountingOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BearingRaceMountingOptions:
    """Special nested class for casting BearingRaceMountingOptions to subclasses."""

    __parent__: "BearingRaceMountingOptions"

    @property
    def inner_bearing_race_mounting_options(
        self: "CastSelf",
    ) -> "_2685.InnerBearingRaceMountingOptions":
        from mastapy._private.system_model.part_model import _2685

        return self.__parent__._cast(_2685.InnerBearingRaceMountingOptions)

    @property
    def outer_bearing_race_mounting_options(
        self: "CastSelf",
    ) -> "_2697.OuterBearingRaceMountingOptions":
        from mastapy._private.system_model.part_model import _2697

        return self.__parent__._cast(_2697.OuterBearingRaceMountingOptions)

    @property
    def bearing_race_mounting_options(self: "CastSelf") -> "BearingRaceMountingOptions":
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
class BearingRaceMountingOptions(_0.APIBase):
    """BearingRaceMountingOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEARING_RACE_MOUNTING_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def axial_mounting(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_RaceAxialMountingType":
        """EnumWithSelectedValue[mastapy.bearings.bearing_results.RaceAxialMountingType]"""
        temp = pythonnet_property_get(self.wrapped, "AxialMounting")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_RaceAxialMountingType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @axial_mounting.setter
    @exception_bridge
    @enforce_parameter_types
    def axial_mounting(self: "Self", value: "_2169.RaceAxialMountingType") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_RaceAxialMountingType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "AxialMounting", value)

    @property
    @exception_bridge
    def bore_mounting_sleeve(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "BoreMountingSleeve")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @bore_mounting_sleeve.setter
    @exception_bridge
    @enforce_parameter_types
    def bore_mounting_sleeve(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "BoreMountingSleeve", value)

    @property
    @exception_bridge
    def has_mounting_sleeve(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "HasMountingSleeve")

        if temp is None:
            return False

        return temp

    @has_mounting_sleeve.setter
    @exception_bridge
    @enforce_parameter_types
    def has_mounting_sleeve(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "HasMountingSleeve",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def left_axial_mounting_clearance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LeftAxialMountingClearance")

        if temp is None:
            return 0.0

        return temp

    @left_axial_mounting_clearance.setter
    @exception_bridge
    @enforce_parameter_types
    def left_axial_mounting_clearance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LeftAxialMountingClearance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def mounting_sleeve_material_reportable(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "MountingSleeveMaterialReportable", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @mounting_sleeve_material_reportable.setter
    @exception_bridge
    @enforce_parameter_types
    def mounting_sleeve_material_reportable(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "MountingSleeveMaterialReportable",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

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
    @exception_bridge
    def outer_diameter_mounting_sleeve(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "OuterDiameterMountingSleeve")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @outer_diameter_mounting_sleeve.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_diameter_mounting_sleeve(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "OuterDiameterMountingSleeve", value)

    @property
    @exception_bridge
    def radial_clearance_contact_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RadialClearanceContactStiffness")

        if temp is None:
            return 0.0

        return temp

    @radial_clearance_contact_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def radial_clearance_contact_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RadialClearanceContactStiffness",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def radial_mounting_clearance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RadialMountingClearance")

        if temp is None:
            return 0.0

        return temp

    @radial_mounting_clearance.setter
    @exception_bridge
    @enforce_parameter_types
    def radial_mounting_clearance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RadialMountingClearance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def right_axial_mounting_clearance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RightAxialMountingClearance")

        if temp is None:
            return 0.0

        return temp

    @right_axial_mounting_clearance.setter
    @exception_bridge
    @enforce_parameter_types
    def right_axial_mounting_clearance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RightAxialMountingClearance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def simple_radial_mounting(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_RaceRadialMountingType":
        """EnumWithSelectedValue[mastapy.bearings.bearing_results.RaceRadialMountingType]"""
        temp = pythonnet_property_get(self.wrapped, "SimpleRadialMounting")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_RaceRadialMountingType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @simple_radial_mounting.setter
    @exception_bridge
    @enforce_parameter_types
    def simple_radial_mounting(
        self: "Self", value: "_2170.RaceRadialMountingType"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_RaceRadialMountingType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "SimpleRadialMounting", value)

    @property
    @exception_bridge
    def temperature_of_mounting_sleeve(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "TemperatureOfMountingSleeve")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @temperature_of_mounting_sleeve.setter
    @exception_bridge
    @enforce_parameter_types
    def temperature_of_mounting_sleeve(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "TemperatureOfMountingSleeve", value)

    @property
    @exception_bridge
    def mounting_sleeve_material(self: "Self") -> "_332.BearingMaterial":
        """mastapy.materials.BearingMaterial

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MountingSleeveMaterial")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_BearingRaceMountingOptions":
        """Cast to another type.

        Returns:
            _Cast_BearingRaceMountingOptions
        """
        return _Cast_BearingRaceMountingOptions(self)
