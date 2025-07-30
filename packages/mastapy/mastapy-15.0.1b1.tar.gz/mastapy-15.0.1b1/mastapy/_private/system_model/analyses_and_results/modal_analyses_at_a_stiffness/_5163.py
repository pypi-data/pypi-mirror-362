"""ConceptGearSetModalAnalysisAtAStiffness"""

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
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
    _5193,
)

_CONCEPT_GEAR_SET_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness",
    "ConceptGearSetModalAnalysisAtAStiffness",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _5132,
        _5161,
        _5162,
        _5215,
        _5234,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7712
    from mastapy._private.system_model.part_model.gears import _2759

    Self = TypeVar("Self", bound="ConceptGearSetModalAnalysisAtAStiffness")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConceptGearSetModalAnalysisAtAStiffness._Cast_ConceptGearSetModalAnalysisAtAStiffness",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConceptGearSetModalAnalysisAtAStiffness",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConceptGearSetModalAnalysisAtAStiffness:
    """Special nested class for casting ConceptGearSetModalAnalysisAtAStiffness to subclasses."""

    __parent__: "ConceptGearSetModalAnalysisAtAStiffness"

    @property
    def gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5193.GearSetModalAnalysisAtAStiffness":
        return self.__parent__._cast(_5193.GearSetModalAnalysisAtAStiffness)

    @property
    def specialised_assembly_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5234.SpecialisedAssemblyModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5234,
        )

        return self.__parent__._cast(_5234.SpecialisedAssemblyModalAnalysisAtAStiffness)

    @property
    def abstract_assembly_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5132.AbstractAssemblyModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5132,
        )

        return self.__parent__._cast(_5132.AbstractAssemblyModalAnalysisAtAStiffness)

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
    def concept_gear_set_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "ConceptGearSetModalAnalysisAtAStiffness":
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
class ConceptGearSetModalAnalysisAtAStiffness(_5193.GearSetModalAnalysisAtAStiffness):
    """ConceptGearSetModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONCEPT_GEAR_SET_MODAL_ANALYSIS_AT_A_STIFFNESS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_design(self: "Self") -> "_2759.ConceptGearSet":
        """mastapy.system_model.part_model.gears.ConceptGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def assembly_load_case(self: "Self") -> "_7712.ConceptGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ConceptGearSetLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gears_modal_analysis_at_a_stiffness(
        self: "Self",
    ) -> "List[_5162.ConceptGearModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.ConceptGearModalAnalysisAtAStiffness]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearsModalAnalysisAtAStiffness")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def concept_gears_modal_analysis_at_a_stiffness(
        self: "Self",
    ) -> "List[_5162.ConceptGearModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.ConceptGearModalAnalysisAtAStiffness]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ConceptGearsModalAnalysisAtAStiffness"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def meshes_modal_analysis_at_a_stiffness(
        self: "Self",
    ) -> "List[_5161.ConceptGearMeshModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.ConceptGearMeshModalAnalysisAtAStiffness]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshesModalAnalysisAtAStiffness")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def concept_meshes_modal_analysis_at_a_stiffness(
        self: "Self",
    ) -> "List[_5161.ConceptGearMeshModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.ConceptGearMeshModalAnalysisAtAStiffness]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ConceptMeshesModalAnalysisAtAStiffness"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ConceptGearSetModalAnalysisAtAStiffness":
        """Cast to another type.

        Returns:
            _Cast_ConceptGearSetModalAnalysisAtAStiffness
        """
        return _Cast_ConceptGearSetModalAnalysisAtAStiffness(self)
