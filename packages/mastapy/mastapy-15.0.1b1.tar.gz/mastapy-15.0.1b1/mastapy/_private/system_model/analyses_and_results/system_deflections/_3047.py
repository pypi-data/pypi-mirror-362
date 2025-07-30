"""ShaftSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._math.vector_3d import Vector3D
from mastapy._private.system_model.analyses_and_results.system_deflections import _2928

_SHAFT_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "ShaftSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, Iterable, List, Type, TypeVar

    from mastapy._private.math_utility.measured_vectors import _1745
    from mastapy._private.shafts import _19, _37
    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7889,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4396
    from mastapy._private.system_model.analyses_and_results.static_loads import _7821
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2927,
        _2956,
        _3028,
        _3045,
        _3046,
    )
    from mastapy._private.system_model.part_model.shaft_model import _2714

    Self = TypeVar("Self", bound="ShaftSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf", bound="ShaftSystemDeflection._Cast_ShaftSystemDeflection"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftSystemDeflection:
    """Special nested class for casting ShaftSystemDeflection to subclasses."""

    __parent__: "ShaftSystemDeflection"

    @property
    def abstract_shaft_system_deflection(
        self: "CastSelf",
    ) -> "_2928.AbstractShaftSystemDeflection":
        return self.__parent__._cast(_2928.AbstractShaftSystemDeflection)

    @property
    def abstract_shaft_or_housing_system_deflection(
        self: "CastSelf",
    ) -> "_2927.AbstractShaftOrHousingSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2927,
        )

        return self.__parent__._cast(_2927.AbstractShaftOrHousingSystemDeflection)

    @property
    def component_system_deflection(
        self: "CastSelf",
    ) -> "_2956.ComponentSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2956,
        )

        return self.__parent__._cast(_2956.ComponentSystemDeflection)

    @property
    def part_system_deflection(self: "CastSelf") -> "_3028.PartSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3028,
        )

        return self.__parent__._cast(_3028.PartSystemDeflection)

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
    def shaft_system_deflection(self: "CastSelf") -> "ShaftSystemDeflection":
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
class ShaftSystemDeflection(_2928.AbstractShaftSystemDeflection):
    """ShaftSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def two_d_drawing_showing_axial_forces_with_mounted_components(
        self: "Self",
    ) -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TwoDDrawingShowingAxialForcesWithMountedComponents"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def first_node_deflection_angular(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FirstNodeDeflectionAngular")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def first_node_deflection_linear(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FirstNodeDeflectionLinear")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def flexible_pin_additional_deflection_amplitude(
        self: "Self",
    ) -> "Iterable[Vector3D]":
        """Iterable[Vector3D]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "FlexiblePinAdditionalDeflectionAmplitude"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_iterable(temp, Vector3D)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def number_of_cycles_for_fatigue(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfCyclesForFatigue")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pin_tangential_oscillation_amplitude(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinTangentialOscillationAmplitude")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def shaft_rating_method(self: "Self") -> "_37.ShaftRatingMethod":
        """mastapy.shafts.ShaftRatingMethod

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftRatingMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Shafts.ShaftRatingMethod")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.shafts._37", "ShaftRatingMethod"
        )(value)

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2714.Shaft":
        """mastapy.system_model.part_model.shaft_model.Shaft

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
    def component_detailed_analysis(self: "Self") -> "_19.ShaftDamageResults":
        """mastapy.shafts.ShaftDamageResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDetailedAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def component_load_case(self: "Self") -> "_7821.ShaftLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ShaftLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def power_flow_results(self: "Self") -> "_4396.ShaftPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.ShaftPowerFlow

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerFlowResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def shaft_section_end_with_worst_fatigue_safety_factor(
        self: "Self",
    ) -> "_3045.ShaftSectionEndResultsSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.ShaftSectionEndResultsSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ShaftSectionEndWithWorstFatigueSafetyFactor"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def shaft_section_end_with_worst_fatigue_safety_factor_for_infinite_life(
        self: "Self",
    ) -> "_3045.ShaftSectionEndResultsSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.ShaftSectionEndResultsSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ShaftSectionEndWithWorstFatigueSafetyFactorForInfiniteLife"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def shaft_section_end_with_worst_static_safety_factor(
        self: "Self",
    ) -> "_3045.ShaftSectionEndResultsSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.ShaftSectionEndResultsSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ShaftSectionEndWithWorstStaticSafetyFactor"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def mounted_components_applying_torque(self: "Self") -> "List[_1745.ForceResults]":
        """List[mastapy.math_utility.measured_vectors.ForceResults]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MountedComponentsApplyingTorque")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def planetaries(self: "Self") -> "List[ShaftSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ShaftSystemDeflection]

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
    def shaft_section_end_results_by_offset_with_worst_safety_factor(
        self: "Self",
    ) -> "List[_3045.ShaftSectionEndResultsSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ShaftSectionEndResultsSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ShaftSectionEndResultsByOffsetWithWorstSafetyFactor"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def shaft_section_results(
        self: "Self",
    ) -> "List[_3046.ShaftSectionSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ShaftSectionSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftSectionResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    def calculate_outer_diameter_to_achieve_fatigue_safety_factor_requirement(
        self: "Self",
    ) -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped,
            "CalculateOuterDiameterToAchieveFatigueSafetyFactorRequirement",
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_ShaftSystemDeflection
        """
        return _Cast_ShaftSystemDeflection(self)
