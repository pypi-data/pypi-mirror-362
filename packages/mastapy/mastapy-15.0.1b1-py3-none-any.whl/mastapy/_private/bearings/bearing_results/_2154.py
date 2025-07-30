"""LoadedBearingDutyCycle"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings import _2078

_LOADED_BEARING_DUTY_CYCLE = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults", "LoadedBearingDutyCycle"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.bearings.bearing_designs import _2340
    from mastapy._private.bearings.bearing_results import _2155, _2162, _2165
    from mastapy._private.bearings.bearing_results.rolling import (
        _2200,
        _2207,
        _2215,
        _2231,
        _2254,
    )
    from mastapy._private.utility.property import _2041

    Self = TypeVar("Self", bound="LoadedBearingDutyCycle")
    CastSelf = TypeVar(
        "CastSelf", bound="LoadedBearingDutyCycle._Cast_LoadedBearingDutyCycle"
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedBearingDutyCycle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedBearingDutyCycle:
    """Special nested class for casting LoadedBearingDutyCycle to subclasses."""

    __parent__: "LoadedBearingDutyCycle"

    @property
    def loaded_non_linear_bearing_duty_cycle_results(
        self: "CastSelf",
    ) -> "_2162.LoadedNonLinearBearingDutyCycleResults":
        from mastapy._private.bearings.bearing_results import _2162

        return self.__parent__._cast(_2162.LoadedNonLinearBearingDutyCycleResults)

    @property
    def loaded_rolling_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "_2165.LoadedRollingBearingDutyCycle":
        from mastapy._private.bearings.bearing_results import _2165

        return self.__parent__._cast(_2165.LoadedRollingBearingDutyCycle)

    @property
    def loaded_axial_thrust_cylindrical_roller_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "_2200.LoadedAxialThrustCylindricalRollerBearingDutyCycle":
        from mastapy._private.bearings.bearing_results.rolling import _2200

        return self.__parent__._cast(
            _2200.LoadedAxialThrustCylindricalRollerBearingDutyCycle
        )

    @property
    def loaded_ball_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "_2207.LoadedBallBearingDutyCycle":
        from mastapy._private.bearings.bearing_results.rolling import _2207

        return self.__parent__._cast(_2207.LoadedBallBearingDutyCycle)

    @property
    def loaded_cylindrical_roller_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "_2215.LoadedCylindricalRollerBearingDutyCycle":
        from mastapy._private.bearings.bearing_results.rolling import _2215

        return self.__parent__._cast(_2215.LoadedCylindricalRollerBearingDutyCycle)

    @property
    def loaded_non_barrel_roller_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "_2231.LoadedNonBarrelRollerBearingDutyCycle":
        from mastapy._private.bearings.bearing_results.rolling import _2231

        return self.__parent__._cast(_2231.LoadedNonBarrelRollerBearingDutyCycle)

    @property
    def loaded_taper_roller_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "_2254.LoadedTaperRollerBearingDutyCycle":
        from mastapy._private.bearings.bearing_results.rolling import _2254

        return self.__parent__._cast(_2254.LoadedTaperRollerBearingDutyCycle)

    @property
    def loaded_bearing_duty_cycle(self: "CastSelf") -> "LoadedBearingDutyCycle":
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
class LoadedBearingDutyCycle(_0.APIBase):
    """LoadedBearingDutyCycle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_BEARING_DUTY_CYCLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def duration(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Duration")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def duty_cycle_name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "DutyCycleName")

        if temp is None:
            return ""

        return temp

    @duty_cycle_name.setter
    @exception_bridge
    @enforce_parameter_types
    def duty_cycle_name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "DutyCycleName", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def bearing_design(self: "Self") -> "_2340.BearingDesign":
        """mastapy.bearings.bearing_designs.BearingDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BearingDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def radial_load_summary(
        self: "Self",
    ) -> "_2041.DutyCyclePropertySummaryForce[_2078.BearingLoadCaseResultsLightweight]":
        """mastapy.utility.property.DutyCyclePropertySummaryForce[mastapy.bearings.BearingLoadCaseResultsLightweight]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RadialLoadSummary")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[
            _2078.BearingLoadCaseResultsLightweight
        ](temp)

    @property
    @exception_bridge
    def z_thrust_reaction_summary(
        self: "Self",
    ) -> "_2041.DutyCyclePropertySummaryForce[_2078.BearingLoadCaseResultsLightweight]":
        """mastapy.utility.property.DutyCyclePropertySummaryForce[mastapy.bearings.BearingLoadCaseResultsLightweight]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ZThrustReactionSummary")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[
            _2078.BearingLoadCaseResultsLightweight
        ](temp)

    @property
    @exception_bridge
    def bearing_load_case_results(self: "Self") -> "List[_2155.LoadedBearingResults]":
        """List[mastapy.bearings.bearing_results.LoadedBearingResults]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BearingLoadCaseResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

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
    def cast_to(self: "Self") -> "_Cast_LoadedBearingDutyCycle":
        """Cast to another type.

        Returns:
            _Cast_LoadedBearingDutyCycle
        """
        return _Cast_LoadedBearingDutyCycle(self)
