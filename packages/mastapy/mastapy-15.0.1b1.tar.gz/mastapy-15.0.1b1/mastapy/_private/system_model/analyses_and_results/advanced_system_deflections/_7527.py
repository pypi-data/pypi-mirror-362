"""ZerolBevelGearAdvancedSystemDeflection"""

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
from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
    _7411,
)

_ZEROL_BEVEL_GEAR_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections",
    "ZerolBevelGearAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.rating.zerol_bevel import _461
    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7399,
        _7420,
        _7427,
        _7455,
        _7477,
        _7479,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7857
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _3084,
    )
    from mastapy._private.system_model.part_model.gears import _2791

    Self = TypeVar("Self", bound="ZerolBevelGearAdvancedSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ZerolBevelGearAdvancedSystemDeflection._Cast_ZerolBevelGearAdvancedSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ZerolBevelGearAdvancedSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ZerolBevelGearAdvancedSystemDeflection:
    """Special nested class for casting ZerolBevelGearAdvancedSystemDeflection to subclasses."""

    __parent__: "ZerolBevelGearAdvancedSystemDeflection"

    @property
    def bevel_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7411.BevelGearAdvancedSystemDeflection":
        return self.__parent__._cast(_7411.BevelGearAdvancedSystemDeflection)

    @property
    def agma_gleason_conical_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7399.AGMAGleasonConicalGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7399,
        )

        return self.__parent__._cast(
            _7399.AGMAGleasonConicalGearAdvancedSystemDeflection
        )

    @property
    def conical_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7427.ConicalGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7427,
        )

        return self.__parent__._cast(_7427.ConicalGearAdvancedSystemDeflection)

    @property
    def gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7455.GearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7455,
        )

        return self.__parent__._cast(_7455.GearAdvancedSystemDeflection)

    @property
    def mountable_component_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7477.MountableComponentAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7477,
        )

        return self.__parent__._cast(_7477.MountableComponentAdvancedSystemDeflection)

    @property
    def component_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7420.ComponentAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7420,
        )

        return self.__parent__._cast(_7420.ComponentAdvancedSystemDeflection)

    @property
    def part_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7479.PartAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7479,
        )

        return self.__parent__._cast(_7479.PartAdvancedSystemDeflection)

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7890.PartStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7890,
        )

        return self.__parent__._cast(_7890.PartStaticLoadAnalysisCase)

    @property
    def part_analysis_case(self: "CastSelf") -> "_7887.PartAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7887,
        )

        return self.__parent__._cast(_7887.PartAnalysisCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2898.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2898

        return self.__parent__._cast(_2898.PartAnalysis)

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
    def zerol_bevel_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "ZerolBevelGearAdvancedSystemDeflection":
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
class ZerolBevelGearAdvancedSystemDeflection(_7411.BevelGearAdvancedSystemDeflection):
    """ZerolBevelGearAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ZEROL_BEVEL_GEAR_ADVANCED_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2791.ZerolBevelGear":
        """mastapy.system_model.part_model.gears.ZerolBevelGear

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
    def component_detailed_analysis(self: "Self") -> "_461.ZerolBevelGearRating":
        """mastapy.gears.rating.zerol_bevel.ZerolBevelGearRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDetailedAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def component_load_case(self: "Self") -> "_7857.ZerolBevelGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def component_system_deflection_results(
        self: "Self",
    ) -> "List[_3084.ZerolBevelGearSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ZerolBevelGearSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentSystemDeflectionResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ZerolBevelGearAdvancedSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_ZerolBevelGearAdvancedSystemDeflection
        """
        return _Cast_ZerolBevelGearAdvancedSystemDeflection(self)
