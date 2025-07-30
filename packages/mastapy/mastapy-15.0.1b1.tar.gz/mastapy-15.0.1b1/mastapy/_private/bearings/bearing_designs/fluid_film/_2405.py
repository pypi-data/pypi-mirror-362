"""TiltingPadJournalBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings.bearing_designs.fluid_film import _2398

_TILTING_PAD_JOURNAL_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.FluidFilm", "TiltingPadJournalBearing"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.bearings import _2080
    from mastapy._private.bearings.bearing_designs import _2340, _2341, _2344

    Self = TypeVar("Self", bound="TiltingPadJournalBearing")
    CastSelf = TypeVar(
        "CastSelf", bound="TiltingPadJournalBearing._Cast_TiltingPadJournalBearing"
    )


__docformat__ = "restructuredtext en"
__all__ = ("TiltingPadJournalBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TiltingPadJournalBearing:
    """Special nested class for casting TiltingPadJournalBearing to subclasses."""

    __parent__: "TiltingPadJournalBearing"

    @property
    def pad_fluid_film_bearing(self: "CastSelf") -> "_2398.PadFluidFilmBearing":
        return self.__parent__._cast(_2398.PadFluidFilmBearing)

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
    def tilting_pad_journal_bearing(self: "CastSelf") -> "TiltingPadJournalBearing":
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
class TiltingPadJournalBearing(_2398.PadFluidFilmBearing):
    """TiltingPadJournalBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TILTING_PAD_JOURNAL_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def bearing_aspect_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BearingAspectRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def difference_between_pad_contact_surface_radius_and_bearing_inner_radius(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "DifferenceBetweenPadContactSurfaceRadiusAndBearingInnerRadius",
        )

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
    @exception_bridge
    def pad_contact_surface_radius(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "PadContactSurfaceRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @pad_contact_surface_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def pad_contact_surface_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "PadContactSurfaceRadius", value)

    @property
    @exception_bridge
    def pivot_angular_offset(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PivotAngularOffset")

        if temp is None:
            return 0.0

        return temp

    @pivot_angular_offset.setter
    @exception_bridge
    @enforce_parameter_types
    def pivot_angular_offset(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PivotAngularOffset",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_TiltingPadJournalBearing":
        """Cast to another type.

        Returns:
            _Cast_TiltingPadJournalBearing
        """
        return _Cast_TiltingPadJournalBearing(self)
