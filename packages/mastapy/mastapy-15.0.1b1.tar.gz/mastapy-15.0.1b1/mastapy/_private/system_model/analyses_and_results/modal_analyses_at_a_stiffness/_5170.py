"""CouplingHalfModalAnalysisAtAStiffness"""

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
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
    _5213,
)

_COUPLING_HALF_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness",
    "CouplingHalfModalAnalysisAtAStiffness",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _5154,
        _5157,
        _5159,
        _5174,
        _5215,
        _5217,
        _5224,
        _5229,
        _5239,
        _5249,
        _5251,
        _5252,
        _5255,
        _5256,
    )
    from mastapy._private.system_model.part_model.couplings import _2824

    Self = TypeVar("Self", bound="CouplingHalfModalAnalysisAtAStiffness")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingHalfModalAnalysisAtAStiffness._Cast_CouplingHalfModalAnalysisAtAStiffness",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingHalfModalAnalysisAtAStiffness",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingHalfModalAnalysisAtAStiffness:
    """Special nested class for casting CouplingHalfModalAnalysisAtAStiffness to subclasses."""

    __parent__: "CouplingHalfModalAnalysisAtAStiffness"

    @property
    def mountable_component_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5213.MountableComponentModalAnalysisAtAStiffness":
        return self.__parent__._cast(_5213.MountableComponentModalAnalysisAtAStiffness)

    @property
    def component_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5157.ComponentModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5157,
        )

        return self.__parent__._cast(_5157.ComponentModalAnalysisAtAStiffness)

    @property
    def part_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5215.PartModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5215,
        )

        return self.__parent__._cast(_5215.PartModalAnalysisAtAStiffness)

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
    def clutch_half_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5154.ClutchHalfModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5154,
        )

        return self.__parent__._cast(_5154.ClutchHalfModalAnalysisAtAStiffness)

    @property
    def concept_coupling_half_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5159.ConceptCouplingHalfModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5159,
        )

        return self.__parent__._cast(_5159.ConceptCouplingHalfModalAnalysisAtAStiffness)

    @property
    def cvt_pulley_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5174.CVTPulleyModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5174,
        )

        return self.__parent__._cast(_5174.CVTPulleyModalAnalysisAtAStiffness)

    @property
    def part_to_part_shear_coupling_half_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5217.PartToPartShearCouplingHalfModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5217,
        )

        return self.__parent__._cast(
            _5217.PartToPartShearCouplingHalfModalAnalysisAtAStiffness
        )

    @property
    def pulley_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5224.PulleyModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5224,
        )

        return self.__parent__._cast(_5224.PulleyModalAnalysisAtAStiffness)

    @property
    def rolling_ring_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5229.RollingRingModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5229,
        )

        return self.__parent__._cast(_5229.RollingRingModalAnalysisAtAStiffness)

    @property
    def spring_damper_half_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5239.SpringDamperHalfModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5239,
        )

        return self.__parent__._cast(_5239.SpringDamperHalfModalAnalysisAtAStiffness)

    @property
    def synchroniser_half_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5249.SynchroniserHalfModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5249,
        )

        return self.__parent__._cast(_5249.SynchroniserHalfModalAnalysisAtAStiffness)

    @property
    def synchroniser_part_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5251.SynchroniserPartModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5251,
        )

        return self.__parent__._cast(_5251.SynchroniserPartModalAnalysisAtAStiffness)

    @property
    def synchroniser_sleeve_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5252.SynchroniserSleeveModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5252,
        )

        return self.__parent__._cast(_5252.SynchroniserSleeveModalAnalysisAtAStiffness)

    @property
    def torque_converter_pump_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5255.TorqueConverterPumpModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5255,
        )

        return self.__parent__._cast(_5255.TorqueConverterPumpModalAnalysisAtAStiffness)

    @property
    def torque_converter_turbine_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5256.TorqueConverterTurbineModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5256,
        )

        return self.__parent__._cast(
            _5256.TorqueConverterTurbineModalAnalysisAtAStiffness
        )

    @property
    def coupling_half_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "CouplingHalfModalAnalysisAtAStiffness":
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
class CouplingHalfModalAnalysisAtAStiffness(
    _5213.MountableComponentModalAnalysisAtAStiffness
):
    """CouplingHalfModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_HALF_MODAL_ANALYSIS_AT_A_STIFFNESS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2824.CouplingHalf":
        """mastapy.system_model.part_model.couplings.CouplingHalf

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CouplingHalfModalAnalysisAtAStiffness":
        """Cast to another type.

        Returns:
            _Cast_CouplingHalfModalAnalysisAtAStiffness
        """
        return _Cast_CouplingHalfModalAnalysisAtAStiffness(self)
