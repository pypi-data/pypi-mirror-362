"""CVTBeltConnectionCompoundAdvancedSystemDeflection"""

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
    _7539,
)

_CVT_BELT_CONNECTION_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound",
    "CVTBeltConnectionCompoundAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7437,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
        _7565,
        _7595,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7881,
        _7885,
    )

    Self = TypeVar("Self", bound="CVTBeltConnectionCompoundAdvancedSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CVTBeltConnectionCompoundAdvancedSystemDeflection._Cast_CVTBeltConnectionCompoundAdvancedSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CVTBeltConnectionCompoundAdvancedSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CVTBeltConnectionCompoundAdvancedSystemDeflection:
    """Special nested class for casting CVTBeltConnectionCompoundAdvancedSystemDeflection to subclasses."""

    __parent__: "CVTBeltConnectionCompoundAdvancedSystemDeflection"

    @property
    def belt_connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7539.BeltConnectionCompoundAdvancedSystemDeflection":
        return self.__parent__._cast(
            _7539.BeltConnectionCompoundAdvancedSystemDeflection
        )

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
    def cvt_belt_connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "CVTBeltConnectionCompoundAdvancedSystemDeflection":
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
class CVTBeltConnectionCompoundAdvancedSystemDeflection(
    _7539.BeltConnectionCompoundAdvancedSystemDeflection
):
    """CVTBeltConnectionCompoundAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CVT_BELT_CONNECTION_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_7437.CVTBeltConnectionAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.CVTBeltConnectionAdvancedSystemDeflection]

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
    ) -> "List[_7437.CVTBeltConnectionAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.CVTBeltConnectionAdvancedSystemDeflection]

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
    ) -> "_Cast_CVTBeltConnectionCompoundAdvancedSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_CVTBeltConnectionCompoundAdvancedSystemDeflection
        """
        return _Cast_CVTBeltConnectionCompoundAdvancedSystemDeflection(self)
