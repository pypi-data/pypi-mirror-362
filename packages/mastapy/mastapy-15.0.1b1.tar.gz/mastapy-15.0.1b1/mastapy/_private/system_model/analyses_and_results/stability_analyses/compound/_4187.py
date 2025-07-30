"""ConceptGearSetCompoundStabilityAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
    _4216,
)

_CONCEPT_GEAR_SET_COMPOUND_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound",
    "ConceptGearSetCompoundStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _4050,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
        _4156,
        _4185,
        _4186,
        _4237,
        _4256,
    )
    from mastapy._private.system_model.part_model.gears import _2759

    Self = TypeVar("Self", bound="ConceptGearSetCompoundStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConceptGearSetCompoundStabilityAnalysis._Cast_ConceptGearSetCompoundStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConceptGearSetCompoundStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConceptGearSetCompoundStabilityAnalysis:
    """Special nested class for casting ConceptGearSetCompoundStabilityAnalysis to subclasses."""

    __parent__: "ConceptGearSetCompoundStabilityAnalysis"

    @property
    def gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4216.GearSetCompoundStabilityAnalysis":
        return self.__parent__._cast(_4216.GearSetCompoundStabilityAnalysis)

    @property
    def specialised_assembly_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4256.SpecialisedAssemblyCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4256,
        )

        return self.__parent__._cast(_4256.SpecialisedAssemblyCompoundStabilityAnalysis)

    @property
    def abstract_assembly_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4156.AbstractAssemblyCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4156,
        )

        return self.__parent__._cast(_4156.AbstractAssemblyCompoundStabilityAnalysis)

    @property
    def part_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4237.PartCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4237,
        )

        return self.__parent__._cast(_4237.PartCompoundStabilityAnalysis)

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7888.PartCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7888,
        )

        return self.__parent__._cast(_7888.PartCompoundAnalysis)

    @property
    def design_entity_compound_analysis(
        self: "CastSelf",
    ) -> "_7885.DesignEntityCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7885,
        )

        return self.__parent__._cast(_7885.DesignEntityCompoundAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2892.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2892

        return self.__parent__._cast(_2892.DesignEntityAnalysis)

    @property
    def concept_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "ConceptGearSetCompoundStabilityAnalysis":
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
class ConceptGearSetCompoundStabilityAnalysis(_4216.GearSetCompoundStabilityAnalysis):
    """ConceptGearSetCompoundStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONCEPT_GEAR_SET_COMPOUND_STABILITY_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2759.ConceptGearSet":
        """mastapy.system_model.part_model.gears.ConceptGearSet

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
    def assembly_design(self: "Self") -> "_2759.ConceptGearSet":
        """mastapy.system_model.part_model.gears.ConceptGearSet

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
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4050.ConceptGearSetStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.ConceptGearSetStabilityAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def concept_gears_compound_stability_analysis(
        self: "Self",
    ) -> "List[_4185.ConceptGearCompoundStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.compound.ConceptGearCompoundStabilityAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ConceptGearsCompoundStabilityAnalysis"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def concept_meshes_compound_stability_analysis(
        self: "Self",
    ) -> "List[_4186.ConceptGearMeshCompoundStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.compound.ConceptGearMeshCompoundStabilityAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ConceptMeshesCompoundStabilityAnalysis"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_4050.ConceptGearSetStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.ConceptGearSetStabilityAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ConceptGearSetCompoundStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConceptGearSetCompoundStabilityAnalysis
        """
        return _Cast_ConceptGearSetCompoundStabilityAnalysis(self)
