"""TransmissionEfficiencySettings"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
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
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears import _422

_TRANSMISSION_EFFICIENCY_SETTINGS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "TransmissionEfficiencySettings",
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    Self = TypeVar("Self", bound="TransmissionEfficiencySettings")
    CastSelf = TypeVar(
        "CastSelf",
        bound="TransmissionEfficiencySettings._Cast_TransmissionEfficiencySettings",
    )


__docformat__ = "restructuredtext en"
__all__ = ("TransmissionEfficiencySettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TransmissionEfficiencySettings:
    """Special nested class for casting TransmissionEfficiencySettings to subclasses."""

    __parent__: "TransmissionEfficiencySettings"

    @property
    def transmission_efficiency_settings(
        self: "CastSelf",
    ) -> "TransmissionEfficiencySettings":
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
class TransmissionEfficiencySettings(_0.APIBase):
    """TransmissionEfficiencySettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TRANSMISSION_EFFICIENCY_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def include_bearing_and_seal_loss(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeBearingAndSealLoss")

        if temp is None:
            return False

        return temp

    @include_bearing_and_seal_loss.setter
    @exception_bridge
    @enforce_parameter_types
    def include_bearing_and_seal_loss(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeBearingAndSealLoss",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def include_belt_loss(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeBeltLoss")

        if temp is None:
            return False

        return temp

    @include_belt_loss.setter
    @exception_bridge
    @enforce_parameter_types
    def include_belt_loss(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "IncludeBeltLoss", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def include_clutch_loss(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeClutchLoss")

        if temp is None:
            return False

        return temp

    @include_clutch_loss.setter
    @exception_bridge
    @enforce_parameter_types
    def include_clutch_loss(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeClutchLoss",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def include_efficiency(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeEfficiency")

        if temp is None:
            return False

        return temp

    @include_efficiency.setter
    @exception_bridge
    @enforce_parameter_types
    def include_efficiency(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeEfficiency",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def include_gear_mesh_loss(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeGearMeshLoss")

        if temp is None:
            return False

        return temp

    @include_gear_mesh_loss.setter
    @exception_bridge
    @enforce_parameter_types
    def include_gear_mesh_loss(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeGearMeshLoss",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def include_gear_windage_loss(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeGearWindageLoss")

        if temp is None:
            return False

        return temp

    @include_gear_windage_loss.setter
    @exception_bridge
    @enforce_parameter_types
    def include_gear_windage_loss(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeGearWindageLoss",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def include_oil_pump_loss(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeOilPumpLoss")

        if temp is None:
            return False

        return temp

    @include_oil_pump_loss.setter
    @exception_bridge
    @enforce_parameter_types
    def include_oil_pump_loss(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeOilPumpLoss",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def include_shaft_windage_loss(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeShaftWindageLoss")

        if temp is None:
            return False

        return temp

    @include_shaft_windage_loss.setter
    @exception_bridge
    @enforce_parameter_types
    def include_shaft_windage_loss(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeShaftWindageLoss",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def shaft_gear_windage_and_churning_loss_calculation_method(
        self: "Self",
    ) -> "overridable.Overridable_GearWindageAndChurningLossCalculationMethod":
        """Overridable[mastapy.gears.GearWindageAndChurningLossCalculationMethod]"""
        temp = pythonnet_property_get(
            self.wrapped, "ShaftGearWindageAndChurningLossCalculationMethod"
        )

        if temp is None:
            return None

        value = overridable.Overridable_GearWindageAndChurningLossCalculationMethod.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @shaft_gear_windage_and_churning_loss_calculation_method.setter
    @exception_bridge
    @enforce_parameter_types
    def shaft_gear_windage_and_churning_loss_calculation_method(
        self: "Self",
        value: "Union[_422.GearWindageAndChurningLossCalculationMethod, Tuple[_422.GearWindageAndChurningLossCalculationMethod, bool]]",
    ) -> None:
        wrapper_type = overridable.Overridable_GearWindageAndChurningLossCalculationMethod.wrapper_type()
        enclosed_type = overridable.Overridable_GearWindageAndChurningLossCalculationMethod.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "ShaftGearWindageAndChurningLossCalculationMethod", value
        )

    @property
    @exception_bridge
    def use_advanced_needle_roller_bearing_power_loss_calculation(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseAdvancedNeedleRollerBearingPowerLossCalculation"
        )

        if temp is None:
            return False

        return temp

    @use_advanced_needle_roller_bearing_power_loss_calculation.setter
    @exception_bridge
    @enforce_parameter_types
    def use_advanced_needle_roller_bearing_power_loss_calculation(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseAdvancedNeedleRollerBearingPowerLossCalculation",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_clearance_bearing_friction_loss_calculation(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseClearanceBearingFrictionLossCalculation"
        )

        if temp is None:
            return False

        return temp

    @use_clearance_bearing_friction_loss_calculation.setter
    @exception_bridge
    @enforce_parameter_types
    def use_clearance_bearing_friction_loss_calculation(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseClearanceBearingFrictionLossCalculation",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def volumetric_oil_air_mixture_ratio(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "VolumetricOilAirMixtureRatio")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @volumetric_oil_air_mixture_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def volumetric_oil_air_mixture_ratio(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "VolumetricOilAirMixtureRatio", value)

    @property
    def cast_to(self: "Self") -> "_Cast_TransmissionEfficiencySettings":
        """Cast to another type.

        Returns:
            _Cast_TransmissionEfficiencySettings
        """
        return _Cast_TransmissionEfficiencySettings(self)
