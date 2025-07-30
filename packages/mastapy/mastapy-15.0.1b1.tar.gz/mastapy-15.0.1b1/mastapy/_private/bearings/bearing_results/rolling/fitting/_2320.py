"""InterferenceComponents"""

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

_INTERFERENCE_COMPONENTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling.Fitting", "InterferenceComponents"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="InterferenceComponents")
    CastSelf = TypeVar(
        "CastSelf", bound="InterferenceComponents._Cast_InterferenceComponents"
    )


__docformat__ = "restructuredtext en"
__all__ = ("InterferenceComponents",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InterferenceComponents:
    """Special nested class for casting InterferenceComponents to subclasses."""

    __parent__: "InterferenceComponents"

    @property
    def interference_components(self: "CastSelf") -> "InterferenceComponents":
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
class InterferenceComponents(_0.APIBase):
    """InterferenceComponents

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INTERFERENCE_COMPONENTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def nominal_interfacial_interference(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalInterfacialInterference")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def reduction_in_interference_from_centrifugal_effects(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ReductionInInterferenceFromCentrifugalEffects"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_interfacial_interference(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalInterfacialInterference")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_InterferenceComponents":
        """Cast to another type.

        Returns:
            _Cast_InterferenceComponents
        """
        return _Cast_InterferenceComponents(self)
