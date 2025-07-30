"""ConicalMeshMisalignments"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
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

_CONICAL_MESH_MISALIGNMENTS = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Conical", "ConicalMeshMisalignments"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ConicalMeshMisalignments")
    CastSelf = TypeVar(
        "CastSelf", bound="ConicalMeshMisalignments._Cast_ConicalMeshMisalignments"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalMeshMisalignments",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalMeshMisalignments:
    """Special nested class for casting ConicalMeshMisalignments to subclasses."""

    __parent__: "ConicalMeshMisalignments"

    @property
    def conical_mesh_misalignments(self: "CastSelf") -> "ConicalMeshMisalignments":
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
class ConicalMeshMisalignments(_0.APIBase):
    """ConicalMeshMisalignments

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_MESH_MISALIGNMENTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def delta_e(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DeltaE")

        if temp is None:
            return 0.0

        return temp

    @delta_e.setter
    @exception_bridge
    @enforce_parameter_types
    def delta_e(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DeltaE", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def delta_sigma(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DeltaSigma")

        if temp is None:
            return 0.0

        return temp

    @delta_sigma.setter
    @exception_bridge
    @enforce_parameter_types
    def delta_sigma(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DeltaSigma", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def delta_xp(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DeltaXP")

        if temp is None:
            return 0.0

        return temp

    @delta_xp.setter
    @exception_bridge
    @enforce_parameter_types
    def delta_xp(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DeltaXP", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def delta_xw(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DeltaXW")

        if temp is None:
            return 0.0

        return temp

    @delta_xw.setter
    @exception_bridge
    @enforce_parameter_types
    def delta_xw(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DeltaXW", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalMeshMisalignments":
        """Cast to another type.

        Returns:
            _Cast_ConicalMeshMisalignments
        """
        return _Cast_ConicalMeshMisalignments(self)
