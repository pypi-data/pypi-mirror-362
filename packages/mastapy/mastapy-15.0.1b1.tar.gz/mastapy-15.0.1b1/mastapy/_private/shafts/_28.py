"""ShaftPointStressCycle"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_SHAFT_POINT_STRESS_CYCLE = python_net_import(
    "SMT.MastaAPI.Shafts", "ShaftPointStressCycle"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.shafts import _27, _47

    Self = TypeVar("Self", bound="ShaftPointStressCycle")
    CastSelf = TypeVar(
        "CastSelf", bound="ShaftPointStressCycle._Cast_ShaftPointStressCycle"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftPointStressCycle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftPointStressCycle:
    """Special nested class for casting ShaftPointStressCycle to subclasses."""

    __parent__: "ShaftPointStressCycle"

    @property
    def shaft_point_stress_cycle(self: "CastSelf") -> "ShaftPointStressCycle":
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
class ShaftPointStressCycle(_0.APIBase):
    """ShaftPointStressCycle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_POINT_STRESS_CYCLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def din743201212_comparative_mean_stress(
        self: "Self",
    ) -> "_47.StressMeasurementShaftAxialBendingTorsionalComponentValues":
        """mastapy.shafts.StressMeasurementShaftAxialBendingTorsionalComponentValues

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DIN743201212ComparativeMeanStress")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def stress_amplitude(self: "Self") -> "_27.ShaftPointStress":
        """mastapy.shafts.ShaftPointStress

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StressAmplitude")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def stress_mean(self: "Self") -> "_27.ShaftPointStress":
        """mastapy.shafts.ShaftPointStress

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StressMean")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def stress_total(self: "Self") -> "_27.ShaftPointStress":
        """mastapy.shafts.ShaftPointStress

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StressTotal")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftPointStressCycle":
        """Cast to another type.

        Returns:
            _Cast_ShaftPointStressCycle
        """
        return _Cast_ShaftPointStressCycle(self)
