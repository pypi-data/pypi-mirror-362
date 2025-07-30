"""ConcentricPartGroupParallelToThis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_CONCENTRIC_PART_GROUP_PARALLEL_TO_THIS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.PartGroups", "ConcentricPartGroupParallelToThis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.part_model.part_groups import _2721

    Self = TypeVar("Self", bound="ConcentricPartGroupParallelToThis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConcentricPartGroupParallelToThis._Cast_ConcentricPartGroupParallelToThis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConcentricPartGroupParallelToThis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConcentricPartGroupParallelToThis:
    """Special nested class for casting ConcentricPartGroupParallelToThis to subclasses."""

    __parent__: "ConcentricPartGroupParallelToThis"

    @property
    def concentric_part_group_parallel_to_this(
        self: "CastSelf",
    ) -> "ConcentricPartGroupParallelToThis":
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
class ConcentricPartGroupParallelToThis(_0.APIBase):
    """ConcentricPartGroupParallelToThis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONCENTRIC_PART_GROUP_PARALLEL_TO_THIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def centre_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CentreDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def parallel_group(self: "Self") -> "_2721.ConcentricOrParallelPartGroup":
        """mastapy.system_model.part_model.part_groups.ConcentricOrParallelPartGroup

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ParallelGroup")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConcentricPartGroupParallelToThis":
        """Cast to another type.

        Returns:
            _Cast_ConcentricPartGroupParallelToThis
        """
        return _Cast_ConcentricPartGroupParallelToThis(self)
