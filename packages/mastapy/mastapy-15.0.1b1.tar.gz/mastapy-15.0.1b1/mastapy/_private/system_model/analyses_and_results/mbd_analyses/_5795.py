"""TorqueConverterConnectionMultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5700

_TORQUE_CONVERTER_CONNECTION_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses",
    "TorqueConverterConnectionMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7884,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
        _5698,
        _5733,
        _5799,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7844
    from mastapy._private.system_model.connections_and_sockets.couplings import _2573

    Self = TypeVar("Self", bound="TorqueConverterConnectionMultibodyDynamicsAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="TorqueConverterConnectionMultibodyDynamicsAnalysis._Cast_TorqueConverterConnectionMultibodyDynamicsAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("TorqueConverterConnectionMultibodyDynamicsAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TorqueConverterConnectionMultibodyDynamicsAnalysis:
    """Special nested class for casting TorqueConverterConnectionMultibodyDynamicsAnalysis to subclasses."""

    __parent__: "TorqueConverterConnectionMultibodyDynamicsAnalysis"

    @property
    def coupling_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5700.CouplingConnectionMultibodyDynamicsAnalysis":
        return self.__parent__._cast(_5700.CouplingConnectionMultibodyDynamicsAnalysis)

    @property
    def inter_mountable_component_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5733.InterMountableComponentConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5733,
        )

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
    def torque_converter_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "TorqueConverterConnectionMultibodyDynamicsAnalysis":
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
class TorqueConverterConnectionMultibodyDynamicsAnalysis(
    _5700.CouplingConnectionMultibodyDynamicsAnalysis
):
    """TorqueConverterConnectionMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TORQUE_CONVERTER_CONNECTION_MULTIBODY_DYNAMICS_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def capacity_factor_k(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CapacityFactorK")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def inverse_capacity_factor_1k(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InverseCapacityFactor1K")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def is_locked(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsLocked")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def lock_up_clutch_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LockUpClutchTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lock_up_viscous_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LockUpViscousTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def locked_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LockedTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def locking_status(self: "Self") -> "_5799.TorqueConverterStatus":
        """mastapy.system_model.analyses_and_results.mbd_analyses.TorqueConverterStatus

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LockingStatus")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.TorqueConverterStatus",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.mbd_analyses._5799",
            "TorqueConverterStatus",
        )(value)

    @property
    @exception_bridge
    def percentage_applied_pressure(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PercentageAppliedPressure")

        if temp is None:
            return 0.0

        return temp

    @percentage_applied_pressure.setter
    @exception_bridge
    @enforce_parameter_types
    def percentage_applied_pressure(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PercentageAppliedPressure",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def power_loss(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerLoss")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pump_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PumpTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def speed_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpeedRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def torque_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorqueRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def turbine_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TurbineTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def connection_design(self: "Self") -> "_2573.TorqueConverterConnection":
        """mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection

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
    def connection_load_case(self: "Self") -> "_7844.TorqueConverterConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.TorqueConverterConnectionLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_TorqueConverterConnectionMultibodyDynamicsAnalysis":
        """Cast to another type.

        Returns:
            _Cast_TorqueConverterConnectionMultibodyDynamicsAnalysis
        """
        return _Cast_TorqueConverterConnectionMultibodyDynamicsAnalysis(self)
