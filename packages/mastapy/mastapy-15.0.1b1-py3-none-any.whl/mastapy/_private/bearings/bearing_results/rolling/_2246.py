"""LoadedSphericalRadialRollerBearingElement"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_results.rolling import _2247

_LOADED_SPHERICAL_RADIAL_ROLLER_BEARING_ELEMENT = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling",
    "LoadedSphericalRadialRollerBearingElement",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling import _2222, _2236

    Self = TypeVar("Self", bound="LoadedSphericalRadialRollerBearingElement")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedSphericalRadialRollerBearingElement._Cast_LoadedSphericalRadialRollerBearingElement",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedSphericalRadialRollerBearingElement",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedSphericalRadialRollerBearingElement:
    """Special nested class for casting LoadedSphericalRadialRollerBearingElement to subclasses."""

    __parent__: "LoadedSphericalRadialRollerBearingElement"

    @property
    def loaded_spherical_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2247.LoadedSphericalRollerBearingElement":
        return self.__parent__._cast(_2247.LoadedSphericalRollerBearingElement)

    @property
    def loaded_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2236.LoadedRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2236

        return self.__parent__._cast(_2236.LoadedRollerBearingElement)

    @property
    def loaded_element(self: "CastSelf") -> "_2222.LoadedElement":
        from mastapy._private.bearings.bearing_results.rolling import _2222

        return self.__parent__._cast(_2222.LoadedElement)

    @property
    def loaded_spherical_radial_roller_bearing_element(
        self: "CastSelf",
    ) -> "LoadedSphericalRadialRollerBearingElement":
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
class LoadedSphericalRadialRollerBearingElement(
    _2247.LoadedSphericalRollerBearingElement
):
    """LoadedSphericalRadialRollerBearingElement

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_SPHERICAL_RADIAL_ROLLER_BEARING_ELEMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedSphericalRadialRollerBearingElement":
        """Cast to another type.

        Returns:
            _Cast_LoadedSphericalRadialRollerBearingElement
        """
        return _Cast_LoadedSphericalRadialRollerBearingElement(self)
