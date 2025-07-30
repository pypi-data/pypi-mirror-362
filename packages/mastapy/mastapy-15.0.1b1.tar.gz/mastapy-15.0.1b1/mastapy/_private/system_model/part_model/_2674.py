"""Datum"""

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
from mastapy._private.system_model.part_model import _2670

_DATUM = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Datum")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.part_model import _2698

    Self = TypeVar("Self", bound="Datum")
    CastSelf = TypeVar("CastSelf", bound="Datum._Cast_Datum")


__docformat__ = "restructuredtext en"
__all__ = ("Datum",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Datum:
    """Special nested class for casting Datum to subclasses."""

    __parent__: "Datum"

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
    def datum(self: "CastSelf") -> "Datum":
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
class Datum(_2670.Component):
    """Datum

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DATUM

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
    def offset(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Offset")

        if temp is None:
            return 0.0

        return temp

    @offset.setter
    @exception_bridge
    @enforce_parameter_types
    def offset(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Offset", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_Datum":
        """Cast to another type.

        Returns:
            _Cast_Datum
        """
        return _Cast_Datum(self)
