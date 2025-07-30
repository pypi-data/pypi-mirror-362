"""ConceptCouplingHalfDynamicAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.dynamic_analyses import _6628

_CONCEPT_COUPLING_HALF_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses",
    "ConceptCouplingHalfDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7889,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6614,
        _6670,
        _6672,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7708
    from mastapy._private.system_model.part_model.couplings import _2821

    Self = TypeVar("Self", bound="ConceptCouplingHalfDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConceptCouplingHalfDynamicAnalysis._Cast_ConceptCouplingHalfDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConceptCouplingHalfDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConceptCouplingHalfDynamicAnalysis:
    """Special nested class for casting ConceptCouplingHalfDynamicAnalysis to subclasses."""

    __parent__: "ConceptCouplingHalfDynamicAnalysis"

    @property
    def coupling_half_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6628.CouplingHalfDynamicAnalysis":
        return self.__parent__._cast(_6628.CouplingHalfDynamicAnalysis)

    @property
    def mountable_component_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6670.MountableComponentDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6670,
        )

        return self.__parent__._cast(_6670.MountableComponentDynamicAnalysis)

    @property
    def component_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6614.ComponentDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6614,
        )

        return self.__parent__._cast(_6614.ComponentDynamicAnalysis)

    @property
    def part_dynamic_analysis(self: "CastSelf") -> "_6672.PartDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6672,
        )

        return self.__parent__._cast(_6672.PartDynamicAnalysis)

    @property
    def part_fe_analysis(self: "CastSelf") -> "_7889.PartFEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7889,
        )

        return self.__parent__._cast(_7889.PartFEAnalysis)

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
    def concept_coupling_half_dynamic_analysis(
        self: "CastSelf",
    ) -> "ConceptCouplingHalfDynamicAnalysis":
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
class ConceptCouplingHalfDynamicAnalysis(_6628.CouplingHalfDynamicAnalysis):
    """ConceptCouplingHalfDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONCEPT_COUPLING_HALF_DYNAMIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2821.ConceptCouplingHalf":
        """mastapy.system_model.part_model.couplings.ConceptCouplingHalf

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
    def component_load_case(self: "Self") -> "_7708.ConceptCouplingHalfLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingHalfLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConceptCouplingHalfDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConceptCouplingHalfDynamicAnalysis
        """
        return _Cast_ConceptCouplingHalfDynamicAnalysis(self)
