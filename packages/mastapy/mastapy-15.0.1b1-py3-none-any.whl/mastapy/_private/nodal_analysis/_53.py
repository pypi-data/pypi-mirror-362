"""AnalysisSettingsItem"""

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
from mastapy._private.utility.databases import _2028

_ANALYSIS_SETTINGS_ITEM = python_net_import(
    "SMT.MastaAPI.NodalAnalysis", "AnalysisSettingsItem"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.nodal_analysis import _87, _88

    Self = TypeVar("Self", bound="AnalysisSettingsItem")
    CastSelf = TypeVar(
        "CastSelf", bound="AnalysisSettingsItem._Cast_AnalysisSettingsItem"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AnalysisSettingsItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AnalysisSettingsItem:
    """Special nested class for casting AnalysisSettingsItem to subclasses."""

    __parent__: "AnalysisSettingsItem"

    @property
    def named_database_item(self: "CastSelf") -> "_2028.NamedDatabaseItem":
        return self.__parent__._cast(_2028.NamedDatabaseItem)

    @property
    def analysis_settings_item(self: "CastSelf") -> "AnalysisSettingsItem":
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
class AnalysisSettingsItem(_2028.NamedDatabaseItem):
    """AnalysisSettingsItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ANALYSIS_SETTINGS_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def eigenvalue_tolerance(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "EigenvalueTolerance")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @eigenvalue_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def eigenvalue_tolerance(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "EigenvalueTolerance", value)

    @property
    @exception_bridge
    def gear_mesh_nodes_per_unit_length_to_diameter_ratio(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "GearMeshNodesPerUnitLengthToDiameterRatio"
        )

        if temp is None:
            return 0.0

        return temp

    @gear_mesh_nodes_per_unit_length_to_diameter_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def gear_mesh_nodes_per_unit_length_to_diameter_ratio(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "GearMeshNodesPerUnitLengthToDiameterRatio",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def log_steps(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "LogSteps")

        if temp is None:
            return False

        return temp

    @log_steps.setter
    @exception_bridge
    @enforce_parameter_types
    def log_steps(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "LogSteps", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def maximum_nodes_for_nvh_analysis(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "MaximumNodesForNVHAnalysis")

        if temp is None:
            return 0

        return temp

    @maximum_nodes_for_nvh_analysis.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_nodes_for_nvh_analysis(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumNodesForNVHAnalysis",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def maximum_section_length_to_diameter_ratio(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumSectionLengthToDiameterRatio"
        )

        if temp is None:
            return 0.0

        return temp

    @maximum_section_length_to_diameter_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_section_length_to_diameter_ratio(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumSectionLengthToDiameterRatio",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def minimum_number_of_gear_mesh_nodes(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "MinimumNumberOfGearMeshNodes")

        if temp is None:
            return 0

        return temp

    @minimum_number_of_gear_mesh_nodes.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_number_of_gear_mesh_nodes(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumNumberOfGearMeshNodes",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def mode_shape_tolerance(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ModeShapeTolerance")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @mode_shape_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def mode_shape_tolerance(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ModeShapeTolerance", value)

    @property
    @exception_bridge
    def overwrite_advanced_system_deflection_load_cases_created_for_harmonic_excitations(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped,
            "OverwriteAdvancedSystemDeflectionLoadCasesCreatedForHarmonicExcitations",
        )

        if temp is None:
            return False

        return temp

    @overwrite_advanced_system_deflection_load_cases_created_for_harmonic_excitations.setter
    @exception_bridge
    @enforce_parameter_types
    def overwrite_advanced_system_deflection_load_cases_created_for_harmonic_excitations(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "OverwriteAdvancedSystemDeflectionLoadCasesCreatedForHarmonicExcitations",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def rating_type_for_bearing_reliability(
        self: "Self",
    ) -> "_87.RatingTypeForBearingReliability":
        """mastapy.nodal_analysis.RatingTypeForBearingReliability"""
        temp = pythonnet_property_get(self.wrapped, "RatingTypeForBearingReliability")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.NodalAnalysis.RatingTypeForBearingReliability"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.nodal_analysis._87", "RatingTypeForBearingReliability"
        )(value)

    @rating_type_for_bearing_reliability.setter
    @exception_bridge
    @enforce_parameter_types
    def rating_type_for_bearing_reliability(
        self: "Self", value: "_87.RatingTypeForBearingReliability"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.NodalAnalysis.RatingTypeForBearingReliability"
        )
        pythonnet_property_set(self.wrapped, "RatingTypeForBearingReliability", value)

    @property
    @exception_bridge
    def rating_type_for_shaft_reliability(
        self: "Self",
    ) -> "_88.RatingTypeForShaftReliability":
        """mastapy.nodal_analysis.RatingTypeForShaftReliability"""
        temp = pythonnet_property_get(self.wrapped, "RatingTypeForShaftReliability")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.NodalAnalysis.RatingTypeForShaftReliability"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.nodal_analysis._88", "RatingTypeForShaftReliability"
        )(value)

    @rating_type_for_shaft_reliability.setter
    @exception_bridge
    @enforce_parameter_types
    def rating_type_for_shaft_reliability(
        self: "Self", value: "_88.RatingTypeForShaftReliability"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.NodalAnalysis.RatingTypeForShaftReliability"
        )
        pythonnet_property_set(self.wrapped, "RatingTypeForShaftReliability", value)

    @property
    @exception_bridge
    def remove_rigid_body_rotation_theta_z_twist_from_shaft_reporting(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "RemoveRigidBodyRotationThetaZTwistFromShaftReporting"
        )

        if temp is None:
            return False

        return temp

    @remove_rigid_body_rotation_theta_z_twist_from_shaft_reporting.setter
    @exception_bridge
    @enforce_parameter_types
    def remove_rigid_body_rotation_theta_z_twist_from_shaft_reporting(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "RemoveRigidBodyRotationThetaZTwistFromShaftReporting",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def spline_nodes_per_unit_length_to_diameter_ratio(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "SplineNodesPerUnitLengthToDiameterRatio"
        )

        if temp is None:
            return 0.0

        return temp

    @spline_nodes_per_unit_length_to_diameter_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def spline_nodes_per_unit_length_to_diameter_ratio(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "SplineNodesPerUnitLengthToDiameterRatio",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def system_deflection_maximum_iterations(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionMaximumIterations")

        if temp is None:
            return 0

        return temp

    @system_deflection_maximum_iterations.setter
    @exception_bridge
    @enforce_parameter_types
    def system_deflection_maximum_iterations(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SystemDeflectionMaximumIterations",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def use_mean_load_and_load_sharing_factor_for_planet_bearing_reliability(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseMeanLoadAndLoadSharingFactorForPlanetBearingReliability"
        )

        if temp is None:
            return False

        return temp

    @use_mean_load_and_load_sharing_factor_for_planet_bearing_reliability.setter
    @exception_bridge
    @enforce_parameter_types
    def use_mean_load_and_load_sharing_factor_for_planet_bearing_reliability(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseMeanLoadAndLoadSharingFactorForPlanetBearingReliability",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_single_node_for_cylindrical_gear_meshes(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseSingleNodeForCylindricalGearMeshes"
        )

        if temp is None:
            return False

        return temp

    @use_single_node_for_cylindrical_gear_meshes.setter
    @exception_bridge
    @enforce_parameter_types
    def use_single_node_for_cylindrical_gear_meshes(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseSingleNodeForCylindricalGearMeshes",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_single_node_for_spline_connections(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseSingleNodeForSplineConnections")

        if temp is None:
            return False

        return temp

    @use_single_node_for_spline_connections.setter
    @exception_bridge
    @enforce_parameter_types
    def use_single_node_for_spline_connections(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseSingleNodeForSplineConnections",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_AnalysisSettingsItem":
        """Cast to another type.

        Returns:
            _Cast_AnalysisSettingsItem
        """
        return _Cast_AnalysisSettingsItem(self)
