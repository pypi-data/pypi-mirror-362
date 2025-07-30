"""LoadedAxialThrustNeedleRollerBearingElement"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_results.rolling import _2201

_LOADED_AXIAL_THRUST_NEEDLE_ROLLER_BEARING_ELEMENT = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling",
    "LoadedAxialThrustNeedleRollerBearingElement",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling import _2222, _2235, _2236

    Self = TypeVar("Self", bound="LoadedAxialThrustNeedleRollerBearingElement")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedAxialThrustNeedleRollerBearingElement._Cast_LoadedAxialThrustNeedleRollerBearingElement",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedAxialThrustNeedleRollerBearingElement",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedAxialThrustNeedleRollerBearingElement:
    """Special nested class for casting LoadedAxialThrustNeedleRollerBearingElement to subclasses."""

    __parent__: "LoadedAxialThrustNeedleRollerBearingElement"

    @property
    def loaded_axial_thrust_cylindrical_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2201.LoadedAxialThrustCylindricalRollerBearingElement":
        return self.__parent__._cast(
            _2201.LoadedAxialThrustCylindricalRollerBearingElement
        )

    @property
    def loaded_non_barrel_roller_element(
        self: "CastSelf",
    ) -> "_2235.LoadedNonBarrelRollerElement":
        from mastapy._private.bearings.bearing_results.rolling import _2235

        return self.__parent__._cast(_2235.LoadedNonBarrelRollerElement)

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
    def loaded_axial_thrust_needle_roller_bearing_element(
        self: "CastSelf",
    ) -> "LoadedAxialThrustNeedleRollerBearingElement":
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
class LoadedAxialThrustNeedleRollerBearingElement(
    _2201.LoadedAxialThrustCylindricalRollerBearingElement
):
    """LoadedAxialThrustNeedleRollerBearingElement

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_AXIAL_THRUST_NEEDLE_ROLLER_BEARING_ELEMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedAxialThrustNeedleRollerBearingElement":
        """Cast to another type.

        Returns:
            _Cast_LoadedAxialThrustNeedleRollerBearingElement
        """
        return _Cast_LoadedAxialThrustNeedleRollerBearingElement(self)
