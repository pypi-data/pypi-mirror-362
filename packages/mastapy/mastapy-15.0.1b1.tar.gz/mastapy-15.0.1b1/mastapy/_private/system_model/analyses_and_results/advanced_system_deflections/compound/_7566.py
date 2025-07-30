"""ConnectorCompoundAdvancedSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
    _7609,
)

_CONNECTOR_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound",
    "ConnectorCompoundAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7431,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
        _7538,
        _7555,
        _7610,
        _7611,
        _7628,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )

    Self = TypeVar("Self", bound="ConnectorCompoundAdvancedSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConnectorCompoundAdvancedSystemDeflection._Cast_ConnectorCompoundAdvancedSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConnectorCompoundAdvancedSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectorCompoundAdvancedSystemDeflection:
    """Special nested class for casting ConnectorCompoundAdvancedSystemDeflection to subclasses."""

    __parent__: "ConnectorCompoundAdvancedSystemDeflection"

    @property
    def mountable_component_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7609.MountableComponentCompoundAdvancedSystemDeflection":
        return self.__parent__._cast(
            _7609.MountableComponentCompoundAdvancedSystemDeflection
        )

    @property
    def component_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7555.ComponentCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7555,
        )

        return self.__parent__._cast(_7555.ComponentCompoundAdvancedSystemDeflection)

    @property
    def part_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7611.PartCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7611,
        )

        return self.__parent__._cast(_7611.PartCompoundAdvancedSystemDeflection)

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
    def bearing_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7538.BearingCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7538,
        )

        return self.__parent__._cast(_7538.BearingCompoundAdvancedSystemDeflection)

    @property
    def oil_seal_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7610.OilSealCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7610,
        )

        return self.__parent__._cast(_7610.OilSealCompoundAdvancedSystemDeflection)

    @property
    def shaft_hub_connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7628.ShaftHubConnectionCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7628,
        )

        return self.__parent__._cast(
            _7628.ShaftHubConnectionCompoundAdvancedSystemDeflection
        )

    @property
    def connector_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "ConnectorCompoundAdvancedSystemDeflection":
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
class ConnectorCompoundAdvancedSystemDeflection(
    _7609.MountableComponentCompoundAdvancedSystemDeflection
):
    """ConnectorCompoundAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTOR_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_7431.ConnectorAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.ConnectorAdvancedSystemDeflection]

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
    @exception_bridge
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_7431.ConnectorAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.ConnectorAdvancedSystemDeflection]

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
    def cast_to(self: "Self") -> "_Cast_ConnectorCompoundAdvancedSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_ConnectorCompoundAdvancedSystemDeflection
        """
        return _Cast_ConnectorCompoundAdvancedSystemDeflection(self)
