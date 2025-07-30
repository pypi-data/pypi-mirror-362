"""AxialInternalClearanceTolerance"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model import _2686

_AXIAL_INTERNAL_CLEARANCE_TOLERANCE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "AxialInternalClearanceTolerance"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="AxialInternalClearanceTolerance")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AxialInternalClearanceTolerance._Cast_AxialInternalClearanceTolerance",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AxialInternalClearanceTolerance",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AxialInternalClearanceTolerance:
    """Special nested class for casting AxialInternalClearanceTolerance to subclasses."""

    __parent__: "AxialInternalClearanceTolerance"

    @property
    def internal_clearance_tolerance(
        self: "CastSelf",
    ) -> "_2686.InternalClearanceTolerance":
        return self.__parent__._cast(_2686.InternalClearanceTolerance)

    @property
    def axial_internal_clearance_tolerance(
        self: "CastSelf",
    ) -> "AxialInternalClearanceTolerance":
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
class AxialInternalClearanceTolerance(_2686.InternalClearanceTolerance):
    """AxialInternalClearanceTolerance

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AXIAL_INTERNAL_CLEARANCE_TOLERANCE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_AxialInternalClearanceTolerance":
        """Cast to another type.

        Returns:
            _Cast_AxialInternalClearanceTolerance
        """
        return _Cast_AxialInternalClearanceTolerance(self)
