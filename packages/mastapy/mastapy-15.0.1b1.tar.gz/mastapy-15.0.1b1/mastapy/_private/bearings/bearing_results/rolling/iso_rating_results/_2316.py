"""RollerISO162812025Results"""

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
from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import _2312

_ROLLER_ISO162812025_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling.IsoRatingResults",
    "RollerISO162812025Results",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import (
        _2315,
    )

    Self = TypeVar("Self", bound="RollerISO162812025Results")
    CastSelf = TypeVar(
        "CastSelf", bound="RollerISO162812025Results._Cast_RollerISO162812025Results"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RollerISO162812025Results",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RollerISO162812025Results:
    """Special nested class for casting RollerISO162812025Results to subclasses."""

    __parent__: "RollerISO162812025Results"

    @property
    def iso162812025_results(self: "CastSelf") -> "_2312.ISO162812025Results":
        return self.__parent__._cast(_2312.ISO162812025Results)

    @property
    def iso_results(self: "CastSelf") -> "_2315.ISOResults":
        from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import (
            _2315,
        )

        return self.__parent__._cast(_2315.ISOResults)

    @property
    def roller_iso162812025_results(self: "CastSelf") -> "RollerISO162812025Results":
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
class RollerISO162812025Results(_2312.ISO162812025Results):
    """RollerISO162812025Results

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROLLER_ISO162812025_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def basic_dynamic_load_rating_of_a_bearing_lamina_of_the_inner_ring(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BasicDynamicLoadRatingOfABearingLaminaOfTheInnerRing"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def basic_dynamic_load_rating_of_a_bearing_lamina_of_the_outer_ring(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BasicDynamicLoadRatingOfABearingLaminaOfTheOuterRing"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def equivalent_load_assuming_line_contacts(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "EquivalentLoadAssumingLineContacts"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_RollerISO162812025Results":
        """Cast to another type.

        Returns:
            _Cast_RollerISO162812025Results
        """
        return _Cast_RollerISO162812025Results(self)
