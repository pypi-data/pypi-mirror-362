"""ClutchConnectionLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.static_loads import _7720

_CLUTCH_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ClutchConnectionLoadCase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility import _1718
    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7718,
        _7780,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import _2563

    Self = TypeVar("Self", bound="ClutchConnectionLoadCase")
    CastSelf = TypeVar(
        "CastSelf", bound="ClutchConnectionLoadCase._Cast_ClutchConnectionLoadCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ClutchConnectionLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ClutchConnectionLoadCase:
    """Special nested class for casting ClutchConnectionLoadCase to subclasses."""

    __parent__: "ClutchConnectionLoadCase"

    @property
    def coupling_connection_load_case(
        self: "CastSelf",
    ) -> "_7720.CouplingConnectionLoadCase":
        return self.__parent__._cast(_7720.CouplingConnectionLoadCase)

    @property
    def inter_mountable_component_connection_load_case(
        self: "CastSelf",
    ) -> "_7780.InterMountableComponentConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7780,
        )

        return self.__parent__._cast(_7780.InterMountableComponentConnectionLoadCase)

    @property
    def connection_load_case(self: "CastSelf") -> "_7718.ConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7718,
        )

        return self.__parent__._cast(_7718.ConnectionLoadCase)

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
    def clutch_connection_load_case(self: "CastSelf") -> "ClutchConnectionLoadCase":
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
class ClutchConnectionLoadCase(_7720.CouplingConnectionLoadCase):
    """ClutchConnectionLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CLUTCH_CONNECTION_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def clutch_initial_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ClutchInitialTemperature")

        if temp is None:
            return 0.0

        return temp

    @clutch_initial_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def clutch_initial_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ClutchInitialTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def clutch_pressures(self: "Self") -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "ClutchPressures")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @clutch_pressures.setter
    @exception_bridge
    @enforce_parameter_types
    def clutch_pressures(self: "Self", value: "_1718.Vector2DListAccessor") -> None:
        pythonnet_property_set(self.wrapped, "ClutchPressures", value.wrapped)

    @property
    @exception_bridge
    def is_initially_locked(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsInitiallyLocked")

        if temp is None:
            return False

        return temp

    @is_initially_locked.setter
    @exception_bridge
    @enforce_parameter_types
    def is_initially_locked(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IsInitiallyLocked",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def unlocked_clutch_linear_resistance_coefficient(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "UnlockedClutchLinearResistanceCoefficient"
        )

        if temp is None:
            return 0.0

        return temp

    @unlocked_clutch_linear_resistance_coefficient.setter
    @exception_bridge
    @enforce_parameter_types
    def unlocked_clutch_linear_resistance_coefficient(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UnlockedClutchLinearResistanceCoefficient",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def use_fixed_update_time(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseFixedUpdateTime")

        if temp is None:
            return False

        return temp

    @use_fixed_update_time.setter
    @exception_bridge
    @enforce_parameter_types
    def use_fixed_update_time(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseFixedUpdateTime",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def connection_design(self: "Self") -> "_2563.ClutchConnection":
        """mastapy.system_model.connections_and_sockets.couplings.ClutchConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ClutchConnectionLoadCase":
        """Cast to another type.

        Returns:
            _Cast_ClutchConnectionLoadCase
        """
        return _Cast_ClutchConnectionLoadCase(self)
