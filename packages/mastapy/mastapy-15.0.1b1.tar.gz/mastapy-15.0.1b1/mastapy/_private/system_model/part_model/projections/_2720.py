"""SpecifiedParallelPartGroupDrawingOrder"""

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

_SPECIFIED_PARALLEL_PART_GROUP_DRAWING_ORDER = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Projections",
    "SpecifiedParallelPartGroupDrawingOrder",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.part_model.projections import _2719

    Self = TypeVar("Self", bound="SpecifiedParallelPartGroupDrawingOrder")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SpecifiedParallelPartGroupDrawingOrder._Cast_SpecifiedParallelPartGroupDrawingOrder",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpecifiedParallelPartGroupDrawingOrder",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpecifiedParallelPartGroupDrawingOrder:
    """Special nested class for casting SpecifiedParallelPartGroupDrawingOrder to subclasses."""

    __parent__: "SpecifiedParallelPartGroupDrawingOrder"

    @property
    def specified_parallel_part_group_drawing_order(
        self: "CastSelf",
    ) -> "SpecifiedParallelPartGroupDrawingOrder":
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
class SpecifiedParallelPartGroupDrawingOrder(_0.APIBase):
    """SpecifiedParallelPartGroupDrawingOrder

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPECIFIED_PARALLEL_PART_GROUP_DRAWING_ORDER

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
    def specified_groups(
        self: "Self",
    ) -> "List[_2719.SpecifiedConcentricPartGroupDrawingOrder]":
        """List[mastapy.system_model.part_model.projections.SpecifiedConcentricPartGroupDrawingOrder]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpecifiedGroups")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_SpecifiedParallelPartGroupDrawingOrder":
        """Cast to another type.

        Returns:
            _Cast_SpecifiedParallelPartGroupDrawingOrder
        """
        return _Cast_SpecifiedParallelPartGroupDrawingOrder(self)
