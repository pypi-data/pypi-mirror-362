"""SynchroniserPartCompoundCriticalSpeedAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
    _7032,
)

_SYNCHRONISER_PART_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound",
    "SynchroniserPartCompoundCriticalSpeedAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6979,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
        _7018,
        _7072,
        _7074,
        _7109,
        _7111,
    )

    Self = TypeVar("Self", bound="SynchroniserPartCompoundCriticalSpeedAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SynchroniserPartCompoundCriticalSpeedAnalysis._Cast_SynchroniserPartCompoundCriticalSpeedAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SynchroniserPartCompoundCriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SynchroniserPartCompoundCriticalSpeedAnalysis:
    """Special nested class for casting SynchroniserPartCompoundCriticalSpeedAnalysis to subclasses."""

    __parent__: "SynchroniserPartCompoundCriticalSpeedAnalysis"

    @property
    def coupling_half_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7032.CouplingHalfCompoundCriticalSpeedAnalysis":
        return self.__parent__._cast(_7032.CouplingHalfCompoundCriticalSpeedAnalysis)

    @property
    def mountable_component_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7072.MountableComponentCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7072,
        )

        return self.__parent__._cast(
            _7072.MountableComponentCompoundCriticalSpeedAnalysis
        )

    @property
    def component_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7018.ComponentCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7018,
        )

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
    def synchroniser_half_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7109.SynchroniserHalfCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7109,
        )

        return self.__parent__._cast(
            _7109.SynchroniserHalfCompoundCriticalSpeedAnalysis
        )

    @property
    def synchroniser_sleeve_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_7111.SynchroniserSleeveCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _7111,
        )

        return self.__parent__._cast(
            _7111.SynchroniserSleeveCompoundCriticalSpeedAnalysis
        )

    @property
    def synchroniser_part_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "SynchroniserPartCompoundCriticalSpeedAnalysis":
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
class SynchroniserPartCompoundCriticalSpeedAnalysis(
    _7032.CouplingHalfCompoundCriticalSpeedAnalysis
):
    """SynchroniserPartCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SYNCHRONISER_PART_COMPOUND_CRITICAL_SPEED_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_6979.SynchroniserPartCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.SynchroniserPartCriticalSpeedAnalysis]

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
    @exception_bridge
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_6979.SynchroniserPartCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.SynchroniserPartCriticalSpeedAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_SynchroniserPartCompoundCriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_SynchroniserPartCompoundCriticalSpeedAnalysis
        """
        return _Cast_SynchroniserPartCompoundCriticalSpeedAnalysis(self)
