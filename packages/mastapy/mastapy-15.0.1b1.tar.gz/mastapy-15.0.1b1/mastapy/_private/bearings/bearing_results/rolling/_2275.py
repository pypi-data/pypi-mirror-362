"""ResultsAtRollerOffset"""

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

_RESULTS_AT_ROLLER_OFFSET = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "ResultsAtRollerOffset"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ResultsAtRollerOffset")
    CastSelf = TypeVar(
        "CastSelf", bound="ResultsAtRollerOffset._Cast_ResultsAtRollerOffset"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ResultsAtRollerOffset",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ResultsAtRollerOffset:
    """Special nested class for casting ResultsAtRollerOffset to subclasses."""

    __parent__: "ResultsAtRollerOffset"

    @property
    def results_at_roller_offset(self: "CastSelf") -> "ResultsAtRollerOffset":
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
class ResultsAtRollerOffset(_0.APIBase):
    """ResultsAtRollerOffset

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RESULTS_AT_ROLLER_OFFSET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def maximum_normal_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumNormalStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_shear_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumShearStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_stress_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalStressInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_stress_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalStressOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def offset(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Offset")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def shear_stress_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShearStressInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def shear_stress_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShearStressOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ResultsAtRollerOffset":
        """Cast to another type.

        Returns:
            _Cast_ResultsAtRollerOffset
        """
        return _Cast_ResultsAtRollerOffset(self)
