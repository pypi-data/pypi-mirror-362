"""BevelDifferentialSunGearLoadCase"""

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
from mastapy._private.system_model.analyses_and_results.static_loads import _7691

_BEVEL_DIFFERENTIAL_SUN_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "BevelDifferentialSunGearLoadCase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7682,
        _7696,
        _7706,
        _7713,
        _7759,
        _7795,
        _7799,
    )
    from mastapy._private.system_model.part_model.gears import _2755

    Self = TypeVar("Self", bound="BevelDifferentialSunGearLoadCase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelDifferentialSunGearLoadCase._Cast_BevelDifferentialSunGearLoadCase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelDifferentialSunGearLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelDifferentialSunGearLoadCase:
    """Special nested class for casting BevelDifferentialSunGearLoadCase to subclasses."""

    __parent__: "BevelDifferentialSunGearLoadCase"

    @property
    def bevel_differential_gear_load_case(
        self: "CastSelf",
    ) -> "_7691.BevelDifferentialGearLoadCase":
        return self.__parent__._cast(_7691.BevelDifferentialGearLoadCase)

    @property
    def bevel_gear_load_case(self: "CastSelf") -> "_7696.BevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7696,
        )

        return self.__parent__._cast(_7696.BevelGearLoadCase)

    @property
    def agma_gleason_conical_gear_load_case(
        self: "CastSelf",
    ) -> "_7682.AGMAGleasonConicalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7682,
        )

        return self.__parent__._cast(_7682.AGMAGleasonConicalGearLoadCase)

    @property
    def conical_gear_load_case(self: "CastSelf") -> "_7713.ConicalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7713,
        )

        return self.__parent__._cast(_7713.ConicalGearLoadCase)

    @property
    def gear_load_case(self: "CastSelf") -> "_7759.GearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7759,
        )

        return self.__parent__._cast(_7759.GearLoadCase)

    @property
    def mountable_component_load_case(
        self: "CastSelf",
    ) -> "_7795.MountableComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7795,
        )

        return self.__parent__._cast(_7795.MountableComponentLoadCase)

    @property
    def component_load_case(self: "CastSelf") -> "_7706.ComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7706,
        )

        return self.__parent__._cast(_7706.ComponentLoadCase)

    @property
    def part_load_case(self: "CastSelf") -> "_7799.PartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7799,
        )

        return self.__parent__._cast(_7799.PartLoadCase)

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
    def bevel_differential_sun_gear_load_case(
        self: "CastSelf",
    ) -> "BevelDifferentialSunGearLoadCase":
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
class BevelDifferentialSunGearLoadCase(_7691.BevelDifferentialGearLoadCase):
    """BevelDifferentialSunGearLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_DIFFERENTIAL_SUN_GEAR_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2755.BevelDifferentialSunGear":
        """mastapy.system_model.part_model.gears.BevelDifferentialSunGear

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_BevelDifferentialSunGearLoadCase":
        """Cast to another type.

        Returns:
            _Cast_BevelDifferentialSunGearLoadCase
        """
        return _Cast_BevelDifferentialSunGearLoadCase(self)
