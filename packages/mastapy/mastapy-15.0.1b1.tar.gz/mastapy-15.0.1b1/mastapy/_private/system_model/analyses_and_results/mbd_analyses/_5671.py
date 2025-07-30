"""BeltConnectionMultibodyDynamicsAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5733

_BELT_CONNECTION_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses",
    "BeltConnectionMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis import _77
    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7884,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
        _5698,
        _5703,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7689
    from mastapy._private.system_model.connections_and_sockets import _2489

    Self = TypeVar("Self", bound="BeltConnectionMultibodyDynamicsAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BeltConnectionMultibodyDynamicsAnalysis._Cast_BeltConnectionMultibodyDynamicsAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BeltConnectionMultibodyDynamicsAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BeltConnectionMultibodyDynamicsAnalysis:
    """Special nested class for casting BeltConnectionMultibodyDynamicsAnalysis to subclasses."""

    __parent__: "BeltConnectionMultibodyDynamicsAnalysis"

    @property
    def inter_mountable_component_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5733.InterMountableComponentConnectionMultibodyDynamicsAnalysis":
        return self.__parent__._cast(
            _5733.InterMountableComponentConnectionMultibodyDynamicsAnalysis
        )

    @property
    def connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5698.ConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5698,
        )

        return self.__parent__._cast(_5698.ConnectionMultibodyDynamicsAnalysis)

    @property
    def connection_time_series_load_analysis_case(
        self: "CastSelf",
    ) -> "_7884.ConnectionTimeSeriesLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7884,
        )

        return self.__parent__._cast(_7884.ConnectionTimeSeriesLoadAnalysisCase)

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
    def cvt_belt_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5703.CVTBeltConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5703,
        )

        return self.__parent__._cast(_5703.CVTBeltConnectionMultibodyDynamicsAnalysis)

    @property
    def belt_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "BeltConnectionMultibodyDynamicsAnalysis":
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
class BeltConnectionMultibodyDynamicsAnalysis(
    _5733.InterMountableComponentConnectionMultibodyDynamicsAnalysis
):
    """BeltConnectionMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BELT_CONNECTION_MULTIBODY_DYNAMICS_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def extension(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Extension")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def loading_status(self: "Self") -> "_77.LoadingStatus":
        """mastapy.nodal_analysis.LoadingStatus

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadingStatus")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.NodalAnalysis.LoadingStatus"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.nodal_analysis._77", "LoadingStatus"
        )(value)

    @property
    @exception_bridge
    def rate_of_change_of_extension(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RateOfChangeOfExtension")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tension(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Tension")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def connection_design(self: "Self") -> "_2489.BeltConnection":
        """mastapy.system_model.connections_and_sockets.BeltConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def connection_load_case(self: "Self") -> "_7689.BeltConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.BeltConnectionLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_BeltConnectionMultibodyDynamicsAnalysis":
        """Cast to another type.

        Returns:
            _Cast_BeltConnectionMultibodyDynamicsAnalysis
        """
        return _Cast_BeltConnectionMultibodyDynamicsAnalysis(self)
