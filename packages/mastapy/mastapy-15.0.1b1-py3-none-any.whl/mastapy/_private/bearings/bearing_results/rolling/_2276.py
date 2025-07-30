"""RingForceAndDisplacement"""

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

_RING_FORCE_AND_DISPLACEMENT = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "RingForceAndDisplacement"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility.measured_vectors import _1748

    Self = TypeVar("Self", bound="RingForceAndDisplacement")
    CastSelf = TypeVar(
        "CastSelf", bound="RingForceAndDisplacement._Cast_RingForceAndDisplacement"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RingForceAndDisplacement",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RingForceAndDisplacement:
    """Special nested class for casting RingForceAndDisplacement to subclasses."""

    __parent__: "RingForceAndDisplacement"

    @property
    def ring_force_and_displacement(self: "CastSelf") -> "RingForceAndDisplacement":
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
class RingForceAndDisplacement(_0.APIBase):
    """RingForceAndDisplacement

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RING_FORCE_AND_DISPLACEMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def magnitude_of_misalignment_normal_to_load_direction(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MagnitudeOfMisalignmentNormalToLoadDirection"
        )

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
    def displacement(self: "Self") -> "_1748.VectorWithLinearAndAngularComponents":
        """mastapy.math_utility.measured_vectors.VectorWithLinearAndAngularComponents

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Displacement")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def force(self: "Self") -> "_1748.VectorWithLinearAndAngularComponents":
        """mastapy.math_utility.measured_vectors.VectorWithLinearAndAngularComponents

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Force")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_RingForceAndDisplacement":
        """Cast to another type.

        Returns:
            _Cast_RingForceAndDisplacement
        """
        return _Cast_RingForceAndDisplacement(self)
