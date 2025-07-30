"""LoadedNonBarrelRollerElement"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.bearings.bearing_results.rolling import _2236

_LOADED_NON_BARREL_ROLLER_ELEMENT = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "LoadedNonBarrelRollerElement"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling import (
        _2201,
        _2204,
        _2216,
        _2222,
        _2228,
        _2255,
    )

    Self = TypeVar("Self", bound="LoadedNonBarrelRollerElement")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedNonBarrelRollerElement._Cast_LoadedNonBarrelRollerElement",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedNonBarrelRollerElement",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedNonBarrelRollerElement:
    """Special nested class for casting LoadedNonBarrelRollerElement to subclasses."""

    __parent__: "LoadedNonBarrelRollerElement"

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
    def loaded_axial_thrust_cylindrical_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2201.LoadedAxialThrustCylindricalRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2201

        return self.__parent__._cast(
            _2201.LoadedAxialThrustCylindricalRollerBearingElement
        )

    @property
    def loaded_axial_thrust_needle_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2204.LoadedAxialThrustNeedleRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2204

        return self.__parent__._cast(_2204.LoadedAxialThrustNeedleRollerBearingElement)

    @property
    def loaded_cylindrical_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2216.LoadedCylindricalRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2216

        return self.__parent__._cast(_2216.LoadedCylindricalRollerBearingElement)

    @property
    def loaded_needle_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2228.LoadedNeedleRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2228

        return self.__parent__._cast(_2228.LoadedNeedleRollerBearingElement)

    @property
    def loaded_taper_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2255.LoadedTaperRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2255

        return self.__parent__._cast(_2255.LoadedTaperRollerBearingElement)

    @property
    def loaded_non_barrel_roller_element(
        self: "CastSelf",
    ) -> "LoadedNonBarrelRollerElement":
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
class LoadedNonBarrelRollerElement(_2236.LoadedRollerBearingElement):
    """LoadedNonBarrelRollerElement

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_NON_BARREL_ROLLER_ELEMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def minimum_smt_rib_stress_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumSMTRibStressSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedNonBarrelRollerElement":
        """Cast to another type.

        Returns:
            _Cast_LoadedNonBarrelRollerElement
        """
        return _Cast_LoadedNonBarrelRollerElement(self)
