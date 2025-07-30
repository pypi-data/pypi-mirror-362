"""MaxStripLoadStressObject"""

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
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_MAX_STRIP_LOAD_STRESS_OBJECT = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "MaxStripLoadStressObject"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MaxStripLoadStressObject")
    CastSelf = TypeVar(
        "CastSelf", bound="MaxStripLoadStressObject._Cast_MaxStripLoadStressObject"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MaxStripLoadStressObject",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MaxStripLoadStressObject:
    """Special nested class for casting MaxStripLoadStressObject to subclasses."""

    __parent__: "MaxStripLoadStressObject"

    @property
    def max_strip_load_stress_object(self: "CastSelf") -> "MaxStripLoadStressObject":
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
class MaxStripLoadStressObject(_0.APIBase):
    """MaxStripLoadStressObject

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MAX_STRIP_LOAD_STRESS_OBJECT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def maximum_strip_load(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumStripLoad")

        if temp is None:
            return 0.0

        return temp

    @maximum_strip_load.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_strip_load(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "MaximumStripLoad", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_MaxStripLoadStressObject":
        """Cast to another type.

        Returns:
            _Cast_MaxStripLoadStressObject
        """
        return _Cast_MaxStripLoadStressObject(self)
