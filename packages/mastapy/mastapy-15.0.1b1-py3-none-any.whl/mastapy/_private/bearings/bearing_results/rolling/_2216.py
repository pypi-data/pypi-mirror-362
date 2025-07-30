"""LoadedCylindricalRollerBearingElement"""

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
from mastapy._private.bearings.bearing_results.rolling import _2235

_LOADED_CYLINDRICAL_ROLLER_BEARING_ELEMENT = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling",
    "LoadedCylindricalRollerBearingElement",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling import _2222, _2228, _2236

    Self = TypeVar("Self", bound="LoadedCylindricalRollerBearingElement")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedCylindricalRollerBearingElement._Cast_LoadedCylindricalRollerBearingElement",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedCylindricalRollerBearingElement",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedCylindricalRollerBearingElement:
    """Special nested class for casting LoadedCylindricalRollerBearingElement to subclasses."""

    __parent__: "LoadedCylindricalRollerBearingElement"

    @property
    def loaded_non_barrel_roller_element(
        self: "CastSelf",
    ) -> "_2235.LoadedNonBarrelRollerElement":
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
    def loaded_needle_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2228.LoadedNeedleRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2228

        return self.__parent__._cast(_2228.LoadedNeedleRollerBearingElement)

    @property
    def loaded_cylindrical_roller_bearing_element(
        self: "CastSelf",
    ) -> "LoadedCylindricalRollerBearingElement":
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
class LoadedCylindricalRollerBearingElement(_2235.LoadedNonBarrelRollerElement):
    """LoadedCylindricalRollerBearingElement

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_CYLINDRICAL_ROLLER_BEARING_ELEMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def height_of_rib_roller_contact_above_race_inner_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HeightOfRibRollerContactAboveRaceInnerLeft"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def height_of_rib_roller_contact_above_race_inner_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HeightOfRibRollerContactAboveRaceInnerRight"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def height_of_rib_roller_contact_above_race_outer_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HeightOfRibRollerContactAboveRaceOuterLeft"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def height_of_rib_roller_contact_above_race_outer_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HeightOfRibRollerContactAboveRaceOuterRight"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_rib_stress_inner_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumRibStressInnerLeft")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_rib_stress_inner_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumRibStressInnerRight")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_rib_stress_outer_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumRibStressOuterLeft")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_rib_stress_outer_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumRibStressOuterRight")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedCylindricalRollerBearingElement":
        """Cast to another type.

        Returns:
            _Cast_LoadedCylindricalRollerBearingElement
        """
        return _Cast_LoadedCylindricalRollerBearingElement(self)
