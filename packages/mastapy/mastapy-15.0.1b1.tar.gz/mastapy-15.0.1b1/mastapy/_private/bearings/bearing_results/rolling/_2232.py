"""LoadedNonBarrelRollerBearingResults"""

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
from mastapy._private.bearings.bearing_results.rolling import _2237

_LOADED_NON_BARREL_ROLLER_BEARING_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling",
    "LoadedNonBarrelRollerBearingResults",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings import _2078
    from mastapy._private.bearings.bearing_results import _2155, _2160, _2163
    from mastapy._private.bearings.bearing_results.rolling import (
        _2202,
        _2205,
        _2217,
        _2229,
        _2241,
        _2256,
        _2281,
    )

    Self = TypeVar("Self", bound="LoadedNonBarrelRollerBearingResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedNonBarrelRollerBearingResults._Cast_LoadedNonBarrelRollerBearingResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedNonBarrelRollerBearingResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedNonBarrelRollerBearingResults:
    """Special nested class for casting LoadedNonBarrelRollerBearingResults to subclasses."""

    __parent__: "LoadedNonBarrelRollerBearingResults"

    @property
    def loaded_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2237.LoadedRollerBearingResults":
        return self.__parent__._cast(_2237.LoadedRollerBearingResults)

    @property
    def loaded_rolling_bearing_results(
        self: "CastSelf",
    ) -> "_2241.LoadedRollingBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2241

        return self.__parent__._cast(_2241.LoadedRollingBearingResults)

    @property
    def loaded_detailed_bearing_results(
        self: "CastSelf",
    ) -> "_2160.LoadedDetailedBearingResults":
        from mastapy._private.bearings.bearing_results import _2160

        return self.__parent__._cast(_2160.LoadedDetailedBearingResults)

    @property
    def loaded_non_linear_bearing_results(
        self: "CastSelf",
    ) -> "_2163.LoadedNonLinearBearingResults":
        from mastapy._private.bearings.bearing_results import _2163

        return self.__parent__._cast(_2163.LoadedNonLinearBearingResults)

    @property
    def loaded_bearing_results(self: "CastSelf") -> "_2155.LoadedBearingResults":
        from mastapy._private.bearings.bearing_results import _2155

        return self.__parent__._cast(_2155.LoadedBearingResults)

    @property
    def bearing_load_case_results_lightweight(
        self: "CastSelf",
    ) -> "_2078.BearingLoadCaseResultsLightweight":
        from mastapy._private.bearings import _2078

        return self.__parent__._cast(_2078.BearingLoadCaseResultsLightweight)

    @property
    def loaded_axial_thrust_cylindrical_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2202.LoadedAxialThrustCylindricalRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2202

        return self.__parent__._cast(
            _2202.LoadedAxialThrustCylindricalRollerBearingResults
        )

    @property
    def loaded_axial_thrust_needle_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2205.LoadedAxialThrustNeedleRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2205

        return self.__parent__._cast(_2205.LoadedAxialThrustNeedleRollerBearingResults)

    @property
    def loaded_cylindrical_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2217.LoadedCylindricalRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2217

        return self.__parent__._cast(_2217.LoadedCylindricalRollerBearingResults)

    @property
    def loaded_needle_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2229.LoadedNeedleRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2229

        return self.__parent__._cast(_2229.LoadedNeedleRollerBearingResults)

    @property
    def loaded_taper_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2256.LoadedTaperRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2256

        return self.__parent__._cast(_2256.LoadedTaperRollerBearingResults)

    @property
    def loaded_non_barrel_roller_bearing_results(
        self: "CastSelf",
    ) -> "LoadedNonBarrelRollerBearingResults":
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
class LoadedNonBarrelRollerBearingResults(_2237.LoadedRollerBearingResults):
    """LoadedNonBarrelRollerBearingResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_NON_BARREL_ROLLER_BEARING_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def smt_rib_stress(self: "Self") -> "_2281.SMTRibStressResults":
        """mastapy.bearings.bearing_results.rolling.SMTRibStressResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SMTRibStress")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedNonBarrelRollerBearingResults":
        """Cast to another type.

        Returns:
            _Cast_LoadedNonBarrelRollerBearingResults
        """
        return _Cast_LoadedNonBarrelRollerBearingResults(self)
