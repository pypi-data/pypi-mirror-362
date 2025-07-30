"""ForceAtLaminaGroupReportable"""

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

_FORCE_AT_LAMINA_GROUP_REPORTABLE = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "ForceAtLaminaGroupReportable"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling import _2178

    Self = TypeVar("Self", bound="ForceAtLaminaGroupReportable")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ForceAtLaminaGroupReportable._Cast_ForceAtLaminaGroupReportable",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ForceAtLaminaGroupReportable",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ForceAtLaminaGroupReportable:
    """Special nested class for casting ForceAtLaminaGroupReportable to subclasses."""

    __parent__: "ForceAtLaminaGroupReportable"

    @property
    def force_at_lamina_group_reportable(
        self: "CastSelf",
    ) -> "ForceAtLaminaGroupReportable":
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
class ForceAtLaminaGroupReportable(_0.APIBase):
    """ForceAtLaminaGroupReportable

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FORCE_AT_LAMINA_GROUP_REPORTABLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def forces_at_laminae(self: "Self") -> "List[_2178.ForceAtLaminaReportable]":
        """List[mastapy.bearings.bearing_results.rolling.ForceAtLaminaReportable]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForcesAtLaminae")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ForceAtLaminaGroupReportable":
        """Cast to another type.

        Returns:
            _Cast_ForceAtLaminaGroupReportable
        """
        return _Cast_ForceAtLaminaGroupReportable(self)
