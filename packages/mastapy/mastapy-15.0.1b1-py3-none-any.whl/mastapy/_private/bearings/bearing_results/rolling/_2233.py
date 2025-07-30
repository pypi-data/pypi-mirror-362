"""LoadedNonBarrelRollerBearingRow"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.bearings.bearing_results.rolling import _2238

_LOADED_NON_BARREL_ROLLER_BEARING_ROW = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "LoadedNonBarrelRollerBearingRow"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling import (
        _2203,
        _2206,
        _2218,
        _2230,
        _2232,
        _2242,
        _2257,
    )

    Self = TypeVar("Self", bound="LoadedNonBarrelRollerBearingRow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedNonBarrelRollerBearingRow._Cast_LoadedNonBarrelRollerBearingRow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedNonBarrelRollerBearingRow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedNonBarrelRollerBearingRow:
    """Special nested class for casting LoadedNonBarrelRollerBearingRow to subclasses."""

    __parent__: "LoadedNonBarrelRollerBearingRow"

    @property
    def loaded_roller_bearing_row(self: "CastSelf") -> "_2238.LoadedRollerBearingRow":
        return self.__parent__._cast(_2238.LoadedRollerBearingRow)

    @property
    def loaded_rolling_bearing_row(self: "CastSelf") -> "_2242.LoadedRollingBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2242

        return self.__parent__._cast(_2242.LoadedRollingBearingRow)

    @property
    def loaded_axial_thrust_cylindrical_roller_bearing_row(
        self: "CastSelf",
    ) -> "_2203.LoadedAxialThrustCylindricalRollerBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2203

        return self.__parent__._cast(_2203.LoadedAxialThrustCylindricalRollerBearingRow)

    @property
    def loaded_axial_thrust_needle_roller_bearing_row(
        self: "CastSelf",
    ) -> "_2206.LoadedAxialThrustNeedleRollerBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2206

        return self.__parent__._cast(_2206.LoadedAxialThrustNeedleRollerBearingRow)

    @property
    def loaded_cylindrical_roller_bearing_row(
        self: "CastSelf",
    ) -> "_2218.LoadedCylindricalRollerBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2218

        return self.__parent__._cast(_2218.LoadedCylindricalRollerBearingRow)

    @property
    def loaded_needle_roller_bearing_row(
        self: "CastSelf",
    ) -> "_2230.LoadedNeedleRollerBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2230

        return self.__parent__._cast(_2230.LoadedNeedleRollerBearingRow)

    @property
    def loaded_taper_roller_bearing_row(
        self: "CastSelf",
    ) -> "_2257.LoadedTaperRollerBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2257

        return self.__parent__._cast(_2257.LoadedTaperRollerBearingRow)

    @property
    def loaded_non_barrel_roller_bearing_row(
        self: "CastSelf",
    ) -> "LoadedNonBarrelRollerBearingRow":
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
class LoadedNonBarrelRollerBearingRow(_2238.LoadedRollerBearingRow):
    """LoadedNonBarrelRollerBearingRow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_NON_BARREL_ROLLER_BEARING_ROW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def rib_normal_contact_stress_inner_left(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RibNormalContactStressInnerLeft")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def rib_normal_contact_stress_inner_right(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RibNormalContactStressInnerRight")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def rib_normal_contact_stress_outer_left(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RibNormalContactStressOuterLeft")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def rib_normal_contact_stress_outer_right(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RibNormalContactStressOuterRight")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def loaded_bearing(self: "Self") -> "_2232.LoadedNonBarrelRollerBearingResults":
        """mastapy.bearings.bearing_results.rolling.LoadedNonBarrelRollerBearingResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadedBearing")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedNonBarrelRollerBearingRow":
        """Cast to another type.

        Returns:
            _Cast_LoadedNonBarrelRollerBearingRow
        """
        return _Cast_LoadedNonBarrelRollerBearingRow(self)
