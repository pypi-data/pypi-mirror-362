"""GearContactStiffnessNode"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.ltca import _951

_GEAR_CONTACT_STIFFNESS_NODE = python_net_import(
    "SMT.MastaAPI.Gears.LTCA", "GearContactStiffnessNode"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.ltca.conical import _969
    from mastapy._private.gears.ltca.cylindrical import _957
    from mastapy._private.nodal_analysis import _70

    Self = TypeVar("Self", bound="GearContactStiffnessNode")
    CastSelf = TypeVar(
        "CastSelf", bound="GearContactStiffnessNode._Cast_GearContactStiffnessNode"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearContactStiffnessNode",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearContactStiffnessNode:
    """Special nested class for casting GearContactStiffnessNode to subclasses."""

    __parent__: "GearContactStiffnessNode"

    @property
    def gear_stiffness_node(self: "CastSelf") -> "_951.GearStiffnessNode":
        return self.__parent__._cast(_951.GearStiffnessNode)

    @property
    def fe_stiffness_node(self: "CastSelf") -> "_70.FEStiffnessNode":
        from mastapy._private.nodal_analysis import _70

        return self.__parent__._cast(_70.FEStiffnessNode)

    @property
    def cylindrical_gear_contact_stiffness_node(
        self: "CastSelf",
    ) -> "_957.CylindricalGearContactStiffnessNode":
        from mastapy._private.gears.ltca.cylindrical import _957

        return self.__parent__._cast(_957.CylindricalGearContactStiffnessNode)

    @property
    def conical_gear_contact_stiffness_node(
        self: "CastSelf",
    ) -> "_969.ConicalGearContactStiffnessNode":
        from mastapy._private.gears.ltca.conical import _969

        return self.__parent__._cast(_969.ConicalGearContactStiffnessNode)

    @property
    def gear_contact_stiffness_node(self: "CastSelf") -> "GearContactStiffnessNode":
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
class GearContactStiffnessNode(_951.GearStiffnessNode):
    """GearContactStiffnessNode

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_CONTACT_STIFFNESS_NODE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_GearContactStiffnessNode":
        """Cast to another type.

        Returns:
            _Cast_GearContactStiffnessNode
        """
        return _Cast_GearContactStiffnessNode(self)
