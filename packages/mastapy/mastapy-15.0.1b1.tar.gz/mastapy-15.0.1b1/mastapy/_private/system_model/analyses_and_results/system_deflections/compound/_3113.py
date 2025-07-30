"""BoltCompoundSystemDeflection"""

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
from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
    _3119,
)

_BOLT_COMPOUND_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound",
    "BoltCompoundSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2951,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
        _3176,
    )
    from mastapy._private.system_model.part_model import _2667

    Self = TypeVar("Self", bound="BoltCompoundSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BoltCompoundSystemDeflection._Cast_BoltCompoundSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BoltCompoundSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BoltCompoundSystemDeflection:
    """Special nested class for casting BoltCompoundSystemDeflection to subclasses."""

    __parent__: "BoltCompoundSystemDeflection"

    @property
    def component_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3119.ComponentCompoundSystemDeflection":
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
    def bolt_compound_system_deflection(
        self: "CastSelf",
    ) -> "BoltCompoundSystemDeflection":
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
class BoltCompoundSystemDeflection(_3119.ComponentCompoundSystemDeflection):
    """BoltCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BOLT_COMPOUND_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2667.Bolt":
        """mastapy.system_model.part_model.Bolt

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
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_2951.BoltSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.BoltSystemDeflection]

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
    @exception_bridge
    def component_analysis_cases(self: "Self") -> "List[_2951.BoltSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.BoltSystemDeflection]

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
    def cast_to(self: "Self") -> "_Cast_BoltCompoundSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_BoltCompoundSystemDeflection
        """
        return _Cast_BoltCompoundSystemDeflection(self)
