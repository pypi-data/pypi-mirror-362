"""CylindricalGearSetDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    overridable_enum_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import (
    enum_with_selected_value,
    list_with_selected_item,
    overridable,
)
from mastapy._private._internal.list_with_selected_item import (
    promote_to_list_with_selected_item,
)
from mastapy._private._internal.overridable_constructor import _unpack_overridable
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
from mastapy._private.gears import _408
from mastapy._private.gears.gear_designs import _1054
from mastapy._private.gears.rating import _450

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_CYLINDRICAL_GEAR_SET_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "CylindricalGearSetDesign"
)

if TYPE_CHECKING:
    from typing import Any, List, Optional, Tuple, Type, TypeVar, Union

    from mastapy._private.gears.gear_designs import _1052
    from mastapy._private.gears.gear_designs.cylindrical import (
        _1102,
        _1122,
        _1128,
        _1132,
        _1139,
        _1140,
        _1151,
        _1157,
        _1170,
        _1173,
        _1183,
        _1201,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1220
    from mastapy._private.gears.manufacturing.cylindrical import _728
    from mastapy._private.gears.rating.cylindrical import _545, _554
    from mastapy._private.gears.rating.cylindrical.iso6336 import _601

    Self = TypeVar("Self", bound="CylindricalGearSetDesign")
    CastSelf = TypeVar(
        "CastSelf", bound="CylindricalGearSetDesign._Cast_CylindricalGearSetDesign"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearSetDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearSetDesign:
    """Special nested class for casting CylindricalGearSetDesign to subclasses."""

    __parent__: "CylindricalGearSetDesign"

    @property
    def gear_set_design(self: "CastSelf") -> "_1054.GearSetDesign":
        return self.__parent__._cast(_1054.GearSetDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_1052.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _1052

        return self.__parent__._cast(_1052.GearDesignComponent)

    @property
    def cylindrical_planetary_gear_set_design(
        self: "CastSelf",
    ) -> "_1151.CylindricalPlanetaryGearSetDesign":
        from mastapy._private.gears.gear_designs.cylindrical import _1151

        return self.__parent__._cast(_1151.CylindricalPlanetaryGearSetDesign)

    @property
    def cylindrical_gear_set_design(self: "CastSelf") -> "CylindricalGearSetDesign":
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
class CylindricalGearSetDesign(_1054.GearSetDesign):
    """CylindricalGearSetDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_SET_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def all_gears_number_of_teeth(self: "Self") -> "List[int]":
        """List[int]"""
        temp = pythonnet_property_get(self.wrapped, "AllGearsNumberOfTeeth")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, int)

        if value is None:
            return None

        return value

    @all_gears_number_of_teeth.setter
    @exception_bridge
    @enforce_parameter_types
    def all_gears_number_of_teeth(self: "Self", value: "List[int]") -> None:
        value = conversion.mp_to_pn_objects_in_list(value)
        pythonnet_property_set(self.wrapped, "AllGearsNumberOfTeeth", value)

    @property
    @exception_bridge
    def axial_pitch(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AxialPitch")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def coefficient_of_friction_calculation_method(
        self: "Self",
    ) -> "overridable.Overridable_CoefficientOfFrictionCalculationMethod":
        """Overridable[mastapy.gears.CoefficientOfFrictionCalculationMethod]"""
        temp = pythonnet_property_get(
            self.wrapped, "CoefficientOfFrictionCalculationMethod"
        )

        if temp is None:
            return None

        value = overridable.Overridable_CoefficientOfFrictionCalculationMethod.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @coefficient_of_friction_calculation_method.setter
    @exception_bridge
    @enforce_parameter_types
    def coefficient_of_friction_calculation_method(
        self: "Self",
        value: "Union[_408.CoefficientOfFrictionCalculationMethod, Tuple[_408.CoefficientOfFrictionCalculationMethod, bool]]",
    ) -> None:
        wrapper_type = overridable.Overridable_CoefficientOfFrictionCalculationMethod.wrapper_type()
        enclosed_type = overridable.Overridable_CoefficientOfFrictionCalculationMethod.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "CoefficientOfFrictionCalculationMethod", value
        )

    @property
    @exception_bridge
    def efficiency_rating_method(
        self: "Self",
    ) -> (
        "enum_with_selected_value.EnumWithSelectedValue_GearMeshEfficiencyRatingMethod"
    ):
        """EnumWithSelectedValue[mastapy.gears.rating.GearMeshEfficiencyRatingMethod]"""
        temp = pythonnet_property_get(self.wrapped, "EfficiencyRatingMethod")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_GearMeshEfficiencyRatingMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @efficiency_rating_method.setter
    @exception_bridge
    @enforce_parameter_types
    def efficiency_rating_method(
        self: "Self", value: "_450.GearMeshEfficiencyRatingMethod"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_GearMeshEfficiencyRatingMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "EfficiencyRatingMethod", value)

    @property
    @exception_bridge
    def fe_model_for_tiff(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "FEModelForTIFF", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @fe_model_for_tiff.setter
    @exception_bridge
    @enforce_parameter_types
    def fe_model_for_tiff(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "FEModelForTIFF",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def face_width(self: "Self") -> "Optional[float]":
        """Optional[float]"""
        temp = pythonnet_property_get(self.wrapped, "FaceWidth")

        if temp is None:
            return None

        return temp

    @face_width.setter
    @exception_bridge
    @enforce_parameter_types
    def face_width(self: "Self", value: "Optional[float]") -> None:
        pythonnet_property_set(self.wrapped, "FaceWidth", value)

    @property
    @exception_bridge
    def face_width_with_constant_axial_contact_ratio(self: "Self") -> "Optional[float]":
        """Optional[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "FaceWidthWithConstantAxialContactRatio"
        )

        if temp is None:
            return None

        return temp

    @face_width_with_constant_axial_contact_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def face_width_with_constant_axial_contact_ratio(
        self: "Self", value: "Optional[float]"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "FaceWidthWithConstantAxialContactRatio", value
        )

    @property
    @exception_bridge
    def gear_fit_system(self: "Self") -> "_1157.GearFitSystems":
        """mastapy.gears.gear_designs.cylindrical.GearFitSystems"""
        temp = pythonnet_property_get(self.wrapped, "GearFitSystem")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.GearFitSystems"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical._1157", "GearFitSystems"
        )(value)

    @gear_fit_system.setter
    @exception_bridge
    @enforce_parameter_types
    def gear_fit_system(self: "Self", value: "_1157.GearFitSystems") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.GearFitSystems"
        )
        pythonnet_property_set(self.wrapped, "GearFitSystem", value)

    @property
    @exception_bridge
    def gear_tooth_thickness_reduction_allowance(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(
            self.wrapped, "GearToothThicknessReductionAllowance"
        )

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @gear_tooth_thickness_reduction_allowance.setter
    @exception_bridge
    @enforce_parameter_types
    def gear_tooth_thickness_reduction_allowance(self: "Self", value: "str") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(
            self.wrapped, "GearToothThicknessReductionAllowance", value
        )

    @property
    @exception_bridge
    def gear_tooth_thickness_tolerance(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "GearToothThicknessTolerance")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @gear_tooth_thickness_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def gear_tooth_thickness_tolerance(self: "Self", value: "str") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "GearToothThicknessTolerance", value)

    @property
    @exception_bridge
    def helical_gear_micro_geometry_option(
        self: "Self",
    ) -> "_601.HelicalGearMicroGeometryOption":
        """mastapy.gears.rating.cylindrical.iso6336.HelicalGearMicroGeometryOption"""
        temp = pythonnet_property_get(self.wrapped, "HelicalGearMicroGeometryOption")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336.HelicalGearMicroGeometryOption",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.rating.cylindrical.iso6336._601",
            "HelicalGearMicroGeometryOption",
        )(value)

    @helical_gear_micro_geometry_option.setter
    @exception_bridge
    @enforce_parameter_types
    def helical_gear_micro_geometry_option(
        self: "Self", value: "_601.HelicalGearMicroGeometryOption"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336.HelicalGearMicroGeometryOption",
        )
        pythonnet_property_set(self.wrapped, "HelicalGearMicroGeometryOption", value)

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
    def helix_angle_maintain_transverse_profile(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "HelixAngleMaintainTransverseProfile"
        )

        if temp is None:
            return 0.0

        return temp

    @helix_angle_maintain_transverse_profile.setter
    @exception_bridge
    @enforce_parameter_types
    def helix_angle_maintain_transverse_profile(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "HelixAngleMaintainTransverseProfile",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def helix_angle_calculating_gear_teeth_numbers(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "HelixAngleCalculatingGearTeethNumbers"
        )

        if temp is None:
            return 0.0

        return temp

    @helix_angle_calculating_gear_teeth_numbers.setter
    @exception_bridge
    @enforce_parameter_types
    def helix_angle_calculating_gear_teeth_numbers(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "HelixAngleCalculatingGearTeethNumbers",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def helix_angle_with_centre_distance_adjustment(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "HelixAngleWithCentreDistanceAdjustment"
        )

        if temp is None:
            return 0.0

        return temp

    @helix_angle_with_centre_distance_adjustment.setter
    @exception_bridge
    @enforce_parameter_types
    def helix_angle_with_centre_distance_adjustment(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "HelixAngleWithCentreDistanceAdjustment",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def is_asymmetric(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsAsymmetric")

        if temp is None:
            return False

        return temp

    @is_asymmetric.setter
    @exception_bridge
    @enforce_parameter_types
    def is_asymmetric(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "IsAsymmetric", bool(value) if value is not None else False
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
    def maximum_axial_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumAxialContactRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_transverse_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumTransverseContactRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_axial_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumAxialContactRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_tip_thickness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumTipThickness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_transverse_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumTransverseContactRatio")

        if temp is None:
            return 0.0

        return temp

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
    def normal_diametral_pitch_per_inch_with_centre_distance_adjustment(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "NormalDiametralPitchPerInchWithCentreDistanceAdjustment"
        )

        if temp is None:
            return 0.0

        return temp

    @normal_diametral_pitch_per_inch_with_centre_distance_adjustment.setter
    @exception_bridge
    @enforce_parameter_types
    def normal_diametral_pitch_per_inch_with_centre_distance_adjustment(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "NormalDiametralPitchPerInchWithCentreDistanceAdjustment",
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
    def normal_module_maintain_transverse_profile(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "NormalModuleMaintainTransverseProfile"
        )

        if temp is None:
            return 0.0

        return temp

    @normal_module_maintain_transverse_profile.setter
    @exception_bridge
    @enforce_parameter_types
    def normal_module_maintain_transverse_profile(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NormalModuleMaintainTransverseProfile",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def normal_module_calculating_gear_teeth_numbers(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "NormalModuleCalculatingGearTeethNumbers"
        )

        if temp is None:
            return 0.0

        return temp

    @normal_module_calculating_gear_teeth_numbers.setter
    @exception_bridge
    @enforce_parameter_types
    def normal_module_calculating_gear_teeth_numbers(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "NormalModuleCalculatingGearTeethNumbers",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def normal_module_with_centre_distance_adjustment(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "NormalModuleWithCentreDistanceAdjustment"
        )

        if temp is None:
            return 0.0

        return temp

    @normal_module_with_centre_distance_adjustment.setter
    @exception_bridge
    @enforce_parameter_types
    def normal_module_with_centre_distance_adjustment(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "NormalModuleWithCentreDistanceAdjustment",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def normal_pitch(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalPitch")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_pressure_angle_constant_base_pitch(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "NormalPressureAngleConstantBasePitch"
        )

        if temp is None:
            return 0.0

        return temp

    @normal_pressure_angle_constant_base_pitch.setter
    @exception_bridge
    @enforce_parameter_types
    def normal_pressure_angle_constant_base_pitch(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NormalPressureAngleConstantBasePitch",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def normal_pressure_angle_maintain_transverse_profile(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "NormalPressureAngleMaintainTransverseProfile"
        )

        if temp is None:
            return 0.0

        return temp

    @normal_pressure_angle_maintain_transverse_profile.setter
    @exception_bridge
    @enforce_parameter_types
    def normal_pressure_angle_maintain_transverse_profile(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "NormalPressureAngleMaintainTransverseProfile",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def profile_shift_distribution_rule(
        self: "Self",
    ) -> "_1102.AddendumModificationDistributionRule":
        """mastapy.gears.gear_designs.cylindrical.AddendumModificationDistributionRule"""
        temp = pythonnet_property_get(self.wrapped, "ProfileShiftDistributionRule")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.AddendumModificationDistributionRule",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical._1102",
            "AddendumModificationDistributionRule",
        )(value)

    @profile_shift_distribution_rule.setter
    @exception_bridge
    @enforce_parameter_types
    def profile_shift_distribution_rule(
        self: "Self", value: "_1102.AddendumModificationDistributionRule"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.AddendumModificationDistributionRule",
        )
        pythonnet_property_set(self.wrapped, "ProfileShiftDistributionRule", value)

    @property
    @exception_bridge
    def root_gear_profile_shift_coefficient_maintain_tip_and_root_diameters(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "RootGearProfileShiftCoefficientMaintainTipAndRootDiameters"
        )

        if temp is None:
            return 0.0

        return temp

    @root_gear_profile_shift_coefficient_maintain_tip_and_root_diameters.setter
    @exception_bridge
    @enforce_parameter_types
    def root_gear_profile_shift_coefficient_maintain_tip_and_root_diameters(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "RootGearProfileShiftCoefficientMaintainTipAndRootDiameters",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def tooth_numbers_are_good(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothNumbersAreGood")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def transverse_diametral_pitch_per_inch(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TransverseDiametralPitchPerInch")

        if temp is None:
            return 0.0

        return temp

    @transverse_diametral_pitch_per_inch.setter
    @exception_bridge
    @enforce_parameter_types
    def transverse_diametral_pitch_per_inch(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TransverseDiametralPitchPerInch",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def transverse_module(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransverseModule")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transverse_pitch(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransversePitch")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def use_advanced_ltca_for_ltca_mean_sliding_power_loss_calculation(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseAdvancedLTCAForLTCAMeanSlidingPowerLossCalculation"
        )

        if temp is None:
            return False

        return temp

    @use_advanced_ltca_for_ltca_mean_sliding_power_loss_calculation.setter
    @exception_bridge
    @enforce_parameter_types
    def use_advanced_ltca_for_ltca_mean_sliding_power_loss_calculation(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseAdvancedLTCAForLTCAMeanSlidingPowerLossCalculation",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def cylindrical_gear_micro_geometry_settings(
        self: "Self",
    ) -> "_1132.CylindricalGearMicroGeometrySettingsItem":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearMicroGeometrySettingsItem

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalGearMicroGeometrySettings"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_gear_set_manufacturing_configuration(
        self: "Self",
    ) -> "_728.CylindricalSetManufacturingConfig":
        """mastapy.gears.manufacturing.cylindrical.CylindricalSetManufacturingConfig

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalGearSetManufacturingConfiguration"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_gear_set_micro_geometry(
        self: "Self",
    ) -> "_1220.CylindricalGearSetMicroGeometry":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearSetMicroGeometry

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearSetMicroGeometry")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def ltca_settings(self: "Self") -> "_1170.LTCASettings":
        """mastapy.gears.gear_designs.cylindrical.LTCASettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LTCASettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def left_flank(self: "Self") -> "_1139.CylindricalGearSetFlankDesign":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearSetFlankDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeftFlank")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def micropitting(self: "Self") -> "_1173.Micropitting":
        """mastapy.gears.gear_designs.cylindrical.Micropitting

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Micropitting")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def rating_settings(
        self: "Self",
    ) -> "_545.CylindricalGearDesignAndRatingSettingsItem":
        """mastapy.gears.rating.cylindrical.CylindricalGearDesignAndRatingSettingsItem

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RatingSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def right_flank(self: "Self") -> "_1139.CylindricalGearSetFlankDesign":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearSetFlankDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RightFlank")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def scuffing(self: "Self") -> "_1183.Scuffing":
        """mastapy.gears.gear_designs.cylindrical.Scuffing

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Scuffing")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def usage(self: "Self") -> "_1201.Usage":
        """mastapy.gears.gear_designs.cylindrical.Usage

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Usage")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gears(self: "Self") -> "List[_1122.CylindricalGearDesign]":
        """List[mastapy.gears.gear_designs.cylindrical.CylindricalGearDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Gears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def cylindrical_gears(self: "Self") -> "List[_1122.CylindricalGearDesign]":
        """List[mastapy.gears.gear_designs.cylindrical.CylindricalGearDesign]

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
    def cylindrical_meshes(self: "Self") -> "List[_1128.CylindricalGearMeshDesign]":
        """List[mastapy.gears.gear_designs.cylindrical.CylindricalGearMeshDesign]

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
    def flanks(self: "Self") -> "List[_1139.CylindricalGearSetFlankDesign]":
        """List[mastapy.gears.gear_designs.cylindrical.CylindricalGearSetFlankDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Flanks")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def both_flanks(self: "Self") -> "_1139.CylindricalGearSetFlankDesign":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearSetFlankDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BothFlanks")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def micro_geometries(self: "Self") -> "List[_1220.CylindricalGearSetMicroGeometry]":
        """List[mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearSetMicroGeometry]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MicroGeometries")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def manufacturing_configurations(
        self: "Self",
    ) -> "List[_728.CylindricalSetManufacturingConfig]":
        """List[mastapy.gears.manufacturing.cylindrical.CylindricalSetManufacturingConfig]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ManufacturingConfigurations")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    def centre_distance_editor(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CentreDistanceEditor")

    @exception_bridge
    def fix_errors_and_warnings(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "FixErrorsAndWarnings")

    @exception_bridge
    def set_helix_angle_for_axial_contact_ratio(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SetHelixAngleForAxialContactRatio")

    @exception_bridge
    @enforce_parameter_types
    def add_new_manufacturing_configuration(
        self: "Self", new_config_name: "str" = "None"
    ) -> "_728.CylindricalSetManufacturingConfig":
        """mastapy.gears.manufacturing.cylindrical.CylindricalSetManufacturingConfig

        Args:
            new_config_name (str, optional)
        """
        new_config_name = str(new_config_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "AddNewManufacturingConfiguration",
            new_config_name if new_config_name else "",
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def add_new_micro_geometry(self: "Self") -> "_1220.CylindricalGearSetMicroGeometry":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearSetMicroGeometry"""
        method_result = pythonnet_method_call(self.wrapped, "AddNewMicroGeometry")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def add_new_micro_geometry_specifying_separate_micro_geometry_per_tooth(
        self: "Self",
    ) -> "_1220.CylindricalGearSetMicroGeometry":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearSetMicroGeometry"""
        method_result = pythonnet_method_call(
            self.wrapped, "AddNewMicroGeometrySpecifyingSeparateMicroGeometryPerTooth"
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_new_micro_geometry_specifying_separate_micro_geometry_per_tooth_for(
        self: "Self", gears: "List[_1122.CylindricalGearDesign]"
    ) -> "_1220.CylindricalGearSetMicroGeometry":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearSetMicroGeometry

        Args:
            gears (List[mastapy.gears.gear_designs.cylindrical.CylindricalGearDesign])
        """
        gears = conversion.mp_to_pn_objects_in_dotnet_list(gears)
        method_result = pythonnet_method_call(
            self.wrapped,
            "AddNewMicroGeometrySpecifyingSeparateMicroGeometryPerToothFor",
            gears,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def create_optimiser(
        self: "Self", duty_cycle: "_554.CylindricalGearSetDutyCycleRating"
    ) -> "_1140.CylindricalGearSetMacroGeometryOptimiser":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearSetMacroGeometryOptimiser

        Args:
            duty_cycle (mastapy.gears.rating.cylindrical.CylindricalGearSetDutyCycleRating)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "CreateOptimiser", duty_cycle.wrapped if duty_cycle else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def delete_manufacturing_configuration(
        self: "Self", config: "_728.CylindricalSetManufacturingConfig"
    ) -> None:
        """Method does not return.

        Args:
            config (mastapy.gears.manufacturing.cylindrical.CylindricalSetManufacturingConfig)
        """
        pythonnet_method_call(
            self.wrapped,
            "DeleteManufacturingConfiguration",
            config.wrapped if config else None,
        )

    @exception_bridge
    @enforce_parameter_types
    def delete_micro_geometry(
        self: "Self", micro_geometry: "_1220.CylindricalGearSetMicroGeometry"
    ) -> None:
        """Method does not return.

        Args:
            micro_geometry (mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearSetMicroGeometry)
        """
        pythonnet_method_call(
            self.wrapped,
            "DeleteMicroGeometry",
            micro_geometry.wrapped if micro_geometry else None,
        )

    @exception_bridge
    def delete_unused_manufacturing_configurations(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "DeleteUnusedManufacturingConfigurations")

    @exception_bridge
    def try_make_valid(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "TryMakeValid")

    @exception_bridge
    @enforce_parameter_types
    def micro_geometry_named(
        self: "Self", micro_geometry_name: "str"
    ) -> "_1220.CylindricalGearSetMicroGeometry":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearSetMicroGeometry

        Args:
            micro_geometry_name (str)
        """
        micro_geometry_name = str(micro_geometry_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "MicroGeometryNamed",
            micro_geometry_name if micro_geometry_name else "",
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def set_active_manufacturing_configuration(
        self: "Self", value: "_728.CylindricalSetManufacturingConfig"
    ) -> None:
        """Method does not return.

        Args:
            value (mastapy.gears.manufacturing.cylindrical.CylindricalSetManufacturingConfig)
        """
        pythonnet_method_call(
            self.wrapped,
            "SetActiveManufacturingConfiguration",
            value.wrapped if value else None,
        )

    @exception_bridge
    @enforce_parameter_types
    def set_active_micro_geometry(
        self: "Self", value: "_1220.CylindricalGearSetMicroGeometry"
    ) -> None:
        """Method does not return.

        Args:
            value (mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearSetMicroGeometry)
        """
        pythonnet_method_call(
            self.wrapped, "SetActiveMicroGeometry", value.wrapped if value else None
        )

    @exception_bridge
    def clear_all_tooth_thickness_specifications(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ClearAllToothThicknessSpecifications")

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearSetDesign":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearSetDesign
        """
        return _Cast_CylindricalGearSetDesign(self)
