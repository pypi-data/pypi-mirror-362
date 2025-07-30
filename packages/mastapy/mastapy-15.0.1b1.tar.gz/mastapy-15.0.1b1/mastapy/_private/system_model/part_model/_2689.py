"""MassDisc"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model import _2711

_MASS_DISC = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "MassDisc")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.part_model import _2670, _2693, _2698

    Self = TypeVar("Self", bound="MassDisc")
    CastSelf = TypeVar("CastSelf", bound="MassDisc._Cast_MassDisc")


__docformat__ = "restructuredtext en"
__all__ = ("MassDisc",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MassDisc:
    """Special nested class for casting MassDisc to subclasses."""

    __parent__: "MassDisc"

    @property
    def virtual_component(self: "CastSelf") -> "_2711.VirtualComponent":
        return self.__parent__._cast(_2711.VirtualComponent)

    @property
    def mountable_component(self: "CastSelf") -> "_2693.MountableComponent":
        from mastapy._private.system_model.part_model import _2693

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
    def mass_disc(self: "CastSelf") -> "MassDisc":
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
class MassDisc(_2711.VirtualComponent):
    """MassDisc

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MASS_DISC

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def density(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Density")

        if temp is None:
            return 0.0

        return temp

    @density.setter
    @exception_bridge
    @enforce_parameter_types
    def density(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Density", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def disc_rotation(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DiscRotation")

        if temp is None:
            return 0.0

        return temp

    @disc_rotation.setter
    @exception_bridge
    @enforce_parameter_types
    def disc_rotation(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DiscRotation", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def disc_skew(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DiscSkew")

        if temp is None:
            return 0.0

        return temp

    @disc_skew.setter
    @exception_bridge
    @enforce_parameter_types
    def disc_skew(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DiscSkew", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def inner_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def is_distributed(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsDistributed")

        if temp is None:
            return False

        return temp

    @is_distributed.setter
    @exception_bridge
    @enforce_parameter_types
    def is_distributed(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "IsDistributed", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def outer_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterDiameter")

        if temp is None:
            return 0.0

        return temp

    @outer_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "OuterDiameter", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Width")

        if temp is None:
            return 0.0

        return temp

    @width.setter
    @exception_bridge
    @enforce_parameter_types
    def width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Width", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_MassDisc":
        """Cast to another type.

        Returns:
            _Cast_MassDisc
        """
        return _Cast_MassDisc(self)
