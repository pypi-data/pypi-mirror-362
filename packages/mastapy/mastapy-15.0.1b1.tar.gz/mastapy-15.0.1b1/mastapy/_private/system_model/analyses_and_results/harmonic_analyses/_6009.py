"""CouplingHarmonicAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _6106

_COUPLING_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "CouplingHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5968,
        _5992,
        _5998,
        _6084,
        _6087,
        _6113,
        _6128,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2972,
    )
    from mastapy._private.system_model.part_model.couplings import _2823

    Self = TypeVar("Self", bound="CouplingHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="CouplingHarmonicAnalysis._Cast_CouplingHarmonicAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingHarmonicAnalysis:
    """Special nested class for casting CouplingHarmonicAnalysis to subclasses."""

    __parent__: "CouplingHarmonicAnalysis"

    @property
    def specialised_assembly_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6106.SpecialisedAssemblyHarmonicAnalysis":
        return self.__parent__._cast(_6106.SpecialisedAssemblyHarmonicAnalysis)

    @property
    def abstract_assembly_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5968.AbstractAssemblyHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5968,
        )

        return self.__parent__._cast(_5968.AbstractAssemblyHarmonicAnalysis)

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
    def clutch_harmonic_analysis(self: "CastSelf") -> "_5992.ClutchHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5992,
        )

        return self.__parent__._cast(_5992.ClutchHarmonicAnalysis)

    @property
    def concept_coupling_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5998.ConceptCouplingHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5998,
        )

        return self.__parent__._cast(_5998.ConceptCouplingHarmonicAnalysis)

    @property
    def part_to_part_shear_coupling_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6087.PartToPartShearCouplingHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6087,
        )

        return self.__parent__._cast(_6087.PartToPartShearCouplingHarmonicAnalysis)

    @property
    def spring_damper_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6113.SpringDamperHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6113,
        )

        return self.__parent__._cast(_6113.SpringDamperHarmonicAnalysis)

    @property
    def torque_converter_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6128.TorqueConverterHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6128,
        )

        return self.__parent__._cast(_6128.TorqueConverterHarmonicAnalysis)

    @property
    def coupling_harmonic_analysis(self: "CastSelf") -> "CouplingHarmonicAnalysis":
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
class CouplingHarmonicAnalysis(_6106.SpecialisedAssemblyHarmonicAnalysis):
    """CouplingHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_HARMONIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_design(self: "Self") -> "_2823.Coupling":
        """mastapy.system_model.part_model.couplings.Coupling

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def system_deflection_results(self: "Self") -> "_2972.CouplingSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.CouplingSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CouplingHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CouplingHarmonicAnalysis
        """
        return _Cast_CouplingHarmonicAnalysis(self)
