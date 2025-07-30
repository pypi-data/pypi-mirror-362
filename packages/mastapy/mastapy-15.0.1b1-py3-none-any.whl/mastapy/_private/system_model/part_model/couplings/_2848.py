"""Synchroniser"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model import _2708

_SYNCHRONISER = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "Synchroniser"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.connections_and_sockets.couplings import _2563
    from mastapy._private.system_model.part_model import _2659, _2698
    from mastapy._private.system_model.part_model.couplings import _2850, _2852

    Self = TypeVar("Self", bound="Synchroniser")
    CastSelf = TypeVar("CastSelf", bound="Synchroniser._Cast_Synchroniser")


__docformat__ = "restructuredtext en"
__all__ = ("Synchroniser",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Synchroniser:
    """Special nested class for casting Synchroniser to subclasses."""

    __parent__: "Synchroniser"

    @property
    def specialised_assembly(self: "CastSelf") -> "_2708.SpecialisedAssembly":
        return self.__parent__._cast(_2708.SpecialisedAssembly)

    @property
    def abstract_assembly(self: "CastSelf") -> "_2659.AbstractAssembly":
        from mastapy._private.system_model.part_model import _2659

        return self.__parent__._cast(_2659.AbstractAssembly)

    @property
    def part(self: "CastSelf") -> "_2698.Part":
        from mastapy._private.system_model.part_model import _2698

        return self.__parent__._cast(_2698.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2414.DesignEntity":
        from mastapy._private.system_model import _2414

        return self.__parent__._cast(_2414.DesignEntity)

    @property
    def synchroniser(self: "CastSelf") -> "Synchroniser":
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
class Synchroniser(_2708.SpecialisedAssembly):
    """Synchroniser

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SYNCHRONISER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def has_left_cone(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "HasLeftCone")

        if temp is None:
            return False

        return temp

    @has_left_cone.setter
    @exception_bridge
    @enforce_parameter_types
    def has_left_cone(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "HasLeftCone", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def has_right_cone(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "HasRightCone")

        if temp is None:
            return False

        return temp

    @has_right_cone.setter
    @exception_bridge
    @enforce_parameter_types
    def has_right_cone(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "HasRightCone", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def clutch_connection_left(self: "Self") -> "_2563.ClutchConnection":
        """mastapy.system_model.connections_and_sockets.couplings.ClutchConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ClutchConnectionLeft")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def clutch_connection_right(self: "Self") -> "_2563.ClutchConnection":
        """mastapy.system_model.connections_and_sockets.couplings.ClutchConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ClutchConnectionRight")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def hub_and_sleeve(self: "Self") -> "_2852.SynchroniserSleeve":
        """mastapy.system_model.part_model.couplings.SynchroniserSleeve

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HubAndSleeve")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def left_cone(self: "Self") -> "_2850.SynchroniserHalf":
        """mastapy.system_model.part_model.couplings.SynchroniserHalf

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeftCone")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def right_cone(self: "Self") -> "_2850.SynchroniserHalf":
        """mastapy.system_model.part_model.couplings.SynchroniserHalf

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RightCone")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_Synchroniser":
        """Cast to another type.

        Returns:
            _Cast_Synchroniser
        """
        return _Cast_Synchroniser(self)
