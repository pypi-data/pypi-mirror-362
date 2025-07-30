"""ConcentricPartGroup"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private._math.vector_2d import Vector2D
from mastapy._private.system_model.part_model.part_groups import _2721

_CONCENTRIC_PART_GROUP = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.PartGroups", "ConcentricPartGroup"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.part_model.part_groups import _2723, _2727

    Self = TypeVar("Self", bound="ConcentricPartGroup")
    CastSelf = TypeVar(
        "CastSelf", bound="ConcentricPartGroup._Cast_ConcentricPartGroup"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConcentricPartGroup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConcentricPartGroup:
    """Special nested class for casting ConcentricPartGroup to subclasses."""

    __parent__: "ConcentricPartGroup"

    @property
    def concentric_or_parallel_part_group(
        self: "CastSelf",
    ) -> "_2721.ConcentricOrParallelPartGroup":
        return self.__parent__._cast(_2721.ConcentricOrParallelPartGroup)

    @property
    def part_group(self: "CastSelf") -> "_2727.PartGroup":
        from mastapy._private.system_model.part_model.part_groups import _2727

        return self.__parent__._cast(_2727.PartGroup)

    @property
    def concentric_part_group(self: "CastSelf") -> "ConcentricPartGroup":
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
class ConcentricPartGroup(_2721.ConcentricOrParallelPartGroup):
    """ConcentricPartGroup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONCENTRIC_PART_GROUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def total_of_cylindrical_gear_face_widths(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalOfCylindricalGearFaceWidths")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def radial_position(self: "Self") -> "Vector2D":
        """Vector2D"""
        temp = pythonnet_property_get(self.wrapped, "RadialPosition")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector2d(temp)

        if value is None:
            return None

        return value

    @radial_position.setter
    @exception_bridge
    @enforce_parameter_types
    def radial_position(self: "Self", value: "Vector2D") -> None:
        value = conversion.mp_to_pn_vector2d(value)
        pythonnet_property_set(self.wrapped, "RadialPosition", value)

    @property
    @exception_bridge
    def parallel_groups(
        self: "Self",
    ) -> "List[_2723.ConcentricPartGroupParallelToThis]":
        """List[mastapy.system_model.part_model.part_groups.ConcentricPartGroupParallelToThis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ParallelGroups")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ConcentricPartGroup":
        """Cast to another type.

        Returns:
            _Cast_ConcentricPartGroup
        """
        return _Cast_ConcentricPartGroup(self)
