"""BevelGearSetCompoundPowerFlow"""

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
from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
    _4436,
)

_BEVEL_GEAR_SET_COMPOUND_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound",
    "BevelGearSetCompoundPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4311
    from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
        _4430,
        _4443,
        _4464,
        _4490,
        _4511,
        _4530,
        _4533,
        _4539,
        _4542,
        _4560,
    )

    Self = TypeVar("Self", bound="BevelGearSetCompoundPowerFlow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelGearSetCompoundPowerFlow._Cast_BevelGearSetCompoundPowerFlow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearSetCompoundPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelGearSetCompoundPowerFlow:
    """Special nested class for casting BevelGearSetCompoundPowerFlow to subclasses."""

    __parent__: "BevelGearSetCompoundPowerFlow"

    @property
    def agma_gleason_conical_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4436.AGMAGleasonConicalGearSetCompoundPowerFlow":
        return self.__parent__._cast(_4436.AGMAGleasonConicalGearSetCompoundPowerFlow)

    @property
    def conical_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4464.ConicalGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4464,
        )

        return self.__parent__._cast(_4464.ConicalGearSetCompoundPowerFlow)

    @property
    def gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4490.GearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4490,
        )

        return self.__parent__._cast(_4490.GearSetCompoundPowerFlow)

    @property
    def specialised_assembly_compound_power_flow(
        self: "CastSelf",
    ) -> "_4530.SpecialisedAssemblyCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4530,
        )

        return self.__parent__._cast(_4530.SpecialisedAssemblyCompoundPowerFlow)

    @property
    def abstract_assembly_compound_power_flow(
        self: "CastSelf",
    ) -> "_4430.AbstractAssemblyCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4430,
        )

        return self.__parent__._cast(_4430.AbstractAssemblyCompoundPowerFlow)

    @property
    def part_compound_power_flow(self: "CastSelf") -> "_4511.PartCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4511,
        )

        return self.__parent__._cast(_4511.PartCompoundPowerFlow)

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
    def bevel_differential_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4443.BevelDifferentialGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4443,
        )

        return self.__parent__._cast(_4443.BevelDifferentialGearSetCompoundPowerFlow)

    @property
    def spiral_bevel_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4533.SpiralBevelGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4533,
        )

        return self.__parent__._cast(_4533.SpiralBevelGearSetCompoundPowerFlow)

    @property
    def straight_bevel_diff_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4539.StraightBevelDiffGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4539,
        )

        return self.__parent__._cast(_4539.StraightBevelDiffGearSetCompoundPowerFlow)

    @property
    def straight_bevel_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4542.StraightBevelGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4542,
        )

        return self.__parent__._cast(_4542.StraightBevelGearSetCompoundPowerFlow)

    @property
    def zerol_bevel_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4560.ZerolBevelGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4560,
        )

        return self.__parent__._cast(_4560.ZerolBevelGearSetCompoundPowerFlow)

    @property
    def bevel_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "BevelGearSetCompoundPowerFlow":
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
class BevelGearSetCompoundPowerFlow(_4436.AGMAGleasonConicalGearSetCompoundPowerFlow):
    """BevelGearSetCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_GEAR_SET_COMPOUND_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_analysis_cases(self: "Self") -> "List[_4311.BevelGearSetPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.BevelGearSetPowerFlow]

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
    @exception_bridge
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4311.BevelGearSetPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.BevelGearSetPowerFlow]

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
    def cast_to(self: "Self") -> "_Cast_BevelGearSetCompoundPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_BevelGearSetCompoundPowerFlow
        """
        return _Cast_BevelGearSetCompoundPowerFlow(self)
