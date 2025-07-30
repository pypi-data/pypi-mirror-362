"""WormGearCompoundDynamicAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
    _6780,
)

_WORM_GEAR_COMPOUND_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound",
    "WormGearCompoundDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6716,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
        _6747,
        _6801,
        _6803,
    )
    from mastapy._private.system_model.part_model.gears import _2789

    Self = TypeVar("Self", bound="WormGearCompoundDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="WormGearCompoundDynamicAnalysis._Cast_WormGearCompoundDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("WormGearCompoundDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WormGearCompoundDynamicAnalysis:
    """Special nested class for casting WormGearCompoundDynamicAnalysis to subclasses."""

    __parent__: "WormGearCompoundDynamicAnalysis"

    @property
    def gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6780.GearCompoundDynamicAnalysis":
        return self.__parent__._cast(_6780.GearCompoundDynamicAnalysis)

    @property
    def mountable_component_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6801.MountableComponentCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6801,
        )

        return self.__parent__._cast(_6801.MountableComponentCompoundDynamicAnalysis)

    @property
    def component_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6747.ComponentCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6747,
        )

        return self.__parent__._cast(_6747.ComponentCompoundDynamicAnalysis)

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
    def worm_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "WormGearCompoundDynamicAnalysis":
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
class WormGearCompoundDynamicAnalysis(_6780.GearCompoundDynamicAnalysis):
    """WormGearCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WORM_GEAR_COMPOUND_DYNAMIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2789.WormGear":
        """mastapy.system_model.part_model.gears.WormGear

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
    ) -> "List[_6716.WormGearDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.WormGearDynamicAnalysis]

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
    def component_analysis_cases(self: "Self") -> "List[_6716.WormGearDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.WormGearDynamicAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_WormGearCompoundDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_WormGearCompoundDynamicAnalysis
        """
        return _Cast_WormGearCompoundDynamicAnalysis(self)
