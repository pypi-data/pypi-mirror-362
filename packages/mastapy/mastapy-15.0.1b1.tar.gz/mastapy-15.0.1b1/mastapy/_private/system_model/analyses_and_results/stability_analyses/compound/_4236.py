"""OilSealCompoundStabilityAnalysis"""

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
    _4192,
)

_OIL_SEAL_COMPOUND_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound",
    "OilSealCompoundStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _4102,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
        _4181,
        _4235,
        _4237,
    )
    from mastapy._private.system_model.part_model import _2695

    Self = TypeVar("Self", bound="OilSealCompoundStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="OilSealCompoundStabilityAnalysis._Cast_OilSealCompoundStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("OilSealCompoundStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_OilSealCompoundStabilityAnalysis:
    """Special nested class for casting OilSealCompoundStabilityAnalysis to subclasses."""

    __parent__: "OilSealCompoundStabilityAnalysis"

    @property
    def connector_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4192.ConnectorCompoundStabilityAnalysis":
        return self.__parent__._cast(_4192.ConnectorCompoundStabilityAnalysis)

    @property
    def mountable_component_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4235.MountableComponentCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4235,
        )

        return self.__parent__._cast(_4235.MountableComponentCompoundStabilityAnalysis)

    @property
    def component_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4181.ComponentCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4181,
        )

        return self.__parent__._cast(_4181.ComponentCompoundStabilityAnalysis)

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
    def oil_seal_compound_stability_analysis(
        self: "CastSelf",
    ) -> "OilSealCompoundStabilityAnalysis":
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
class OilSealCompoundStabilityAnalysis(_4192.ConnectorCompoundStabilityAnalysis):
    """OilSealCompoundStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _OIL_SEAL_COMPOUND_STABILITY_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2695.OilSeal":
        """mastapy.system_model.part_model.OilSeal

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
    ) -> "List[_4102.OilSealStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.OilSealStabilityAnalysis]

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
    ) -> "List[_4102.OilSealStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.OilSealStabilityAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_OilSealCompoundStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_OilSealCompoundStabilityAnalysis
        """
        return _Cast_OilSealCompoundStabilityAnalysis(self)
