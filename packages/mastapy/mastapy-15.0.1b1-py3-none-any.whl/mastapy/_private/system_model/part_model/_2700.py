"""PlanetCarrier"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model import _2693

_PLANET_CARRIER = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "PlanetCarrier"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.connections_and_sockets import _2509
    from mastapy._private.system_model.part_model import _2670, _2688, _2698
    from mastapy._private.system_model.part_model.shaft_model import _2714

    Self = TypeVar("Self", bound="PlanetCarrier")
    CastSelf = TypeVar("CastSelf", bound="PlanetCarrier._Cast_PlanetCarrier")


__docformat__ = "restructuredtext en"
__all__ = ("PlanetCarrier",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlanetCarrier:
    """Special nested class for casting PlanetCarrier to subclasses."""

    __parent__: "PlanetCarrier"

    @property
    def mountable_component(self: "CastSelf") -> "_2693.MountableComponent":
        return self.__parent__._cast(_2693.MountableComponent)

    @property
    def component(self: "CastSelf") -> "_2670.Component":
        from mastapy._private.system_model.part_model import _2670

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
    def planet_carrier(self: "CastSelf") -> "PlanetCarrier":
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
class PlanetCarrier(_2693.MountableComponent):
    """PlanetCarrier

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLANET_CARRIER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Length")

        if temp is None:
            return 0.0

        return temp

    @length.setter
    @exception_bridge
    @enforce_parameter_types
    def length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Length", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def number_of_planetary_sockets(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfPlanetarySockets")

        if temp is None:
            return 0

        return temp

    @number_of_planetary_sockets.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_planetary_sockets(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfPlanetarySockets",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def load_sharing_settings(self: "Self") -> "_2688.LoadSharingSettings":
        """mastapy.system_model.part_model.LoadSharingSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadSharingSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def planetary_sockets(self: "Self") -> "List[_2509.PlanetarySocket]":
        """List[mastapy.system_model.connections_and_sockets.PlanetarySocket]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PlanetarySockets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    @enforce_parameter_types
    def attach_carrier_shaft(
        self: "Self", shaft: "_2714.Shaft", offset: "float" = float("nan")
    ) -> None:
        """Method does not return.

        Args:
            shaft (mastapy.system_model.part_model.shaft_model.Shaft)
            offset (float, optional)
        """
        offset = float(offset)
        pythonnet_method_call(
            self.wrapped,
            "AttachCarrierShaft",
            shaft.wrapped if shaft else None,
            offset if offset else 0.0,
        )

    @exception_bridge
    @enforce_parameter_types
    def attach_pin_shaft(
        self: "Self", shaft: "_2714.Shaft", offset: "float" = float("nan")
    ) -> None:
        """Method does not return.

        Args:
            shaft (mastapy.system_model.part_model.shaft_model.Shaft)
            offset (float, optional)
        """
        offset = float(offset)
        pythonnet_method_call(
            self.wrapped,
            "AttachPinShaft",
            shaft.wrapped if shaft else None,
            offset if offset else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_PlanetCarrier":
        """Cast to another type.

        Returns:
            _Cast_PlanetCarrier
        """
        return _Cast_PlanetCarrier(self)
