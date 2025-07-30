"""AcousticAnalysisOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_ACOUSTIC_ANALYSIS_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Acoustics", "AcousticAnalysisOptions"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.system_model.analyses_and_results.acoustic_analyses import (
        _7662,
        _7666,
        _7667,
        _7668,
        _7669,
    )

    Self = TypeVar("Self", bound="AcousticAnalysisOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="AcousticAnalysisOptions._Cast_AcousticAnalysisOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AcousticAnalysisOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AcousticAnalysisOptions:
    """Special nested class for casting AcousticAnalysisOptions to subclasses."""

    __parent__: "AcousticAnalysisOptions"

    @property
    def acoustic_analysis_options(self: "CastSelf") -> "AcousticAnalysisOptions":
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
class AcousticAnalysisOptions(_0.APIBase):
    """AcousticAnalysisOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ACOUSTIC_ANALYSIS_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def force_unit_velocity(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ForceUnitVelocity")

        if temp is None:
            return False

        return temp

    @force_unit_velocity.setter
    @exception_bridge
    @enforce_parameter_types
    def force_unit_velocity(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ForceUnitVelocity",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def frequency_threshold_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "FrequencyThresholdFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @frequency_threshold_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def frequency_threshold_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "FrequencyThresholdFactor", value)

    @property
    @exception_bridge
    def high_frequency_multiplier(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "HighFrequencyMultiplier")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @high_frequency_multiplier.setter
    @exception_bridge
    @enforce_parameter_types
    def high_frequency_multiplier(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "HighFrequencyMultiplier", value)

    @property
    @exception_bridge
    def initial_guess(self: "Self") -> "_7666.InitialGuessOption":
        """mastapy.system_model.analyses_and_results.acoustic_analyses.InitialGuessOption"""
        temp = pythonnet_property_get(self.wrapped, "InitialGuess")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.AcousticAnalyses.InitialGuessOption",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.acoustic_analyses._7666",
            "InitialGuessOption",
        )(value)

    @initial_guess.setter
    @exception_bridge
    @enforce_parameter_types
    def initial_guess(self: "Self", value: "_7666.InitialGuessOption") -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.AcousticAnalyses.InitialGuessOption",
        )
        pythonnet_property_set(self.wrapped, "InitialGuess", value)

    @property
    @exception_bridge
    def integration_order(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "IntegrationOrder")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @integration_order.setter
    @exception_bridge
    @enforce_parameter_types
    def integration_order(self: "Self", value: "Union[int, Tuple[int, bool]]") -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "IntegrationOrder", value)

    @property
    @exception_bridge
    def integration_order_moments(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "IntegrationOrderMoments")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @integration_order_moments.setter
    @exception_bridge
    @enforce_parameter_types
    def integration_order_moments(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "IntegrationOrderMoments", value)

    @property
    @exception_bridge
    def low_frequency_multiplier(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "LowFrequencyMultiplier")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @low_frequency_multiplier.setter
    @exception_bridge
    @enforce_parameter_types
    def low_frequency_multiplier(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "LowFrequencyMultiplier", value)

    @property
    @exception_bridge
    def m2l_cache_type(self: "Self") -> "_7667.M2LHfCacheType":
        """mastapy.system_model.analyses_and_results.acoustic_analyses.M2LHfCacheType"""
        temp = pythonnet_property_get(self.wrapped, "M2LCacheType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.AcousticAnalyses.M2LHfCacheType",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.acoustic_analyses._7667",
            "M2LHfCacheType",
        )(value)

    @m2l_cache_type.setter
    @exception_bridge
    @enforce_parameter_types
    def m2l_cache_type(self: "Self", value: "_7667.M2LHfCacheType") -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.AcousticAnalyses.M2LHfCacheType",
        )
        pythonnet_property_set(self.wrapped, "M2LCacheType", value)

    @property
    @exception_bridge
    def maximum_level(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "MaximumLevel")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @maximum_level.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_level(self: "Self", value: "Union[int, Tuple[int, bool]]") -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MaximumLevel", value)

    @property
    @exception_bridge
    def maximum_number_of_elements(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "MaximumNumberOfElements")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @maximum_number_of_elements.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_number_of_elements(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MaximumNumberOfElements", value)

    @property
    @exception_bridge
    def maximum_number_of_iterations(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "MaximumNumberOfIterations")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @maximum_number_of_iterations.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_number_of_iterations(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MaximumNumberOfIterations", value)

    @property
    @exception_bridge
    def near_field_integrals_cache_type(
        self: "Self",
    ) -> "_7668.NearFieldIntegralsCacheType":
        """mastapy.system_model.analyses_and_results.acoustic_analyses.NearFieldIntegralsCacheType"""
        temp = pythonnet_property_get(self.wrapped, "NearFieldIntegralsCacheType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.AcousticAnalyses.NearFieldIntegralsCacheType",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.acoustic_analyses._7668",
            "NearFieldIntegralsCacheType",
        )(value)

    @near_field_integrals_cache_type.setter
    @exception_bridge
    @enforce_parameter_types
    def near_field_integrals_cache_type(
        self: "Self", value: "_7668.NearFieldIntegralsCacheType"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.AcousticAnalyses.NearFieldIntegralsCacheType",
        )
        pythonnet_property_set(self.wrapped, "NearFieldIntegralsCacheType", value)

    @property
    @exception_bridge
    def octree_creation_method(self: "Self") -> "_7669.OctreeCreationMethod":
        """mastapy.system_model.analyses_and_results.acoustic_analyses.OctreeCreationMethod"""
        temp = pythonnet_property_get(self.wrapped, "OctreeCreationMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.AcousticAnalyses.OctreeCreationMethod",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.acoustic_analyses._7669",
            "OctreeCreationMethod",
        )(value)

    @octree_creation_method.setter
    @exception_bridge
    @enforce_parameter_types
    def octree_creation_method(
        self: "Self", value: "_7669.OctreeCreationMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.AcousticAnalyses.OctreeCreationMethod",
        )
        pythonnet_property_set(self.wrapped, "OctreeCreationMethod", value)

    @property
    @exception_bridge
    def optimise_maximum_number_of_elements(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "OptimiseMaximumNumberOfElements")

        if temp is None:
            return False

        return temp

    @optimise_maximum_number_of_elements.setter
    @exception_bridge
    @enforce_parameter_types
    def optimise_maximum_number_of_elements(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OptimiseMaximumNumberOfElements",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def perform_iterative_solver_logging(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "PerformIterativeSolverLogging")

        if temp is None:
            return False

        return temp

    @perform_iterative_solver_logging.setter
    @exception_bridge
    @enforce_parameter_types
    def perform_iterative_solver_logging(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PerformIterativeSolverLogging",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def preconditioner(self: "Self") -> "_7662.AcousticPreconditionerType":
        """mastapy.system_model.analyses_and_results.acoustic_analyses.AcousticPreconditionerType"""
        temp = pythonnet_property_get(self.wrapped, "Preconditioner")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.AcousticAnalyses.AcousticPreconditionerType",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.acoustic_analyses._7662",
            "AcousticPreconditionerType",
        )(value)

    @preconditioner.setter
    @exception_bridge
    @enforce_parameter_types
    def preconditioner(self: "Self", value: "_7662.AcousticPreconditionerType") -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.AcousticAnalyses.AcousticPreconditionerType",
        )
        pythonnet_property_set(self.wrapped, "Preconditioner", value)

    @property
    @exception_bridge
    def show_advanced_solver_settings(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowAdvancedSolverSettings")

        if temp is None:
            return False

        return temp

    @show_advanced_solver_settings.setter
    @exception_bridge
    @enforce_parameter_types
    def show_advanced_solver_settings(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowAdvancedSolverSettings",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def solver_relative_tolerance(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "SolverRelativeTolerance")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @solver_relative_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def solver_relative_tolerance(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "SolverRelativeTolerance", value)

    @property
    @exception_bridge
    def use_residuals_scaling(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseResidualsScaling")

        if temp is None:
            return False

        return temp

    @use_residuals_scaling.setter
    @exception_bridge
    @enforce_parameter_types
    def use_residuals_scaling(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseResidualsScaling",
            bool(value) if value is not None else False,
        )

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
    def cast_to(self: "Self") -> "_Cast_AcousticAnalysisOptions":
        """Cast to another type.

        Returns:
            _Cast_AcousticAnalysisOptions
        """
        return _Cast_AcousticAnalysisOptions(self)
