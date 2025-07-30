"""CouplingConnectionPowerFlow"""

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
from mastapy._private.system_model.analyses_and_results.power_flows import _4361

_COUPLING_CONNECTION_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows",
    "CouplingConnectionPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7883,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4314,
        _4319,
        _4328,
        _4378,
        _4402,
        _4418,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import _2567

    Self = TypeVar("Self", bound="CouplingConnectionPowerFlow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingConnectionPowerFlow._Cast_CouplingConnectionPowerFlow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingConnectionPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingConnectionPowerFlow:
    """Special nested class for casting CouplingConnectionPowerFlow to subclasses."""

    __parent__: "CouplingConnectionPowerFlow"

    @property
    def inter_mountable_component_connection_power_flow(
        self: "CastSelf",
    ) -> "_4361.InterMountableComponentConnectionPowerFlow":
        return self.__parent__._cast(_4361.InterMountableComponentConnectionPowerFlow)

    @property
    def connection_power_flow(self: "CastSelf") -> "_4328.ConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4328

        return self.__parent__._cast(_4328.ConnectionPowerFlow)

    @property
    def connection_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7883.ConnectionStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7883,
        )

        return self.__parent__._cast(_7883.ConnectionStaticLoadAnalysisCase)

    @property
    def connection_analysis_case(self: "CastSelf") -> "_7880.ConnectionAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7880,
        )

        return self.__parent__._cast(_7880.ConnectionAnalysisCase)

    @property
    def connection_analysis(self: "CastSelf") -> "_2890.ConnectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2890

        return self.__parent__._cast(_2890.ConnectionAnalysis)

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
    def clutch_connection_power_flow(
        self: "CastSelf",
    ) -> "_4314.ClutchConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4314

        return self.__parent__._cast(_4314.ClutchConnectionPowerFlow)

    @property
    def concept_coupling_connection_power_flow(
        self: "CastSelf",
    ) -> "_4319.ConceptCouplingConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4319

        return self.__parent__._cast(_4319.ConceptCouplingConnectionPowerFlow)

    @property
    def part_to_part_shear_coupling_connection_power_flow(
        self: "CastSelf",
    ) -> "_4378.PartToPartShearCouplingConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4378

        return self.__parent__._cast(_4378.PartToPartShearCouplingConnectionPowerFlow)

    @property
    def spring_damper_connection_power_flow(
        self: "CastSelf",
    ) -> "_4402.SpringDamperConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4402

        return self.__parent__._cast(_4402.SpringDamperConnectionPowerFlow)

    @property
    def torque_converter_connection_power_flow(
        self: "CastSelf",
    ) -> "_4418.TorqueConverterConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4418

        return self.__parent__._cast(_4418.TorqueConverterConnectionPowerFlow)

    @property
    def coupling_connection_power_flow(
        self: "CastSelf",
    ) -> "CouplingConnectionPowerFlow":
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
class CouplingConnectionPowerFlow(_4361.InterMountableComponentConnectionPowerFlow):
    """CouplingConnectionPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_CONNECTION_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_design(self: "Self") -> "_2567.CouplingConnection":
        """mastapy.system_model.connections_and_sockets.couplings.CouplingConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CouplingConnectionPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_CouplingConnectionPowerFlow
        """
        return _Cast_CouplingConnectionPowerFlow(self)
