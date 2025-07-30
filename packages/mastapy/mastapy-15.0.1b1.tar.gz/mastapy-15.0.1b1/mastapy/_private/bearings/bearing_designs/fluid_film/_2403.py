"""PlainJournalHousing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_PLAIN_JOURNAL_HOUSING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.FluidFilm", "PlainJournalHousing"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_designs.fluid_film import _2396, _2397, _2399
    from mastapy._private.bearings.bearing_results import _2149

    Self = TypeVar("Self", bound="PlainJournalHousing")
    CastSelf = TypeVar(
        "CastSelf", bound="PlainJournalHousing._Cast_PlainJournalHousing"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlainJournalHousing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlainJournalHousing:
    """Special nested class for casting PlainJournalHousing to subclasses."""

    __parent__: "PlainJournalHousing"

    @property
    def cylindrical_housing_journal_bearing(
        self: "CastSelf",
    ) -> "_2396.CylindricalHousingJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2396

        return self.__parent__._cast(_2396.CylindricalHousingJournalBearing)

    @property
    def machinery_encased_journal_bearing(
        self: "CastSelf",
    ) -> "_2397.MachineryEncasedJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2397

        return self.__parent__._cast(_2397.MachineryEncasedJournalBearing)

    @property
    def pedestal_journal_bearing(self: "CastSelf") -> "_2399.PedestalJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2399

        return self.__parent__._cast(_2399.PedestalJournalBearing)

    @property
    def plain_journal_housing(self: "CastSelf") -> "PlainJournalHousing":
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
class PlainJournalHousing(_0.APIBase):
    """PlainJournalHousing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLAIN_JOURNAL_HOUSING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def heat_emitting_area(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "HeatEmittingArea")

        if temp is None:
            return 0.0

        return temp

    @heat_emitting_area.setter
    @exception_bridge
    @enforce_parameter_types
    def heat_emitting_area(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "HeatEmittingArea", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def heat_emitting_area_method(self: "Self") -> "_2149.DefaultOrUserInput":
        """mastapy.bearings.bearing_results.DefaultOrUserInput"""
        temp = pythonnet_property_get(self.wrapped, "HeatEmittingAreaMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.BearingResults.DefaultOrUserInput"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings.bearing_results._2149", "DefaultOrUserInput"
        )(value)

    @heat_emitting_area_method.setter
    @exception_bridge
    @enforce_parameter_types
    def heat_emitting_area_method(
        self: "Self", value: "_2149.DefaultOrUserInput"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Bearings.BearingResults.DefaultOrUserInput"
        )
        pythonnet_property_set(self.wrapped, "HeatEmittingAreaMethod", value)

    @property
    def cast_to(self: "Self") -> "_Cast_PlainJournalHousing":
        """Cast to another type.

        Returns:
            _Cast_PlainJournalHousing
        """
        return _Cast_PlainJournalHousing(self)
