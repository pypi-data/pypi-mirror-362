"""ParallelPartGroupSelection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.part_model.part_groups import _2725

_PARALLEL_PART_GROUP_SELECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.PartGroups", "ParallelPartGroupSelection"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.part_model.part_groups import _2721, _2724, _2727

    Self = TypeVar("Self", bound="ParallelPartGroupSelection")
    CastSelf = TypeVar(
        "CastSelf", bound="ParallelPartGroupSelection._Cast_ParallelPartGroupSelection"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ParallelPartGroupSelection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ParallelPartGroupSelection:
    """Special nested class for casting ParallelPartGroupSelection to subclasses."""

    __parent__: "ParallelPartGroupSelection"

    @property
    def parallel_part_group(self: "CastSelf") -> "_2725.ParallelPartGroup":
        return self.__parent__._cast(_2725.ParallelPartGroup)

    @property
    def concentric_or_parallel_part_group(
        self: "CastSelf",
    ) -> "_2721.ConcentricOrParallelPartGroup":
        from mastapy._private.system_model.part_model.part_groups import _2721

        return self.__parent__._cast(_2721.ConcentricOrParallelPartGroup)

    @property
    def part_group(self: "CastSelf") -> "_2727.PartGroup":
        from mastapy._private.system_model.part_model.part_groups import _2727

        return self.__parent__._cast(_2727.PartGroup)

    @property
    def parallel_part_group_selection(self: "CastSelf") -> "ParallelPartGroupSelection":
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
class ParallelPartGroupSelection(_2725.ParallelPartGroup):
    """ParallelPartGroupSelection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PARALLEL_PART_GROUP_SELECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def design_measurements(self: "Self") -> "List[_2724.DesignMeasurements]":
        """List[mastapy.system_model.part_model.part_groups.DesignMeasurements]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DesignMeasurements")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ParallelPartGroupSelection":
        """Cast to another type.

        Returns:
            _Cast_ParallelPartGroupSelection
        """
        return _Cast_ParallelPartGroupSelection(self)
