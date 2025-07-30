"""AdvancedSystemDeflectionSubAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.system_deflections import _3068

_ADVANCED_SYSTEM_DEFLECTION_SUB_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections",
    "AdvancedSystemDeflectionSubAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2891
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7877,
        _7886,
        _7892,
    )

    Self = TypeVar("Self", bound="AdvancedSystemDeflectionSubAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AdvancedSystemDeflectionSubAnalysis._Cast_AdvancedSystemDeflectionSubAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AdvancedSystemDeflectionSubAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AdvancedSystemDeflectionSubAnalysis:
    """Special nested class for casting AdvancedSystemDeflectionSubAnalysis to subclasses."""

    __parent__: "AdvancedSystemDeflectionSubAnalysis"

    @property
    def system_deflection(self: "CastSelf") -> "_3068.SystemDeflection":
        return self.__parent__._cast(_3068.SystemDeflection)

    @property
    def fe_analysis(self: "CastSelf") -> "_7886.FEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7886,
        )

        return self.__parent__._cast(_7886.FEAnalysis)

    @property
    def static_load_analysis_case(self: "CastSelf") -> "_7892.StaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7892,
        )

        return self.__parent__._cast(_7892.StaticLoadAnalysisCase)

    @property
    def analysis_case(self: "CastSelf") -> "_7877.AnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7877,
        )

        return self.__parent__._cast(_7877.AnalysisCase)

    @property
    def context(self: "CastSelf") -> "_2891.Context":
        from mastapy._private.system_model.analyses_and_results import _2891

        return self.__parent__._cast(_2891.Context)

    @property
    def advanced_system_deflection_sub_analysis(
        self: "CastSelf",
    ) -> "AdvancedSystemDeflectionSubAnalysis":
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
class AdvancedSystemDeflectionSubAnalysis(_3068.SystemDeflection):
    """AdvancedSystemDeflectionSubAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ADVANCED_SYSTEM_DEFLECTION_SUB_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def current_time(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CurrentTime")

        if temp is None:
            return 0.0

        return temp

    @current_time.setter
    @exception_bridge
    @enforce_parameter_types
    def current_time(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "CurrentTime", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_AdvancedSystemDeflectionSubAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AdvancedSystemDeflectionSubAnalysis
        """
        return _Cast_AdvancedSystemDeflectionSubAnalysis(self)
