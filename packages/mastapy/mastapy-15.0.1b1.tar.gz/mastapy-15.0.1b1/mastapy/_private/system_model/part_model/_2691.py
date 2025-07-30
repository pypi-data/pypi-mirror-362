"""Microphone"""

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
from mastapy._private._math.vector_3d import Vector3D
from mastapy._private.system_model.part_model import _2670

_MICROPHONE = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Microphone")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.part_model import _2698

    Self = TypeVar("Self", bound="Microphone")
    CastSelf = TypeVar("CastSelf", bound="Microphone._Cast_Microphone")


__docformat__ = "restructuredtext en"
__all__ = ("Microphone",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Microphone:
    """Special nested class for casting Microphone to subclasses."""

    __parent__: "Microphone"

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
    def microphone(self: "CastSelf") -> "Microphone":
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
class Microphone(_2670.Component):
    """Microphone

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MICROPHONE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def drawing_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DrawingDiameter")

        if temp is None:
            return 0.0

        return temp

    @drawing_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def drawing_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DrawingDiameter", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def position_in_datum_coordinate_system(self: "Self") -> "Vector3D":
        """Vector3D"""
        temp = pythonnet_property_get(self.wrapped, "PositionInDatumCoordinateSystem")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @position_in_datum_coordinate_system.setter
    @exception_bridge
    @enforce_parameter_types
    def position_in_datum_coordinate_system(self: "Self", value: "Vector3D") -> None:
        value = conversion.mp_to_pn_vector3d(value)
        pythonnet_property_set(self.wrapped, "PositionInDatumCoordinateSystem", value)

    @property
    def cast_to(self: "Self") -> "_Cast_Microphone":
        """Cast to another type.

        Returns:
            _Cast_Microphone
        """
        return _Cast_Microphone(self)
