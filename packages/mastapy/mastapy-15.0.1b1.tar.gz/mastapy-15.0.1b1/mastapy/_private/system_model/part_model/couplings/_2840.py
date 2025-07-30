"""ShaftHubConnection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

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
from mastapy._private.system_model.part_model import _2673
from mastapy._private.system_model.part_model.couplings import _2833, _2836, _2837

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_ARRAY = python_net_import("System", "Array")
_SHAFT_HUB_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ShaftHubConnection"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.detailed_rigid_connectors.interference_fits import _1630
    from mastapy._private.detailed_rigid_connectors.splines import _1595, _1600
    from mastapy._private.nodal_analysis import _60
    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.part_model import _2670, _2693, _2698
    from mastapy._private.system_model.part_model.couplings import (
        _2834,
        _2835,
        _2841,
        _2842,
        _2843,
        _2845,
    )

    Self = TypeVar("Self", bound="ShaftHubConnection")
    CastSelf = TypeVar("CastSelf", bound="ShaftHubConnection._Cast_ShaftHubConnection")


__docformat__ = "restructuredtext en"
__all__ = ("ShaftHubConnection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftHubConnection:
    """Special nested class for casting ShaftHubConnection to subclasses."""

    __parent__: "ShaftHubConnection"

    @property
    def connector(self: "CastSelf") -> "_2673.Connector":
        return self.__parent__._cast(_2673.Connector)

    @property
    def mountable_component(self: "CastSelf") -> "_2693.MountableComponent":
        from mastapy._private.system_model.part_model import _2693

        return self.__parent__._cast(_2693.MountableComponent)

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
    def shaft_hub_connection(self: "CastSelf") -> "ShaftHubConnection":
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
class ShaftHubConnection(_2673.Connector):
    """ShaftHubConnection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_HUB_CONNECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def two_d_spline_drawing(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TwoDSplineDrawing")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def additional_tilt_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AdditionalTiltStiffness")

        if temp is None:
            return 0.0

        return temp

    @additional_tilt_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def additional_tilt_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AdditionalTiltStiffness",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def angle_of_first_connection_point(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "AngleOfFirstConnectionPoint")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @angle_of_first_connection_point.setter
    @exception_bridge
    @enforce_parameter_types
    def angle_of_first_connection_point(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "AngleOfFirstConnectionPoint", value)

    @property
    @exception_bridge
    def angular_backlash(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AngularBacklash")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def angular_extent_of_external_teeth(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "AngularExtentOfExternalTeeth")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @angular_extent_of_external_teeth.setter
    @exception_bridge
    @enforce_parameter_types
    def angular_extent_of_external_teeth(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "AngularExtentOfExternalTeeth", value)

    @property
    @exception_bridge
    def axial_preload(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AxialPreload")

        if temp is None:
            return 0.0

        return temp

    @axial_preload.setter
    @exception_bridge
    @enforce_parameter_types
    def axial_preload(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "AxialPreload", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def axial_stiffness_shaft_hub_connection(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AxialStiffnessShaftHubConnection")

        if temp is None:
            return 0.0

        return temp

    @axial_stiffness_shaft_hub_connection.setter
    @exception_bridge
    @enforce_parameter_types
    def axial_stiffness_shaft_hub_connection(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AxialStiffnessShaftHubConnection",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def centre_angle_of_first_external_tooth(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CentreAngleOfFirstExternalTooth")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @centre_angle_of_first_external_tooth.setter
    @exception_bridge
    @enforce_parameter_types
    def centre_angle_of_first_external_tooth(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CentreAngleOfFirstExternalTooth", value)

    @property
    @exception_bridge
    def coefficient_of_friction(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CoefficientOfFriction")

        if temp is None:
            return 0.0

        return temp

    @coefficient_of_friction.setter
    @exception_bridge
    @enforce_parameter_types
    def coefficient_of_friction(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CoefficientOfFriction",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def contact_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ContactDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @contact_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def contact_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ContactDiameter", value)

    @property
    @exception_bridge
    def flank_contact_stiffness(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "FlankContactStiffness")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @flank_contact_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def flank_contact_stiffness(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "FlankContactStiffness", value)

    @property
    @exception_bridge
    def helix_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "HelixAngle")

        if temp is None:
            return 0.0

        return temp

    @helix_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def helix_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "HelixAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def inner_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "InnerDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @inner_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def inner_diameter(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "InnerDiameter", value)

    @property
    @exception_bridge
    def inner_half_material(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "InnerHalfMaterial", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @inner_half_material.setter
    @exception_bridge
    @enforce_parameter_types
    def inner_half_material(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "InnerHalfMaterial",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def left_flank_helix_angle(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "LeftFlankHelixAngle")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @left_flank_helix_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def left_flank_helix_angle(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "LeftFlankHelixAngle", value)

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
    def normal_clearance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NormalClearance")

        if temp is None:
            return 0.0

        return temp

    @normal_clearance.setter
    @exception_bridge
    @enforce_parameter_types
    def normal_clearance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "NormalClearance", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def number_of_connection_points(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfConnectionPoints")

        if temp is None:
            return 0

        return temp

    @number_of_connection_points.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_connection_points(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfConnectionPoints",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def number_of_contacts_per_direction(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfContactsPerDirection")

        if temp is None:
            return 0

        return temp

    @number_of_contacts_per_direction.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_contacts_per_direction(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfContactsPerDirection",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def outer_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "OuterDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @outer_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_diameter(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "OuterDiameter", value)

    @property
    @exception_bridge
    def outer_half_material(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "OuterHalfMaterial", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @outer_half_material.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_half_material(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "OuterHalfMaterial",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def pressure_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PressureAngle")

        if temp is None:
            return 0.0

        return temp

    @pressure_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def pressure_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "PressureAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def radial_clearance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RadialClearance")

        if temp is None:
            return 0.0

        return temp

    @radial_clearance.setter
    @exception_bridge
    @enforce_parameter_types
    def radial_clearance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RadialClearance", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def radial_stiffness_shaft_hub_connection(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RadialStiffnessShaftHubConnection")

        if temp is None:
            return 0.0

        return temp

    @radial_stiffness_shaft_hub_connection.setter
    @exception_bridge
    @enforce_parameter_types
    def radial_stiffness_shaft_hub_connection(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RadialStiffnessShaftHubConnection",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def right_flank_helix_angle(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RightFlankHelixAngle")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @right_flank_helix_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def right_flank_helix_angle(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RightFlankHelixAngle", value)

    @property
    @exception_bridge
    def spline_type(self: "Self") -> "_1595.SplineDesignTypes":
        """mastapy.detailed_rigid_connectors.splines.SplineDesignTypes"""
        temp = pythonnet_property_get(self.wrapped, "SplineType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.DetailedRigidConnectors.Splines.SplineDesignTypes"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.detailed_rigid_connectors.splines._1595",
            "SplineDesignTypes",
        )(value)

    @spline_type.setter
    @exception_bridge
    @enforce_parameter_types
    def spline_type(self: "Self", value: "_1595.SplineDesignTypes") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.DetailedRigidConnectors.Splines.SplineDesignTypes"
        )
        pythonnet_property_set(self.wrapped, "SplineType", value)

    @property
    @exception_bridge
    def stiffness_type(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_RigidConnectorStiffnessType":
        """EnumWithSelectedValue[mastapy.system_model.part_model.couplings.RigidConnectorStiffnessType]"""
        temp = pythonnet_property_get(self.wrapped, "StiffnessType")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_RigidConnectorStiffnessType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @stiffness_type.setter
    @exception_bridge
    @enforce_parameter_types
    def stiffness_type(
        self: "Self", value: "_2833.RigidConnectorStiffnessType"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_RigidConnectorStiffnessType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "StiffnessType", value)

    @property
    @exception_bridge
    def tangential_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TangentialStiffness")

        if temp is None:
            return 0.0

        return temp

    @tangential_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def tangential_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TangentialStiffness",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def tilt_clearance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TiltClearance")

        if temp is None:
            return 0.0

        return temp

    @tilt_clearance.setter
    @exception_bridge
    @enforce_parameter_types
    def tilt_clearance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "TiltClearance", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def tilt_stiffness_shaft_hub_connection(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TiltStiffnessShaftHubConnection")

        if temp is None:
            return 0.0

        return temp

    @tilt_stiffness_shaft_hub_connection.setter
    @exception_bridge
    @enforce_parameter_types
    def tilt_stiffness_shaft_hub_connection(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TiltStiffnessShaftHubConnection",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def tilt_stiffness_type(self: "Self") -> "_2834.RigidConnectorTiltStiffnessTypes":
        """mastapy.system_model.part_model.couplings.RigidConnectorTiltStiffnessTypes"""
        temp = pythonnet_property_get(self.wrapped, "TiltStiffnessType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.PartModel.Couplings.RigidConnectorTiltStiffnessTypes",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.part_model.couplings._2834",
            "RigidConnectorTiltStiffnessTypes",
        )(value)

    @tilt_stiffness_type.setter
    @exception_bridge
    @enforce_parameter_types
    def tilt_stiffness_type(
        self: "Self", value: "_2834.RigidConnectorTiltStiffnessTypes"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.PartModel.Couplings.RigidConnectorTiltStiffnessTypes",
        )
        pythonnet_property_set(self.wrapped, "TiltStiffnessType", value)

    @property
    @exception_bridge
    def tooth_spacing_type(
        self: "Self",
    ) -> (
        "enum_with_selected_value.EnumWithSelectedValue_RigidConnectorToothSpacingType"
    ):
        """EnumWithSelectedValue[mastapy.system_model.part_model.couplings.RigidConnectorToothSpacingType]"""
        temp = pythonnet_property_get(self.wrapped, "ToothSpacingType")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_RigidConnectorToothSpacingType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @tooth_spacing_type.setter
    @exception_bridge
    @enforce_parameter_types
    def tooth_spacing_type(
        self: "Self", value: "_2836.RigidConnectorToothSpacingType"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_RigidConnectorToothSpacingType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ToothSpacingType", value)

    @property
    @exception_bridge
    def torsional_stiffness_shaft_hub_connection(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "TorsionalStiffnessShaftHubConnection"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @torsional_stiffness_shaft_hub_connection.setter
    @exception_bridge
    @enforce_parameter_types
    def torsional_stiffness_shaft_hub_connection(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "TorsionalStiffnessShaftHubConnection", value
        )

    @property
    @exception_bridge
    def torsional_twist_preload(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TorsionalTwistPreload")

        if temp is None:
            return 0.0

        return temp

    @torsional_twist_preload.setter
    @exception_bridge
    @enforce_parameter_types
    def torsional_twist_preload(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TorsionalTwistPreload",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def type_(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_RigidConnectorTypes":
        """EnumWithSelectedValue[mastapy.system_model.part_model.couplings.RigidConnectorTypes]"""
        temp = pythonnet_property_get(self.wrapped, "Type")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_RigidConnectorTypes.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @type_.setter
    @exception_bridge
    @enforce_parameter_types
    def type_(self: "Self", value: "_2837.RigidConnectorTypes") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_RigidConnectorTypes.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "Type", value)

    @property
    @exception_bridge
    def external_half_manufacturing_error(
        self: "Self",
    ) -> "_2842.SplineHalfManufacturingError":
        """mastapy.system_model.part_model.couplings.SplineHalfManufacturingError

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExternalHalfManufacturingError")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def interference_fit_design(self: "Self") -> "_1630.InterferenceFitDesign":
        """mastapy.detailed_rigid_connectors.interference_fits.InterferenceFitDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InterferenceFitDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def internal_half_manufacturing_error(
        self: "Self",
    ) -> "_2842.SplineHalfManufacturingError":
        """mastapy.system_model.part_model.couplings.SplineHalfManufacturingError

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InternalHalfManufacturingError")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def left_flank_lead_relief(self: "Self") -> "_2843.SplineLeadRelief":
        """mastapy.system_model.part_model.couplings.SplineLeadRelief

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeftFlankLeadRelief")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def major_fit_options(self: "Self") -> "_2841.SplineFitOptions":
        """mastapy.system_model.part_model.couplings.SplineFitOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MajorFitOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def minor_fit_options(self: "Self") -> "_2841.SplineFitOptions":
        """mastapy.system_model.part_model.couplings.SplineFitOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinorFitOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def non_linear_stiffness(self: "Self") -> "_60.DiagonalNonLinearStiffness":
        """mastapy.nodal_analysis.DiagonalNonLinearStiffness

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NonLinearStiffness")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def right_flank_lead_relief(self: "Self") -> "_2843.SplineLeadRelief":
        """mastapy.system_model.part_model.couplings.SplineLeadRelief

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RightFlankLeadRelief")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def spline_joint_design(self: "Self") -> "_1600.SplineJointDesign":
        """mastapy.detailed_rigid_connectors.splines.SplineJointDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SplineJointDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def spline_pitch_error_options(self: "Self") -> "_2845.SplinePitchErrorOptions":
        """mastapy.system_model.part_model.couplings.SplinePitchErrorOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SplinePitchErrorOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def fit_options(self: "Self") -> "List[_2841.SplineFitOptions]":
        """List[mastapy.system_model.part_model.couplings.SplineFitOptions]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FitOptions")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def lead_reliefs(self: "Self") -> "List[_2843.SplineLeadRelief]":
        """List[mastapy.system_model.part_model.couplings.SplineLeadRelief]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeadReliefs")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def spline_half_manufacturing_errors(
        self: "Self",
    ) -> "List[_2842.SplineHalfManufacturingError]":
        """List[mastapy.system_model.part_model.couplings.SplineHalfManufacturingError]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SplineHalfManufacturingErrors")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def tooth_locations_external_spline_half(
        self: "Self",
    ) -> "List[_2835.RigidConnectorToothLocation]":
        """List[mastapy.system_model.part_model.couplings.RigidConnectorToothLocation]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothLocationsExternalSplineHalf")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def full_stiffness_matrix(self: "Self") -> "List[List[float]]":
        """List[List[float]]"""
        temp = pythonnet_property_get(self.wrapped, "FullStiffnessMatrix")

        if temp is None:
            return None

        value = conversion.pn_to_mp_list_float_2d(temp)

        if value is None:
            return None

        return value

    @full_stiffness_matrix.setter
    @exception_bridge
    @enforce_parameter_types
    def full_stiffness_matrix(self: "Self", value: "List[List[float]]") -> None:
        value = conversion.mp_to_pn_list_float_2d(value)
        pythonnet_property_set(self.wrapped, "FullStiffnessMatrix", value)

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftHubConnection":
        """Cast to another type.

        Returns:
            _Cast_ShaftHubConnection
        """
        return _Cast_ShaftHubConnection(self)
