"""CouplingConnectionDynamicAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.dynamic_analyses import _6656

_COUPLING_CONNECTION_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses",
    "CouplingConnectionDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7882,
        _7883,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6610,
        _6615,
        _6624,
        _6673,
        _6695,
        _6710,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import _2567

    Self = TypeVar("Self", bound="CouplingConnectionDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingConnectionDynamicAnalysis._Cast_CouplingConnectionDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingConnectionDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingConnectionDynamicAnalysis:
    """Special nested class for casting CouplingConnectionDynamicAnalysis to subclasses."""

    __parent__: "CouplingConnectionDynamicAnalysis"

    @property
    def inter_mountable_component_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6656.InterMountableComponentConnectionDynamicAnalysis":
        return self.__parent__._cast(
            _6656.InterMountableComponentConnectionDynamicAnalysis
        )

    @property
    def connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6624.ConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6624,
        )

        return self.__parent__._cast(_6624.ConnectionDynamicAnalysis)

    @property
    def connection_fe_analysis(self: "CastSelf") -> "_7882.ConnectionFEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7882,
        )

        return self.__parent__._cast(_7882.ConnectionFEAnalysis)

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
    def clutch_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6610.ClutchConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6610,
        )

        return self.__parent__._cast(_6610.ClutchConnectionDynamicAnalysis)

    @property
    def concept_coupling_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6615.ConceptCouplingConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6615,
        )

        return self.__parent__._cast(_6615.ConceptCouplingConnectionDynamicAnalysis)

    @property
    def part_to_part_shear_coupling_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6673.PartToPartShearCouplingConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6673,
        )

        return self.__parent__._cast(
            _6673.PartToPartShearCouplingConnectionDynamicAnalysis
        )

    @property
    def spring_damper_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6695.SpringDamperConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6695,
        )

        return self.__parent__._cast(_6695.SpringDamperConnectionDynamicAnalysis)

    @property
    def torque_converter_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6710.TorqueConverterConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6710,
        )

        return self.__parent__._cast(_6710.TorqueConverterConnectionDynamicAnalysis)

    @property
    def coupling_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "CouplingConnectionDynamicAnalysis":
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
class CouplingConnectionDynamicAnalysis(
    _6656.InterMountableComponentConnectionDynamicAnalysis
):
    """CouplingConnectionDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_CONNECTION_DYNAMIC_ANALYSIS

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
    def cast_to(self: "Self") -> "_Cast_CouplingConnectionDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CouplingConnectionDynamicAnalysis
        """
        return _Cast_CouplingConnectionDynamicAnalysis(self)
