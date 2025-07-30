"""LoadedPlainJournalBearingRow"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_LOADED_PLAIN_JOURNAL_BEARING_ROW = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.FluidFilm", "LoadedPlainJournalBearingRow"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.bearings import _2081
    from mastapy._private.bearings.bearing_results.fluid_film import _2335

    Self = TypeVar("Self", bound="LoadedPlainJournalBearingRow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedPlainJournalBearingRow._Cast_LoadedPlainJournalBearingRow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedPlainJournalBearingRow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedPlainJournalBearingRow:
    """Special nested class for casting LoadedPlainJournalBearingRow to subclasses."""

    __parent__: "LoadedPlainJournalBearingRow"

    @property
    def loaded_plain_oil_fed_journal_bearing_row(
        self: "CastSelf",
    ) -> "_2335.LoadedPlainOilFedJournalBearingRow":
        from mastapy._private.bearings.bearing_results.fluid_film import _2335

        return self.__parent__._cast(_2335.LoadedPlainOilFedJournalBearingRow)

    @property
    def loaded_plain_journal_bearing_row(
        self: "CastSelf",
    ) -> "LoadedPlainJournalBearingRow":
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
class LoadedPlainJournalBearingRow(_0.APIBase):
    """LoadedPlainJournalBearingRow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_PLAIN_JOURNAL_BEARING_ROW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def angular_position_of_the_minimum_film_thickness_from_the_x_axis(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AngularPositionOfTheMinimumFilmThicknessFromTheXAxis"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def attitude_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AttitudeAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def attitude_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AttitudeForce")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def clipped_minimum_film_thickness_at_row_centre(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ClippedMinimumFilmThicknessAtRowCentre"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def coefficient_of_traction(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CoefficientOfTraction")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def eccentricity_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EccentricityRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def force_x(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceX")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def force_y(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceY")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def journal_bearing_loading_chart(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "JournalBearingLoadingChart")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def minimum_film_thickness_at_row_centre(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumFilmThicknessAtRowCentre")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def non_dimensional_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NonDimensionalLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def radial_load_per_unit_of_projected_area(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RadialLoadPerUnitOfProjectedArea")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def row(self: "Self") -> "_2081.BearingRow":
        """mastapy.bearings.BearingRow

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Row")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Bearings.BearingRow")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings._2081", "BearingRow"
        )(value)

    @property
    @exception_bridge
    def sommerfeld_number(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SommerfeldNumber")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @exception_bridge
    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputDefaultReportTo", file_path)

    @exception_bridge
    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportTo", file_path)

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportAsTextTo", file_path)

    @exception_bridge
    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedPlainJournalBearingRow":
        """Cast to another type.

        Returns:
            _Cast_LoadedPlainJournalBearingRow
        """
        return _Cast_LoadedPlainJournalBearingRow(self)
