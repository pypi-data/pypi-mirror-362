"""CVTBeltConnectionAdvancedSystemDeflection"""

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
from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
    _7404,
)

_CVT_BELT_CONNECTION_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections",
    "CVTBeltConnectionAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7430,
        _7462,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7883,
    )
    from mastapy._private.system_model.connections_and_sockets import _2494

    Self = TypeVar("Self", bound="CVTBeltConnectionAdvancedSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CVTBeltConnectionAdvancedSystemDeflection._Cast_CVTBeltConnectionAdvancedSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CVTBeltConnectionAdvancedSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CVTBeltConnectionAdvancedSystemDeflection:
    """Special nested class for casting CVTBeltConnectionAdvancedSystemDeflection to subclasses."""

    __parent__: "CVTBeltConnectionAdvancedSystemDeflection"

    @property
    def belt_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7404.BeltConnectionAdvancedSystemDeflection":
        return self.__parent__._cast(_7404.BeltConnectionAdvancedSystemDeflection)

    @property
    def inter_mountable_component_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7462.InterMountableComponentConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7462,
        )

        return self.__parent__._cast(
            _7462.InterMountableComponentConnectionAdvancedSystemDeflection
        )

    @property
    def connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7430.ConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7430,
        )

        return self.__parent__._cast(_7430.ConnectionAdvancedSystemDeflection)

    @property
    def connection_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7883.ConnectionStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7883,
        )

        return self.__parent__._cast(_7883.ConnectionStaticLoadAnalysisCase)

    @property
    def connection_analysis_case(self: "CastSelf") -> "_7880.ConnectionAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7880,
        )

        return self.__parent__._cast(_7880.ConnectionAnalysisCase)

    @property
    def connection_analysis(self: "CastSelf") -> "_2890.ConnectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2890

        return self.__parent__._cast(_2890.ConnectionAnalysis)

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
    def cvt_belt_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "CVTBeltConnectionAdvancedSystemDeflection":
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
class CVTBeltConnectionAdvancedSystemDeflection(
    _7404.BeltConnectionAdvancedSystemDeflection
):
    """CVTBeltConnectionAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CVT_BELT_CONNECTION_ADVANCED_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_design(self: "Self") -> "_2494.CVTBeltConnection":
        """mastapy.system_model.connections_and_sockets.CVTBeltConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CVTBeltConnectionAdvancedSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_CVTBeltConnectionAdvancedSystemDeflection
        """
        return _Cast_CVTBeltConnectionAdvancedSystemDeflection(self)
