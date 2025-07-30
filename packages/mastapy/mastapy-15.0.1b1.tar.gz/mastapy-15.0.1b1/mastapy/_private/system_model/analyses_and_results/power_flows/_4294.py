"""AbstractShaftOrHousingPowerFlow"""

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
from mastapy._private.system_model.analyses_and_results.power_flows import _4318

_ABSTRACT_SHAFT_OR_HOUSING_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows",
    "AbstractShaftOrHousingPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4295,
        _4339,
        _4352,
        _4377,
        _4396,
    )
    from mastapy._private.system_model.part_model import _2661

    Self = TypeVar("Self", bound="AbstractShaftOrHousingPowerFlow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractShaftOrHousingPowerFlow._Cast_AbstractShaftOrHousingPowerFlow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractShaftOrHousingPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftOrHousingPowerFlow:
    """Special nested class for casting AbstractShaftOrHousingPowerFlow to subclasses."""

    __parent__: "AbstractShaftOrHousingPowerFlow"

    @property
    def component_power_flow(self: "CastSelf") -> "_4318.ComponentPowerFlow":
        return self.__parent__._cast(_4318.ComponentPowerFlow)

    @property
    def part_power_flow(self: "CastSelf") -> "_4377.PartPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4377

        return self.__parent__._cast(_4377.PartPowerFlow)

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
    def abstract_shaft_power_flow(self: "CastSelf") -> "_4295.AbstractShaftPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4295

        return self.__parent__._cast(_4295.AbstractShaftPowerFlow)

    @property
    def cycloidal_disc_power_flow(self: "CastSelf") -> "_4339.CycloidalDiscPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4339

        return self.__parent__._cast(_4339.CycloidalDiscPowerFlow)

    @property
    def fe_part_power_flow(self: "CastSelf") -> "_4352.FEPartPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4352

        return self.__parent__._cast(_4352.FEPartPowerFlow)

    @property
    def shaft_power_flow(self: "CastSelf") -> "_4396.ShaftPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4396

        return self.__parent__._cast(_4396.ShaftPowerFlow)

    @property
    def abstract_shaft_or_housing_power_flow(
        self: "CastSelf",
    ) -> "AbstractShaftOrHousingPowerFlow":
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
class AbstractShaftOrHousingPowerFlow(_4318.ComponentPowerFlow):
    """AbstractShaftOrHousingPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_SHAFT_OR_HOUSING_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2661.AbstractShaftOrHousing":
        """mastapy.system_model.part_model.AbstractShaftOrHousing

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractShaftOrHousingPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftOrHousingPowerFlow
        """
        return _Cast_AbstractShaftOrHousingPowerFlow(self)
