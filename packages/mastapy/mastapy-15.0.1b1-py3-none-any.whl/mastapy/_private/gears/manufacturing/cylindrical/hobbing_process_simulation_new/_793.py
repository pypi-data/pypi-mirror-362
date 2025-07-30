"""RackMountingError"""

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
from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
    _782,
)

_RACK_MOUNTING_ERROR = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew",
    "RackMountingError",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RackMountingError")
    CastSelf = TypeVar("CastSelf", bound="RackMountingError._Cast_RackMountingError")


__docformat__ = "restructuredtext en"
__all__ = ("RackMountingError",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RackMountingError:
    """Special nested class for casting RackMountingError to subclasses."""

    __parent__: "RackMountingError"

    @property
    def mounting_error(self: "CastSelf") -> "_782.MountingError":
        return self.__parent__._cast(_782.MountingError)

    @property
    def rack_mounting_error(self: "CastSelf") -> "RackMountingError":
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
class RackMountingError(_782.MountingError):
    """RackMountingError

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RACK_MOUNTING_ERROR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def axial_runout(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AxialRunout")

        if temp is None:
            return 0.0

        return temp

    @axial_runout.setter
    @exception_bridge
    @enforce_parameter_types
    def axial_runout(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "AxialRunout", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def axial_runout_phase_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AxialRunoutPhaseAngle")

        if temp is None:
            return 0.0

        return temp

    @axial_runout_phase_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def axial_runout_phase_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AxialRunoutPhaseAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_RackMountingError":
        """Cast to another type.

        Returns:
            _Cast_RackMountingError
        """
        return _Cast_RackMountingError(self)
