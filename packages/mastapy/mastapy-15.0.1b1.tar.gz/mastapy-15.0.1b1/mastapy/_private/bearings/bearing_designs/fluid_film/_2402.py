"""PlainJournalBearing"""

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
from mastapy._private.bearings.bearing_designs import _2341

_PLAIN_JOURNAL_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.FluidFilm", "PlainJournalBearing"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings import _2080
    from mastapy._private.bearings.bearing_designs import _2340, _2344
    from mastapy._private.bearings.bearing_designs.fluid_film import _2400, _2404

    Self = TypeVar("Self", bound="PlainJournalBearing")
    CastSelf = TypeVar(
        "CastSelf", bound="PlainJournalBearing._Cast_PlainJournalBearing"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlainJournalBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlainJournalBearing:
    """Special nested class for casting PlainJournalBearing to subclasses."""

    __parent__: "PlainJournalBearing"

    @property
    def detailed_bearing(self: "CastSelf") -> "_2341.DetailedBearing":
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
    ) -> "_2400.PlainGreaseFilledJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2400

        return self.__parent__._cast(_2400.PlainGreaseFilledJournalBearing)

    @property
    def plain_oil_fed_journal_bearing(
        self: "CastSelf",
    ) -> "_2404.PlainOilFedJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2404

        return self.__parent__._cast(_2404.PlainOilFedJournalBearing)

    @property
    def plain_journal_bearing(self: "CastSelf") -> "PlainJournalBearing":
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
class PlainJournalBearing(_2341.DetailedBearing):
    """PlainJournalBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLAIN_JOURNAL_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def diametrical_clearance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DiametricalClearance")

        if temp is None:
            return 0.0

        return temp

    @diametrical_clearance.setter
    @exception_bridge
    @enforce_parameter_types
    def diametrical_clearance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DiametricalClearance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def land_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LandWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def land_width_to_diameter_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LandWidthToDiameterRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def model(self: "Self") -> "_2080.BearingModel":
        """mastapy.bearings.BearingModel

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Model")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Bearings.BearingModel")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings._2080", "BearingModel"
        )(value)

    @property
    def cast_to(self: "Self") -> "_Cast_PlainJournalBearing":
        """Cast to another type.

        Returns:
            _Cast_PlainJournalBearing
        """
        return _Cast_PlainJournalBearing(self)
