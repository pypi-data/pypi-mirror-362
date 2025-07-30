"""BearingLoadCaseResultsLightweight"""

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

_BEARING_LOAD_CASE_RESULTS_LIGHTWEIGHT = python_net_import(
    "SMT.MastaAPI.Bearings", "BearingLoadCaseResultsLightweight"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.bearings import _2077
    from mastapy._private.bearings.bearing_results import (
        _2155,
        _2157,
        _2158,
        _2159,
        _2160,
        _2161,
        _2163,
    )
    from mastapy._private.bearings.bearing_results.fluid_film import (
        _2329,
        _2330,
        _2331,
        _2332,
        _2334,
        _2337,
        _2338,
    )
    from mastapy._private.bearings.bearing_results.rolling import (
        _2191,
        _2194,
        _2197,
        _2202,
        _2205,
        _2210,
        _2213,
        _2217,
        _2220,
        _2225,
        _2229,
        _2232,
        _2237,
        _2241,
        _2244,
        _2248,
        _2251,
        _2256,
        _2259,
        _2262,
        _2265,
    )

    Self = TypeVar("Self", bound="BearingLoadCaseResultsLightweight")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BearingLoadCaseResultsLightweight._Cast_BearingLoadCaseResultsLightweight",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BearingLoadCaseResultsLightweight",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BearingLoadCaseResultsLightweight:
    """Special nested class for casting BearingLoadCaseResultsLightweight to subclasses."""

    __parent__: "BearingLoadCaseResultsLightweight"

    @property
    def bearing_load_case_results_for_pst(
        self: "CastSelf",
    ) -> "_2077.BearingLoadCaseResultsForPST":
        from mastapy._private.bearings import _2077

        return self.__parent__._cast(_2077.BearingLoadCaseResultsForPST)

    @property
    def loaded_bearing_results(self: "CastSelf") -> "_2155.LoadedBearingResults":
        from mastapy._private.bearings.bearing_results import _2155

        return self.__parent__._cast(_2155.LoadedBearingResults)

    @property
    def loaded_concept_axial_clearance_bearing_results(
        self: "CastSelf",
    ) -> "_2157.LoadedConceptAxialClearanceBearingResults":
        from mastapy._private.bearings.bearing_results import _2157

        return self.__parent__._cast(_2157.LoadedConceptAxialClearanceBearingResults)

    @property
    def loaded_concept_clearance_bearing_results(
        self: "CastSelf",
    ) -> "_2158.LoadedConceptClearanceBearingResults":
        from mastapy._private.bearings.bearing_results import _2158

        return self.__parent__._cast(_2158.LoadedConceptClearanceBearingResults)

    @property
    def loaded_concept_radial_clearance_bearing_results(
        self: "CastSelf",
    ) -> "_2159.LoadedConceptRadialClearanceBearingResults":
        from mastapy._private.bearings.bearing_results import _2159

        return self.__parent__._cast(_2159.LoadedConceptRadialClearanceBearingResults)

    @property
    def loaded_detailed_bearing_results(
        self: "CastSelf",
    ) -> "_2160.LoadedDetailedBearingResults":
        from mastapy._private.bearings.bearing_results import _2160

        return self.__parent__._cast(_2160.LoadedDetailedBearingResults)

    @property
    def loaded_linear_bearing_results(
        self: "CastSelf",
    ) -> "_2161.LoadedLinearBearingResults":
        from mastapy._private.bearings.bearing_results import _2161

        return self.__parent__._cast(_2161.LoadedLinearBearingResults)

    @property
    def loaded_non_linear_bearing_results(
        self: "CastSelf",
    ) -> "_2163.LoadedNonLinearBearingResults":
        from mastapy._private.bearings.bearing_results import _2163

        return self.__parent__._cast(_2163.LoadedNonLinearBearingResults)

    @property
    def loaded_angular_contact_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2191.LoadedAngularContactBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2191

        return self.__parent__._cast(_2191.LoadedAngularContactBallBearingResults)

    @property
    def loaded_angular_contact_thrust_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2194.LoadedAngularContactThrustBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2194

        return self.__parent__._cast(_2194.LoadedAngularContactThrustBallBearingResults)

    @property
    def loaded_asymmetric_spherical_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2197.LoadedAsymmetricSphericalRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2197

        return self.__parent__._cast(
            _2197.LoadedAsymmetricSphericalRollerBearingResults
        )

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
    def loaded_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2210.LoadedBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2210

        return self.__parent__._cast(_2210.LoadedBallBearingResults)

    @property
    def loaded_crossed_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2213.LoadedCrossedRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2213

        return self.__parent__._cast(_2213.LoadedCrossedRollerBearingResults)

    @property
    def loaded_cylindrical_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2217.LoadedCylindricalRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2217

        return self.__parent__._cast(_2217.LoadedCylindricalRollerBearingResults)

    @property
    def loaded_deep_groove_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2220.LoadedDeepGrooveBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2220

        return self.__parent__._cast(_2220.LoadedDeepGrooveBallBearingResults)

    @property
    def loaded_four_point_contact_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2225.LoadedFourPointContactBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2225

        return self.__parent__._cast(_2225.LoadedFourPointContactBallBearingResults)

    @property
    def loaded_needle_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2229.LoadedNeedleRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2229

        return self.__parent__._cast(_2229.LoadedNeedleRollerBearingResults)

    @property
    def loaded_non_barrel_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2232.LoadedNonBarrelRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2232

        return self.__parent__._cast(_2232.LoadedNonBarrelRollerBearingResults)

    @property
    def loaded_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2237.LoadedRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2237

        return self.__parent__._cast(_2237.LoadedRollerBearingResults)

    @property
    def loaded_rolling_bearing_results(
        self: "CastSelf",
    ) -> "_2241.LoadedRollingBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2241

        return self.__parent__._cast(_2241.LoadedRollingBearingResults)

    @property
    def loaded_self_aligning_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2244.LoadedSelfAligningBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2244

        return self.__parent__._cast(_2244.LoadedSelfAligningBallBearingResults)

    @property
    def loaded_spherical_roller_radial_bearing_results(
        self: "CastSelf",
    ) -> "_2248.LoadedSphericalRollerRadialBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2248

        return self.__parent__._cast(_2248.LoadedSphericalRollerRadialBearingResults)

    @property
    def loaded_spherical_roller_thrust_bearing_results(
        self: "CastSelf",
    ) -> "_2251.LoadedSphericalRollerThrustBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2251

        return self.__parent__._cast(_2251.LoadedSphericalRollerThrustBearingResults)

    @property
    def loaded_taper_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2256.LoadedTaperRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2256

        return self.__parent__._cast(_2256.LoadedTaperRollerBearingResults)

    @property
    def loaded_three_point_contact_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2259.LoadedThreePointContactBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2259

        return self.__parent__._cast(_2259.LoadedThreePointContactBallBearingResults)

    @property
    def loaded_thrust_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2262.LoadedThrustBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2262

        return self.__parent__._cast(_2262.LoadedThrustBallBearingResults)

    @property
    def loaded_toroidal_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2265.LoadedToroidalRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2265

        return self.__parent__._cast(_2265.LoadedToroidalRollerBearingResults)

    @property
    def loaded_fluid_film_bearing_results(
        self: "CastSelf",
    ) -> "_2329.LoadedFluidFilmBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2329

        return self.__parent__._cast(_2329.LoadedFluidFilmBearingResults)

    @property
    def loaded_grease_filled_journal_bearing_results(
        self: "CastSelf",
    ) -> "_2330.LoadedGreaseFilledJournalBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2330

        return self.__parent__._cast(_2330.LoadedGreaseFilledJournalBearingResults)

    @property
    def loaded_pad_fluid_film_bearing_results(
        self: "CastSelf",
    ) -> "_2331.LoadedPadFluidFilmBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2331

        return self.__parent__._cast(_2331.LoadedPadFluidFilmBearingResults)

    @property
    def loaded_plain_journal_bearing_results(
        self: "CastSelf",
    ) -> "_2332.LoadedPlainJournalBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2332

        return self.__parent__._cast(_2332.LoadedPlainJournalBearingResults)

    @property
    def loaded_plain_oil_fed_journal_bearing(
        self: "CastSelf",
    ) -> "_2334.LoadedPlainOilFedJournalBearing":
        from mastapy._private.bearings.bearing_results.fluid_film import _2334

        return self.__parent__._cast(_2334.LoadedPlainOilFedJournalBearing)

    @property
    def loaded_tilting_pad_journal_bearing_results(
        self: "CastSelf",
    ) -> "_2337.LoadedTiltingPadJournalBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2337

        return self.__parent__._cast(_2337.LoadedTiltingPadJournalBearingResults)

    @property
    def loaded_tilting_pad_thrust_bearing_results(
        self: "CastSelf",
    ) -> "_2338.LoadedTiltingPadThrustBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2338

        return self.__parent__._cast(_2338.LoadedTiltingPadThrustBearingResults)

    @property
    def bearing_load_case_results_lightweight(
        self: "CastSelf",
    ) -> "BearingLoadCaseResultsLightweight":
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
class BearingLoadCaseResultsLightweight(_0.APIBase):
    """BearingLoadCaseResultsLightweight

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEARING_LOAD_CASE_RESULTS_LIGHTWEIGHT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def relative_misalignment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeMisalignment")

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
    def cast_to(self: "Self") -> "_Cast_BearingLoadCaseResultsLightweight":
        """Cast to another type.

        Returns:
            _Cast_BearingLoadCaseResultsLightweight
        """
        return _Cast_BearingLoadCaseResultsLightweight(self)
