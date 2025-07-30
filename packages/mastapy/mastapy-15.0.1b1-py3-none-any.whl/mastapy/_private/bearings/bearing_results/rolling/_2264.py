"""LoadedToroidalRollerBearingElement"""

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
from mastapy._private.bearings.bearing_results.rolling import _2236

_LOADED_TOROIDAL_ROLLER_BEARING_ELEMENT = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "LoadedToroidalRollerBearingElement"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling import _2222

    Self = TypeVar("Self", bound="LoadedToroidalRollerBearingElement")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedToroidalRollerBearingElement._Cast_LoadedToroidalRollerBearingElement",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedToroidalRollerBearingElement",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedToroidalRollerBearingElement:
    """Special nested class for casting LoadedToroidalRollerBearingElement to subclasses."""

    __parent__: "LoadedToroidalRollerBearingElement"

    @property
    def loaded_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2236.LoadedRollerBearingElement":
        return self.__parent__._cast(_2236.LoadedRollerBearingElement)

    @property
    def loaded_element(self: "CastSelf") -> "_2222.LoadedElement":
        from mastapy._private.bearings.bearing_results.rolling import _2222

        return self.__parent__._cast(_2222.LoadedElement)

    @property
    def loaded_toroidal_roller_bearing_element(
        self: "CastSelf",
    ) -> "LoadedToroidalRollerBearingElement":
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
class LoadedToroidalRollerBearingElement(_2236.LoadedRollerBearingElement):
    """LoadedToroidalRollerBearingElement

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_TOROIDAL_ROLLER_BEARING_ELEMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def contact_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ContactAngle")

        if temp is None:
            return 0.0

        return temp

    @contact_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def contact_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ContactAngle", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedToroidalRollerBearingElement":
        """Cast to another type.

        Returns:
            _Cast_LoadedToroidalRollerBearingElement
        """
        return _Cast_LoadedToroidalRollerBearingElement(self)
