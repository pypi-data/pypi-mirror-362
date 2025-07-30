"""WormGearSetAdvancedTimeSteppingAnalysisForModulation"""

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
from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
    _7189,
)

_WORM_GEAR_SET_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation",
    "WormGearSetAdvancedTimeSteppingAnalysisForModulation",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _7124,
        _7211,
        _7230,
        _7255,
        _7256,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7856
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _3080,
    )
    from mastapy._private.system_model.part_model.gears import _2790

    Self = TypeVar("Self", bound="WormGearSetAdvancedTimeSteppingAnalysisForModulation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="WormGearSetAdvancedTimeSteppingAnalysisForModulation._Cast_WormGearSetAdvancedTimeSteppingAnalysisForModulation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("WormGearSetAdvancedTimeSteppingAnalysisForModulation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WormGearSetAdvancedTimeSteppingAnalysisForModulation:
    """Special nested class for casting WormGearSetAdvancedTimeSteppingAnalysisForModulation to subclasses."""

    __parent__: "WormGearSetAdvancedTimeSteppingAnalysisForModulation"

    @property
    def gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7189.GearSetAdvancedTimeSteppingAnalysisForModulation":
        return self.__parent__._cast(
            _7189.GearSetAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def specialised_assembly_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7230.SpecialisedAssemblyAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7230,
        )

        return self.__parent__._cast(
            _7230.SpecialisedAssemblyAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def abstract_assembly_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7124.AbstractAssemblyAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7124,
        )

        return self.__parent__._cast(
            _7124.AbstractAssemblyAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def part_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7211.PartAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7211,
        )

        return self.__parent__._cast(
            _7211.PartAdvancedTimeSteppingAnalysisForModulation
        )

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
    def worm_gear_set_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "WormGearSetAdvancedTimeSteppingAnalysisForModulation":
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
class WormGearSetAdvancedTimeSteppingAnalysisForModulation(
    _7189.GearSetAdvancedTimeSteppingAnalysisForModulation
):
    """WormGearSetAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _WORM_GEAR_SET_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_design(self: "Self") -> "_2790.WormGearSet":
        """mastapy.system_model.part_model.gears.WormGearSet

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
    def assembly_load_case(self: "Self") -> "_7856.WormGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.WormGearSetLoadCase

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
    def system_deflection_results(self: "Self") -> "_3080.WormGearSetSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.WormGearSetSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gears_advanced_time_stepping_analysis_for_modulation(
        self: "Self",
    ) -> "List[_7255.WormGearAdvancedTimeSteppingAnalysisForModulation]":
        """List[mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.WormGearAdvancedTimeSteppingAnalysisForModulation]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GearsAdvancedTimeSteppingAnalysisForModulation"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def worm_gears_advanced_time_stepping_analysis_for_modulation(
        self: "Self",
    ) -> "List[_7255.WormGearAdvancedTimeSteppingAnalysisForModulation]":
        """List[mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.WormGearAdvancedTimeSteppingAnalysisForModulation]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WormGearsAdvancedTimeSteppingAnalysisForModulation"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def meshes_advanced_time_stepping_analysis_for_modulation(
        self: "Self",
    ) -> "List[_7256.WormGearMeshAdvancedTimeSteppingAnalysisForModulation]":
        """List[mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.WormGearMeshAdvancedTimeSteppingAnalysisForModulation]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MeshesAdvancedTimeSteppingAnalysisForModulation"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def worm_meshes_advanced_time_stepping_analysis_for_modulation(
        self: "Self",
    ) -> "List[_7256.WormGearMeshAdvancedTimeSteppingAnalysisForModulation]":
        """List[mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.WormGearMeshAdvancedTimeSteppingAnalysisForModulation]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WormMeshesAdvancedTimeSteppingAnalysisForModulation"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_WormGearSetAdvancedTimeSteppingAnalysisForModulation":
        """Cast to another type.

        Returns:
            _Cast_WormGearSetAdvancedTimeSteppingAnalysisForModulation
        """
        return _Cast_WormGearSetAdvancedTimeSteppingAnalysisForModulation(self)
