"""CVTCompoundDynamicAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
    _6732,
)

_CVT_COMPOUND_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound",
    "CVTCompoundDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6630,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
        _6722,
        _6803,
        _6822,
    )

    Self = TypeVar("Self", bound="CVTCompoundDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="CVTCompoundDynamicAnalysis._Cast_CVTCompoundDynamicAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CVTCompoundDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CVTCompoundDynamicAnalysis:
    """Special nested class for casting CVTCompoundDynamicAnalysis to subclasses."""

    __parent__: "CVTCompoundDynamicAnalysis"

    @property
    def belt_drive_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6732.BeltDriveCompoundDynamicAnalysis":
        return self.__parent__._cast(_6732.BeltDriveCompoundDynamicAnalysis)

    @property
    def specialised_assembly_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6822.SpecialisedAssemblyCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6822,
        )

        return self.__parent__._cast(_6822.SpecialisedAssemblyCompoundDynamicAnalysis)

    @property
    def abstract_assembly_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6722.AbstractAssemblyCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6722,
        )

        return self.__parent__._cast(_6722.AbstractAssemblyCompoundDynamicAnalysis)

    @property
    def part_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6803.PartCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6803,
        )

        return self.__parent__._cast(_6803.PartCompoundDynamicAnalysis)

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
    def cvt_compound_dynamic_analysis(self: "CastSelf") -> "CVTCompoundDynamicAnalysis":
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
class CVTCompoundDynamicAnalysis(_6732.BeltDriveCompoundDynamicAnalysis):
    """CVTCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CVT_COMPOUND_DYNAMIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_analysis_cases_ready(self: "Self") -> "List[_6630.CVTDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.CVTDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def assembly_analysis_cases(self: "Self") -> "List[_6630.CVTDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.CVTDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CVTCompoundDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CVTCompoundDynamicAnalysis
        """
        return _Cast_CVTCompoundDynamicAnalysis(self)
