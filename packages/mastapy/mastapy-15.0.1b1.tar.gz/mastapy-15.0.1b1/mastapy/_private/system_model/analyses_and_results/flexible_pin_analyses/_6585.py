"""FlexiblePinAnalysisManufactureLevel"""

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
from mastapy._private.system_model.analyses_and_results.flexible_pin_analyses import (
    _6581,
)

_FLEXIBLE_PIN_ANALYSIS_MANUFACTURE_LEVEL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.FlexiblePinAnalyses",
    "FlexiblePinAnalysisManufactureLevel",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.flexible_pin_analyses import (
        _6580,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4608,
    )

    Self = TypeVar("Self", bound="FlexiblePinAnalysisManufactureLevel")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FlexiblePinAnalysisManufactureLevel._Cast_FlexiblePinAnalysisManufactureLevel",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FlexiblePinAnalysisManufactureLevel",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FlexiblePinAnalysisManufactureLevel:
    """Special nested class for casting FlexiblePinAnalysisManufactureLevel to subclasses."""

    __parent__: "FlexiblePinAnalysisManufactureLevel"

    @property
    def flexible_pin_analysis(self: "CastSelf") -> "_6581.FlexiblePinAnalysis":
        return self.__parent__._cast(_6581.FlexiblePinAnalysis)

    @property
    def combination_analysis(self: "CastSelf") -> "_6580.CombinationAnalysis":
        from mastapy._private.system_model.analyses_and_results.flexible_pin_analyses import (
            _6580,
        )

        return self.__parent__._cast(_6580.CombinationAnalysis)

    @property
    def flexible_pin_analysis_manufacture_level(
        self: "CastSelf",
    ) -> "FlexiblePinAnalysisManufactureLevel":
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
class FlexiblePinAnalysisManufactureLevel(_6581.FlexiblePinAnalysis):
    """FlexiblePinAnalysisManufactureLevel

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FLEXIBLE_PIN_ANALYSIS_MANUFACTURE_LEVEL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def load_sharing_factors(self: "Self") -> "List[float]":
        """List[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadSharingFactors")

        if temp is None:
            return None

        value = conversion.to_list_any(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def planetary_mesh_analysis(
        self: "Self",
    ) -> "_4608.CylindricalGearMeshParametricStudyTool":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.CylindricalGearMeshParametricStudyTool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PlanetaryMeshAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_FlexiblePinAnalysisManufactureLevel":
        """Cast to another type.

        Returns:
            _Cast_FlexiblePinAnalysisManufactureLevel
        """
        return _Cast_FlexiblePinAnalysisManufactureLevel(self)
