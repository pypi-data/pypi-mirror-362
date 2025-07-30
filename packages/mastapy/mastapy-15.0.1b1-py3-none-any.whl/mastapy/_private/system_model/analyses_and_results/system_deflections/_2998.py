"""FEPartSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.system_deflections import _2927

_FE_PART_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "FEPartSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.math_utility.measured_vectors import _1744, _1748
    from mastapy._private.nodal_analysis import _82
    from mastapy._private.nodal_analysis.component_mode_synthesis import _322
    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7889,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4352
    from mastapy._private.system_model.analyses_and_results.static_loads import _7756
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2956,
        _3028,
    )
    from mastapy._private.system_model.fe import _2635
    from mastapy._private.system_model.part_model import _2680

    Self = TypeVar("Self", bound="FEPartSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf", bound="FEPartSystemDeflection._Cast_FEPartSystemDeflection"
    )


__docformat__ = "restructuredtext en"
__all__ = ("FEPartSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FEPartSystemDeflection:
    """Special nested class for casting FEPartSystemDeflection to subclasses."""

    __parent__: "FEPartSystemDeflection"

    @property
    def abstract_shaft_or_housing_system_deflection(
        self: "CastSelf",
    ) -> "_2927.AbstractShaftOrHousingSystemDeflection":
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
    def fe_part_system_deflection(self: "CastSelf") -> "FEPartSystemDeflection":
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
class FEPartSystemDeflection(_2927.AbstractShaftOrHousingSystemDeflection):
    """FEPartSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_PART_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2680.FEPart":
        """mastapy.system_model.part_model.FEPart

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
    def component_load_case(self: "Self") -> "_7756.FEPartLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.FEPartLoadCase

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
    def full_fe_results(self: "Self") -> "_322.StaticCMSResults":
        """mastapy.nodal_analysis.component_mode_synthesis.StaticCMSResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FullFEResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def mass_in_world_coordinate_system_mn_rad_s_kg(self: "Self") -> "_82.NodalMatrix":
        """mastapy.nodal_analysis.NodalMatrix

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MassInWorldCoordinateSystemMNRadSKg"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def power_flow_results(self: "Self") -> "_4352.FEPartPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.FEPartPowerFlow

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
    def stiffness_in_world_coordinate_system_mn_rad(self: "Self") -> "_82.NodalMatrix":
        """mastapy.nodal_analysis.NodalMatrix

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StiffnessInWorldCoordinateSystemMNRad"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def applied_internal_forces_in_world_coordinate_system(
        self: "Self",
    ) -> "List[_1748.VectorWithLinearAndAngularComponents]":
        """List[mastapy.math_utility.measured_vectors.VectorWithLinearAndAngularComponents]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AppliedInternalForcesInWorldCoordinateSystem"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def node_results_in_shaft_coordinate_system(
        self: "Self",
    ) -> "List[_1744.ForceAndDisplacementResults]":
        """List[mastapy.math_utility.measured_vectors.ForceAndDisplacementResults]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NodeResultsInShaftCoordinateSystem"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def planetaries(self: "Self") -> "List[FEPartSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.FEPartSystemDeflection]

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
    def export(self: "Self") -> "_2635.SystemDeflectionFEExportOptions":
        """mastapy.system_model.fe.SystemDeflectionFEExportOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Export")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    def export_displacements(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ExportDisplacements")

    @exception_bridge
    def export_forces(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ExportForces")

    @property
    def cast_to(self: "Self") -> "_Cast_FEPartSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_FEPartSystemDeflection
        """
        return _Cast_FEPartSystemDeflection(self)
