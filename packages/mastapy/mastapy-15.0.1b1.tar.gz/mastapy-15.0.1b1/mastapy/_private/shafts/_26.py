"""ShaftMaterialForReports"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
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

_SHAFT_MATERIAL_FOR_REPORTS = python_net_import(
    "SMT.MastaAPI.Shafts", "ShaftMaterialForReports"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.shafts import _6, _7, _8, _11, _12, _24

    Self = TypeVar("Self", bound="ShaftMaterialForReports")
    CastSelf = TypeVar(
        "CastSelf", bound="ShaftMaterialForReports._Cast_ShaftMaterialForReports"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftMaterialForReports",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftMaterialForReports:
    """Special nested class for casting ShaftMaterialForReports to subclasses."""

    __parent__: "ShaftMaterialForReports"

    @property
    def shaft_material_for_reports(self: "CastSelf") -> "ShaftMaterialForReports":
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
class ShaftMaterialForReports(_0.APIBase):
    """ShaftMaterialForReports

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_MATERIAL_FOR_REPORTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def casting_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CastingFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @casting_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def casting_factor(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CastingFactor", value)

    @property
    @exception_bridge
    def casting_factor_condition(self: "Self") -> "_7.CastingFactorCondition":
        """mastapy.shafts.CastingFactorCondition"""
        temp = pythonnet_property_get(self.wrapped, "CastingFactorCondition")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Shafts.CastingFactorCondition"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.shafts._7", "CastingFactorCondition"
        )(value)

    @casting_factor_condition.setter
    @exception_bridge
    @enforce_parameter_types
    def casting_factor_condition(
        self: "Self", value: "_7.CastingFactorCondition"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Shafts.CastingFactorCondition"
        )
        pythonnet_property_set(self.wrapped, "CastingFactorCondition", value)

    @property
    @exception_bridge
    def consequence_of_failure(self: "Self") -> "_8.ConsequenceOfFailure":
        """mastapy.shafts.ConsequenceOfFailure"""
        temp = pythonnet_property_get(self.wrapped, "ConsequenceOfFailure")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Shafts.ConsequenceOfFailure"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.shafts._8", "ConsequenceOfFailure"
        )(value)

    @consequence_of_failure.setter
    @exception_bridge
    @enforce_parameter_types
    def consequence_of_failure(self: "Self", value: "_8.ConsequenceOfFailure") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Shafts.ConsequenceOfFailure"
        )
        pythonnet_property_set(self.wrapped, "ConsequenceOfFailure", value)

    @property
    @exception_bridge
    def constant_rpmax(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ConstantRpmax")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @constant_rpmax.setter
    @exception_bridge
    @enforce_parameter_types
    def constant_rpmax(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ConstantRpmax", value)

    @property
    @exception_bridge
    def curve_model(self: "Self") -> "_12.FkmSnCurveModel":
        """mastapy.shafts.FkmSnCurveModel"""
        temp = pythonnet_property_get(self.wrapped, "CurveModel")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Shafts.FkmSnCurveModel")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.shafts._12", "FkmSnCurveModel"
        )(value)

    @curve_model.setter
    @exception_bridge
    @enforce_parameter_types
    def curve_model(self: "Self", value: "_12.FkmSnCurveModel") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.Shafts.FkmSnCurveModel")
        pythonnet_property_set(self.wrapped, "CurveModel", value)

    @property
    @exception_bridge
    def endurance_limit(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "EnduranceLimit")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @endurance_limit.setter
    @exception_bridge
    @enforce_parameter_types
    def endurance_limit(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "EnduranceLimit", value)

    @property
    @exception_bridge
    def factor_to_second_knee_point(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FactorToSecondKneePoint")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def fatigue_strength_factor_for_normal_stress(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "FatigueStrengthFactorForNormalStress"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @fatigue_strength_factor_for_normal_stress.setter
    @exception_bridge
    @enforce_parameter_types
    def fatigue_strength_factor_for_normal_stress(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "FatigueStrengthFactorForNormalStress", value
        )

    @property
    @exception_bridge
    def fatigue_strength_factor_for_shear_stress(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "FatigueStrengthFactorForShearStress"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @fatigue_strength_factor_for_shear_stress.setter
    @exception_bridge
    @enforce_parameter_types
    def fatigue_strength_factor_for_shear_stress(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "FatigueStrengthFactorForShearStress", value
        )

    @property
    @exception_bridge
    def fatigue_strength_under_reversed_bending_stresses(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "FatigueStrengthUnderReversedBendingStresses"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @fatigue_strength_under_reversed_bending_stresses.setter
    @exception_bridge
    @enforce_parameter_types
    def fatigue_strength_under_reversed_bending_stresses(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "FatigueStrengthUnderReversedBendingStresses", value
        )

    @property
    @exception_bridge
    def fatigue_strength_under_reversed_compression_tension_stresses(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "FatigueStrengthUnderReversedCompressionTensionStresses"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @fatigue_strength_under_reversed_compression_tension_stresses.setter
    @exception_bridge
    @enforce_parameter_types
    def fatigue_strength_under_reversed_compression_tension_stresses(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped,
            "FatigueStrengthUnderReversedCompressionTensionStresses",
            value,
        )

    @property
    @exception_bridge
    def fatigue_strength_under_reversed_torsional_stresses(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "FatigueStrengthUnderReversedTorsionalStresses"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @fatigue_strength_under_reversed_torsional_stresses.setter
    @exception_bridge
    @enforce_parameter_types
    def fatigue_strength_under_reversed_torsional_stresses(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "FatigueStrengthUnderReversedTorsionalStresses", value
        )

    @property
    @exception_bridge
    def first_exponent(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FirstExponent")

        if temp is None:
            return 0.0

        return temp

    @first_exponent.setter
    @exception_bridge
    @enforce_parameter_types
    def first_exponent(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FirstExponent", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def hardening_type_for_agma60016101e08(self: "Self") -> "_6.AGMAHardeningType":
        """mastapy.shafts.AGMAHardeningType"""
        temp = pythonnet_property_get(self.wrapped, "HardeningTypeForAGMA60016101E08")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Shafts.AGMAHardeningType")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.shafts._6", "AGMAHardeningType"
        )(value)

    @hardening_type_for_agma60016101e08.setter
    @exception_bridge
    @enforce_parameter_types
    def hardening_type_for_agma60016101e08(
        self: "Self", value: "_6.AGMAHardeningType"
    ) -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.Shafts.AGMAHardeningType")
        pythonnet_property_set(self.wrapped, "HardeningTypeForAGMA60016101E08", value)

    @property
    @exception_bridge
    def has_hard_surface(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "HasHardSurface")

        if temp is None:
            return False

        return temp

    @has_hard_surface.setter
    @exception_bridge
    @enforce_parameter_types
    def has_hard_surface(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "HasHardSurface", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def is_regularly_inspected(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsRegularlyInspected")

        if temp is None:
            return False

        return temp

    @is_regularly_inspected.setter
    @exception_bridge
    @enforce_parameter_types
    def is_regularly_inspected(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IsRegularlyInspected",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def load_safety_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LoadSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @load_safety_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def load_safety_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "LoadSafetyFactor", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def lower_limit_of_the_effective_damage_sum(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "LowerLimitOfTheEffectiveDamageSum")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @lower_limit_of_the_effective_damage_sum.setter
    @exception_bridge
    @enforce_parameter_types
    def lower_limit_of_the_effective_damage_sum(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "LowerLimitOfTheEffectiveDamageSum", value)

    @property
    @exception_bridge
    def material_fatigue_limit(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MaterialFatigueLimit")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @material_fatigue_limit.setter
    @exception_bridge
    @enforce_parameter_types
    def material_fatigue_limit(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MaterialFatigueLimit", value)

    @property
    @exception_bridge
    def material_fatigue_limit_shear(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MaterialFatigueLimitShear")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @material_fatigue_limit_shear.setter
    @exception_bridge
    @enforce_parameter_types
    def material_fatigue_limit_shear(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MaterialFatigueLimitShear", value)

    @property
    @exception_bridge
    def material_group(self: "Self") -> "_11.FkmMaterialGroup":
        """mastapy.shafts.FkmMaterialGroup"""
        temp = pythonnet_property_get(self.wrapped, "MaterialGroup")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Shafts.FkmMaterialGroup")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.shafts._11", "FkmMaterialGroup"
        )(value)

    @material_group.setter
    @exception_bridge
    @enforce_parameter_types
    def material_group(self: "Self", value: "_11.FkmMaterialGroup") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.Shafts.FkmMaterialGroup")
        pythonnet_property_set(self.wrapped, "MaterialGroup", value)

    @property
    @exception_bridge
    def material_safety_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MaterialSafetyFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @material_safety_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def material_safety_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MaterialSafetyFactor", value)

    @property
    @exception_bridge
    def number_of_cycles_at_knee_point(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfCyclesAtKneePoint")

        if temp is None:
            return 0.0

        return temp

    @number_of_cycles_at_knee_point.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_cycles_at_knee_point(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfCyclesAtKneePoint",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def number_of_cycles_at_second_knee_point(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfCyclesAtSecondKneePoint")

        if temp is None:
            return 0.0

        return temp

    @number_of_cycles_at_second_knee_point.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_cycles_at_second_knee_point(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfCyclesAtSecondKneePoint",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def second_exponent(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SecondExponent")

        if temp is None:
            return 0.0

        return temp

    @second_exponent.setter
    @exception_bridge
    @enforce_parameter_types
    def second_exponent(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "SecondExponent", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def temperature_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TemperatureFactor")

        if temp is None:
            return 0.0

        return temp

    @temperature_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def temperature_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TemperatureFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def tensile_yield_strength(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TensileYieldStrength")

        if temp is None:
            return 0.0

        return temp

    @tensile_yield_strength.setter
    @exception_bridge
    @enforce_parameter_types
    def tensile_yield_strength(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TensileYieldStrength",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def total_safety_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "TotalSafetyFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @total_safety_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def total_safety_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "TotalSafetyFactor", value)

    @property
    @exception_bridge
    def use_custom_sn_curve(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseCustomSNCurve")

        if temp is None:
            return False

        return temp

    @use_custom_sn_curve.setter
    @exception_bridge
    @enforce_parameter_types
    def use_custom_sn_curve(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseCustomSNCurve",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def material_details(self: "Self") -> "_24.ShaftMaterial":
        """mastapy.shafts.ShaftMaterial

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaterialDetails")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @exception_bridge
    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputDefaultReportTo", file_path)

    @exception_bridge
    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportTo", file_path)

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportAsTextTo", file_path)

    @exception_bridge
    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftMaterialForReports":
        """Cast to another type.

        Returns:
            _Cast_ShaftMaterialForReports
        """
        return _Cast_ShaftMaterialForReports(self)
