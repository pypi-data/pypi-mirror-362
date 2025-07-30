"""LoadedAxialThrustNeedleRollerBearingRow"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.bearings.bearing_results.rolling import _2203

_LOADED_AXIAL_THRUST_NEEDLE_ROLLER_BEARING_ROW = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling",
    "LoadedAxialThrustNeedleRollerBearingRow",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling import (
        _2205,
        _2233,
        _2238,
        _2242,
    )

    Self = TypeVar("Self", bound="LoadedAxialThrustNeedleRollerBearingRow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedAxialThrustNeedleRollerBearingRow._Cast_LoadedAxialThrustNeedleRollerBearingRow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedAxialThrustNeedleRollerBearingRow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedAxialThrustNeedleRollerBearingRow:
    """Special nested class for casting LoadedAxialThrustNeedleRollerBearingRow to subclasses."""

    __parent__: "LoadedAxialThrustNeedleRollerBearingRow"

    @property
    def loaded_axial_thrust_cylindrical_roller_bearing_row(
        self: "CastSelf",
    ) -> "_2203.LoadedAxialThrustCylindricalRollerBearingRow":
        return self.__parent__._cast(_2203.LoadedAxialThrustCylindricalRollerBearingRow)

    @property
    def loaded_non_barrel_roller_bearing_row(
        self: "CastSelf",
    ) -> "_2233.LoadedNonBarrelRollerBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2233

        return self.__parent__._cast(_2233.LoadedNonBarrelRollerBearingRow)

    @property
    def loaded_roller_bearing_row(self: "CastSelf") -> "_2238.LoadedRollerBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2238

        return self.__parent__._cast(_2238.LoadedRollerBearingRow)

    @property
    def loaded_rolling_bearing_row(self: "CastSelf") -> "_2242.LoadedRollingBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2242

        return self.__parent__._cast(_2242.LoadedRollingBearingRow)

    @property
    def loaded_axial_thrust_needle_roller_bearing_row(
        self: "CastSelf",
    ) -> "LoadedAxialThrustNeedleRollerBearingRow":
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
class LoadedAxialThrustNeedleRollerBearingRow(
    _2203.LoadedAxialThrustCylindricalRollerBearingRow
):
    """LoadedAxialThrustNeedleRollerBearingRow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_AXIAL_THRUST_NEEDLE_ROLLER_BEARING_ROW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def loaded_bearing(
        self: "Self",
    ) -> "_2205.LoadedAxialThrustNeedleRollerBearingResults":
        """mastapy.bearings.bearing_results.rolling.LoadedAxialThrustNeedleRollerBearingResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadedBearing")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedAxialThrustNeedleRollerBearingRow":
        """Cast to another type.

        Returns:
            _Cast_LoadedAxialThrustNeedleRollerBearingRow
        """
        return _Cast_LoadedAxialThrustNeedleRollerBearingRow(self)
