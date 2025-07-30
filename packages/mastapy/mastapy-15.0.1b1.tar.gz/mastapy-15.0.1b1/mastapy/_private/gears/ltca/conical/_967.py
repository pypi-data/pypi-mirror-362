"""ConicalGearBendingStiffnessNode"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.ltca import _937

_CONICAL_GEAR_BENDING_STIFFNESS_NODE = python_net_import(
    "SMT.MastaAPI.Gears.LTCA.Conical", "ConicalGearBendingStiffnessNode"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.ltca import _951
    from mastapy._private.nodal_analysis import _70

    Self = TypeVar("Self", bound="ConicalGearBendingStiffnessNode")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearBendingStiffnessNode._Cast_ConicalGearBendingStiffnessNode",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearBendingStiffnessNode",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearBendingStiffnessNode:
    """Special nested class for casting ConicalGearBendingStiffnessNode to subclasses."""

    __parent__: "ConicalGearBendingStiffnessNode"

    @property
    def gear_bending_stiffness_node(
        self: "CastSelf",
    ) -> "_937.GearBendingStiffnessNode":
        return self.__parent__._cast(_937.GearBendingStiffnessNode)

    @property
    def gear_stiffness_node(self: "CastSelf") -> "_951.GearStiffnessNode":
        from mastapy._private.gears.ltca import _951

        return self.__parent__._cast(_951.GearStiffnessNode)

    @property
    def fe_stiffness_node(self: "CastSelf") -> "_70.FEStiffnessNode":
        from mastapy._private.nodal_analysis import _70

        return self.__parent__._cast(_70.FEStiffnessNode)

    @property
    def conical_gear_bending_stiffness_node(
        self: "CastSelf",
    ) -> "ConicalGearBendingStiffnessNode":
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
class ConicalGearBendingStiffnessNode(_937.GearBendingStiffnessNode):
    """ConicalGearBendingStiffnessNode

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_BENDING_STIFFNESS_NODE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearBendingStiffnessNode":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearBendingStiffnessNode
        """
        return _Cast_ConicalGearBendingStiffnessNode(self)
