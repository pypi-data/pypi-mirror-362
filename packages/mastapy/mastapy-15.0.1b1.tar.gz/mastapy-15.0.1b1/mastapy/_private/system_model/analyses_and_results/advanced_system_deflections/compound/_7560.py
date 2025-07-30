"""ConceptGearMeshCompoundAdvancedSystemDeflection"""

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
from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
    _7589,
)

_CONCEPT_GEAR_MESH_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound",
    "ConceptGearMeshCompoundAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7425,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
        _7565,
        _7595,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7881,
        _7885,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2526

    Self = TypeVar("Self", bound="ConceptGearMeshCompoundAdvancedSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConceptGearMeshCompoundAdvancedSystemDeflection._Cast_ConceptGearMeshCompoundAdvancedSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConceptGearMeshCompoundAdvancedSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConceptGearMeshCompoundAdvancedSystemDeflection:
    """Special nested class for casting ConceptGearMeshCompoundAdvancedSystemDeflection to subclasses."""

    __parent__: "ConceptGearMeshCompoundAdvancedSystemDeflection"

    @property
    def gear_mesh_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7589.GearMeshCompoundAdvancedSystemDeflection":
        return self.__parent__._cast(_7589.GearMeshCompoundAdvancedSystemDeflection)

    @property
    def inter_mountable_component_connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7595.InterMountableComponentConnectionCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7595,
        )

        return self.__parent__._cast(
            _7595.InterMountableComponentConnectionCompoundAdvancedSystemDeflection
        )

    @property
    def connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7565.ConnectionCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7565,
        )

        return self.__parent__._cast(_7565.ConnectionCompoundAdvancedSystemDeflection)

    @property
    def connection_compound_analysis(
        self: "CastSelf",
    ) -> "_7881.ConnectionCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7881,
        )

        return self.__parent__._cast(_7881.ConnectionCompoundAnalysis)

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
    def concept_gear_mesh_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "ConceptGearMeshCompoundAdvancedSystemDeflection":
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
class ConceptGearMeshCompoundAdvancedSystemDeflection(
    _7589.GearMeshCompoundAdvancedSystemDeflection
):
    """ConceptGearMeshCompoundAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONCEPT_GEAR_MESH_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2526.ConceptGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh

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
    def connection_design(self: "Self") -> "_2526.ConceptGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_7425.ConceptGearMeshAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptGearMeshAdvancedSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_7425.ConceptGearMeshAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptGearMeshAdvancedSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_ConceptGearMeshCompoundAdvancedSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_ConceptGearMeshCompoundAdvancedSystemDeflection
        """
        return _Cast_ConceptGearMeshCompoundAdvancedSystemDeflection(self)
