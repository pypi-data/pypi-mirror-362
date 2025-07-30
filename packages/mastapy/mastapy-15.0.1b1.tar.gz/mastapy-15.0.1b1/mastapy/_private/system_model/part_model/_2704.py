"""RadialInternalClearanceTolerance"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model import _2686

_RADIAL_INTERNAL_CLEARANCE_TOLERANCE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "RadialInternalClearanceTolerance"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RadialInternalClearanceTolerance")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RadialInternalClearanceTolerance._Cast_RadialInternalClearanceTolerance",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RadialInternalClearanceTolerance",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RadialInternalClearanceTolerance:
    """Special nested class for casting RadialInternalClearanceTolerance to subclasses."""

    __parent__: "RadialInternalClearanceTolerance"

    @property
    def internal_clearance_tolerance(
        self: "CastSelf",
    ) -> "_2686.InternalClearanceTolerance":
        return self.__parent__._cast(_2686.InternalClearanceTolerance)

    @property
    def radial_internal_clearance_tolerance(
        self: "CastSelf",
    ) -> "RadialInternalClearanceTolerance":
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
class RadialInternalClearanceTolerance(_2686.InternalClearanceTolerance):
    """RadialInternalClearanceTolerance

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RADIAL_INTERNAL_CLEARANCE_TOLERANCE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_RadialInternalClearanceTolerance":
        """Cast to another type.

        Returns:
            _Cast_RadialInternalClearanceTolerance
        """
        return _Cast_RadialInternalClearanceTolerance(self)
