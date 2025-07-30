"""RingFittingThermalResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_RING_FITTING_THERMAL_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling.Fitting", "RingFittingThermalResults"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling.fitting import (
        _2319,
        _2320,
        _2321,
    )

    Self = TypeVar("Self", bound="RingFittingThermalResults")
    CastSelf = TypeVar(
        "CastSelf", bound="RingFittingThermalResults._Cast_RingFittingThermalResults"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RingFittingThermalResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RingFittingThermalResults:
    """Special nested class for casting RingFittingThermalResults to subclasses."""

    __parent__: "RingFittingThermalResults"

    @property
    def inner_ring_fitting_thermal_results(
        self: "CastSelf",
    ) -> "_2319.InnerRingFittingThermalResults":
        from mastapy._private.bearings.bearing_results.rolling.fitting import _2319

        return self.__parent__._cast(_2319.InnerRingFittingThermalResults)

    @property
    def outer_ring_fitting_thermal_results(
        self: "CastSelf",
    ) -> "_2321.OuterRingFittingThermalResults":
        from mastapy._private.bearings.bearing_results.rolling.fitting import _2321

        return self.__parent__._cast(_2321.OuterRingFittingThermalResults)

    @property
    def ring_fitting_thermal_results(self: "CastSelf") -> "RingFittingThermalResults":
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
class RingFittingThermalResults(_0.APIBase):
    """RingFittingThermalResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RING_FITTING_THERMAL_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def change_in_diameter_due_to_interference_and_centrifugal_effects(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ChangeInDiameterDueToInterferenceAndCentrifugalEffects"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def interfacial_clearance_included_in_analysis(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "InterfacialClearanceIncludedInAnalysis"
        )

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def interfacial_normal_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InterfacialNormalStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_hoop_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumHoopStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def interference_values(self: "Self") -> "List[_2320.InterferenceComponents]":
        """List[mastapy.bearings.bearing_results.rolling.fitting.InterferenceComponents]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InterferenceValues")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_RingFittingThermalResults":
        """Cast to another type.

        Returns:
            _Cast_RingFittingThermalResults
        """
        return _Cast_RingFittingThermalResults(self)
