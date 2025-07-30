"""CouplingCompoundModalAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
    _5101,
)

_COUPLING_COMPOUND_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound",
    "CouplingCompoundModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4882
    from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
        _5001,
        _5022,
        _5027,
        _5082,
        _5083,
        _5105,
        _5120,
    )

    Self = TypeVar("Self", bound="CouplingCompoundModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingCompoundModalAnalysis._Cast_CouplingCompoundModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingCompoundModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingCompoundModalAnalysis:
    """Special nested class for casting CouplingCompoundModalAnalysis to subclasses."""

    __parent__: "CouplingCompoundModalAnalysis"

    @property
    def specialised_assembly_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5101.SpecialisedAssemblyCompoundModalAnalysis":
        return self.__parent__._cast(_5101.SpecialisedAssemblyCompoundModalAnalysis)

    @property
    def abstract_assembly_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5001.AbstractAssemblyCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5001,
        )

        return self.__parent__._cast(_5001.AbstractAssemblyCompoundModalAnalysis)

    @property
    def part_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5082.PartCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5082,
        )

        return self.__parent__._cast(_5082.PartCompoundModalAnalysis)

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
    def clutch_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5022.ClutchCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5022,
        )

        return self.__parent__._cast(_5022.ClutchCompoundModalAnalysis)

    @property
    def concept_coupling_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5027.ConceptCouplingCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5027,
        )

        return self.__parent__._cast(_5027.ConceptCouplingCompoundModalAnalysis)

    @property
    def part_to_part_shear_coupling_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5083.PartToPartShearCouplingCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5083,
        )

        return self.__parent__._cast(_5083.PartToPartShearCouplingCompoundModalAnalysis)

    @property
    def spring_damper_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5105.SpringDamperCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5105,
        )

        return self.__parent__._cast(_5105.SpringDamperCompoundModalAnalysis)

    @property
    def torque_converter_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5120.TorqueConverterCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5120,
        )

        return self.__parent__._cast(_5120.TorqueConverterCompoundModalAnalysis)

    @property
    def coupling_compound_modal_analysis(
        self: "CastSelf",
    ) -> "CouplingCompoundModalAnalysis":
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
class CouplingCompoundModalAnalysis(_5101.SpecialisedAssemblyCompoundModalAnalysis):
    """CouplingCompoundModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_COMPOUND_MODAL_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_analysis_cases(self: "Self") -> "List[_4882.CouplingModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.CouplingModalAnalysis]

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
    ) -> "List[_4882.CouplingModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.CouplingModalAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_CouplingCompoundModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CouplingCompoundModalAnalysis
        """
        return _Cast_CouplingCompoundModalAnalysis(self)
