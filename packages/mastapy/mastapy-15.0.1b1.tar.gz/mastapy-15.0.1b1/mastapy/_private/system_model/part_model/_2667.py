"""Bolt"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.part_model import _2670

_BOLT = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Bolt")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bolts import _1667
    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.part_model import _2668, _2698

    Self = TypeVar("Self", bound="Bolt")
    CastSelf = TypeVar("CastSelf", bound="Bolt._Cast_Bolt")


__docformat__ = "restructuredtext en"
__all__ = ("Bolt",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Bolt:
    """Special nested class for casting Bolt to subclasses."""

    __parent__: "Bolt"

    @property
    def component(self: "CastSelf") -> "_2670.Component":
        return self.__parent__._cast(_2670.Component)

    @property
    def part(self: "CastSelf") -> "_2698.Part":
        from mastapy._private.system_model.part_model import _2698

        return self.__parent__._cast(_2698.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2414.DesignEntity":
        from mastapy._private.system_model import _2414

        return self.__parent__._cast(_2414.DesignEntity)

    @property
    def bolt(self: "CastSelf") -> "Bolt":
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
class Bolt(_2670.Component):
    """Bolt

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BOLT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def bolted_joint(self: "Self") -> "_2668.BoltedJoint":
        """mastapy.system_model.part_model.BoltedJoint

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BoltedJoint")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def loaded_bolt(self: "Self") -> "_1667.LoadedBolt":
        """mastapy.bolts.LoadedBolt

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadedBolt")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_Bolt":
        """Cast to another type.

        Returns:
            _Cast_Bolt
        """
        return _Cast_Bolt(self)
