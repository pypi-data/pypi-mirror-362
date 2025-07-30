"""GearLoadCase"""

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
from mastapy._private.system_model.analyses_and_results.static_loads import _7795

_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "GearLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7682,
        _7691,
        _7694,
        _7695,
        _7696,
        _7706,
        _7710,
        _7713,
        _7730,
        _7735,
        _7753,
        _7760,
        _7774,
        _7781,
        _7784,
        _7787,
        _7799,
        _7824,
        _7830,
        _7833,
        _7836,
        _7837,
        _7854,
        _7857,
    )
    from mastapy._private.system_model.part_model.gears import _2767

    Self = TypeVar("Self", bound="GearLoadCase")
    CastSelf = TypeVar("CastSelf", bound="GearLoadCase._Cast_GearLoadCase")


__docformat__ = "restructuredtext en"
__all__ = ("GearLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearLoadCase:
    """Special nested class for casting GearLoadCase to subclasses."""

    __parent__: "GearLoadCase"

    @property
    def mountable_component_load_case(
        self: "CastSelf",
    ) -> "_7795.MountableComponentLoadCase":
        return self.__parent__._cast(_7795.MountableComponentLoadCase)

    @property
    def component_load_case(self: "CastSelf") -> "_7706.ComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7706,
        )

        return self.__parent__._cast(_7706.ComponentLoadCase)

    @property
    def part_load_case(self: "CastSelf") -> "_7799.PartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7799,
        )

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
    def agma_gleason_conical_gear_load_case(
        self: "CastSelf",
    ) -> "_7682.AGMAGleasonConicalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7682,
        )

        return self.__parent__._cast(_7682.AGMAGleasonConicalGearLoadCase)

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
    def face_gear_load_case(self: "CastSelf") -> "_7753.FaceGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7753,
        )

        return self.__parent__._cast(_7753.FaceGearLoadCase)

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
    def spiral_bevel_gear_load_case(
        self: "CastSelf",
    ) -> "_7824.SpiralBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7824,
        )

        return self.__parent__._cast(_7824.SpiralBevelGearLoadCase)

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
    def gear_load_case(self: "CastSelf") -> "GearLoadCase":
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
class GearLoadCase(_7795.MountableComponentLoadCase):
    """GearLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def gear_temperature(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "GearTemperature")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @gear_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def gear_temperature(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "GearTemperature", value)

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2767.Gear":
        """mastapy.system_model.part_model.gears.Gear

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear_manufacture_errors(self: "Self") -> "_7760.GearManufactureError":
        """mastapy.system_model.analyses_and_results.static_loads.GearManufactureError

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearManufactureErrors")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_GearLoadCase":
        """Cast to another type.

        Returns:
            _Cast_GearLoadCase
        """
        return _Cast_GearLoadCase(self)
