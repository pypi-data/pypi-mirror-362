"""LoadedToroidalRollerBearingRow"""

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
from mastapy._private.bearings.bearing_results.rolling import _2238

_LOADED_TOROIDAL_ROLLER_BEARING_ROW = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "LoadedToroidalRollerBearingRow"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling import _2242, _2265

    Self = TypeVar("Self", bound="LoadedToroidalRollerBearingRow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedToroidalRollerBearingRow._Cast_LoadedToroidalRollerBearingRow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedToroidalRollerBearingRow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedToroidalRollerBearingRow:
    """Special nested class for casting LoadedToroidalRollerBearingRow to subclasses."""

    __parent__: "LoadedToroidalRollerBearingRow"

    @property
    def loaded_roller_bearing_row(self: "CastSelf") -> "_2238.LoadedRollerBearingRow":
        return self.__parent__._cast(_2238.LoadedRollerBearingRow)

    @property
    def loaded_rolling_bearing_row(self: "CastSelf") -> "_2242.LoadedRollingBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2242

        return self.__parent__._cast(_2242.LoadedRollingBearingRow)

    @property
    def loaded_toroidal_roller_bearing_row(
        self: "CastSelf",
    ) -> "LoadedToroidalRollerBearingRow":
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
class LoadedToroidalRollerBearingRow(_2238.LoadedRollerBearingRow):
    """LoadedToroidalRollerBearingRow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_TOROIDAL_ROLLER_BEARING_ROW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def loaded_bearing(self: "Self") -> "_2265.LoadedToroidalRollerBearingResults":
        """mastapy.bearings.bearing_results.rolling.LoadedToroidalRollerBearingResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadedBearing")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedToroidalRollerBearingRow":
        """Cast to another type.

        Returns:
            _Cast_LoadedToroidalRollerBearingRow
        """
        return _Cast_LoadedToroidalRollerBearingRow(self)
