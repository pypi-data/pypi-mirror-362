"""CylindricalGearPairCreationOptions"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, ClassVar

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
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs.creation_options import _1267
from mastapy._private.gears.gear_designs.cylindrical import _1138

_CYLINDRICAL_GEAR_PAIR_CREATION_OPTIONS = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.CreationOptions",
    "CylindricalGearPairCreationOptions",
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    Self = TypeVar("Self", bound="CylindricalGearPairCreationOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearPairCreationOptions._Cast_CylindricalGearPairCreationOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearPairCreationOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearPairCreationOptions:
    """Special nested class for casting CylindricalGearPairCreationOptions to subclasses."""

    __parent__: "CylindricalGearPairCreationOptions"

    @property
    def gear_set_creation_options(self: "CastSelf") -> "_1267.GearSetCreationOptions":
        return self.__parent__._cast(_1267.GearSetCreationOptions)

    @property
    def cylindrical_gear_pair_creation_options(
        self: "CastSelf",
    ) -> "CylindricalGearPairCreationOptions":
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
class CylindricalGearPairCreationOptions(
    _1267.GearSetCreationOptions[_1138.CylindricalGearSetDesign]
):
    """CylindricalGearPairCreationOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_PAIR_CREATION_OPTIONS

    class DerivedParameterOption(Enum):
        """DerivedParameterOption is a nested enum."""

        @classmethod
        def type_(cls) -> "Type":
            return _CYLINDRICAL_GEAR_PAIR_CREATION_OPTIONS.DerivedParameterOption

        CENTRE_DISTANCE = 0
        NORMAL_MODULE = 1
        HELIX_ANGLE = 2

    def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
        raise AttributeError("Cannot set the attributes of an Enum.") from None

    def __enum_delattr(self: "Self", attr: str) -> None:
        raise AttributeError("Cannot delete the attributes of an Enum.") from None

    DerivedParameterOption.__setattr__ = __enum_setattr
    DerivedParameterOption.__delattr__ = __enum_delattr

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def centre_distance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CentreDistance")

        if temp is None:
            return 0.0

        return temp

    @centre_distance.setter
    @exception_bridge
    @enforce_parameter_types
    def centre_distance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "CentreDistance", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def centre_distance_target(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CentreDistanceTarget")

        if temp is None:
            return 0.0

        return temp

    @centre_distance_target.setter
    @exception_bridge
    @enforce_parameter_types
    def centre_distance_target(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CentreDistanceTarget",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def derived_parameter(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_CylindricalGearPairCreationOptions_DerivedParameterOption":
        """EnumWithSelectedValue[mastapy.gears.gear_designs.creation_options.CylindricalGearPairCreationOptions.DerivedParameterOption]"""
        temp = pythonnet_property_get(self.wrapped, "DerivedParameter")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_CylindricalGearPairCreationOptions_DerivedParameterOption.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @derived_parameter.setter
    @exception_bridge
    @enforce_parameter_types
    def derived_parameter(
        self: "Self", value: "CylindricalGearPairCreationOptions.DerivedParameterOption"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_CylindricalGearPairCreationOptions_DerivedParameterOption.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "DerivedParameter", value)

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
    def helix_angle_target(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "HelixAngleTarget")

        if temp is None:
            return 0.0

        return temp

    @helix_angle_target.setter
    @exception_bridge
    @enforce_parameter_types
    def helix_angle_target(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "HelixAngleTarget", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def normal_diametral_pitch_per_inch(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NormalDiametralPitchPerInch")

        if temp is None:
            return 0.0

        return temp

    @normal_diametral_pitch_per_inch.setter
    @exception_bridge
    @enforce_parameter_types
    def normal_diametral_pitch_per_inch(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NormalDiametralPitchPerInch",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def normal_diametral_pitch_target(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NormalDiametralPitchTarget")

        if temp is None:
            return 0.0

        return temp

    @normal_diametral_pitch_target.setter
    @exception_bridge
    @enforce_parameter_types
    def normal_diametral_pitch_target(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NormalDiametralPitchTarget",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def normal_module(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NormalModule")

        if temp is None:
            return 0.0

        return temp

    @normal_module.setter
    @exception_bridge
    @enforce_parameter_types
    def normal_module(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "NormalModule", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def normal_module_target(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NormalModuleTarget")

        if temp is None:
            return 0.0

        return temp

    @normal_module_target.setter
    @exception_bridge
    @enforce_parameter_types
    def normal_module_target(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NormalModuleTarget",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def normal_pressure_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NormalPressureAngle")

        if temp is None:
            return 0.0

        return temp

    @normal_pressure_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def normal_pressure_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NormalPressureAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def pinion_face_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PinionFaceWidth")

        if temp is None:
            return 0.0

        return temp

    @pinion_face_width.setter
    @exception_bridge
    @enforce_parameter_types
    def pinion_face_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "PinionFaceWidth", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def pinion_number_of_teeth(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "PinionNumberOfTeeth")

        if temp is None:
            return 0

        return temp

    @pinion_number_of_teeth.setter
    @exception_bridge
    @enforce_parameter_types
    def pinion_number_of_teeth(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "PinionNumberOfTeeth", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def ratio_guide(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RatioGuide")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @ratio_guide.setter
    @exception_bridge
    @enforce_parameter_types
    def ratio_guide(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RatioGuide", value)

    @property
    @exception_bridge
    def wheel_face_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WheelFaceWidth")

        if temp is None:
            return 0.0

        return temp

    @wheel_face_width.setter
    @exception_bridge
    @enforce_parameter_types
    def wheel_face_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "WheelFaceWidth", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def wheel_number_of_teeth(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "WheelNumberOfTeeth")

        if temp is None:
            return 0

        return temp

    @wheel_number_of_teeth.setter
    @exception_bridge
    @enforce_parameter_types
    def wheel_number_of_teeth(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "WheelNumberOfTeeth", int(value) if value is not None else 0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearPairCreationOptions":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearPairCreationOptions
        """
        return _Cast_CylindricalGearPairCreationOptions(self)
