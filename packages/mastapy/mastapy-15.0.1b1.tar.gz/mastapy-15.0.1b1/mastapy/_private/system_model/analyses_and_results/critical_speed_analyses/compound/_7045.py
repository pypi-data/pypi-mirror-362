"""ExternalCADModelCompoundCriticalSpeedAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
    _7018,
)

_EXTERNAL_CAD_MODEL_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound",
    "ExternalCADModelCompoundCriticalSpeedAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6914,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
        _7074,
    )
    from mastapy._private.system_model.part_model import _2679

    Self = TypeVar("Self", bound="ExternalCADModelCompoundCriticalSpeedAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ExternalCADModelCompoundCriticalSpeedAnalysis._Cast_ExternalCADModelCompoundCriticalSpeedAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ExternalCADModelCompoundCriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ExternalCADModelCompoundCriticalSpeedAnalysis:
    """Special nested class for casting ExternalCADModelCompoundCriticalSpeedAnalysis to subclasses."""

    __parent__: "ExternalCADModelCompoundCriticalSpeedAnalysis"

    @property
    def component_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7018.ComponentCompoundCriticalSpeedAnalysis":
        return self.__parent__._cast(_7018.ComponentCompoundCriticalSpeedAnalysis)

    @property
    def part_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7074.PartCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7074,
        )

        return self.__parent__._cast(_7074.PartCompoundCriticalSpeedAnalysis)

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
    def external_cad_model_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "ExternalCADModelCompoundCriticalSpeedAnalysis":
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
class ExternalCADModelCompoundCriticalSpeedAnalysis(
    _7018.ComponentCompoundCriticalSpeedAnalysis
):
    """ExternalCADModelCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _EXTERNAL_CAD_MODEL_COMPOUND_CRITICAL_SPEED_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2679.ExternalCADModel":
        """mastapy.system_model.part_model.ExternalCADModel

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
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_6914.ExternalCADModelCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.ExternalCADModelCriticalSpeedAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_6914.ExternalCADModelCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.ExternalCADModelCriticalSpeedAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ExternalCADModelCompoundCriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ExternalCADModelCompoundCriticalSpeedAnalysis
        """
        return _Cast_ExternalCADModelCompoundCriticalSpeedAnalysis(self)
