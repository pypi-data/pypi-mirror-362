"""DynamicForceResultAtTime"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.mbd_analyses.reporting import (
    _5810,
)

_DYNAMIC_FORCE_RESULT_AT_TIME = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Reporting",
    "DynamicForceResultAtTime",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="DynamicForceResultAtTime")
    CastSelf = TypeVar(
        "CastSelf", bound="DynamicForceResultAtTime._Cast_DynamicForceResultAtTime"
    )


__docformat__ = "restructuredtext en"
__all__ = ("DynamicForceResultAtTime",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DynamicForceResultAtTime:
    """Special nested class for casting DynamicForceResultAtTime to subclasses."""

    __parent__: "DynamicForceResultAtTime"

    @property
    def abstract_measured_dynamic_response_at_time(
        self: "CastSelf",
    ) -> "_5810.AbstractMeasuredDynamicResponseAtTime":
        return self.__parent__._cast(_5810.AbstractMeasuredDynamicResponseAtTime)

    @property
    def dynamic_force_result_at_time(self: "CastSelf") -> "DynamicForceResultAtTime":
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
class DynamicForceResultAtTime(_5810.AbstractMeasuredDynamicResponseAtTime):
    """DynamicForceResultAtTime

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DYNAMIC_FORCE_RESULT_AT_TIME

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def absolute_dynamic_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AbsoluteDynamicForce")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def dynamic_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicForce")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Force")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanForce")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_DynamicForceResultAtTime":
        """Cast to another type.

        Returns:
            _Cast_DynamicForceResultAtTime
        """
        return _Cast_DynamicForceResultAtTime(self)
