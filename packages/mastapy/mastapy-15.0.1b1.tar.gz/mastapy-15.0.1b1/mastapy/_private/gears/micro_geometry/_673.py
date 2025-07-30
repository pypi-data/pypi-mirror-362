"""ProfileModification"""

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
from mastapy._private.gears.micro_geometry import _664, _665, _666, _667, _670

_PROFILE_MODIFICATION = python_net_import(
    "SMT.MastaAPI.Gears.MicroGeometry", "ProfileModification"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.conical.micro_geometry import _1295
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import (
        _1218,
        _1219,
    )
    from mastapy._private.gears.micro_geometry import _668, _669, _671, _672
    from mastapy._private.math_utility import _1718

    Self = TypeVar("Self", bound="ProfileModification")
    CastSelf = TypeVar(
        "CastSelf", bound="ProfileModification._Cast_ProfileModification"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ProfileModification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ProfileModification:
    """Special nested class for casting ProfileModification to subclasses."""

    __parent__: "ProfileModification"

    @property
    def modification(self: "CastSelf") -> "_670.Modification":
        return self.__parent__._cast(_670.Modification)

    @property
    def cylindrical_gear_profile_modification(
        self: "CastSelf",
    ) -> "_1218.CylindricalGearProfileModification":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1218

        return self.__parent__._cast(_1218.CylindricalGearProfileModification)

    @property
    def cylindrical_gear_profile_modification_at_face_width_position(
        self: "CastSelf",
    ) -> "_1219.CylindricalGearProfileModificationAtFaceWidthPosition":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1219

        return self.__parent__._cast(
            _1219.CylindricalGearProfileModificationAtFaceWidthPosition
        )

    @property
    def conical_gear_profile_modification(
        self: "CastSelf",
    ) -> "_1295.ConicalGearProfileModification":
        from mastapy._private.gears.gear_designs.conical.micro_geometry import _1295

        return self.__parent__._cast(_1295.ConicalGearProfileModification)

    @property
    def profile_modification(self: "CastSelf") -> "ProfileModification":
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
class ProfileModification(_670.Modification):
    """ProfileModification

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PROFILE_MODIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def barrelling_peak_point_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BarrellingPeakPointFactor")

        if temp is None:
            return 0.0

        return temp

    @barrelling_peak_point_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def barrelling_peak_point_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "BarrellingPeakPointFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def barrelling_relief(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BarrellingRelief")

        if temp is None:
            return 0.0

        return temp

    @barrelling_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def barrelling_relief(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "BarrellingRelief", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def evaluation_lower_limit_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EvaluationLowerLimitFactor")

        if temp is None:
            return 0.0

        return temp

    @evaluation_lower_limit_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_lower_limit_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationLowerLimitFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_lower_limit_factor_for_zero_root_relief(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationLowerLimitFactorForZeroRootRelief"
        )

        if temp is None:
            return 0.0

        return temp

    @evaluation_lower_limit_factor_for_zero_root_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_lower_limit_factor_for_zero_root_relief(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationLowerLimitFactorForZeroRootRelief",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_upper_limit_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EvaluationUpperLimitFactor")

        if temp is None:
            return 0.0

        return temp

    @evaluation_upper_limit_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_upper_limit_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationUpperLimitFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_upper_limit_factor_for_zero_tip_relief(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationUpperLimitFactorForZeroTipRelief"
        )

        if temp is None:
            return 0.0

        return temp

    @evaluation_upper_limit_factor_for_zero_tip_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_upper_limit_factor_for_zero_tip_relief(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationUpperLimitFactorForZeroTipRelief",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_of_linear_root_relief_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationOfLinearRootReliefFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_linear_root_relief_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_of_linear_root_relief_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationOfLinearRootReliefFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_of_linear_tip_relief_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EvaluationOfLinearTipReliefFactor")

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_linear_tip_relief_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_of_linear_tip_relief_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationOfLinearTipReliefFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_of_parabolic_root_relief_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationOfParabolicRootReliefFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_parabolic_root_relief_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_of_parabolic_root_relief_factor(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationOfParabolicRootReliefFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_of_parabolic_tip_relief_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationOfParabolicTipReliefFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_parabolic_tip_relief_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_of_parabolic_tip_relief_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationOfParabolicTipReliefFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def linear_relief(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LinearRelief")

        if temp is None:
            return 0.0

        return temp

    @linear_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def linear_relief(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "LinearRelief", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def linear_root_relief(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LinearRootRelief")

        if temp is None:
            return 0.0

        return temp

    @linear_root_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def linear_root_relief(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "LinearRootRelief", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def linear_tip_relief(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LinearTipRelief")

        if temp is None:
            return 0.0

        return temp

    @linear_tip_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def linear_tip_relief(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "LinearTipRelief", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def location_of_evaluation_lower_limit(
        self: "Self",
    ) -> (
        "enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationLowerLimit"
    ):
        """EnumWithSelectedValue[mastapy.gears.micro_geometry.LocationOfEvaluationLowerLimit]"""
        temp = pythonnet_property_get(self.wrapped, "LocationOfEvaluationLowerLimit")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationLowerLimit.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @location_of_evaluation_lower_limit.setter
    @exception_bridge
    @enforce_parameter_types
    def location_of_evaluation_lower_limit(
        self: "Self", value: "_664.LocationOfEvaluationLowerLimit"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationLowerLimit.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "LocationOfEvaluationLowerLimit", value)

    @property
    @exception_bridge
    def location_of_evaluation_lower_limit_for_zero_root_relief(
        self: "Self",
    ) -> (
        "enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationLowerLimit"
    ):
        """EnumWithSelectedValue[mastapy.gears.micro_geometry.LocationOfEvaluationLowerLimit]"""
        temp = pythonnet_property_get(
            self.wrapped, "LocationOfEvaluationLowerLimitForZeroRootRelief"
        )

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationLowerLimit.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @location_of_evaluation_lower_limit_for_zero_root_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def location_of_evaluation_lower_limit_for_zero_root_relief(
        self: "Self", value: "_664.LocationOfEvaluationLowerLimit"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationLowerLimit.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(
            self.wrapped, "LocationOfEvaluationLowerLimitForZeroRootRelief", value
        )

    @property
    @exception_bridge
    def location_of_evaluation_upper_limit(
        self: "Self",
    ) -> (
        "enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationUpperLimit"
    ):
        """EnumWithSelectedValue[mastapy.gears.micro_geometry.LocationOfEvaluationUpperLimit]"""
        temp = pythonnet_property_get(self.wrapped, "LocationOfEvaluationUpperLimit")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationUpperLimit.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @location_of_evaluation_upper_limit.setter
    @exception_bridge
    @enforce_parameter_types
    def location_of_evaluation_upper_limit(
        self: "Self", value: "_665.LocationOfEvaluationUpperLimit"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationUpperLimit.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "LocationOfEvaluationUpperLimit", value)

    @property
    @exception_bridge
    def location_of_evaluation_upper_limit_for_zero_tip_relief(
        self: "Self",
    ) -> (
        "enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationUpperLimit"
    ):
        """EnumWithSelectedValue[mastapy.gears.micro_geometry.LocationOfEvaluationUpperLimit]"""
        temp = pythonnet_property_get(
            self.wrapped, "LocationOfEvaluationUpperLimitForZeroTipRelief"
        )

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationUpperLimit.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @location_of_evaluation_upper_limit_for_zero_tip_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def location_of_evaluation_upper_limit_for_zero_tip_relief(
        self: "Self", value: "_665.LocationOfEvaluationUpperLimit"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationUpperLimit.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(
            self.wrapped, "LocationOfEvaluationUpperLimitForZeroTipRelief", value
        )

    @property
    @exception_bridge
    def location_of_root_modification_start(
        self: "Self",
    ) -> (
        "enum_with_selected_value.EnumWithSelectedValue_LocationOfRootReliefEvaluation"
    ):
        """EnumWithSelectedValue[mastapy.gears.micro_geometry.LocationOfRootReliefEvaluation]"""
        temp = pythonnet_property_get(self.wrapped, "LocationOfRootModificationStart")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_LocationOfRootReliefEvaluation.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @location_of_root_modification_start.setter
    @exception_bridge
    @enforce_parameter_types
    def location_of_root_modification_start(
        self: "Self", value: "_666.LocationOfRootReliefEvaluation"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LocationOfRootReliefEvaluation.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "LocationOfRootModificationStart", value)

    @property
    @exception_bridge
    def location_of_root_relief_evaluation(
        self: "Self",
    ) -> (
        "enum_with_selected_value.EnumWithSelectedValue_LocationOfRootReliefEvaluation"
    ):
        """EnumWithSelectedValue[mastapy.gears.micro_geometry.LocationOfRootReliefEvaluation]"""
        temp = pythonnet_property_get(self.wrapped, "LocationOfRootReliefEvaluation")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_LocationOfRootReliefEvaluation.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @location_of_root_relief_evaluation.setter
    @exception_bridge
    @enforce_parameter_types
    def location_of_root_relief_evaluation(
        self: "Self", value: "_666.LocationOfRootReliefEvaluation"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LocationOfRootReliefEvaluation.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "LocationOfRootReliefEvaluation", value)

    @property
    @exception_bridge
    def location_of_tip_relief_evaluation(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_LocationOfTipReliefEvaluation":
        """EnumWithSelectedValue[mastapy.gears.micro_geometry.LocationOfTipReliefEvaluation]"""
        temp = pythonnet_property_get(self.wrapped, "LocationOfTipReliefEvaluation")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_LocationOfTipReliefEvaluation.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @location_of_tip_relief_evaluation.setter
    @exception_bridge
    @enforce_parameter_types
    def location_of_tip_relief_evaluation(
        self: "Self", value: "_667.LocationOfTipReliefEvaluation"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LocationOfTipReliefEvaluation.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "LocationOfTipReliefEvaluation", value)

    @property
    @exception_bridge
    def location_of_tip_relief_start(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_LocationOfTipReliefEvaluation":
        """EnumWithSelectedValue[mastapy.gears.micro_geometry.LocationOfTipReliefEvaluation]"""
        temp = pythonnet_property_get(self.wrapped, "LocationOfTipReliefStart")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_LocationOfTipReliefEvaluation.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @location_of_tip_relief_start.setter
    @exception_bridge
    @enforce_parameter_types
    def location_of_tip_relief_start(
        self: "Self", value: "_667.LocationOfTipReliefEvaluation"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LocationOfTipReliefEvaluation.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "LocationOfTipReliefStart", value)

    @property
    @exception_bridge
    def main_profile_modification_ends_at_the_start_of_root_relief(
        self: "Self",
    ) -> "_668.MainProfileReliefEndsAtTheStartOfRootReliefOption":
        """mastapy.gears.micro_geometry.MainProfileReliefEndsAtTheStartOfRootReliefOption"""
        temp = pythonnet_property_get(
            self.wrapped, "MainProfileModificationEndsAtTheStartOfRootRelief"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.MicroGeometry.MainProfileReliefEndsAtTheStartOfRootReliefOption",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.micro_geometry._668",
            "MainProfileReliefEndsAtTheStartOfRootReliefOption",
        )(value)

    @main_profile_modification_ends_at_the_start_of_root_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def main_profile_modification_ends_at_the_start_of_root_relief(
        self: "Self", value: "_668.MainProfileReliefEndsAtTheStartOfRootReliefOption"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.MicroGeometry.MainProfileReliefEndsAtTheStartOfRootReliefOption",
        )
        pythonnet_property_set(
            self.wrapped, "MainProfileModificationEndsAtTheStartOfRootRelief", value
        )

    @property
    @exception_bridge
    def main_profile_modification_ends_at_the_start_of_tip_relief(
        self: "Self",
    ) -> "_669.MainProfileReliefEndsAtTheStartOfTipReliefOption":
        """mastapy.gears.micro_geometry.MainProfileReliefEndsAtTheStartOfTipReliefOption"""
        temp = pythonnet_property_get(
            self.wrapped, "MainProfileModificationEndsAtTheStartOfTipRelief"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.MicroGeometry.MainProfileReliefEndsAtTheStartOfTipReliefOption",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.micro_geometry._669",
            "MainProfileReliefEndsAtTheStartOfTipReliefOption",
        )(value)

    @main_profile_modification_ends_at_the_start_of_tip_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def main_profile_modification_ends_at_the_start_of_tip_relief(
        self: "Self", value: "_669.MainProfileReliefEndsAtTheStartOfTipReliefOption"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.MicroGeometry.MainProfileReliefEndsAtTheStartOfTipReliefOption",
        )
        pythonnet_property_set(
            self.wrapped, "MainProfileModificationEndsAtTheStartOfTipRelief", value
        )

    @property
    @exception_bridge
    def measure_root_reliefs_from_extrapolated_linear_relief(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "MeasureRootReliefsFromExtrapolatedLinearRelief"
        )

        if temp is None:
            return False

        return temp

    @measure_root_reliefs_from_extrapolated_linear_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def measure_root_reliefs_from_extrapolated_linear_relief(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MeasureRootReliefsFromExtrapolatedLinearRelief",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def measure_tip_reliefs_from_extrapolated_linear_relief(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "MeasureTipReliefsFromExtrapolatedLinearRelief"
        )

        if temp is None:
            return False

        return temp

    @measure_tip_reliefs_from_extrapolated_linear_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def measure_tip_reliefs_from_extrapolated_linear_relief(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MeasureTipReliefsFromExtrapolatedLinearRelief",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def measured_data(self: "Self") -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "MeasuredData")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @measured_data.setter
    @exception_bridge
    @enforce_parameter_types
    def measured_data(self: "Self", value: "_1718.Vector2DListAccessor") -> None:
        pythonnet_property_set(self.wrapped, "MeasuredData", value.wrapped)

    @property
    @exception_bridge
    def parabolic_root_relief(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ParabolicRootRelief")

        if temp is None:
            return 0.0

        return temp

    @parabolic_root_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def parabolic_root_relief(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ParabolicRootRelief",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def parabolic_root_relief_starts_tangent_to_main_profile_relief(
        self: "Self",
    ) -> "_671.ParabolicRootReliefStartsTangentToMainProfileRelief":
        """mastapy.gears.micro_geometry.ParabolicRootReliefStartsTangentToMainProfileRelief"""
        temp = pythonnet_property_get(
            self.wrapped, "ParabolicRootReliefStartsTangentToMainProfileRelief"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.MicroGeometry.ParabolicRootReliefStartsTangentToMainProfileRelief",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.micro_geometry._671",
            "ParabolicRootReliefStartsTangentToMainProfileRelief",
        )(value)

    @parabolic_root_relief_starts_tangent_to_main_profile_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def parabolic_root_relief_starts_tangent_to_main_profile_relief(
        self: "Self", value: "_671.ParabolicRootReliefStartsTangentToMainProfileRelief"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.MicroGeometry.ParabolicRootReliefStartsTangentToMainProfileRelief",
        )
        pythonnet_property_set(
            self.wrapped, "ParabolicRootReliefStartsTangentToMainProfileRelief", value
        )

    @property
    @exception_bridge
    def parabolic_tip_relief(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ParabolicTipRelief")

        if temp is None:
            return 0.0

        return temp

    @parabolic_tip_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def parabolic_tip_relief(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ParabolicTipRelief",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def parabolic_tip_relief_starts_tangent_to_main_profile_relief(
        self: "Self",
    ) -> "_672.ParabolicTipReliefStartsTangentToMainProfileRelief":
        """mastapy.gears.micro_geometry.ParabolicTipReliefStartsTangentToMainProfileRelief"""
        temp = pythonnet_property_get(
            self.wrapped, "ParabolicTipReliefStartsTangentToMainProfileRelief"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.MicroGeometry.ParabolicTipReliefStartsTangentToMainProfileRelief",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.micro_geometry._672",
            "ParabolicTipReliefStartsTangentToMainProfileRelief",
        )(value)

    @parabolic_tip_relief_starts_tangent_to_main_profile_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def parabolic_tip_relief_starts_tangent_to_main_profile_relief(
        self: "Self", value: "_672.ParabolicTipReliefStartsTangentToMainProfileRelief"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.MicroGeometry.ParabolicTipReliefStartsTangentToMainProfileRelief",
        )
        pythonnet_property_set(
            self.wrapped, "ParabolicTipReliefStartsTangentToMainProfileRelief", value
        )

    @property
    @exception_bridge
    def start_of_linear_root_relief_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StartOfLinearRootReliefFactor")

        if temp is None:
            return 0.0

        return temp

    @start_of_linear_root_relief_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def start_of_linear_root_relief_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StartOfLinearRootReliefFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def start_of_linear_tip_relief_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StartOfLinearTipReliefFactor")

        if temp is None:
            return 0.0

        return temp

    @start_of_linear_tip_relief_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def start_of_linear_tip_relief_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StartOfLinearTipReliefFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def start_of_parabolic_root_relief_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StartOfParabolicRootReliefFactor")

        if temp is None:
            return 0.0

        return temp

    @start_of_parabolic_root_relief_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def start_of_parabolic_root_relief_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StartOfParabolicRootReliefFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def start_of_parabolic_tip_relief_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StartOfParabolicTipReliefFactor")

        if temp is None:
            return 0.0

        return temp

    @start_of_parabolic_tip_relief_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def start_of_parabolic_tip_relief_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StartOfParabolicTipReliefFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def use_measured_data(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseMeasuredData")

        if temp is None:
            return False

        return temp

    @use_measured_data.setter
    @exception_bridge
    @enforce_parameter_types
    def use_measured_data(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "UseMeasuredData", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def use_user_specified_barrelling_peak_point(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseUserSpecifiedBarrellingPeakPoint"
        )

        if temp is None:
            return False

        return temp

    @use_user_specified_barrelling_peak_point.setter
    @exception_bridge
    @enforce_parameter_types
    def use_user_specified_barrelling_peak_point(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseUserSpecifiedBarrellingPeakPoint",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ProfileModification":
        """Cast to another type.

        Returns:
            _Cast_ProfileModification
        """
        return _Cast_ProfileModification(self)
