"""SynchroniserPartCompoundSystemDeflection"""

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
    _3133,
)

_SYNCHRONISER_PART_COMPOUND_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound",
    "SynchroniserPartCompoundSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _3065,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
        _3119,
        _3174,
        _3176,
        _3212,
        _3214,
    )

    Self = TypeVar("Self", bound="SynchroniserPartCompoundSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SynchroniserPartCompoundSystemDeflection._Cast_SynchroniserPartCompoundSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SynchroniserPartCompoundSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SynchroniserPartCompoundSystemDeflection:
    """Special nested class for casting SynchroniserPartCompoundSystemDeflection to subclasses."""

    __parent__: "SynchroniserPartCompoundSystemDeflection"

    @property
    def coupling_half_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3133.CouplingHalfCompoundSystemDeflection":
        return self.__parent__._cast(_3133.CouplingHalfCompoundSystemDeflection)

    @property
    def mountable_component_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3174.MountableComponentCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3174,
        )

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
    def synchroniser_half_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3212.SynchroniserHalfCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3212,
        )

        return self.__parent__._cast(_3212.SynchroniserHalfCompoundSystemDeflection)

    @property
    def synchroniser_sleeve_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3214.SynchroniserSleeveCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3214,
        )

        return self.__parent__._cast(_3214.SynchroniserSleeveCompoundSystemDeflection)

    @property
    def synchroniser_part_compound_system_deflection(
        self: "CastSelf",
    ) -> "SynchroniserPartCompoundSystemDeflection":
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
class SynchroniserPartCompoundSystemDeflection(
    _3133.CouplingHalfCompoundSystemDeflection
):
    """SynchroniserPartCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SYNCHRONISER_PART_COMPOUND_SYSTEM_DEFLECTION

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
    ) -> "List[_3065.SynchroniserPartSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.SynchroniserPartSystemDeflection]

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
    ) -> "List[_3065.SynchroniserPartSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.SynchroniserPartSystemDeflection]

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
    def cast_to(self: "Self") -> "_Cast_SynchroniserPartCompoundSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_SynchroniserPartCompoundSystemDeflection
        """
        return _Cast_SynchroniserPartCompoundSystemDeflection(self)
