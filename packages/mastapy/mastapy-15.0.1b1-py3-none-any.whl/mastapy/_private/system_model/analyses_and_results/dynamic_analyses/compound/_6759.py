"""CouplingCompoundDynamicAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
    _6822,
)

_COUPLING_COMPOUND_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound",
    "CouplingCompoundDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6627,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
        _6722,
        _6743,
        _6748,
        _6803,
        _6804,
        _6826,
        _6841,
    )

    Self = TypeVar("Self", bound="CouplingCompoundDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingCompoundDynamicAnalysis._Cast_CouplingCompoundDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingCompoundDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingCompoundDynamicAnalysis:
    """Special nested class for casting CouplingCompoundDynamicAnalysis to subclasses."""

    __parent__: "CouplingCompoundDynamicAnalysis"

    @property
    def specialised_assembly_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6822.SpecialisedAssemblyCompoundDynamicAnalysis":
        return self.__parent__._cast(_6822.SpecialisedAssemblyCompoundDynamicAnalysis)

    @property
    def abstract_assembly_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6722.AbstractAssemblyCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6722,
        )

        return self.__parent__._cast(_6722.AbstractAssemblyCompoundDynamicAnalysis)

    @property
    def part_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6803.PartCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6803,
        )

        return self.__parent__._cast(_6803.PartCompoundDynamicAnalysis)

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
    def clutch_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6743.ClutchCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6743,
        )

        return self.__parent__._cast(_6743.ClutchCompoundDynamicAnalysis)

    @property
    def concept_coupling_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6748.ConceptCouplingCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6748,
        )

        return self.__parent__._cast(_6748.ConceptCouplingCompoundDynamicAnalysis)

    @property
    def part_to_part_shear_coupling_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6804.PartToPartShearCouplingCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6804,
        )

        return self.__parent__._cast(
            _6804.PartToPartShearCouplingCompoundDynamicAnalysis
        )

    @property
    def spring_damper_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6826.SpringDamperCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6826,
        )

        return self.__parent__._cast(_6826.SpringDamperCompoundDynamicAnalysis)

    @property
    def torque_converter_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6841.TorqueConverterCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6841,
        )

        return self.__parent__._cast(_6841.TorqueConverterCompoundDynamicAnalysis)

    @property
    def coupling_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "CouplingCompoundDynamicAnalysis":
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
class CouplingCompoundDynamicAnalysis(_6822.SpecialisedAssemblyCompoundDynamicAnalysis):
    """CouplingCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_COMPOUND_DYNAMIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_analysis_cases(self: "Self") -> "List[_6627.CouplingDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.CouplingDynamicAnalysis]

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
    @exception_bridge
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_6627.CouplingDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.CouplingDynamicAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_CouplingCompoundDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CouplingCompoundDynamicAnalysis
        """
        return _Cast_CouplingCompoundDynamicAnalysis(self)
