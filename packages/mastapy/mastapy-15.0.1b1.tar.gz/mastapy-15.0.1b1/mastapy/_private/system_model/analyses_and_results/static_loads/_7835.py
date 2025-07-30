"""StraightBevelGearSetLoadCase"""

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
from mastapy._private.system_model.analyses_and_results.static_loads import _7698

_STRAIGHT_BEVEL_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "StraightBevelGearSetLoadCase",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7675,
        _7684,
        _7717,
        _7764,
        _7799,
        _7823,
        _7833,
        _7834,
    )
    from mastapy._private.system_model.part_model.gears import _2786

    Self = TypeVar("Self", bound="StraightBevelGearSetLoadCase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelGearSetLoadCase._Cast_StraightBevelGearSetLoadCase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelGearSetLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelGearSetLoadCase:
    """Special nested class for casting StraightBevelGearSetLoadCase to subclasses."""

    __parent__: "StraightBevelGearSetLoadCase"

    @property
    def bevel_gear_set_load_case(self: "CastSelf") -> "_7698.BevelGearSetLoadCase":
        return self.__parent__._cast(_7698.BevelGearSetLoadCase)

    @property
    def agma_gleason_conical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7684.AGMAGleasonConicalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7684,
        )

        return self.__parent__._cast(_7684.AGMAGleasonConicalGearSetLoadCase)

    @property
    def conical_gear_set_load_case(self: "CastSelf") -> "_7717.ConicalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7717,
        )

        return self.__parent__._cast(_7717.ConicalGearSetLoadCase)

    @property
    def gear_set_load_case(self: "CastSelf") -> "_7764.GearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7764,
        )

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
    def straight_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "StraightBevelGearSetLoadCase":
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
class StraightBevelGearSetLoadCase(_7698.BevelGearSetLoadCase):
    """StraightBevelGearSetLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_GEAR_SET_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_design(self: "Self") -> "_2786.StraightBevelGearSet":
        """mastapy.system_model.part_model.gears.StraightBevelGearSet

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
    def bevel_gears_load_case(self: "Self") -> "List[_7833.StraightBevelGearLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelGearsLoadCase")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def straight_bevel_gears_load_case(
        self: "Self",
    ) -> "List[_7833.StraightBevelGearLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StraightBevelGearsLoadCase")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def bevel_meshes_load_case(
        self: "Self",
    ) -> "List[_7834.StraightBevelGearMeshLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearMeshLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelMeshesLoadCase")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def straight_bevel_meshes_load_case(
        self: "Self",
    ) -> "List[_7834.StraightBevelGearMeshLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearMeshLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StraightBevelMeshesLoadCase")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_StraightBevelGearSetLoadCase":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelGearSetLoadCase
        """
        return _Cast_StraightBevelGearSetLoadCase(self)
