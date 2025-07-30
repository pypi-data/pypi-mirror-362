"""LoadedRollingBearingRow"""

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

_LOADED_ROLLING_BEARING_ROW = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "LoadedRollingBearingRow"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.bearings.bearing_results.rolling import (
        _2180,
        _2192,
        _2195,
        _2198,
        _2203,
        _2206,
        _2211,
        _2214,
        _2218,
        _2221,
        _2222,
        _2226,
        _2230,
        _2233,
        _2238,
        _2240,
        _2241,
        _2245,
        _2249,
        _2252,
        _2257,
        _2260,
        _2263,
        _2266,
        _2276,
        _2282,
    )
    from mastapy._private.utility_gui.charts import _2070

    Self = TypeVar("Self", bound="LoadedRollingBearingRow")
    CastSelf = TypeVar(
        "CastSelf", bound="LoadedRollingBearingRow._Cast_LoadedRollingBearingRow"
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedRollingBearingRow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedRollingBearingRow:
    """Special nested class for casting LoadedRollingBearingRow to subclasses."""

    __parent__: "LoadedRollingBearingRow"

    @property
    def loaded_angular_contact_ball_bearing_row(
        self: "CastSelf",
    ) -> "_2192.LoadedAngularContactBallBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2192

        return self.__parent__._cast(_2192.LoadedAngularContactBallBearingRow)

    @property
    def loaded_angular_contact_thrust_ball_bearing_row(
        self: "CastSelf",
    ) -> "_2195.LoadedAngularContactThrustBallBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2195

        return self.__parent__._cast(_2195.LoadedAngularContactThrustBallBearingRow)

    @property
    def loaded_asymmetric_spherical_roller_bearing_row(
        self: "CastSelf",
    ) -> "_2198.LoadedAsymmetricSphericalRollerBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2198

        return self.__parent__._cast(_2198.LoadedAsymmetricSphericalRollerBearingRow)

    @property
    def loaded_axial_thrust_cylindrical_roller_bearing_row(
        self: "CastSelf",
    ) -> "_2203.LoadedAxialThrustCylindricalRollerBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2203

        return self.__parent__._cast(_2203.LoadedAxialThrustCylindricalRollerBearingRow)

    @property
    def loaded_axial_thrust_needle_roller_bearing_row(
        self: "CastSelf",
    ) -> "_2206.LoadedAxialThrustNeedleRollerBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2206

        return self.__parent__._cast(_2206.LoadedAxialThrustNeedleRollerBearingRow)

    @property
    def loaded_ball_bearing_row(self: "CastSelf") -> "_2211.LoadedBallBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2211

        return self.__parent__._cast(_2211.LoadedBallBearingRow)

    @property
    def loaded_crossed_roller_bearing_row(
        self: "CastSelf",
    ) -> "_2214.LoadedCrossedRollerBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2214

        return self.__parent__._cast(_2214.LoadedCrossedRollerBearingRow)

    @property
    def loaded_cylindrical_roller_bearing_row(
        self: "CastSelf",
    ) -> "_2218.LoadedCylindricalRollerBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2218

        return self.__parent__._cast(_2218.LoadedCylindricalRollerBearingRow)

    @property
    def loaded_deep_groove_ball_bearing_row(
        self: "CastSelf",
    ) -> "_2221.LoadedDeepGrooveBallBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2221

        return self.__parent__._cast(_2221.LoadedDeepGrooveBallBearingRow)

    @property
    def loaded_four_point_contact_ball_bearing_row(
        self: "CastSelf",
    ) -> "_2226.LoadedFourPointContactBallBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2226

        return self.__parent__._cast(_2226.LoadedFourPointContactBallBearingRow)

    @property
    def loaded_needle_roller_bearing_row(
        self: "CastSelf",
    ) -> "_2230.LoadedNeedleRollerBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2230

        return self.__parent__._cast(_2230.LoadedNeedleRollerBearingRow)

    @property
    def loaded_non_barrel_roller_bearing_row(
        self: "CastSelf",
    ) -> "_2233.LoadedNonBarrelRollerBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2233

        return self.__parent__._cast(_2233.LoadedNonBarrelRollerBearingRow)

    @property
    def loaded_roller_bearing_row(self: "CastSelf") -> "_2238.LoadedRollerBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2238

        return self.__parent__._cast(_2238.LoadedRollerBearingRow)

    @property
    def loaded_self_aligning_ball_bearing_row(
        self: "CastSelf",
    ) -> "_2245.LoadedSelfAligningBallBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2245

        return self.__parent__._cast(_2245.LoadedSelfAligningBallBearingRow)

    @property
    def loaded_spherical_roller_radial_bearing_row(
        self: "CastSelf",
    ) -> "_2249.LoadedSphericalRollerRadialBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2249

        return self.__parent__._cast(_2249.LoadedSphericalRollerRadialBearingRow)

    @property
    def loaded_spherical_roller_thrust_bearing_row(
        self: "CastSelf",
    ) -> "_2252.LoadedSphericalRollerThrustBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2252

        return self.__parent__._cast(_2252.LoadedSphericalRollerThrustBearingRow)

    @property
    def loaded_taper_roller_bearing_row(
        self: "CastSelf",
    ) -> "_2257.LoadedTaperRollerBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2257

        return self.__parent__._cast(_2257.LoadedTaperRollerBearingRow)

    @property
    def loaded_three_point_contact_ball_bearing_row(
        self: "CastSelf",
    ) -> "_2260.LoadedThreePointContactBallBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2260

        return self.__parent__._cast(_2260.LoadedThreePointContactBallBearingRow)

    @property
    def loaded_thrust_ball_bearing_row(
        self: "CastSelf",
    ) -> "_2263.LoadedThrustBallBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2263

        return self.__parent__._cast(_2263.LoadedThrustBallBearingRow)

    @property
    def loaded_toroidal_roller_bearing_row(
        self: "CastSelf",
    ) -> "_2266.LoadedToroidalRollerBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2266

        return self.__parent__._cast(_2266.LoadedToroidalRollerBearingRow)

    @property
    def loaded_rolling_bearing_row(self: "CastSelf") -> "LoadedRollingBearingRow":
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
class LoadedRollingBearingRow(_0.APIBase):
    """LoadedRollingBearingRow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_ROLLING_BEARING_ROW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def dynamic_equivalent_reference_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicEquivalentReferenceLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def life_modification_factor_for_systems_approach(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LifeModificationFactorForSystemsApproach"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_element_normal_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumElementNormalStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_element_normal_stress_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumElementNormalStressInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_element_normal_stress_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumElementNormalStressOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_normal_load_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumNormalLoadInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_normal_load_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumNormalLoadOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_contact_stress_chart_inner(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalContactStressChartInner")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def normal_contact_stress_chart_left(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalContactStressChartLeft")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def normal_contact_stress_chart_outer(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalContactStressChartOuter")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def normal_contact_stress_chart_right(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalContactStressChartRight")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def row_id(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RowID")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def subsurface_stress_chart_inner(self: "Self") -> "_2070.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SubsurfaceStressChartInner")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def subsurface_stress_chart_outer(self: "Self") -> "_2070.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SubsurfaceStressChartOuter")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def loaded_bearing(self: "Self") -> "_2241.LoadedRollingBearingResults":
        """mastapy.bearings.bearing_results.rolling.LoadedRollingBearingResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadedBearing")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def maximum_operating_internal_clearance(self: "Self") -> "_2180.InternalClearance":
        """mastapy.bearings.bearing_results.rolling.InternalClearance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumOperatingInternalClearance")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def minimum_operating_internal_clearance(self: "Self") -> "_2180.InternalClearance":
        """mastapy.bearings.bearing_results.rolling.InternalClearance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumOperatingInternalClearance")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def ring_force_and_displacement_results_inner(
        self: "Self",
    ) -> "_2276.RingForceAndDisplacement":
        """mastapy.bearings.bearing_results.rolling.RingForceAndDisplacement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RingForceAndDisplacementResultsInner"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def ring_force_and_displacement_results_outer(
        self: "Self",
    ) -> "_2276.RingForceAndDisplacement":
        """mastapy.bearings.bearing_results.rolling.RingForceAndDisplacement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RingForceAndDisplacementResultsOuter"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def elements(self: "Self") -> "List[_2222.LoadedElement]":
        """List[mastapy.bearings.bearing_results.rolling.LoadedElement]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Elements")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def race_results(self: "Self") -> "List[_2240.LoadedRollingBearingRaceResults]":
        """List[mastapy.bearings.bearing_results.rolling.LoadedRollingBearingRaceResults]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RaceResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def ring_force_and_displacement_results(
        self: "Self",
    ) -> "List[_2276.RingForceAndDisplacement]":
        """List[mastapy.bearings.bearing_results.rolling.RingForceAndDisplacement]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RingForceAndDisplacementResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def subsurface_shear_stress_for_most_heavily_loaded_element_inner(
        self: "Self",
    ) -> "List[_2282.StressAtPosition]":
        """List[mastapy.bearings.bearing_results.rolling.StressAtPosition]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SubsurfaceShearStressForMostHeavilyLoadedElementInner"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def subsurface_shear_stress_for_most_heavily_loaded_element_outer(
        self: "Self",
    ) -> "List[_2282.StressAtPosition]":
        """List[mastapy.bearings.bearing_results.rolling.StressAtPosition]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SubsurfaceShearStressForMostHeavilyLoadedElementOuter"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def subsurface_von_mises_stress_for_most_heavily_loaded_element_inner(
        self: "Self",
    ) -> "List[_2282.StressAtPosition]":
        """List[mastapy.bearings.bearing_results.rolling.StressAtPosition]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SubsurfaceVonMisesStressForMostHeavilyLoadedElementInner"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def subsurface_von_mises_stress_for_most_heavily_loaded_element_outer(
        self: "Self",
    ) -> "List[_2282.StressAtPosition]":
        """List[mastapy.bearings.bearing_results.rolling.StressAtPosition]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SubsurfaceVonMisesStressForMostHeavilyLoadedElementOuter"
        )

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
    def cast_to(self: "Self") -> "_Cast_LoadedRollingBearingRow":
        """Cast to another type.

        Returns:
            _Cast_LoadedRollingBearingRow
        """
        return _Cast_LoadedRollingBearingRow(self)
