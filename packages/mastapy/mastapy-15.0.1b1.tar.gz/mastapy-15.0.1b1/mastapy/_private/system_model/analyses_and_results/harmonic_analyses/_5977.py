"""BearingHarmonicAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _6006

_BEARING_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "BearingHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling import _2280
    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5995,
        _6082,
        _6084,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7688
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2939,
    )
    from mastapy._private.system_model.part_model import _2664

    Self = TypeVar("Self", bound="BearingHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="BearingHarmonicAnalysis._Cast_BearingHarmonicAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BearingHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BearingHarmonicAnalysis:
    """Special nested class for casting BearingHarmonicAnalysis to subclasses."""

    __parent__: "BearingHarmonicAnalysis"

    @property
    def connector_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6006.ConnectorHarmonicAnalysis":
        return self.__parent__._cast(_6006.ConnectorHarmonicAnalysis)

    @property
    def mountable_component_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6082.MountableComponentHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6082,
        )

        return self.__parent__._cast(_6082.MountableComponentHarmonicAnalysis)

    @property
    def component_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5995.ComponentHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5995,
        )

        return self.__parent__._cast(_5995.ComponentHarmonicAnalysis)

    @property
    def part_harmonic_analysis(self: "CastSelf") -> "_6084.PartHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6084,
        )

        return self.__parent__._cast(_6084.PartHarmonicAnalysis)

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
    def bearing_harmonic_analysis(self: "CastSelf") -> "BearingHarmonicAnalysis":
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
class BearingHarmonicAnalysis(_6006.ConnectorHarmonicAnalysis):
    """BearingHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEARING_HARMONIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2664.Bearing":
        """mastapy.system_model.part_model.Bearing

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
    def component_load_case(self: "Self") -> "_7688.BearingLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.BearingLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def rolling_bearing_speed_results(
        self: "Self",
    ) -> "_2280.RollingBearingSpeedResults":
        """mastapy.bearings.bearing_results.rolling.RollingBearingSpeedResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RollingBearingSpeedResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def system_deflection_results(self: "Self") -> "_2939.BearingSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.BearingSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def planetaries(self: "Self") -> "List[BearingHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.BearingHarmonicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Planetaries")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_BearingHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_BearingHarmonicAnalysis
        """
        return _Cast_BearingHarmonicAnalysis(self)
