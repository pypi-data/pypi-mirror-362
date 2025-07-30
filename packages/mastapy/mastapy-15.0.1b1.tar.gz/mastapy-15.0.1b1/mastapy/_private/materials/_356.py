"""LubricationDetail"""

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
from mastapy._private._internal.implicit import enum_with_selected_value, overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.materials import _350, _354
from mastapy._private.utility.databases import _2028

_LUBRICATION_DETAIL = python_net_import("SMT.MastaAPI.Materials", "LubricationDetail")

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.materials import (
        _326,
        _331,
        _339,
        _346,
        _349,
        _351,
        _352,
        _353,
        _355,
        _365,
        _366,
    )
    from mastapy._private.math_utility import _1718

    Self = TypeVar("Self", bound="LubricationDetail")
    CastSelf = TypeVar("CastSelf", bound="LubricationDetail._Cast_LubricationDetail")


__docformat__ = "restructuredtext en"
__all__ = ("LubricationDetail",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LubricationDetail:
    """Special nested class for casting LubricationDetail to subclasses."""

    __parent__: "LubricationDetail"

    @property
    def named_database_item(self: "CastSelf") -> "_2028.NamedDatabaseItem":
        return self.__parent__._cast(_2028.NamedDatabaseItem)

    @property
    def lubrication_detail(self: "CastSelf") -> "LubricationDetail":
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
class LubricationDetail(_2028.NamedDatabaseItem):
    """LubricationDetail

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LUBRICATION_DETAIL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def agma925a03_lubricant_type(self: "Self") -> "_326.AGMALubricantType":
        """mastapy.materials.AGMALubricantType"""
        temp = pythonnet_property_get(self.wrapped, "AGMA925A03LubricantType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Materials.AGMALubricantType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials._326", "AGMALubricantType"
        )(value)

    @agma925a03_lubricant_type.setter
    @exception_bridge
    @enforce_parameter_types
    def agma925a03_lubricant_type(
        self: "Self", value: "_326.AGMALubricantType"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Materials.AGMALubricantType"
        )
        pythonnet_property_set(self.wrapped, "AGMA925A03LubricantType", value)

    @property
    @exception_bridge
    def air_flow_velocity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AirFlowVelocity")

        if temp is None:
            return 0.0

        return temp

    @air_flow_velocity.setter
    @exception_bridge
    @enforce_parameter_types
    def air_flow_velocity(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "AirFlowVelocity", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def contamination_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ContaminationFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @contamination_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def contamination_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ContaminationFactor", value)

    @property
    @exception_bridge
    def delivery(self: "Self") -> "_351.LubricantDelivery":
        """mastapy.materials.LubricantDelivery

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Delivery")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Materials.LubricantDelivery"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials._351", "LubricantDelivery"
        )(value)

    @property
    @exception_bridge
    def density(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Density")

        if temp is None:
            return 0.0

        return temp

    @density.setter
    @exception_bridge
    @enforce_parameter_types
    def density(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Density", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def density_specification_method(self: "Self") -> "_339.DensitySpecificationMethod":
        """mastapy.materials.DensitySpecificationMethod"""
        temp = pythonnet_property_get(self.wrapped, "DensitySpecificationMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Materials.DensitySpecificationMethod"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials._339", "DensitySpecificationMethod"
        )(value)

    @density_specification_method.setter
    @exception_bridge
    @enforce_parameter_types
    def density_specification_method(
        self: "Self", value: "_339.DensitySpecificationMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Materials.DensitySpecificationMethod"
        )
        pythonnet_property_set(self.wrapped, "DensitySpecificationMethod", value)

    @property
    @exception_bridge
    def density_vs_temperature(self: "Self") -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "DensityVsTemperature")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @density_vs_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def density_vs_temperature(
        self: "Self", value: "_1718.Vector2DListAccessor"
    ) -> None:
        pythonnet_property_set(self.wrapped, "DensityVsTemperature", value.wrapped)

    @property
    @exception_bridge
    def dynamic_viscosity_at_38c(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicViscosityAt38C")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def dynamic_viscosity_of_the_lubricant_at_100_degrees_c(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "DynamicViscosityOfTheLubricantAt100DegreesC"
        )

        if temp is None:
            return 0.0

        return temp

    @dynamic_viscosity_of_the_lubricant_at_100_degrees_c.setter
    @exception_bridge
    @enforce_parameter_types
    def dynamic_viscosity_of_the_lubricant_at_100_degrees_c(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "DynamicViscosityOfTheLubricantAt100DegreesC",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def dynamic_viscosity_of_the_lubricant_at_40_degrees_c(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "DynamicViscosityOfTheLubricantAt40DegreesC"
        )

        if temp is None:
            return 0.0

        return temp

    @dynamic_viscosity_of_the_lubricant_at_40_degrees_c.setter
    @exception_bridge
    @enforce_parameter_types
    def dynamic_viscosity_of_the_lubricant_at_40_degrees_c(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "DynamicViscosityOfTheLubricantAt40DegreesC",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def ep_additives_proven_with_severe_contamination(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "EPAdditivesProvenWithSevereContamination"
        )

        if temp is None:
            return False

        return temp

    @ep_additives_proven_with_severe_contamination.setter
    @exception_bridge
    @enforce_parameter_types
    def ep_additives_proven_with_severe_contamination(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "EPAdditivesProvenWithSevereContamination",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def ep_and_aw_additives_present(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "EPAndAWAdditivesPresent")

        if temp is None:
            return False

        return temp

    @ep_and_aw_additives_present.setter
    @exception_bridge
    @enforce_parameter_types
    def ep_and_aw_additives_present(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EPAndAWAdditivesPresent",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def factor_for_newly_greased_bearings(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FactorForNewlyGreasedBearings")

        if temp is None:
            return 0.0

        return temp

    @factor_for_newly_greased_bearings.setter
    @exception_bridge
    @enforce_parameter_types
    def factor_for_newly_greased_bearings(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FactorForNewlyGreasedBearings",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def grease_contamination_level(self: "Self") -> "_346.GreaseContaminationOptions":
        """mastapy.materials.GreaseContaminationOptions"""
        temp = pythonnet_property_get(self.wrapped, "GreaseContaminationLevel")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Materials.GreaseContaminationOptions"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials._346", "GreaseContaminationOptions"
        )(value)

    @grease_contamination_level.setter
    @exception_bridge
    @enforce_parameter_types
    def grease_contamination_level(
        self: "Self", value: "_346.GreaseContaminationOptions"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Materials.GreaseContaminationOptions"
        )
        pythonnet_property_set(self.wrapped, "GreaseContaminationLevel", value)

    @property
    @exception_bridge
    def heat_transfer_coefficient(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "HeatTransferCoefficient")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @heat_transfer_coefficient.setter
    @exception_bridge
    @enforce_parameter_types
    def heat_transfer_coefficient(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "HeatTransferCoefficient", value)

    @property
    @exception_bridge
    def iso_lubricant_type(self: "Self") -> "_349.ISOLubricantType":
        """mastapy.materials.ISOLubricantType"""
        temp = pythonnet_property_get(self.wrapped, "ISOLubricantType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Materials.ISOLubricantType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials._349", "ISOLubricantType"
        )(value)

    @iso_lubricant_type.setter
    @exception_bridge
    @enforce_parameter_types
    def iso_lubricant_type(self: "Self", value: "_349.ISOLubricantType") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Materials.ISOLubricantType"
        )
        pythonnet_property_set(self.wrapped, "ISOLubricantType", value)

    @property
    @exception_bridge
    def kinematic_viscosity_at_38c(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "KinematicViscosityAt38C")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def kinematic_viscosity_of_the_lubricant_at_100_degrees_c(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "KinematicViscosityOfTheLubricantAt100DegreesC"
        )

        if temp is None:
            return 0.0

        return temp

    @kinematic_viscosity_of_the_lubricant_at_100_degrees_c.setter
    @exception_bridge
    @enforce_parameter_types
    def kinematic_viscosity_of_the_lubricant_at_100_degrees_c(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "KinematicViscosityOfTheLubricantAt100DegreesC",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def kinematic_viscosity_of_the_lubricant_at_40_degrees_c(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "KinematicViscosityOfTheLubricantAt40DegreesC"
        )

        if temp is None:
            return 0.0

        return temp

    @kinematic_viscosity_of_the_lubricant_at_40_degrees_c.setter
    @exception_bridge
    @enforce_parameter_types
    def kinematic_viscosity_of_the_lubricant_at_40_degrees_c(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "KinematicViscosityOfTheLubricantAt40DegreesC",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def lubricant_definition(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_LubricantDefinition":
        """EnumWithSelectedValue[mastapy.materials.LubricantDefinition]"""
        temp = pythonnet_property_get(self.wrapped, "LubricantDefinition")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_LubricantDefinition.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @lubricant_definition.setter
    @exception_bridge
    @enforce_parameter_types
    def lubricant_definition(self: "Self", value: "_350.LubricantDefinition") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LubricantDefinition.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "LubricantDefinition", value)

    @property
    @exception_bridge
    def lubricant_grade_agma(self: "Self") -> "_352.LubricantViscosityClassAGMA":
        """mastapy.materials.LubricantViscosityClassAGMA"""
        temp = pythonnet_property_get(self.wrapped, "LubricantGradeAGMA")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Materials.LubricantViscosityClassAGMA"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials._352", "LubricantViscosityClassAGMA"
        )(value)

    @lubricant_grade_agma.setter
    @exception_bridge
    @enforce_parameter_types
    def lubricant_grade_agma(
        self: "Self", value: "_352.LubricantViscosityClassAGMA"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Materials.LubricantViscosityClassAGMA"
        )
        pythonnet_property_set(self.wrapped, "LubricantGradeAGMA", value)

    @property
    @exception_bridge
    def lubricant_grade_iso(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_LubricantViscosityClassISO":
        """EnumWithSelectedValue[mastapy.materials.LubricantViscosityClassISO]"""
        temp = pythonnet_property_get(self.wrapped, "LubricantGradeISO")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_LubricantViscosityClassISO.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @lubricant_grade_iso.setter
    @exception_bridge
    @enforce_parameter_types
    def lubricant_grade_iso(
        self: "Self", value: "_354.LubricantViscosityClassISO"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LubricantViscosityClassISO.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "LubricantGradeISO", value)

    @property
    @exception_bridge
    def lubricant_grade_sae(self: "Self") -> "_355.LubricantViscosityClassSAE":
        """mastapy.materials.LubricantViscosityClassSAE"""
        temp = pythonnet_property_get(self.wrapped, "LubricantGradeSAE")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Materials.LubricantViscosityClassSAE"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials._355", "LubricantViscosityClassSAE"
        )(value)

    @lubricant_grade_sae.setter
    @exception_bridge
    @enforce_parameter_types
    def lubricant_grade_sae(
        self: "Self", value: "_355.LubricantViscosityClassSAE"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Materials.LubricantViscosityClassSAE"
        )
        pythonnet_property_set(self.wrapped, "LubricantGradeSAE", value)

    @property
    @exception_bridge
    def lubricant_shear_modulus(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LubricantShearModulus")

        if temp is None:
            return 0.0

        return temp

    @lubricant_shear_modulus.setter
    @exception_bridge
    @enforce_parameter_types
    def lubricant_shear_modulus(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LubricantShearModulus",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def lubricant_type_and_supply(self: "Self") -> "_331.BearingLubricationCondition":
        """mastapy.materials.BearingLubricationCondition"""
        temp = pythonnet_property_get(self.wrapped, "LubricantTypeAndSupply")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Materials.BearingLubricationCondition"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials._331", "BearingLubricationCondition"
        )(value)

    @lubricant_type_and_supply.setter
    @exception_bridge
    @enforce_parameter_types
    def lubricant_type_and_supply(
        self: "Self", value: "_331.BearingLubricationCondition"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Materials.BearingLubricationCondition"
        )
        pythonnet_property_set(self.wrapped, "LubricantTypeAndSupply", value)

    @property
    @exception_bridge
    def lubricant_viscosity_classification(
        self: "Self",
    ) -> "_353.LubricantViscosityClassification":
        """mastapy.materials.LubricantViscosityClassification"""
        temp = pythonnet_property_get(self.wrapped, "LubricantViscosityClassification")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Materials.LubricantViscosityClassification"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials._353", "LubricantViscosityClassification"
        )(value)

    @lubricant_viscosity_classification.setter
    @exception_bridge
    @enforce_parameter_types
    def lubricant_viscosity_classification(
        self: "Self", value: "_353.LubricantViscosityClassification"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Materials.LubricantViscosityClassification"
        )
        pythonnet_property_set(self.wrapped, "LubricantViscosityClassification", value)

    @property
    @exception_bridge
    def micropitting_failure_load_stage(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "MicropittingFailureLoadStage")

        if temp is None:
            return 0

        return temp

    @micropitting_failure_load_stage.setter
    @exception_bridge
    @enforce_parameter_types
    def micropitting_failure_load_stage(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MicropittingFailureLoadStage",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def micropitting_failure_load_stage_test_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MicropittingFailureLoadStageTestTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @micropitting_failure_load_stage_test_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def micropitting_failure_load_stage_test_temperature(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MicropittingFailureLoadStageTestTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def oil_filtration_and_contamination(self: "Self") -> "_365.OilFiltrationOptions":
        """mastapy.materials.OilFiltrationOptions"""
        temp = pythonnet_property_get(self.wrapped, "OilFiltrationAndContamination")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Materials.OilFiltrationOptions"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials._365", "OilFiltrationOptions"
        )(value)

    @oil_filtration_and_contamination.setter
    @exception_bridge
    @enforce_parameter_types
    def oil_filtration_and_contamination(
        self: "Self", value: "_365.OilFiltrationOptions"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Materials.OilFiltrationOptions"
        )
        pythonnet_property_set(self.wrapped, "OilFiltrationAndContamination", value)

    @property
    @exception_bridge
    def oil_to_air_heat_transfer_area(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OilToAirHeatTransferArea")

        if temp is None:
            return 0.0

        return temp

    @oil_to_air_heat_transfer_area.setter
    @exception_bridge
    @enforce_parameter_types
    def oil_to_air_heat_transfer_area(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OilToAirHeatTransferArea",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def pressure_viscosity_coefficient(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PressureViscosityCoefficient")

        if temp is None:
            return 0.0

        return temp

    @pressure_viscosity_coefficient.setter
    @exception_bridge
    @enforce_parameter_types
    def pressure_viscosity_coefficient(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PressureViscosityCoefficient",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def pressure_viscosity_coefficient_method(
        self: "Self",
    ) -> "_366.PressureViscosityCoefficientMethod":
        """mastapy.materials.PressureViscosityCoefficientMethod"""
        temp = pythonnet_property_get(
            self.wrapped, "PressureViscosityCoefficientMethod"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Materials.PressureViscosityCoefficientMethod"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials._366", "PressureViscosityCoefficientMethod"
        )(value)

    @pressure_viscosity_coefficient_method.setter
    @exception_bridge
    @enforce_parameter_types
    def pressure_viscosity_coefficient_method(
        self: "Self", value: "_366.PressureViscosityCoefficientMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Materials.PressureViscosityCoefficientMethod"
        )
        pythonnet_property_set(
            self.wrapped, "PressureViscosityCoefficientMethod", value
        )

    @property
    @exception_bridge
    def scuffing_failure_load_stage(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "ScuffingFailureLoadStage")

        if temp is None:
            return 0

        return temp

    @scuffing_failure_load_stage.setter
    @exception_bridge
    @enforce_parameter_types
    def scuffing_failure_load_stage(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ScuffingFailureLoadStage",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def specific_heat_capacity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpecificHeatCapacity")

        if temp is None:
            return 0.0

        return temp

    @specific_heat_capacity.setter
    @exception_bridge
    @enforce_parameter_types
    def specific_heat_capacity(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecificHeatCapacity",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def specified_parameter_k(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpecifiedParameterK")

        if temp is None:
            return 0.0

        return temp

    @specified_parameter_k.setter
    @exception_bridge
    @enforce_parameter_types
    def specified_parameter_k(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifiedParameterK",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def specified_parameter_s(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpecifiedParameterS")

        if temp is None:
            return 0.0

        return temp

    @specified_parameter_s.setter
    @exception_bridge
    @enforce_parameter_types
    def specified_parameter_s(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifiedParameterS",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def temperature_at_which_density_is_specified(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "TemperatureAtWhichDensityIsSpecified"
        )

        if temp is None:
            return 0.0

        return temp

    @temperature_at_which_density_is_specified.setter
    @exception_bridge
    @enforce_parameter_types
    def temperature_at_which_density_is_specified(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TemperatureAtWhichDensityIsSpecified",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def temperature_at_which_pressure_viscosity_coefficient_is_specified(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "TemperatureAtWhichPressureViscosityCoefficientIsSpecified"
        )

        if temp is None:
            return 0.0

        return temp

    @temperature_at_which_pressure_viscosity_coefficient_is_specified.setter
    @exception_bridge
    @enforce_parameter_types
    def temperature_at_which_pressure_viscosity_coefficient_is_specified(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "TemperatureAtWhichPressureViscosityCoefficientIsSpecified",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def thermal_conductivity(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ThermalConductivity")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @thermal_conductivity.setter
    @exception_bridge
    @enforce_parameter_types
    def thermal_conductivity(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ThermalConductivity", value)

    @exception_bridge
    @enforce_parameter_types
    def dynamic_viscosity_at(self: "Self", temperature: "float") -> "float":
        """float

        Args:
            temperature (float)
        """
        temperature = float(temperature)
        method_result = pythonnet_method_call(
            self.wrapped, "DynamicViscosityAt", temperature if temperature else 0.0
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def kinematic_viscosity_at(self: "Self", temperature: "float") -> "float":
        """float

        Args:
            temperature (float)
        """
        temperature = float(temperature)
        method_result = pythonnet_method_call(
            self.wrapped, "KinematicViscosityAt", temperature if temperature else 0.0
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def lubricant_density_at(self: "Self", temperature: "float") -> "float":
        """float

        Args:
            temperature (float)
        """
        temperature = float(temperature)
        method_result = pythonnet_method_call(
            self.wrapped, "LubricantDensityAt", temperature if temperature else 0.0
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_LubricationDetail":
        """Cast to another type.

        Returns:
            _Cast_LubricationDetail
        """
        return _Cast_LubricationDetail(self)
