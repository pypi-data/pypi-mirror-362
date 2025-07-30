"""ForceAtLaminaReportable"""

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

_FORCE_AT_LAMINA_REPORTABLE = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "ForceAtLaminaReportable"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ForceAtLaminaReportable")
    CastSelf = TypeVar(
        "CastSelf", bound="ForceAtLaminaReportable._Cast_ForceAtLaminaReportable"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ForceAtLaminaReportable",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ForceAtLaminaReportable:
    """Special nested class for casting ForceAtLaminaReportable to subclasses."""

    __parent__: "ForceAtLaminaReportable"

    @property
    def force_at_lamina_reportable(self: "CastSelf") -> "ForceAtLaminaReportable":
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
class ForceAtLaminaReportable(_0.APIBase):
    """ForceAtLaminaReportable

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FORCE_AT_LAMINA_REPORTABLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def dynamic_equivalent_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicEquivalentLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lamina_index(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LaminaIndex")

        if temp is None:
            return 0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ForceAtLaminaReportable":
        """Cast to another type.

        Returns:
            _Cast_ForceAtLaminaReportable
        """
        return _Cast_ForceAtLaminaReportable(self)
