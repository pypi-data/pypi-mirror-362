"""FindleyCriticalPlaneAnalysis"""

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
from mastapy._private._math.vector_2d import Vector2D

_FINDLEY_CRITICAL_PLANE_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.GearTwoDFEAnalysis", "FindleyCriticalPlaneAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="FindleyCriticalPlaneAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FindleyCriticalPlaneAnalysis._Cast_FindleyCriticalPlaneAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FindleyCriticalPlaneAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FindleyCriticalPlaneAnalysis:
    """Special nested class for casting FindleyCriticalPlaneAnalysis to subclasses."""

    __parent__: "FindleyCriticalPlaneAnalysis"

    @property
    def findley_critical_plane_analysis(
        self: "CastSelf",
    ) -> "FindleyCriticalPlaneAnalysis":
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
class FindleyCriticalPlaneAnalysis(_0.APIBase):
    """FindleyCriticalPlaneAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FINDLEY_CRITICAL_PLANE_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def crack_initiation_risk_factor(self: "Self") -> "List[float]":
        """List[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CrackInitiationRiskFactor")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, float)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def max_normal_stress(self: "Self") -> "List[float]":
        """List[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaxNormalStress")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, float)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def max_shear_amplitude(self: "Self") -> "List[float]":
        """List[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaxShearAmplitude")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, float)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def maximum_findley_critical_plane_angle(self: "Self") -> "List[Vector2D]":
        """List[Vector2D]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumFindleyCriticalPlaneAngle")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, Vector2D)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def maximum_findley_critical_plane_stress(self: "Self") -> "List[float]":
        """List[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumFindleyCriticalPlaneStress")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, float)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_FindleyCriticalPlaneAnalysis":
        """Cast to another type.

        Returns:
            _Cast_FindleyCriticalPlaneAnalysis
        """
        return _Cast_FindleyCriticalPlaneAnalysis(self)
