"""VDI2737SafetyFactorReportingObject"""

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

_VDI2737_SAFETY_FACTOR_REPORTING_OBJECT = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical", "VDI2737SafetyFactorReportingObject"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="VDI2737SafetyFactorReportingObject")
    CastSelf = TypeVar(
        "CastSelf",
        bound="VDI2737SafetyFactorReportingObject._Cast_VDI2737SafetyFactorReportingObject",
    )


__docformat__ = "restructuredtext en"
__all__ = ("VDI2737SafetyFactorReportingObject",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_VDI2737SafetyFactorReportingObject:
    """Special nested class for casting VDI2737SafetyFactorReportingObject to subclasses."""

    __parent__: "VDI2737SafetyFactorReportingObject"

    @property
    def vdi2737_safety_factor_reporting_object(
        self: "CastSelf",
    ) -> "VDI2737SafetyFactorReportingObject":
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
class VDI2737SafetyFactorReportingObject(_0.APIBase):
    """VDI2737SafetyFactorReportingObject

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _VDI2737_SAFETY_FACTOR_REPORTING_OBJECT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def crack_initiation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CrackInitiation")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def fatigue_fracture(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FatigueFracture")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def permanent_deformation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PermanentDeformation")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_VDI2737SafetyFactorReportingObject":
        """Cast to another type.

        Returns:
            _Cast_VDI2737SafetyFactorReportingObject
        """
        return _Cast_VDI2737SafetyFactorReportingObject(self)
