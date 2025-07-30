"""SpiralBevelGearHarmonicAnalysisOfSingleExcitation"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
    _6332,
)

_SPIRAL_BEVEL_GEAR_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation",
    "SpiralBevelGearHarmonicAnalysisOfSingleExcitation",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
        _6320,
        _6341,
        _6348,
        _6374,
        _6397,
        _6399,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7824
    from mastapy._private.system_model.part_model.gears import _2781

    Self = TypeVar("Self", bound="SpiralBevelGearHarmonicAnalysisOfSingleExcitation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SpiralBevelGearHarmonicAnalysisOfSingleExcitation._Cast_SpiralBevelGearHarmonicAnalysisOfSingleExcitation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpiralBevelGearHarmonicAnalysisOfSingleExcitation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpiralBevelGearHarmonicAnalysisOfSingleExcitation:
    """Special nested class for casting SpiralBevelGearHarmonicAnalysisOfSingleExcitation to subclasses."""

    __parent__: "SpiralBevelGearHarmonicAnalysisOfSingleExcitation"

    @property
    def bevel_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6332.BevelGearHarmonicAnalysisOfSingleExcitation":
        return self.__parent__._cast(_6332.BevelGearHarmonicAnalysisOfSingleExcitation)

    @property
    def agma_gleason_conical_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6320.AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6320,
        )

        return self.__parent__._cast(
            _6320.AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def conical_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6348.ConicalGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6348,
        )

        return self.__parent__._cast(
            _6348.ConicalGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6374.GearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6374,
        )

        return self.__parent__._cast(_6374.GearHarmonicAnalysisOfSingleExcitation)

    @property
    def mountable_component_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6397.MountableComponentHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6397,
        )

        return self.__parent__._cast(
            _6397.MountableComponentHarmonicAnalysisOfSingleExcitation
        )

    @property
    def component_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6341.ComponentHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6341,
        )

        return self.__parent__._cast(_6341.ComponentHarmonicAnalysisOfSingleExcitation)

    @property
    def part_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6399.PartHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6399,
        )

        return self.__parent__._cast(_6399.PartHarmonicAnalysisOfSingleExcitation)

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7890.PartStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7890,
        )

        return self.__parent__._cast(_7890.PartStaticLoadAnalysisCase)

    @property
    def part_analysis_case(self: "CastSelf") -> "_7887.PartAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7887,
        )

        return self.__parent__._cast(_7887.PartAnalysisCase)

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
    def spiral_bevel_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "SpiralBevelGearHarmonicAnalysisOfSingleExcitation":
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
class SpiralBevelGearHarmonicAnalysisOfSingleExcitation(
    _6332.BevelGearHarmonicAnalysisOfSingleExcitation
):
    """SpiralBevelGearHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPIRAL_BEVEL_GEAR_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2781.SpiralBevelGear":
        """mastapy.system_model.part_model.gears.SpiralBevelGear

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
    def component_load_case(self: "Self") -> "_7824.SpiralBevelGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_SpiralBevelGearHarmonicAnalysisOfSingleExcitation":
        """Cast to another type.

        Returns:
            _Cast_SpiralBevelGearHarmonicAnalysisOfSingleExcitation
        """
        return _Cast_SpiralBevelGearHarmonicAnalysisOfSingleExcitation(self)
