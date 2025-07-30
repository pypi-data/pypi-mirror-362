"""ConnectorCompoundSystemDeflection"""

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
from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
    _3174,
)

_CONNECTOR_COMPOUND_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound",
    "ConnectorCompoundSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2969,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
        _3102,
        _3119,
        _3175,
        _3176,
        _3194,
    )

    Self = TypeVar("Self", bound="ConnectorCompoundSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConnectorCompoundSystemDeflection._Cast_ConnectorCompoundSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConnectorCompoundSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectorCompoundSystemDeflection:
    """Special nested class for casting ConnectorCompoundSystemDeflection to subclasses."""

    __parent__: "ConnectorCompoundSystemDeflection"

    @property
    def mountable_component_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3174.MountableComponentCompoundSystemDeflection":
        return self.__parent__._cast(_3174.MountableComponentCompoundSystemDeflection)

    @property
    def component_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3119.ComponentCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3119,
        )

        return self.__parent__._cast(_3119.ComponentCompoundSystemDeflection)

    @property
    def part_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3176.PartCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3176,
        )

        return self.__parent__._cast(_3176.PartCompoundSystemDeflection)

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
    def bearing_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3102.BearingCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3102,
        )

        return self.__parent__._cast(_3102.BearingCompoundSystemDeflection)

    @property
    def oil_seal_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3175.OilSealCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3175,
        )

        return self.__parent__._cast(_3175.OilSealCompoundSystemDeflection)

    @property
    def shaft_hub_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3194.ShaftHubConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3194,
        )

        return self.__parent__._cast(_3194.ShaftHubConnectionCompoundSystemDeflection)

    @property
    def connector_compound_system_deflection(
        self: "CastSelf",
    ) -> "ConnectorCompoundSystemDeflection":
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
class ConnectorCompoundSystemDeflection(
    _3174.MountableComponentCompoundSystemDeflection
):
    """ConnectorCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTOR_COMPOUND_SYSTEM_DEFLECTION

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
    ) -> "List[_2969.ConnectorSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ConnectorSystemDeflection]

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
    ) -> "List[_2969.ConnectorSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ConnectorSystemDeflection]

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
    def cast_to(self: "Self") -> "_Cast_ConnectorCompoundSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_ConnectorCompoundSystemDeflection
        """
        return _Cast_ConnectorCompoundSystemDeflection(self)
