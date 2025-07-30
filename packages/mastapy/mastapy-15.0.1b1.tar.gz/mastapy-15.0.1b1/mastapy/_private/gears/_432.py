"""PocketingPowerLossCoefficients"""

from __future__ import annotations

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
from mastapy._private._internal.implicit import enum_with_selected_value
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.math_utility import _1694
from mastapy._private.utility.databases import _2028

_POCKETING_POWER_LOSS_COEFFICIENTS = python_net_import(
    "SMT.MastaAPI.Gears", "PocketingPowerLossCoefficients"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears import _436
    from mastapy._private.math_utility.measured_data import _1749

    Self = TypeVar("Self", bound="PocketingPowerLossCoefficients")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PocketingPowerLossCoefficients._Cast_PocketingPowerLossCoefficients",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PocketingPowerLossCoefficients",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PocketingPowerLossCoefficients:
    """Special nested class for casting PocketingPowerLossCoefficients to subclasses."""

    __parent__: "PocketingPowerLossCoefficients"

    @property
    def named_database_item(self: "CastSelf") -> "_2028.NamedDatabaseItem":
        return self.__parent__._cast(_2028.NamedDatabaseItem)

    @property
    def pocketing_power_loss_coefficients(
        self: "CastSelf",
    ) -> "PocketingPowerLossCoefficients":
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
class PocketingPowerLossCoefficients(_2028.NamedDatabaseItem):
    """PocketingPowerLossCoefficients

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _POCKETING_POWER_LOSS_COEFFICIENTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def extrapolation_options(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ExtrapolationOptions":
        """EnumWithSelectedValue[mastapy.math_utility.ExtrapolationOptions]"""
        temp = pythonnet_property_get(self.wrapped, "ExtrapolationOptions")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ExtrapolationOptions.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @extrapolation_options.setter
    @exception_bridge
    @enforce_parameter_types
    def extrapolation_options(
        self: "Self", value: "_1694.ExtrapolationOptions"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ExtrapolationOptions.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ExtrapolationOptions", value)

    @property
    @exception_bridge
    def intercept_of_linear_equation_defining_the_effect_of_gear_face_width(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "InterceptOfLinearEquationDefiningTheEffectOfGearFaceWidth"
        )

        if temp is None:
            return 0.0

        return temp

    @intercept_of_linear_equation_defining_the_effect_of_gear_face_width.setter
    @exception_bridge
    @enforce_parameter_types
    def intercept_of_linear_equation_defining_the_effect_of_gear_face_width(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "InterceptOfLinearEquationDefiningTheEffectOfGearFaceWidth",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def intercept_of_linear_equation_defining_the_effect_of_helix_angle(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "InterceptOfLinearEquationDefiningTheEffectOfHelixAngle"
        )

        if temp is None:
            return 0.0

        return temp

    @intercept_of_linear_equation_defining_the_effect_of_helix_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def intercept_of_linear_equation_defining_the_effect_of_helix_angle(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "InterceptOfLinearEquationDefiningTheEffectOfHelixAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def lower_bound_for_oil_kinematic_viscosity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "LowerBoundForOilKinematicViscosity"
        )

        if temp is None:
            return 0.0

        return temp

    @lower_bound_for_oil_kinematic_viscosity.setter
    @exception_bridge
    @enforce_parameter_types
    def lower_bound_for_oil_kinematic_viscosity(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LowerBoundForOilKinematicViscosity",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def raw_pocketing_power_loss_lookup_table(
        self: "Self",
    ) -> "_1749.GriddedSurfaceAccessor":
        """mastapy.math_utility.measured_data.GriddedSurfaceAccessor"""
        temp = pythonnet_property_get(self.wrapped, "RawPocketingPowerLossLookupTable")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @raw_pocketing_power_loss_lookup_table.setter
    @exception_bridge
    @enforce_parameter_types
    def raw_pocketing_power_loss_lookup_table(
        self: "Self", value: "_1749.GriddedSurfaceAccessor"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "RawPocketingPowerLossLookupTable", value.wrapped
        )

    @property
    @exception_bridge
    def reference_gear_outer_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ReferenceGearOuterDiameter")

        if temp is None:
            return 0.0

        return temp

    @reference_gear_outer_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def reference_gear_outer_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ReferenceGearOuterDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def reference_gear_pocket_dimension(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ReferenceGearPocketDimension")

        if temp is None:
            return 0.0

        return temp

    @reference_gear_pocket_dimension.setter
    @exception_bridge
    @enforce_parameter_types
    def reference_gear_pocket_dimension(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ReferenceGearPocketDimension",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def slope_of_linear_equation_defining_the_effect_of_gear_face_width(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "SlopeOfLinearEquationDefiningTheEffectOfGearFaceWidth"
        )

        if temp is None:
            return 0.0

        return temp

    @slope_of_linear_equation_defining_the_effect_of_gear_face_width.setter
    @exception_bridge
    @enforce_parameter_types
    def slope_of_linear_equation_defining_the_effect_of_gear_face_width(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "SlopeOfLinearEquationDefiningTheEffectOfGearFaceWidth",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def slope_of_linear_equation_defining_the_effect_of_helix_angle(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "SlopeOfLinearEquationDefiningTheEffectOfHelixAngle"
        )

        if temp is None:
            return 0.0

        return temp

    @slope_of_linear_equation_defining_the_effect_of_helix_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def slope_of_linear_equation_defining_the_effect_of_helix_angle(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "SlopeOfLinearEquationDefiningTheEffectOfHelixAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def upper_bound_for_oil_kinematic_viscosity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "UpperBoundForOilKinematicViscosity"
        )

        if temp is None:
            return 0.0

        return temp

    @upper_bound_for_oil_kinematic_viscosity.setter
    @exception_bridge
    @enforce_parameter_types
    def upper_bound_for_oil_kinematic_viscosity(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UpperBoundForOilKinematicViscosity",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def specifications_for_the_effect_of_oil_kinematic_viscosity(
        self: "Self",
    ) -> "List[_436.SpecificationForTheEffectOfOilKinematicViscosity]":
        """List[mastapy.gears.SpecificationForTheEffectOfOilKinematicViscosity]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SpecificationsForTheEffectOfOilKinematicViscosity"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_PocketingPowerLossCoefficients":
        """Cast to another type.

        Returns:
            _Cast_PocketingPowerLossCoefficients
        """
        return _Cast_PocketingPowerLossCoefficients(self)
