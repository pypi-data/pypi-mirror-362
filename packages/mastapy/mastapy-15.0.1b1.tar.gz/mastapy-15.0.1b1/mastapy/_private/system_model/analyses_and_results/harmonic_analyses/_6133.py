"""VirtualComponentHarmonicAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _6082

_VIRTUAL_COMPONENT_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "VirtualComponentHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5995,
        _6077,
        _6078,
        _6084,
        _6092,
        _6093,
        _6132,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _3078,
    )
    from mastapy._private.system_model.part_model import _2711

    Self = TypeVar("Self", bound="VirtualComponentHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="VirtualComponentHarmonicAnalysis._Cast_VirtualComponentHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("VirtualComponentHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_VirtualComponentHarmonicAnalysis:
    """Special nested class for casting VirtualComponentHarmonicAnalysis to subclasses."""

    __parent__: "VirtualComponentHarmonicAnalysis"

    @property
    def mountable_component_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6082.MountableComponentHarmonicAnalysis":
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
    def mass_disc_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6077.MassDiscHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6077,
        )

        return self.__parent__._cast(_6077.MassDiscHarmonicAnalysis)

    @property
    def measurement_component_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6078.MeasurementComponentHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6078,
        )

        return self.__parent__._cast(_6078.MeasurementComponentHarmonicAnalysis)

    @property
    def point_load_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6092.PointLoadHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6092,
        )

        return self.__parent__._cast(_6092.PointLoadHarmonicAnalysis)

    @property
    def power_load_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6093.PowerLoadHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6093,
        )

        return self.__parent__._cast(_6093.PowerLoadHarmonicAnalysis)

    @property
    def unbalanced_mass_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6132.UnbalancedMassHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6132,
        )

        return self.__parent__._cast(_6132.UnbalancedMassHarmonicAnalysis)

    @property
    def virtual_component_harmonic_analysis(
        self: "CastSelf",
    ) -> "VirtualComponentHarmonicAnalysis":
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
class VirtualComponentHarmonicAnalysis(_6082.MountableComponentHarmonicAnalysis):
    """VirtualComponentHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _VIRTUAL_COMPONENT_HARMONIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2711.VirtualComponent":
        """mastapy.system_model.part_model.VirtualComponent

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
    def system_deflection_results(
        self: "Self",
    ) -> "_3078.VirtualComponentSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.VirtualComponentSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_VirtualComponentHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_VirtualComponentHarmonicAnalysis
        """
        return _Cast_VirtualComponentHarmonicAnalysis(self)
