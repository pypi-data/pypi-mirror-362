"""DetailedBoltedJointDesign"""

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

_DETAILED_BOLTED_JOINT_DESIGN = python_net_import(
    "SMT.MastaAPI.Bolts", "DetailedBoltedJointDesign"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.bolts import _1667

    Self = TypeVar("Self", bound="DetailedBoltedJointDesign")
    CastSelf = TypeVar(
        "CastSelf", bound="DetailedBoltedJointDesign._Cast_DetailedBoltedJointDesign"
    )


__docformat__ = "restructuredtext en"
__all__ = ("DetailedBoltedJointDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DetailedBoltedJointDesign:
    """Special nested class for casting DetailedBoltedJointDesign to subclasses."""

    __parent__: "DetailedBoltedJointDesign"

    @property
    def detailed_bolted_joint_design(self: "CastSelf") -> "DetailedBoltedJointDesign":
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
class DetailedBoltedJointDesign(_0.APIBase):
    """DetailedBoltedJointDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DETAILED_BOLTED_JOINT_DESIGN

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
    def number_of_bolts(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfBolts")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def loaded_bolts(self: "Self") -> "List[_1667.LoadedBolt]":
        """List[mastapy.bolts.LoadedBolt]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadedBolts")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_DetailedBoltedJointDesign":
        """Cast to another type.

        Returns:
            _Cast_DetailedBoltedJointDesign
        """
        return _Cast_DetailedBoltedJointDesign(self)
