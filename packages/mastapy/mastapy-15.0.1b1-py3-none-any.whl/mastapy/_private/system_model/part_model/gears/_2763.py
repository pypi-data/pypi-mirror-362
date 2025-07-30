"""CylindricalGearSet"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    overridable_enum_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_get_with_method,
    pythonnet_property_set,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears import _411
from mastapy._private.system_model.part_model.gears import _2769

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_CYLINDRICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "CylindricalGearSet"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.gears.gear_designs.cylindrical import _1138
    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.connections_and_sockets.gears import _2530
    from mastapy._private.system_model.part_model import _2659, _2698, _2708
    from mastapy._private.system_model.part_model.gears import _2762, _2779
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set import (
        _2801,
    )

    Self = TypeVar("Self", bound="CylindricalGearSet")
    CastSelf = TypeVar("CastSelf", bound="CylindricalGearSet._Cast_CylindricalGearSet")


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearSet",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearSet:
    """Special nested class for casting CylindricalGearSet to subclasses."""

    __parent__: "CylindricalGearSet"

    @property
    def gear_set(self: "CastSelf") -> "_2769.GearSet":
        return self.__parent__._cast(_2769.GearSet)

    @property
    def specialised_assembly(self: "CastSelf") -> "_2708.SpecialisedAssembly":
        from mastapy._private.system_model.part_model import _2708

        return self.__parent__._cast(_2708.SpecialisedAssembly)

    @property
    def abstract_assembly(self: "CastSelf") -> "_2659.AbstractAssembly":
        from mastapy._private.system_model.part_model import _2659

        return self.__parent__._cast(_2659.AbstractAssembly)

    @property
    def part(self: "CastSelf") -> "_2698.Part":
        from mastapy._private.system_model.part_model import _2698

        return self.__parent__._cast(_2698.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2414.DesignEntity":
        from mastapy._private.system_model import _2414

        return self.__parent__._cast(_2414.DesignEntity)

    @property
    def planetary_gear_set(self: "CastSelf") -> "_2779.PlanetaryGearSet":
        from mastapy._private.system_model.part_model.gears import _2779

        return self.__parent__._cast(_2779.PlanetaryGearSet)

    @property
    def cylindrical_gear_set(self: "CastSelf") -> "CylindricalGearSet":
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
class CylindricalGearSet(_2769.GearSet):
    """CylindricalGearSet

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_SET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def axial_contact_ratio_requirement(
        self: "Self",
    ) -> "overridable.Overridable_ContactRatioRequirements":
        """Overridable[mastapy.gears.ContactRatioRequirements]"""
        temp = pythonnet_property_get(self.wrapped, "AxialContactRatioRequirement")

        if temp is None:
            return None

        value = overridable.Overridable_ContactRatioRequirements.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @axial_contact_ratio_requirement.setter
    @exception_bridge
    @enforce_parameter_types
    def axial_contact_ratio_requirement(
        self: "Self",
        value: "Union[_411.ContactRatioRequirements, Tuple[_411.ContactRatioRequirements, bool]]",
    ) -> None:
        wrapper_type = overridable.Overridable_ContactRatioRequirements.wrapper_type()
        enclosed_type = overridable.Overridable_ContactRatioRequirements.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(self.wrapped, "AxialContactRatioRequirement", value)

    @property
    @exception_bridge
    def is_supercharger_rotor_set(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsSuperchargerRotorSet")

        if temp is None:
            return False

        return temp

    @is_supercharger_rotor_set.setter
    @exception_bridge
    @enforce_parameter_types
    def is_supercharger_rotor_set(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IsSuperchargerRotorSet",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def maximum_acceptable_axial_contact_ratio(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumAcceptableAxialContactRatio"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @maximum_acceptable_axial_contact_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_acceptable_axial_contact_ratio(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "MaximumAcceptableAxialContactRatio", value
        )

    @property
    @exception_bridge
    def maximum_acceptable_transverse_contact_ratio(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumAcceptableTransverseContactRatio"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @maximum_acceptable_transverse_contact_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_acceptable_transverse_contact_ratio(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "MaximumAcceptableTransverseContactRatio", value
        )

    @property
    @exception_bridge
    def maximum_face_width(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MaximumFaceWidth")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @maximum_face_width.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_face_width(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MaximumFaceWidth", value)

    @property
    @exception_bridge
    def maximum_helix_angle(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MaximumHelixAngle")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @maximum_helix_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_helix_angle(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MaximumHelixAngle", value)

    @property
    @exception_bridge
    def maximum_normal_module(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MaximumNormalModule")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @maximum_normal_module.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_normal_module(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MaximumNormalModule", value)

    @property
    @exception_bridge
    def maximum_normal_pressure_angle(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MaximumNormalPressureAngle")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @maximum_normal_pressure_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_normal_pressure_angle(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MaximumNormalPressureAngle", value)

    @property
    @exception_bridge
    def minimum_acceptable_axial_contact_ratio(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "MinimumAcceptableAxialContactRatio"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @minimum_acceptable_axial_contact_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_acceptable_axial_contact_ratio(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "MinimumAcceptableAxialContactRatio", value
        )

    @property
    @exception_bridge
    def minimum_acceptable_transverse_contact_ratio(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "MinimumAcceptableTransverseContactRatio"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @minimum_acceptable_transverse_contact_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_acceptable_transverse_contact_ratio(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "MinimumAcceptableTransverseContactRatio", value
        )

    @property
    @exception_bridge
    def minimum_face_width(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MinimumFaceWidth")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @minimum_face_width.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_face_width(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MinimumFaceWidth", value)

    @property
    @exception_bridge
    def minimum_helix_angle(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MinimumHelixAngle")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @minimum_helix_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_helix_angle(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MinimumHelixAngle", value)

    @property
    @exception_bridge
    def minimum_normal_module(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MinimumNormalModule")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @minimum_normal_module.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_normal_module(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MinimumNormalModule", value)

    @property
    @exception_bridge
    def minimum_normal_pressure_angle(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MinimumNormalPressureAngle")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @minimum_normal_pressure_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_normal_pressure_angle(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MinimumNormalPressureAngle", value)

    @property
    @exception_bridge
    def opposite_hand(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "OppositeHand")

        if temp is None:
            return False

        return temp

    @opposite_hand.setter
    @exception_bridge
    @enforce_parameter_types
    def opposite_hand(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "OppositeHand", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def supercharger_rotor_set_database(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "SuperchargerRotorSetDatabase", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @supercharger_rotor_set_database.setter
    @exception_bridge
    @enforce_parameter_types
    def supercharger_rotor_set_database(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "SuperchargerRotorSetDatabase",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def transverse_contact_ratio_requirement(
        self: "Self",
    ) -> "overridable.Overridable_ContactRatioRequirements":
        """Overridable[mastapy.gears.ContactRatioRequirements]"""
        temp = pythonnet_property_get(self.wrapped, "TransverseContactRatioRequirement")

        if temp is None:
            return None

        value = overridable.Overridable_ContactRatioRequirements.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @transverse_contact_ratio_requirement.setter
    @exception_bridge
    @enforce_parameter_types
    def transverse_contact_ratio_requirement(
        self: "Self",
        value: "Union[_411.ContactRatioRequirements, Tuple[_411.ContactRatioRequirements, bool]]",
    ) -> None:
        wrapper_type = overridable.Overridable_ContactRatioRequirements.wrapper_type()
        enclosed_type = overridable.Overridable_ContactRatioRequirements.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(self.wrapped, "TransverseContactRatioRequirement", value)

    @property
    @exception_bridge
    def active_gear_set_design(self: "Self") -> "_1138.CylindricalGearSetDesign":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveGearSetDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_gear_set_design(self: "Self") -> "_1138.CylindricalGearSetDesign":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearSetDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def supercharger_rotor_set(self: "Self") -> "_2801.SuperchargerRotorSet":
        """mastapy.system_model.part_model.gears.supercharger_rotor_set.SuperchargerRotorSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SuperchargerRotorSet")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_gears(self: "Self") -> "List[_2762.CylindricalGear]":
        """List[mastapy.system_model.part_model.gears.CylindricalGear]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

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

    @property
    @exception_bridge
    def gear_set_designs(self: "Self") -> "List[_1138.CylindricalGearSetDesign]":
        """List[mastapy.gears.gear_designs.cylindrical.CylindricalGearSetDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSetDesigns")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    def add_gear(self: "Self") -> "_2762.CylindricalGear":
        """mastapy.system_model.part_model.gears.CylindricalGear"""
        method_result = pythonnet_method_call(self.wrapped, "AddGear")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearSet":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearSet
        """
        return _Cast_CylindricalGearSet(self)
