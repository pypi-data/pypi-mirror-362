"""ConicalGearSetLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.static_loads import _7764

_CONICAL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ConicalGearSetLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7675,
        _7684,
        _7693,
        _7698,
        _7713,
        _7715,
        _7716,
        _7776,
        _7783,
        _7786,
        _7789,
        _7799,
        _7823,
        _7826,
        _7832,
        _7835,
        _7859,
    )
    from mastapy._private.system_model.part_model.gears import _2761

    Self = TypeVar("Self", bound="ConicalGearSetLoadCase")
    CastSelf = TypeVar(
        "CastSelf", bound="ConicalGearSetLoadCase._Cast_ConicalGearSetLoadCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearSetLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearSetLoadCase:
    """Special nested class for casting ConicalGearSetLoadCase to subclasses."""

    __parent__: "ConicalGearSetLoadCase"

    @property
    def gear_set_load_case(self: "CastSelf") -> "_7764.GearSetLoadCase":
        return self.__parent__._cast(_7764.GearSetLoadCase)

    @property
    def specialised_assembly_load_case(
        self: "CastSelf",
    ) -> "_7823.SpecialisedAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7823,
        )

        return self.__parent__._cast(_7823.SpecialisedAssemblyLoadCase)

    @property
    def abstract_assembly_load_case(
        self: "CastSelf",
    ) -> "_7675.AbstractAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7675,
        )

        return self.__parent__._cast(_7675.AbstractAssemblyLoadCase)

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
    def agma_gleason_conical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7684.AGMAGleasonConicalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7684,
        )

        return self.__parent__._cast(_7684.AGMAGleasonConicalGearSetLoadCase)

    @property
    def bevel_differential_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7693.BevelDifferentialGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7693,
        )

        return self.__parent__._cast(_7693.BevelDifferentialGearSetLoadCase)

    @property
    def bevel_gear_set_load_case(self: "CastSelf") -> "_7698.BevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7698,
        )

        return self.__parent__._cast(_7698.BevelGearSetLoadCase)

    @property
    def hypoid_gear_set_load_case(self: "CastSelf") -> "_7776.HypoidGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7776,
        )

        return self.__parent__._cast(_7776.HypoidGearSetLoadCase)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7783.KlingelnbergCycloPalloidConicalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7783,
        )

        return self.__parent__._cast(
            _7783.KlingelnbergCycloPalloidConicalGearSetLoadCase
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7786.KlingelnbergCycloPalloidHypoidGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7786,
        )

        return self.__parent__._cast(
            _7786.KlingelnbergCycloPalloidHypoidGearSetLoadCase
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7789.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7789,
        )

        return self.__parent__._cast(
            _7789.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase
        )

    @property
    def spiral_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7826.SpiralBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7826,
        )

        return self.__parent__._cast(_7826.SpiralBevelGearSetLoadCase)

    @property
    def straight_bevel_diff_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7832.StraightBevelDiffGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7832,
        )

        return self.__parent__._cast(_7832.StraightBevelDiffGearSetLoadCase)

    @property
    def straight_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7835.StraightBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7835,
        )

        return self.__parent__._cast(_7835.StraightBevelGearSetLoadCase)

    @property
    def zerol_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7859.ZerolBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7859,
        )

        return self.__parent__._cast(_7859.ZerolBevelGearSetLoadCase)

    @property
    def conical_gear_set_load_case(self: "CastSelf") -> "ConicalGearSetLoadCase":
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
class ConicalGearSetLoadCase(_7764.GearSetLoadCase):
    """ConicalGearSetLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_SET_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_design(self: "Self") -> "_2761.ConicalGearSet":
        """mastapy.system_model.part_model.gears.ConicalGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gears_load_case(self: "Self") -> "List[_7713.ConicalGearLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.ConicalGearLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearsLoadCase")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def conical_gears_load_case(self: "Self") -> "List[_7713.ConicalGearLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.ConicalGearLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalGearsLoadCase")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def meshes_load_case(self: "Self") -> "List[_7715.ConicalGearMeshLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.ConicalGearMeshLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshesLoadCase")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def conical_meshes_load_case(self: "Self") -> "List[_7715.ConicalGearMeshLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.ConicalGearMeshLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalMeshesLoadCase")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    def get_harmonic_load_data_for_import(
        self: "Self",
    ) -> "_7716.ConicalGearSetHarmonicLoadData":
        """mastapy.system_model.analyses_and_results.static_loads.ConicalGearSetHarmonicLoadData"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetHarmonicLoadDataForImport"
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearSetLoadCase":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearSetLoadCase
        """
        return _Cast_ConicalGearSetLoadCase(self)
