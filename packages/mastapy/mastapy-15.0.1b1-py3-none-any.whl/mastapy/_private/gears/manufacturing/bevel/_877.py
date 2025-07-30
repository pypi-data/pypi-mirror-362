"""ConicalFlankDeviationsData"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_CONICAL_FLANK_DEVIATIONS_DATA = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel", "ConicalFlankDeviationsData"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ConicalFlankDeviationsData")
    CastSelf = TypeVar(
        "CastSelf", bound="ConicalFlankDeviationsData._Cast_ConicalFlankDeviationsData"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalFlankDeviationsData",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalFlankDeviationsData:
    """Special nested class for casting ConicalFlankDeviationsData to subclasses."""

    __parent__: "ConicalFlankDeviationsData"

    @property
    def conical_flank_deviations_data(self: "CastSelf") -> "ConicalFlankDeviationsData":
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
class ConicalFlankDeviationsData(_0.APIBase):
    """ConicalFlankDeviationsData

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_FLANK_DEVIATIONS_DATA

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def average_crowning_deviation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AverageCrowningDeviation")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def average_pressure_angle_deviation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AveragePressureAngleDeviation")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def average_profile_curvature_deviation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AverageProfileCurvatureDeviation")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def average_spiral_angle_deviation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AverageSpiralAngleDeviation")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def bias_deviation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BiasDeviation")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalFlankDeviationsData":
        """Cast to another type.

        Returns:
            _Cast_ConicalFlankDeviationsData
        """
        return _Cast_ConicalFlankDeviationsData(self)
