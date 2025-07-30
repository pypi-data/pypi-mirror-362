"""ISOResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_ISO_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling.IsoRatingResults", "ISOResults"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.bearings.bearing_results.rolling.abma import (
        _2325,
        _2326,
        _2327,
    )
    from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import (
        _2310,
        _2311,
        _2312,
        _2313,
        _2316,
        _2317,
    )

    Self = TypeVar("Self", bound="ISOResults")
    CastSelf = TypeVar("CastSelf", bound="ISOResults._Cast_ISOResults")


__docformat__ = "restructuredtext en"
__all__ = ("ISOResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISOResults:
    """Special nested class for casting ISOResults to subclasses."""

    __parent__: "ISOResults"

    @property
    def ball_iso162812025_results(self: "CastSelf") -> "_2310.BallISO162812025Results":
        from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import (
            _2310,
        )

        return self.__parent__._cast(_2310.BallISO162812025Results)

    @property
    def ball_iso2812007_results(self: "CastSelf") -> "_2311.BallISO2812007Results":
        from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import (
            _2311,
        )

        return self.__parent__._cast(_2311.BallISO2812007Results)

    @property
    def iso162812025_results(self: "CastSelf") -> "_2312.ISO162812025Results":
        from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import (
            _2312,
        )

        return self.__parent__._cast(_2312.ISO162812025Results)

    @property
    def iso2812007_results(self: "CastSelf") -> "_2313.ISO2812007Results":
        from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import (
            _2313,
        )

        return self.__parent__._cast(_2313.ISO2812007Results)

    @property
    def roller_iso162812025_results(
        self: "CastSelf",
    ) -> "_2316.RollerISO162812025Results":
        from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import (
            _2316,
        )

        return self.__parent__._cast(_2316.RollerISO162812025Results)

    @property
    def roller_iso2812007_results(self: "CastSelf") -> "_2317.RollerISO2812007Results":
        from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import (
            _2317,
        )

        return self.__parent__._cast(_2317.RollerISO2812007Results)

    @property
    def ansiabma112014_results(self: "CastSelf") -> "_2325.ANSIABMA112014Results":
        from mastapy._private.bearings.bearing_results.rolling.abma import _2325

        return self.__parent__._cast(_2325.ANSIABMA112014Results)

    @property
    def ansiabma92015_results(self: "CastSelf") -> "_2326.ANSIABMA92015Results":
        from mastapy._private.bearings.bearing_results.rolling.abma import _2326

        return self.__parent__._cast(_2326.ANSIABMA92015Results)

    @property
    def ansiabma_results(self: "CastSelf") -> "_2327.ANSIABMAResults":
        from mastapy._private.bearings.bearing_results.rolling.abma import _2327

        return self.__parent__._cast(_2327.ANSIABMAResults)

    @property
    def iso_results(self: "CastSelf") -> "ISOResults":
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
class ISOResults(_0.APIBase):
    """ISOResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISO_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def life_modification_factor_for_reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LifeModificationFactorForReliability"
        )

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
    def cast_to(self: "Self") -> "_Cast_ISOResults":
        """Cast to another type.

        Returns:
            _Cast_ISOResults
        """
        return _Cast_ISOResults(self)
