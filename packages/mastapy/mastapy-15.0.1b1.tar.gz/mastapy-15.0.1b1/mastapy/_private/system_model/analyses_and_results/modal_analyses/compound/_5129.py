"""ZerolBevelGearCompoundModalAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
    _5017,
)

_ZEROL_BEVEL_GEAR_COMPOUND_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound",
    "ZerolBevelGearCompoundModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4987
    from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
        _5005,
        _5026,
        _5033,
        _5059,
        _5080,
        _5082,
    )
    from mastapy._private.system_model.part_model.gears import _2791

    Self = TypeVar("Self", bound="ZerolBevelGearCompoundModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ZerolBevelGearCompoundModalAnalysis._Cast_ZerolBevelGearCompoundModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ZerolBevelGearCompoundModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ZerolBevelGearCompoundModalAnalysis:
    """Special nested class for casting ZerolBevelGearCompoundModalAnalysis to subclasses."""

    __parent__: "ZerolBevelGearCompoundModalAnalysis"

    @property
    def bevel_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5017.BevelGearCompoundModalAnalysis":
        return self.__parent__._cast(_5017.BevelGearCompoundModalAnalysis)

    @property
    def agma_gleason_conical_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5005.AGMAGleasonConicalGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5005,
        )

        return self.__parent__._cast(_5005.AGMAGleasonConicalGearCompoundModalAnalysis)

    @property
    def conical_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5033.ConicalGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5033,
        )

        return self.__parent__._cast(_5033.ConicalGearCompoundModalAnalysis)

    @property
    def gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5059.GearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5059,
        )

        return self.__parent__._cast(_5059.GearCompoundModalAnalysis)

    @property
    def mountable_component_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5080.MountableComponentCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5080,
        )

        return self.__parent__._cast(_5080.MountableComponentCompoundModalAnalysis)

    @property
    def component_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5026.ComponentCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _5026,
        )

        return self.__parent__._cast(_5026.ComponentCompoundModalAnalysis)

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
    def zerol_bevel_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "ZerolBevelGearCompoundModalAnalysis":
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
class ZerolBevelGearCompoundModalAnalysis(_5017.BevelGearCompoundModalAnalysis):
    """ZerolBevelGearCompoundModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ZEROL_BEVEL_GEAR_COMPOUND_MODAL_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2791.ZerolBevelGear":
        """mastapy.system_model.part_model.gears.ZerolBevelGear

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
    ) -> "List[_4987.ZerolBevelGearModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.ZerolBevelGearModalAnalysis]

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
    ) -> "List[_4987.ZerolBevelGearModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.ZerolBevelGearModalAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_ZerolBevelGearCompoundModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ZerolBevelGearCompoundModalAnalysis
        """
        return _Cast_ZerolBevelGearCompoundModalAnalysis(self)
