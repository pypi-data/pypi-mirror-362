"""GeometricConstants"""

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

_GEOMETRIC_CONSTANTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling", "GeometricConstants"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_designs.rolling import _2366, _2367

    Self = TypeVar("Self", bound="GeometricConstants")
    CastSelf = TypeVar("CastSelf", bound="GeometricConstants._Cast_GeometricConstants")


__docformat__ = "restructuredtext en"
__all__ = ("GeometricConstants",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GeometricConstants:
    """Special nested class for casting GeometricConstants to subclasses."""

    __parent__: "GeometricConstants"

    @property
    def geometric_constants(self: "CastSelf") -> "GeometricConstants":
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
class GeometricConstants(_0.APIBase):
    """GeometricConstants

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEOMETRIC_CONSTANTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def geometric_constants_for_rolling_frictional_moments(
        self: "Self",
    ) -> "_2366.GeometricConstantsForRollingFrictionalMoments":
        """mastapy.bearings.bearing_designs.rolling.GeometricConstantsForRollingFrictionalMoments

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GeometricConstantsForRollingFrictionalMoments"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def geometric_constants_for_sliding_frictional_moments(
        self: "Self",
    ) -> "_2367.GeometricConstantsForSlidingFrictionalMoments":
        """mastapy.bearings.bearing_designs.rolling.GeometricConstantsForSlidingFrictionalMoments

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GeometricConstantsForSlidingFrictionalMoments"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_GeometricConstants":
        """Cast to another type.

        Returns:
            _Cast_GeometricConstants
        """
        return _Cast_GeometricConstants(self)
