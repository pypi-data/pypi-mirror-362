"""MassDiscCompoundModalAnalysis"""

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
    _5125,
)

_MASS_DISC_COMPOUND_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound",
    "MassDiscCompoundModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4922
    from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
        _5026,
        _5080,
        _5082,
    )
    from mastapy._private.system_model.part_model import _2689

    Self = TypeVar("Self", bound="MassDiscCompoundModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MassDiscCompoundModalAnalysis._Cast_MassDiscCompoundModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MassDiscCompoundModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MassDiscCompoundModalAnalysis:
    """Special nested class for casting MassDiscCompoundModalAnalysis to subclasses."""

    __parent__: "MassDiscCompoundModalAnalysis"

    @property
    def virtual_component_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_5125.VirtualComponentCompoundModalAnalysis":
        return self.__parent__._cast(_5125.VirtualComponentCompoundModalAnalysis)

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
    def mass_disc_compound_modal_analysis(
        self: "CastSelf",
    ) -> "MassDiscCompoundModalAnalysis":
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
class MassDiscCompoundModalAnalysis(_5125.VirtualComponentCompoundModalAnalysis):
    """MassDiscCompoundModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MASS_DISC_COMPOUND_MODAL_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2689.MassDisc":
        """mastapy.system_model.part_model.MassDisc

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
    ) -> "List[_4922.MassDiscModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.MassDiscModalAnalysis]

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
    def planetaries(self: "Self") -> "List[MassDiscCompoundModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.compound.MassDiscCompoundModalAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Planetaries")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def component_analysis_cases(self: "Self") -> "List[_4922.MassDiscModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.MassDiscModalAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_MassDiscCompoundModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_MassDiscCompoundModalAnalysis
        """
        return _Cast_MassDiscCompoundModalAnalysis(self)
