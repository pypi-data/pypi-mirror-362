"""ComponentLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
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
from mastapy._private.system_model.analyses_and_results.static_loads import _7799

_COMPONENT_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ComponentLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7676,
        _7677,
        _7682,
        _7688,
        _7691,
        _7694,
        _7695,
        _7696,
        _7700,
        _7702,
        _7708,
        _7710,
        _7713,
        _7719,
        _7721,
        _7725,
        _7728,
        _7730,
        _7735,
        _7738,
        _7752,
        _7753,
        _7756,
        _7759,
        _7765,
        _7774,
        _7781,
        _7784,
        _7787,
        _7790,
        _7791,
        _7794,
        _7795,
        _7797,
        _7801,
        _7806,
        _7809,
        _7810,
        _7811,
        _7814,
        _7818,
        _7820,
        _7821,
        _7824,
        _7828,
        _7830,
        _7833,
        _7836,
        _7837,
        _7838,
        _7840,
        _7841,
        _7846,
        _7847,
        _7852,
        _7853,
        _7854,
        _7857,
    )
    from mastapy._private.system_model.part_model import _2670

    Self = TypeVar("Self", bound="ComponentLoadCase")
    CastSelf = TypeVar("CastSelf", bound="ComponentLoadCase._Cast_ComponentLoadCase")


__docformat__ = "restructuredtext en"
__all__ = ("ComponentLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ComponentLoadCase:
    """Special nested class for casting ComponentLoadCase to subclasses."""

    __parent__: "ComponentLoadCase"

    @property
    def part_load_case(self: "CastSelf") -> "_7799.PartLoadCase":
        return self.__parent__._cast(_7799.PartLoadCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2898.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2898

        return self.__parent__._cast(_2898.PartAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2894.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2894

        return self.__parent__._cast(_2894.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2892.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2892

        return self.__parent__._cast(_2892.DesignEntityAnalysis)

    @property
    def abstract_shaft_load_case(self: "CastSelf") -> "_7676.AbstractShaftLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7676,
        )

        return self.__parent__._cast(_7676.AbstractShaftLoadCase)

    @property
    def abstract_shaft_or_housing_load_case(
        self: "CastSelf",
    ) -> "_7677.AbstractShaftOrHousingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7677,
        )

        return self.__parent__._cast(_7677.AbstractShaftOrHousingLoadCase)

    @property
    def agma_gleason_conical_gear_load_case(
        self: "CastSelf",
    ) -> "_7682.AGMAGleasonConicalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7682,
        )

        return self.__parent__._cast(_7682.AGMAGleasonConicalGearLoadCase)

    @property
    def bearing_load_case(self: "CastSelf") -> "_7688.BearingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7688,
        )

        return self.__parent__._cast(_7688.BearingLoadCase)

    @property
    def bevel_differential_gear_load_case(
        self: "CastSelf",
    ) -> "_7691.BevelDifferentialGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7691,
        )

        return self.__parent__._cast(_7691.BevelDifferentialGearLoadCase)

    @property
    def bevel_differential_planet_gear_load_case(
        self: "CastSelf",
    ) -> "_7694.BevelDifferentialPlanetGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7694,
        )

        return self.__parent__._cast(_7694.BevelDifferentialPlanetGearLoadCase)

    @property
    def bevel_differential_sun_gear_load_case(
        self: "CastSelf",
    ) -> "_7695.BevelDifferentialSunGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7695,
        )

        return self.__parent__._cast(_7695.BevelDifferentialSunGearLoadCase)

    @property
    def bevel_gear_load_case(self: "CastSelf") -> "_7696.BevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7696,
        )

        return self.__parent__._cast(_7696.BevelGearLoadCase)

    @property
    def bolt_load_case(self: "CastSelf") -> "_7700.BoltLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7700,
        )

        return self.__parent__._cast(_7700.BoltLoadCase)

    @property
    def clutch_half_load_case(self: "CastSelf") -> "_7702.ClutchHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7702,
        )

        return self.__parent__._cast(_7702.ClutchHalfLoadCase)

    @property
    def concept_coupling_half_load_case(
        self: "CastSelf",
    ) -> "_7708.ConceptCouplingHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7708,
        )

        return self.__parent__._cast(_7708.ConceptCouplingHalfLoadCase)

    @property
    def concept_gear_load_case(self: "CastSelf") -> "_7710.ConceptGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7710,
        )

        return self.__parent__._cast(_7710.ConceptGearLoadCase)

    @property
    def conical_gear_load_case(self: "CastSelf") -> "_7713.ConicalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7713,
        )

        return self.__parent__._cast(_7713.ConicalGearLoadCase)

    @property
    def connector_load_case(self: "CastSelf") -> "_7719.ConnectorLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7719,
        )

        return self.__parent__._cast(_7719.ConnectorLoadCase)

    @property
    def coupling_half_load_case(self: "CastSelf") -> "_7721.CouplingHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7721,
        )

        return self.__parent__._cast(_7721.CouplingHalfLoadCase)

    @property
    def cvt_pulley_load_case(self: "CastSelf") -> "_7725.CVTPulleyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7725,
        )

        return self.__parent__._cast(_7725.CVTPulleyLoadCase)

    @property
    def cycloidal_disc_load_case(self: "CastSelf") -> "_7728.CycloidalDiscLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7728,
        )

        return self.__parent__._cast(_7728.CycloidalDiscLoadCase)

    @property
    def cylindrical_gear_load_case(self: "CastSelf") -> "_7730.CylindricalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7730,
        )

        return self.__parent__._cast(_7730.CylindricalGearLoadCase)

    @property
    def cylindrical_planet_gear_load_case(
        self: "CastSelf",
    ) -> "_7735.CylindricalPlanetGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7735,
        )

        return self.__parent__._cast(_7735.CylindricalPlanetGearLoadCase)

    @property
    def datum_load_case(self: "CastSelf") -> "_7738.DatumLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7738,
        )

        return self.__parent__._cast(_7738.DatumLoadCase)

    @property
    def external_cad_model_load_case(
        self: "CastSelf",
    ) -> "_7752.ExternalCADModelLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7752,
        )

        return self.__parent__._cast(_7752.ExternalCADModelLoadCase)

    @property
    def face_gear_load_case(self: "CastSelf") -> "_7753.FaceGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7753,
        )

        return self.__parent__._cast(_7753.FaceGearLoadCase)

    @property
    def fe_part_load_case(self: "CastSelf") -> "_7756.FEPartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7756,
        )

        return self.__parent__._cast(_7756.FEPartLoadCase)

    @property
    def gear_load_case(self: "CastSelf") -> "_7759.GearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7759,
        )

        return self.__parent__._cast(_7759.GearLoadCase)

    @property
    def guide_dxf_model_load_case(self: "CastSelf") -> "_7765.GuideDxfModelLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7765,
        )

        return self.__parent__._cast(_7765.GuideDxfModelLoadCase)

    @property
    def hypoid_gear_load_case(self: "CastSelf") -> "_7774.HypoidGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7774,
        )

        return self.__parent__._cast(_7774.HypoidGearLoadCase)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_load_case(
        self: "CastSelf",
    ) -> "_7781.KlingelnbergCycloPalloidConicalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7781,
        )

        return self.__parent__._cast(_7781.KlingelnbergCycloPalloidConicalGearLoadCase)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_load_case(
        self: "CastSelf",
    ) -> "_7784.KlingelnbergCycloPalloidHypoidGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7784,
        )

        return self.__parent__._cast(_7784.KlingelnbergCycloPalloidHypoidGearLoadCase)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_load_case(
        self: "CastSelf",
    ) -> "_7787.KlingelnbergCycloPalloidSpiralBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7787,
        )

        return self.__parent__._cast(
            _7787.KlingelnbergCycloPalloidSpiralBevelGearLoadCase
        )

    @property
    def mass_disc_load_case(self: "CastSelf") -> "_7790.MassDiscLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7790,
        )

        return self.__parent__._cast(_7790.MassDiscLoadCase)

    @property
    def measurement_component_load_case(
        self: "CastSelf",
    ) -> "_7791.MeasurementComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7791,
        )

        return self.__parent__._cast(_7791.MeasurementComponentLoadCase)

    @property
    def microphone_load_case(self: "CastSelf") -> "_7794.MicrophoneLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7794,
        )

        return self.__parent__._cast(_7794.MicrophoneLoadCase)

    @property
    def mountable_component_load_case(
        self: "CastSelf",
    ) -> "_7795.MountableComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7795,
        )

        return self.__parent__._cast(_7795.MountableComponentLoadCase)

    @property
    def oil_seal_load_case(self: "CastSelf") -> "_7797.OilSealLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7797,
        )

        return self.__parent__._cast(_7797.OilSealLoadCase)

    @property
    def part_to_part_shear_coupling_half_load_case(
        self: "CastSelf",
    ) -> "_7801.PartToPartShearCouplingHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7801,
        )

        return self.__parent__._cast(_7801.PartToPartShearCouplingHalfLoadCase)

    @property
    def planet_carrier_load_case(self: "CastSelf") -> "_7806.PlanetCarrierLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7806,
        )

        return self.__parent__._cast(_7806.PlanetCarrierLoadCase)

    @property
    def point_load_load_case(self: "CastSelf") -> "_7809.PointLoadLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7809,
        )

        return self.__parent__._cast(_7809.PointLoadLoadCase)

    @property
    def power_load_load_case(self: "CastSelf") -> "_7810.PowerLoadLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7810,
        )

        return self.__parent__._cast(_7810.PowerLoadLoadCase)

    @property
    def pulley_load_case(self: "CastSelf") -> "_7811.PulleyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7811,
        )

        return self.__parent__._cast(_7811.PulleyLoadCase)

    @property
    def ring_pins_load_case(self: "CastSelf") -> "_7814.RingPinsLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7814,
        )

        return self.__parent__._cast(_7814.RingPinsLoadCase)

    @property
    def rolling_ring_load_case(self: "CastSelf") -> "_7818.RollingRingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7818,
        )

        return self.__parent__._cast(_7818.RollingRingLoadCase)

    @property
    def shaft_hub_connection_load_case(
        self: "CastSelf",
    ) -> "_7820.ShaftHubConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7820,
        )

        return self.__parent__._cast(_7820.ShaftHubConnectionLoadCase)

    @property
    def shaft_load_case(self: "CastSelf") -> "_7821.ShaftLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7821,
        )

        return self.__parent__._cast(_7821.ShaftLoadCase)

    @property
    def spiral_bevel_gear_load_case(
        self: "CastSelf",
    ) -> "_7824.SpiralBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7824,
        )

        return self.__parent__._cast(_7824.SpiralBevelGearLoadCase)

    @property
    def spring_damper_half_load_case(
        self: "CastSelf",
    ) -> "_7828.SpringDamperHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7828,
        )

        return self.__parent__._cast(_7828.SpringDamperHalfLoadCase)

    @property
    def straight_bevel_diff_gear_load_case(
        self: "CastSelf",
    ) -> "_7830.StraightBevelDiffGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7830,
        )

        return self.__parent__._cast(_7830.StraightBevelDiffGearLoadCase)

    @property
    def straight_bevel_gear_load_case(
        self: "CastSelf",
    ) -> "_7833.StraightBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7833,
        )

        return self.__parent__._cast(_7833.StraightBevelGearLoadCase)

    @property
    def straight_bevel_planet_gear_load_case(
        self: "CastSelf",
    ) -> "_7836.StraightBevelPlanetGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7836,
        )

        return self.__parent__._cast(_7836.StraightBevelPlanetGearLoadCase)

    @property
    def straight_bevel_sun_gear_load_case(
        self: "CastSelf",
    ) -> "_7837.StraightBevelSunGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7837,
        )

        return self.__parent__._cast(_7837.StraightBevelSunGearLoadCase)

    @property
    def synchroniser_half_load_case(
        self: "CastSelf",
    ) -> "_7838.SynchroniserHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7838,
        )

        return self.__parent__._cast(_7838.SynchroniserHalfLoadCase)

    @property
    def synchroniser_part_load_case(
        self: "CastSelf",
    ) -> "_7840.SynchroniserPartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7840,
        )

        return self.__parent__._cast(_7840.SynchroniserPartLoadCase)

    @property
    def synchroniser_sleeve_load_case(
        self: "CastSelf",
    ) -> "_7841.SynchroniserSleeveLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7841,
        )

        return self.__parent__._cast(_7841.SynchroniserSleeveLoadCase)

    @property
    def torque_converter_pump_load_case(
        self: "CastSelf",
    ) -> "_7846.TorqueConverterPumpLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7846,
        )

        return self.__parent__._cast(_7846.TorqueConverterPumpLoadCase)

    @property
    def torque_converter_turbine_load_case(
        self: "CastSelf",
    ) -> "_7847.TorqueConverterTurbineLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7847,
        )

        return self.__parent__._cast(_7847.TorqueConverterTurbineLoadCase)

    @property
    def unbalanced_mass_load_case(self: "CastSelf") -> "_7852.UnbalancedMassLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7852,
        )

        return self.__parent__._cast(_7852.UnbalancedMassLoadCase)

    @property
    def virtual_component_load_case(
        self: "CastSelf",
    ) -> "_7853.VirtualComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7853,
        )

        return self.__parent__._cast(_7853.VirtualComponentLoadCase)

    @property
    def worm_gear_load_case(self: "CastSelf") -> "_7854.WormGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7854,
        )

        return self.__parent__._cast(_7854.WormGearLoadCase)

    @property
    def zerol_bevel_gear_load_case(self: "CastSelf") -> "_7857.ZerolBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7857,
        )

        return self.__parent__._cast(_7857.ZerolBevelGearLoadCase)

    @property
    def component_load_case(self: "CastSelf") -> "ComponentLoadCase":
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
class ComponentLoadCase(_7799.PartLoadCase):
    """ComponentLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPONENT_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def additional_modal_damping_ratio(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "AdditionalModalDampingRatio")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @additional_modal_damping_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def additional_modal_damping_ratio(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "AdditionalModalDampingRatio", value)

    @property
    @exception_bridge
    def is_connected_to_ground(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsConnectedToGround")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def is_torsionally_free(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsTorsionallyFree")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def magnitude_of_rotation(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MagnitudeOfRotation")

        if temp is None:
            return 0.0

        return temp

    @magnitude_of_rotation.setter
    @exception_bridge
    @enforce_parameter_types
    def magnitude_of_rotation(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MagnitudeOfRotation",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def rayleigh_damping_beta(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RayleighDampingBeta")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @rayleigh_damping_beta.setter
    @exception_bridge
    @enforce_parameter_types
    def rayleigh_damping_beta(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RayleighDampingBeta", value)

    @property
    @exception_bridge
    def rotation_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RotationAngle")

        if temp is None:
            return 0.0

        return temp

    @rotation_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def rotation_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RotationAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2670.Component":
        """mastapy.system_model.part_model.Component

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ComponentLoadCase":
        """Cast to another type.

        Returns:
            _Cast_ComponentLoadCase
        """
        return _Cast_ComponentLoadCase(self)
