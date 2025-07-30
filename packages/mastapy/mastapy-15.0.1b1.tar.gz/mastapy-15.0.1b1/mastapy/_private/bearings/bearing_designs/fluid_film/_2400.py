"""PlainGreaseFilledJournalBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

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
from mastapy._private.bearings.bearing_designs.fluid_film import _2402

_PLAIN_GREASE_FILLED_JOURNAL_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.FluidFilm", "PlainGreaseFilledJournalBearing"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_designs import _2340, _2341, _2344
    from mastapy._private.bearings.bearing_designs.fluid_film import _2401, _2403

    Self = TypeVar("Self", bound="PlainGreaseFilledJournalBearing")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PlainGreaseFilledJournalBearing._Cast_PlainGreaseFilledJournalBearing",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlainGreaseFilledJournalBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlainGreaseFilledJournalBearing:
    """Special nested class for casting PlainGreaseFilledJournalBearing to subclasses."""

    __parent__: "PlainGreaseFilledJournalBearing"

    @property
    def plain_journal_bearing(self: "CastSelf") -> "_2402.PlainJournalBearing":
        return self.__parent__._cast(_2402.PlainJournalBearing)

    @property
    def detailed_bearing(self: "CastSelf") -> "_2341.DetailedBearing":
        from mastapy._private.bearings.bearing_designs import _2341

        return self.__parent__._cast(_2341.DetailedBearing)

    @property
    def non_linear_bearing(self: "CastSelf") -> "_2344.NonLinearBearing":
        from mastapy._private.bearings.bearing_designs import _2344

        return self.__parent__._cast(_2344.NonLinearBearing)

    @property
    def bearing_design(self: "CastSelf") -> "_2340.BearingDesign":
        from mastapy._private.bearings.bearing_designs import _2340

        return self.__parent__._cast(_2340.BearingDesign)

    @property
    def plain_grease_filled_journal_bearing(
        self: "CastSelf",
    ) -> "PlainGreaseFilledJournalBearing":
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
class PlainGreaseFilledJournalBearing(_2402.PlainJournalBearing):
    """PlainGreaseFilledJournalBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLAIN_GREASE_FILLED_JOURNAL_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def housing_type(
        self: "Self",
    ) -> "_2401.PlainGreaseFilledJournalBearingHousingType":
        """mastapy.bearings.bearing_designs.fluid_film.PlainGreaseFilledJournalBearingHousingType"""
        temp = pythonnet_property_get(self.wrapped, "HousingType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Bearings.BearingDesigns.FluidFilm.PlainGreaseFilledJournalBearingHousingType",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings.bearing_designs.fluid_film._2401",
            "PlainGreaseFilledJournalBearingHousingType",
        )(value)

    @housing_type.setter
    @exception_bridge
    @enforce_parameter_types
    def housing_type(
        self: "Self", value: "_2401.PlainGreaseFilledJournalBearingHousingType"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Bearings.BearingDesigns.FluidFilm.PlainGreaseFilledJournalBearingHousingType",
        )
        pythonnet_property_set(self.wrapped, "HousingType", value)

    @property
    @exception_bridge
    def housing_detail(self: "Self") -> "_2403.PlainJournalHousing":
        """mastapy.bearings.bearing_designs.fluid_film.PlainJournalHousing

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HousingDetail")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_PlainGreaseFilledJournalBearing":
        """Cast to another type.

        Returns:
            _Cast_PlainGreaseFilledJournalBearing
        """
        return _Cast_PlainGreaseFilledJournalBearing(self)
