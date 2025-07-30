"""AcousticSurfaceWithSelection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
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

_ACOUSTIC_SURFACE_WITH_SELECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AcousticAnalyses",
    "AcousticSurfaceWithSelection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="AcousticSurfaceWithSelection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AcousticSurfaceWithSelection._Cast_AcousticSurfaceWithSelection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AcousticSurfaceWithSelection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AcousticSurfaceWithSelection:
    """Special nested class for casting AcousticSurfaceWithSelection to subclasses."""

    __parent__: "AcousticSurfaceWithSelection"

    @property
    def acoustic_surface_with_selection(
        self: "CastSelf",
    ) -> "AcousticSurfaceWithSelection":
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
class AcousticSurfaceWithSelection(_0.APIBase):
    """AcousticSurfaceWithSelection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ACOUSTIC_SURFACE_WITH_SELECTION

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
    def selected(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "Selected")

        if temp is None:
            return False

        return temp

    @selected.setter
    @exception_bridge
    @enforce_parameter_types
    def selected(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "Selected", bool(value) if value is not None else False
        )

    @exception_bridge
    def sound_intensity(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SoundIntensity")

    @exception_bridge
    def sound_pressure(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SoundPressure")

    @exception_bridge
    def sound_velocity(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SoundVelocity")

    @property
    def cast_to(self: "Self") -> "_Cast_AcousticSurfaceWithSelection":
        """Cast to another type.

        Returns:
            _Cast_AcousticSurfaceWithSelection
        """
        return _Cast_AcousticSurfaceWithSelection(self)
