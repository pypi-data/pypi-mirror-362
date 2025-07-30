"""LoadedAbstractSphericalRollerBearingStripLoadResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_results.rolling import _2239

_LOADED_ABSTRACT_SPHERICAL_ROLLER_BEARING_STRIP_LOAD_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling",
    "LoadedAbstractSphericalRollerBearingStripLoadResults",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling import _2199, _2250, _2267

    Self = TypeVar("Self", bound="LoadedAbstractSphericalRollerBearingStripLoadResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedAbstractSphericalRollerBearingStripLoadResults._Cast_LoadedAbstractSphericalRollerBearingStripLoadResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedAbstractSphericalRollerBearingStripLoadResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedAbstractSphericalRollerBearingStripLoadResults:
    """Special nested class for casting LoadedAbstractSphericalRollerBearingStripLoadResults to subclasses."""

    __parent__: "LoadedAbstractSphericalRollerBearingStripLoadResults"

    @property
    def loaded_roller_strip_load_results(
        self: "CastSelf",
    ) -> "_2239.LoadedRollerStripLoadResults":
        return self.__parent__._cast(_2239.LoadedRollerStripLoadResults)

    @property
    def loaded_asymmetric_spherical_roller_bearing_strip_load_results(
        self: "CastSelf",
    ) -> "_2199.LoadedAsymmetricSphericalRollerBearingStripLoadResults":
        from mastapy._private.bearings.bearing_results.rolling import _2199

        return self.__parent__._cast(
            _2199.LoadedAsymmetricSphericalRollerBearingStripLoadResults
        )

    @property
    def loaded_spherical_roller_radial_bearing_strip_load_results(
        self: "CastSelf",
    ) -> "_2250.LoadedSphericalRollerRadialBearingStripLoadResults":
        from mastapy._private.bearings.bearing_results.rolling import _2250

        return self.__parent__._cast(
            _2250.LoadedSphericalRollerRadialBearingStripLoadResults
        )

    @property
    def loaded_toroidal_roller_bearing_strip_load_results(
        self: "CastSelf",
    ) -> "_2267.LoadedToroidalRollerBearingStripLoadResults":
        from mastapy._private.bearings.bearing_results.rolling import _2267

        return self.__parent__._cast(_2267.LoadedToroidalRollerBearingStripLoadResults)

    @property
    def loaded_abstract_spherical_roller_bearing_strip_load_results(
        self: "CastSelf",
    ) -> "LoadedAbstractSphericalRollerBearingStripLoadResults":
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
class LoadedAbstractSphericalRollerBearingStripLoadResults(
    _2239.LoadedRollerStripLoadResults
):
    """LoadedAbstractSphericalRollerBearingStripLoadResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _LOADED_ABSTRACT_SPHERICAL_ROLLER_BEARING_STRIP_LOAD_RESULTS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_LoadedAbstractSphericalRollerBearingStripLoadResults":
        """Cast to another type.

        Returns:
            _Cast_LoadedAbstractSphericalRollerBearingStripLoadResults
        """
        return _Cast_LoadedAbstractSphericalRollerBearingStripLoadResults(self)
