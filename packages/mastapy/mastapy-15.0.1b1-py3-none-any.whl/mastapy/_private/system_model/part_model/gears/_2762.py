"""CylindricalGear"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model.gears import _2767

_CYLINDRICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "CylindricalGear"
)

if TYPE_CHECKING:
    from typing import Any, List, Optional, Tuple, Type, TypeVar, Union

    from mastapy._private.gears.gear_designs.cylindrical import _1122
    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.connections_and_sockets.gears import _2530
    from mastapy._private.system_model.part_model import _2670, _2693, _2698
    from mastapy._private.system_model.part_model.gears import _2764

    Self = TypeVar("Self", bound="CylindricalGear")
    CastSelf = TypeVar("CastSelf", bound="CylindricalGear._Cast_CylindricalGear")


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGear",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGear:
    """Special nested class for casting CylindricalGear to subclasses."""

    __parent__: "CylindricalGear"

    @property
    def gear(self: "CastSelf") -> "_2767.Gear":
        return self.__parent__._cast(_2767.Gear)

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
    def cylindrical_planet_gear(self: "CastSelf") -> "_2764.CylindricalPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2764

        return self.__parent__._cast(_2764.CylindricalPlanetGear)

    @property
    def cylindrical_gear(self: "CastSelf") -> "CylindricalGear":
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
class CylindricalGear(_2767.Gear):
    """CylindricalGear

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def centre_of_estimated_micro_geometry_range(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CentreOfEstimatedMicroGeometryRange"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def clearance_to_tip_diameter_limit(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ClearanceToTipDiameterLimit")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def clocking_angle_error(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ClockingAngleError")

        if temp is None:
            return 0.0

        return temp

    @clocking_angle_error.setter
    @exception_bridge
    @enforce_parameter_types
    def clocking_angle_error(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ClockingAngleError",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def estimated_crowning(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "EstimatedCrowning")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @estimated_crowning.setter
    @exception_bridge
    @enforce_parameter_types
    def estimated_crowning(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "EstimatedCrowning", value)

    @property
    @exception_bridge
    def extra_backlash(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ExtraBacklash")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @extra_backlash.setter
    @exception_bridge
    @enforce_parameter_types
    def extra_backlash(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ExtraBacklash", value)

    @property
    @exception_bridge
    def has_concept_synchroniser(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "HasConceptSynchroniser")

        if temp is None:
            return False

        return temp

    @has_concept_synchroniser.setter
    @exception_bridge
    @enforce_parameter_types
    def has_concept_synchroniser(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "HasConceptSynchroniser",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def is_position_fixed_for_centre_distance_modification(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "IsPositionFixedForCentreDistanceModification"
        )

        if temp is None:
            return False

        return temp

    @is_position_fixed_for_centre_distance_modification.setter
    @exception_bridge
    @enforce_parameter_types
    def is_position_fixed_for_centre_distance_modification(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "IsPositionFixedForCentreDistanceModification",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def left_limit_of_estimated_micro_geometry_range(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LeftLimitOfEstimatedMicroGeometryRange"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def linear_relief(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "LinearRelief")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @linear_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def linear_relief(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "LinearRelief", value)

    @property
    @exception_bridge
    def minimum_rim_thickness_normal_module(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MinimumRimThicknessNormalModule")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @minimum_rim_thickness_normal_module.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_rim_thickness_normal_module(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MinimumRimThicknessNormalModule", value)

    @property
    @exception_bridge
    def reference_axis_angle_about_local_z_axis_from_y_axis(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ReferenceAxisAngleAboutLocalZAxisFromYAxis"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def right_limit_of_estimated_micro_geometry_range(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RightLimitOfEstimatedMicroGeometryRange"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def root_diameter_limit(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RootDiameterLimit")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @root_diameter_limit.setter
    @exception_bridge
    @enforce_parameter_types
    def root_diameter_limit(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RootDiameterLimit", value)

    @property
    @exception_bridge
    def tip_diameter_limit(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "TipDiameterLimit")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @tip_diameter_limit.setter
    @exception_bridge
    @enforce_parameter_types
    def tip_diameter_limit(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "TipDiameterLimit", value)

    @property
    @exception_bridge
    def active_gear_design(self: "Self") -> "_1122.CylindricalGearDesign":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveGearDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_gear_design(self: "Self") -> "_1122.CylindricalGearDesign":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_meshes(self: "Self") -> "List[_2530.CylindricalGearMesh]":
        """List[mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalMeshes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    @enforce_parameter_types
    def make_carrier_assembly(
        self: "Self",
        number_of_radial_bearings: "int",
        add_left_thrust_bearing: "bool",
        add_right_thrust_bearing: "bool",
        gear_bore: "float",
        carrier_bore: "float",
        carrier_width: "float",
        gear_offset: "float" = 0.0,
        left_bearing_indent: "float" = 0.0,
        right_bearing_indent: "float" = 0.0,
        thrust_pad_clearance: "float" = 0.0,
        adding_bearing: "bool" = True,
        left_thurst_pad_contact_diameter: Optional["Optional[float]"] = None,
        right_thurst_pad_contact_diameter: Optional["Optional[float]"] = None,
    ) -> None:
        """Method does not return.

        Args:
            number_of_radial_bearings (int)
            add_left_thrust_bearing (bool)
            add_right_thrust_bearing (bool)
            gear_bore (float)
            carrier_bore (float)
            carrier_width (float)
            gear_offset (float, optional)
            left_bearing_indent (float, optional)
            right_bearing_indent (float, optional)
            thrust_pad_clearance (float, optional)
            adding_bearing (bool, optional)
            left_thurst_pad_contact_diameter (Optional[float], optional)
            right_thurst_pad_contact_diameter (Optional[float], optional)
        """
        number_of_radial_bearings = int(number_of_radial_bearings)
        add_left_thrust_bearing = bool(add_left_thrust_bearing)
        add_right_thrust_bearing = bool(add_right_thrust_bearing)
        gear_bore = float(gear_bore)
        carrier_bore = float(carrier_bore)
        carrier_width = float(carrier_width)
        gear_offset = float(gear_offset)
        left_bearing_indent = float(left_bearing_indent)
        right_bearing_indent = float(right_bearing_indent)
        thrust_pad_clearance = float(thrust_pad_clearance)
        adding_bearing = bool(adding_bearing)
        pythonnet_method_call(
            self.wrapped,
            "MakeCarrierAssembly",
            number_of_radial_bearings if number_of_radial_bearings else 0,
            add_left_thrust_bearing if add_left_thrust_bearing else False,
            add_right_thrust_bearing if add_right_thrust_bearing else False,
            gear_bore if gear_bore else 0.0,
            carrier_bore if carrier_bore else 0.0,
            carrier_width if carrier_width else 0.0,
            gear_offset if gear_offset else 0.0,
            left_bearing_indent if left_bearing_indent else 0.0,
            right_bearing_indent if right_bearing_indent else 0.0,
            thrust_pad_clearance if thrust_pad_clearance else 0.0,
            adding_bearing if adding_bearing else False,
            left_thurst_pad_contact_diameter,
            right_thurst_pad_contact_diameter,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGear":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGear
        """
        return _Cast_CylindricalGear(self)
