"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter

if TYPE_CHECKING:
    from .active_process_method import EnumWithSelectedValue_ActiveProcessMethod
    from .agma_gleason_conical_gear_geometry_methods import (
        EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods,
    )
    from .alignment_axis import EnumWithSelectedValue_AlignmentAxis
    from .analysis_type import EnumWithSelectedValue_AnalysisType
    from .axis import EnumWithSelectedValue_Axis
    from .ball_bearing_analysis_method import (
        EnumWithSelectedValue_BallBearingAnalysisMethod,
    )
    from .bar_model_export_type import EnumWithSelectedValue_BarModelExportType
    from .basic_curve_types import EnumWithSelectedValue_BasicCurveTypes
    from .basic_dynamic_load_rating_calculation_method import (
        EnumWithSelectedValue_BasicDynamicLoadRatingCalculationMethod,
    )
    from .basic_static_load_rating_calculation_method import (
        EnumWithSelectedValue_BasicStaticLoadRatingCalculationMethod,
    )
    from .bearing_efficiency_rating_method import (
        EnumWithSelectedValue_BearingEfficiencyRatingMethod,
    )
    from .bearing_model import EnumWithSelectedValue_BearingModel
    from .bearing_node_option import EnumWithSelectedValue_BearingNodeOption
    from .bearing_stiffness_model import EnumWithSelectedValue_BearingStiffnessModel
    from .bearing_tolerance_class import EnumWithSelectedValue_BearingToleranceClass
    from .bearing_tolerance_definition_options import (
        EnumWithSelectedValue_BearingToleranceDefinitionOptions,
    )
    from .boundary_condition_type import EnumWithSelectedValue_BoundaryConditionType
    from .cad_page_orientation import EnumWithSelectedValue_CadPageOrientation
    from .candidate_display_choice import EnumWithSelectedValue_CandidateDisplayChoice
    from .chart_type import EnumWithSelectedValue_ChartType
    from .coefficient_of_friction_calculation_method import (
        EnumWithSelectedValue_CoefficientOfFrictionCalculationMethod,
    )
    from .coil_position_in_slot import EnumWithSelectedValue_CoilPositionInSlot
    from .complex_number_output import (
        EnumWithSelectedValue_HarmonicAnalysisFEExportOptions_ComplexNumberOutput,
    )
    from .complex_part_display_option import (
        EnumWithSelectedValue_ComplexPartDisplayOption,
    )
    from .component_orientation_option import (
        EnumWithSelectedValue_ComponentOrientationOption,
    )
    from .conical_machine_setting_calculation_methods import (
        EnumWithSelectedValue_ConicalMachineSettingCalculationMethods,
    )
    from .conical_manufacture_methods import (
        EnumWithSelectedValue_ConicalManufactureMethods,
    )
    from .contact_result_type import EnumWithSelectedValue_ContactResultType
    from .cutter_flank_sections import EnumWithSelectedValue_CutterFlankSections
    from .cylindrical_gear_rating_methods import (
        EnumWithSelectedValue_CylindricalGearRatingMethods,
    )
    from .cylindrical_mft_finishing_methods import (
        EnumWithSelectedValue_CylindricalMftFinishingMethods,
    )
    from .cylindrical_mft_roughing_methods import (
        EnumWithSelectedValue_CylindricalMftRoughingMethods,
    )
    from .damping_specification import EnumWithSelectedValue_DampingSpecification
    from .degree_of_freedom import EnumWithSelectedValue_DegreeOfFreedom
    from .derived_parameter_option import (
        EnumWithSelectedValue_CylindricalGearPairCreationOptions_DerivedParameterOption,
    )
    from .design_entity_id import EnumWithSelectedValue_DesignEntityId
    from .destination_design_state import EnumWithSelectedValue_DestinationDesignState
    from .doe_value_specification_option import (
        EnumWithSelectedValue_DoeValueSpecificationOption,
    )
    from .dudley_effective_length_approximation_option import (
        EnumWithSelectedValue_DudleyEffectiveLengthApproximationOption,
    )
    from .dxf_version_with_name import EnumWithSelectedValue_DxfVersionWithName
    from .dynamics_response_3d_chart_type import (
        EnumWithSelectedValue_DynamicsResponse3DChartType,
    )
    from .dynamics_response_scaling import EnumWithSelectedValue_DynamicsResponseScaling
    from .dynamics_response_type import EnumWithSelectedValue_DynamicsResponseType
    from .electric_machine_analysis_period import (
        EnumWithSelectedValue_ElectricMachineAnalysisPeriod,
    )
    from .elmer_result_type import EnumWithSelectedValue_ElmerResultType
    from .end_winding_cooling_flow_source import (
        EnumWithSelectedValue_EndWindingCoolingFlowSource,
    )
    from .excitation_analysis_view_option import (
        EnumWithSelectedValue_ExcitationAnalysisViewOption,
    )
    from .export_output_type import EnumWithSelectedValue_ExportOutputType
    from .extrapolation_options import EnumWithSelectedValue_ExtrapolationOptions
    from .fatigue_load_limit_calculation_method_enum import (
        EnumWithSelectedValue_FatigueLoadLimitCalculationMethodEnum,
    )
    from .fe_export_format import EnumWithSelectedValue_FEExportFormat
    from .fe_substructure_type import EnumWithSelectedValue_FESubstructureType
    from .fe_substructuring_file_format import (
        EnumWithSelectedValue_FESubstructuringFileFormat,
    )
    from .flank import EnumWithSelectedValue_Flank
    from .fluid_film_temperature_options import (
        EnumWithSelectedValue_FluidFilmTemperatureOptions,
    )
    from .force_display_option import EnumWithSelectedValue_ForceDisplayOption
    from .force_specification import (
        EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification,
    )
    from .friction_model_for_gyroscopic_moment import (
        EnumWithSelectedValue_FrictionModelForGyroscopicMoment,
    )
    from .gear_mesh_efficiency_rating_method import (
        EnumWithSelectedValue_GearMeshEfficiencyRatingMethod,
    )
    from .gear_mesh_stiffness_model import EnumWithSelectedValue_GearMeshStiffnessModel
    from .gear_windage_and_churning_loss_calculation_method import (
        EnumWithSelectedValue_GearWindageAndChurningLossCalculationMethod,
    )
    from .geometry_specification_type import (
        EnumWithSelectedValue_GeometrySpecificationType,
    )
    from .harmonic_analysis_torque_input_type import (
        EnumWithSelectedValue_HarmonicAnalysisTorqueInputType,
    )
    from .harmonic_excitation_type import EnumWithSelectedValue_HarmonicExcitationType
    from .harmonic_load_data_type import EnumWithSelectedValue_HarmonicLoadDataType
    from .hertzian_contact_deflection_calculation_method import (
        EnumWithSelectedValue_HertzianContactDeflectionCalculationMethod,
    )
    from .integration_method import EnumWithSelectedValue_IntegrationMethod
    from .internal_clearance_class import EnumWithSelectedValue_InternalClearanceClass
    from .it_designation import EnumWithSelectedValue_ITDesignation
    from .link_node_source import EnumWithSelectedValue_LinkNodeSource
    from .load_case_override_option import EnumWithSelectedValue_LoadCaseOverrideOption
    from .load_case_type import EnumWithSelectedValue_LoadCaseType
    from .load_distribution_factor_methods import (
        EnumWithSelectedValue_LoadDistributionFactorMethods,
    )
    from .loaded_ball_element_property_type import (
        EnumWithSelectedValue_LoadedBallElementPropertyType,
    )
    from .location_of_evaluation_lower_limit import (
        EnumWithSelectedValue_LocationOfEvaluationLowerLimit,
    )
    from .location_of_evaluation_upper_limit import (
        EnumWithSelectedValue_LocationOfEvaluationUpperLimit,
    )
    from .location_of_root_relief_evaluation import (
        EnumWithSelectedValue_LocationOfRootReliefEvaluation,
    )
    from .location_of_tip_relief_evaluation import (
        EnumWithSelectedValue_LocationOfTipReliefEvaluation,
    )
    from .lubricant_definition import EnumWithSelectedValue_LubricantDefinition
    from .lubricant_viscosity_class_iso import (
        EnumWithSelectedValue_LubricantViscosityClassISO,
    )
    from .lubrication_methods import EnumWithSelectedValue_LubricationMethods
    from .material_property_class import EnumWithSelectedValue_MaterialPropertyClass
    from .mesh_stiffness_model import EnumWithSelectedValue_MeshStiffnessModel
    from .micro_geometry_definition_method import (
        EnumWithSelectedValue_MicroGeometryDefinitionMethod,
    )
    from .micro_geometry_definition_type import (
        EnumWithSelectedValue_MicroGeometryDefinitionType,
    )
    from .micro_geometry_model import EnumWithSelectedValue_MicroGeometryModel
    from .micropitting_coefficient_of_friction_calculation_method import (
        EnumWithSelectedValue_MicropittingCoefficientOfFrictionCalculationMethod,
    )
    from .modal_correction_method import EnumWithSelectedValue_ModalCorrectionMethod
    from .mode_input_type import EnumWithSelectedValue_ModeInputType
    from .modules import EnumWithSelectedValue_Modules
    from .oil_seal_loss_calculation_method import (
        EnumWithSelectedValue_OilSealLossCalculationMethod,
    )
    from .power_load_input_torque_specification_method import (
        EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod,
    )
    from .power_load_type import EnumWithSelectedValue_PowerLoadType
    from .preload_type import EnumWithSelectedValue_PreloadType
    from .pressure_angle_types import EnumWithSelectedValue_PressureAngleTypes
    from .pro_solve_mpc_type import EnumWithSelectedValue_ProSolveMpcType
    from .pro_solve_solver_type import EnumWithSelectedValue_ProSolveSolverType
    from .profile_tooth_drawing_method import (
        EnumWithSelectedValue_ProfileToothDrawingMethod,
    )
    from .property_specification_method import (
        EnumWithSelectedValue_PropertySpecificationMethod,
    )
    from .race_axial_mounting_type import EnumWithSelectedValue_RaceAxialMountingType
    from .race_radial_mounting_type import EnumWithSelectedValue_RaceRadialMountingType
    from .residual_stress_calculation_method import (
        EnumWithSelectedValue_ResidualStressCalculationMethod,
    )
    from .result_options_for_3d_vector import (
        EnumWithSelectedValue_ResultOptionsFor3DVector,
    )
    from .rigid_connector_stiffness_type import (
        EnumWithSelectedValue_RigidConnectorStiffnessType,
    )
    from .rigid_connector_tooth_spacing_type import (
        EnumWithSelectedValue_RigidConnectorToothSpacingType,
    )
    from .rigid_connector_types import EnumWithSelectedValue_RigidConnectorTypes
    from .roller_bearing_profile_types import (
        EnumWithSelectedValue_RollerBearingProfileTypes,
    )
    from .rolling_bearing_arrangement import (
        EnumWithSelectedValue_RollingBearingArrangement,
    )
    from .rolling_bearing_race_type import EnumWithSelectedValue_RollingBearingRaceType
    from .rotational_directions import EnumWithSelectedValue_RotationalDirections
    from .scuffing_coefficient_of_friction_methods import (
        EnumWithSelectedValue_ScuffingCoefficientOfFrictionMethods,
    )
    from .scuffing_flash_temperature_rating_method import (
        EnumWithSelectedValue_ScuffingFlashTemperatureRatingMethod,
    )
    from .scuffing_integral_temperature_rating_method import (
        EnumWithSelectedValue_ScuffingIntegralTemperatureRatingMethod,
    )
    from .severity import EnumWithSelectedValue_Severity
    from .shaft_and_housing_flexibility_option import (
        EnumWithSelectedValue_ShaftAndHousingFlexibilityOption,
    )
    from .shaft_diameter_modification_due_to_rolling_bearing_ring import (
        EnumWithSelectedValue_ShaftDiameterModificationDueToRollingBearingRing,
    )
    from .shaft_rating_method import EnumWithSelectedValue_ShaftRatingMethod
    from .shear_area_factor_method import EnumWithSelectedValue_ShearAreaFactorMethod
    from .single_point_selection_method import (
        EnumWithSelectedValue_SinglePointSelectionMethod,
    )
    from .specify_torque_or_current import EnumWithSelectedValue_SpecifyTorqueOrCurrent
    from .spline_fit_class_type import EnumWithSelectedValue_SplineFitClassType
    from .spline_rating_types import EnumWithSelectedValue_SplineRatingTypes
    from .spline_tolerance_class_types import (
        EnumWithSelectedValue_SplineToleranceClassTypes,
    )
    from .status_item_severity import EnumWithSelectedValue_StatusItemSeverity
    from .step_creation import (
        EnumWithSelectedValue_StiffnessOptionsForHarmonicAnalysis_StepCreation,
    )
    from .stress_concentration_method import (
        EnumWithSelectedValue_StressConcentrationMethod,
    )
    from .stress_results_type import EnumWithSelectedValue_StressResultsType
    from .support_tolerance_location_designation import (
        EnumWithSelectedValue_SupportToleranceLocationDesignation,
    )
    from .surface_finishes import EnumWithSelectedValue_SurfaceFinishes
    from .table_4_joint_interface_types import (
        EnumWithSelectedValue_Table4JointInterfaceTypes,
    )
    from .thermal_expansion_option import EnumWithSelectedValue_ThermalExpansionOption
    from .thickness_type import EnumWithSelectedValue_ThicknessType
    from .three_d_view_contour_option import (
        EnumWithSelectedValue_ThreeDViewContourOption,
    )
    from .three_d_view_contour_option_first_selection import (
        EnumWithSelectedValue_ThreeDViewContourOptionFirstSelection,
    )
    from .three_d_view_contour_option_second_selection import (
        EnumWithSelectedValue_ThreeDViewContourOptionSecondSelection,
    )
    from .tooth_thickness_specification_method import (
        EnumWithSelectedValue_ToothThicknessSpecificationMethod,
    )
    from .torque_converter_lockup_rule import (
        EnumWithSelectedValue_TorqueConverterLockupRule,
    )
    from .torque_ripple_input_type import EnumWithSelectedValue_TorqueRippleInputType
    from .torque_specification_for_system_deflection import (
        EnumWithSelectedValue_TorqueSpecificationForSystemDeflection,
    )
    from .value_input_option import EnumWithSelectedValue_ValueInputOption
else:
    import_structure = {
        "shaft_rating_method": ["EnumWithSelectedValue_ShaftRatingMethod"],
        "surface_finishes": ["EnumWithSelectedValue_SurfaceFinishes"],
        "integration_method": ["EnumWithSelectedValue_IntegrationMethod"],
        "value_input_option": ["EnumWithSelectedValue_ValueInputOption"],
        "single_point_selection_method": [
            "EnumWithSelectedValue_SinglePointSelectionMethod"
        ],
        "extrapolation_options": ["EnumWithSelectedValue_ExtrapolationOptions"],
        "property_specification_method": [
            "EnumWithSelectedValue_PropertySpecificationMethod"
        ],
        "result_options_for_3d_vector": [
            "EnumWithSelectedValue_ResultOptionsFor3DVector"
        ],
        "elmer_result_type": ["EnumWithSelectedValue_ElmerResultType"],
        "mode_input_type": ["EnumWithSelectedValue_ModeInputType"],
        "material_property_class": ["EnumWithSelectedValue_MaterialPropertyClass"],
        "lubricant_definition": ["EnumWithSelectedValue_LubricantDefinition"],
        "lubricant_viscosity_class_iso": [
            "EnumWithSelectedValue_LubricantViscosityClassISO"
        ],
        "micro_geometry_model": ["EnumWithSelectedValue_MicroGeometryModel"],
        "coefficient_of_friction_calculation_method": [
            "EnumWithSelectedValue_CoefficientOfFrictionCalculationMethod"
        ],
        "cylindrical_gear_rating_methods": [
            "EnumWithSelectedValue_CylindricalGearRatingMethods"
        ],
        "scuffing_flash_temperature_rating_method": [
            "EnumWithSelectedValue_ScuffingFlashTemperatureRatingMethod"
        ],
        "scuffing_integral_temperature_rating_method": [
            "EnumWithSelectedValue_ScuffingIntegralTemperatureRatingMethod"
        ],
        "location_of_evaluation_lower_limit": [
            "EnumWithSelectedValue_LocationOfEvaluationLowerLimit"
        ],
        "location_of_evaluation_upper_limit": [
            "EnumWithSelectedValue_LocationOfEvaluationUpperLimit"
        ],
        "location_of_root_relief_evaluation": [
            "EnumWithSelectedValue_LocationOfRootReliefEvaluation"
        ],
        "location_of_tip_relief_evaluation": [
            "EnumWithSelectedValue_LocationOfTipReliefEvaluation"
        ],
        "cylindrical_mft_finishing_methods": [
            "EnumWithSelectedValue_CylindricalMftFinishingMethods"
        ],
        "cylindrical_mft_roughing_methods": [
            "EnumWithSelectedValue_CylindricalMftRoughingMethods"
        ],
        "micro_geometry_definition_method": [
            "EnumWithSelectedValue_MicroGeometryDefinitionMethod"
        ],
        "micro_geometry_definition_type": [
            "EnumWithSelectedValue_MicroGeometryDefinitionType"
        ],
        "chart_type": ["EnumWithSelectedValue_ChartType"],
        "flank": ["EnumWithSelectedValue_Flank"],
        "active_process_method": ["EnumWithSelectedValue_ActiveProcessMethod"],
        "cutter_flank_sections": ["EnumWithSelectedValue_CutterFlankSections"],
        "basic_curve_types": ["EnumWithSelectedValue_BasicCurveTypes"],
        "thickness_type": ["EnumWithSelectedValue_ThicknessType"],
        "conical_machine_setting_calculation_methods": [
            "EnumWithSelectedValue_ConicalMachineSettingCalculationMethods"
        ],
        "conical_manufacture_methods": [
            "EnumWithSelectedValue_ConicalManufactureMethods"
        ],
        "contact_result_type": ["EnumWithSelectedValue_ContactResultType"],
        "candidate_display_choice": ["EnumWithSelectedValue_CandidateDisplayChoice"],
        "severity": ["EnumWithSelectedValue_Severity"],
        "geometry_specification_type": [
            "EnumWithSelectedValue_GeometrySpecificationType"
        ],
        "status_item_severity": ["EnumWithSelectedValue_StatusItemSeverity"],
        "lubrication_methods": ["EnumWithSelectedValue_LubricationMethods"],
        "gear_mesh_efficiency_rating_method": [
            "EnumWithSelectedValue_GearMeshEfficiencyRatingMethod"
        ],
        "micropitting_coefficient_of_friction_calculation_method": [
            "EnumWithSelectedValue_MicropittingCoefficientOfFrictionCalculationMethod"
        ],
        "scuffing_coefficient_of_friction_methods": [
            "EnumWithSelectedValue_ScuffingCoefficientOfFrictionMethods"
        ],
        "residual_stress_calculation_method": [
            "EnumWithSelectedValue_ResidualStressCalculationMethod"
        ],
        "stress_results_type": ["EnumWithSelectedValue_StressResultsType"],
        "derived_parameter_option": [
            "EnumWithSelectedValue_CylindricalGearPairCreationOptions_DerivedParameterOption"
        ],
        "tooth_thickness_specification_method": [
            "EnumWithSelectedValue_ToothThicknessSpecificationMethod"
        ],
        "load_distribution_factor_methods": [
            "EnumWithSelectedValue_LoadDistributionFactorMethods"
        ],
        "agma_gleason_conical_gear_geometry_methods": [
            "EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods"
        ],
        "pro_solve_mpc_type": ["EnumWithSelectedValue_ProSolveMpcType"],
        "pro_solve_solver_type": ["EnumWithSelectedValue_ProSolveSolverType"],
        "coil_position_in_slot": ["EnumWithSelectedValue_CoilPositionInSlot"],
        "end_winding_cooling_flow_source": [
            "EnumWithSelectedValue_EndWindingCoolingFlowSource"
        ],
        "electric_machine_analysis_period": [
            "EnumWithSelectedValue_ElectricMachineAnalysisPeriod"
        ],
        "specify_torque_or_current": ["EnumWithSelectedValue_SpecifyTorqueOrCurrent"],
        "load_case_type": ["EnumWithSelectedValue_LoadCaseType"],
        "harmonic_load_data_type": ["EnumWithSelectedValue_HarmonicLoadDataType"],
        "force_display_option": ["EnumWithSelectedValue_ForceDisplayOption"],
        "it_designation": ["EnumWithSelectedValue_ITDesignation"],
        "dudley_effective_length_approximation_option": [
            "EnumWithSelectedValue_DudleyEffectiveLengthApproximationOption"
        ],
        "spline_rating_types": ["EnumWithSelectedValue_SplineRatingTypes"],
        "modules": ["EnumWithSelectedValue_Modules"],
        "pressure_angle_types": ["EnumWithSelectedValue_PressureAngleTypes"],
        "spline_fit_class_type": ["EnumWithSelectedValue_SplineFitClassType"],
        "spline_tolerance_class_types": [
            "EnumWithSelectedValue_SplineToleranceClassTypes"
        ],
        "table_4_joint_interface_types": [
            "EnumWithSelectedValue_Table4JointInterfaceTypes"
        ],
        "dynamics_response_scaling": ["EnumWithSelectedValue_DynamicsResponseScaling"],
        "cad_page_orientation": ["EnumWithSelectedValue_CadPageOrientation"],
        "fluid_film_temperature_options": [
            "EnumWithSelectedValue_FluidFilmTemperatureOptions"
        ],
        "support_tolerance_location_designation": [
            "EnumWithSelectedValue_SupportToleranceLocationDesignation"
        ],
        "loaded_ball_element_property_type": [
            "EnumWithSelectedValue_LoadedBallElementPropertyType"
        ],
        "roller_bearing_profile_types": [
            "EnumWithSelectedValue_RollerBearingProfileTypes"
        ],
        "rolling_bearing_arrangement": [
            "EnumWithSelectedValue_RollingBearingArrangement"
        ],
        "basic_dynamic_load_rating_calculation_method": [
            "EnumWithSelectedValue_BasicDynamicLoadRatingCalculationMethod"
        ],
        "basic_static_load_rating_calculation_method": [
            "EnumWithSelectedValue_BasicStaticLoadRatingCalculationMethod"
        ],
        "fatigue_load_limit_calculation_method_enum": [
            "EnumWithSelectedValue_FatigueLoadLimitCalculationMethodEnum"
        ],
        "rolling_bearing_race_type": ["EnumWithSelectedValue_RollingBearingRaceType"],
        "rotational_directions": ["EnumWithSelectedValue_RotationalDirections"],
        "bearing_efficiency_rating_method": [
            "EnumWithSelectedValue_BearingEfficiencyRatingMethod"
        ],
        "shaft_diameter_modification_due_to_rolling_bearing_ring": [
            "EnumWithSelectedValue_ShaftDiameterModificationDueToRollingBearingRing"
        ],
        "gear_windage_and_churning_loss_calculation_method": [
            "EnumWithSelectedValue_GearWindageAndChurningLossCalculationMethod"
        ],
        "dynamics_response_type": ["EnumWithSelectedValue_DynamicsResponseType"],
        "excitation_analysis_view_option": [
            "EnumWithSelectedValue_ExcitationAnalysisViewOption"
        ],
        "three_d_view_contour_option_first_selection": [
            "EnumWithSelectedValue_ThreeDViewContourOptionFirstSelection"
        ],
        "three_d_view_contour_option_second_selection": [
            "EnumWithSelectedValue_ThreeDViewContourOptionSecondSelection"
        ],
        "component_orientation_option": [
            "EnumWithSelectedValue_ComponentOrientationOption"
        ],
        "axis": ["EnumWithSelectedValue_Axis"],
        "alignment_axis": ["EnumWithSelectedValue_AlignmentAxis"],
        "design_entity_id": ["EnumWithSelectedValue_DesignEntityId"],
        "thermal_expansion_option": ["EnumWithSelectedValue_ThermalExpansionOption"],
        "fe_substructure_type": ["EnumWithSelectedValue_FESubstructureType"],
        "fe_substructuring_file_format": [
            "EnumWithSelectedValue_FESubstructuringFileFormat"
        ],
        "three_d_view_contour_option": [
            "EnumWithSelectedValue_ThreeDViewContourOption"
        ],
        "boundary_condition_type": ["EnumWithSelectedValue_BoundaryConditionType"],
        "fe_export_format": ["EnumWithSelectedValue_FEExportFormat"],
        "bearing_node_option": ["EnumWithSelectedValue_BearingNodeOption"],
        "link_node_source": ["EnumWithSelectedValue_LinkNodeSource"],
        "bearing_tolerance_class": ["EnumWithSelectedValue_BearingToleranceClass"],
        "bearing_model": ["EnumWithSelectedValue_BearingModel"],
        "preload_type": ["EnumWithSelectedValue_PreloadType"],
        "race_axial_mounting_type": ["EnumWithSelectedValue_RaceAxialMountingType"],
        "race_radial_mounting_type": ["EnumWithSelectedValue_RaceRadialMountingType"],
        "internal_clearance_class": ["EnumWithSelectedValue_InternalClearanceClass"],
        "bearing_tolerance_definition_options": [
            "EnumWithSelectedValue_BearingToleranceDefinitionOptions"
        ],
        "oil_seal_loss_calculation_method": [
            "EnumWithSelectedValue_OilSealLossCalculationMethod"
        ],
        "dxf_version_with_name": ["EnumWithSelectedValue_DxfVersionWithName"],
        "profile_tooth_drawing_method": [
            "EnumWithSelectedValue_ProfileToothDrawingMethod"
        ],
        "power_load_type": ["EnumWithSelectedValue_PowerLoadType"],
        "rigid_connector_stiffness_type": [
            "EnumWithSelectedValue_RigidConnectorStiffnessType"
        ],
        "rigid_connector_tooth_spacing_type": [
            "EnumWithSelectedValue_RigidConnectorToothSpacingType"
        ],
        "rigid_connector_types": ["EnumWithSelectedValue_RigidConnectorTypes"],
        "doe_value_specification_option": [
            "EnumWithSelectedValue_DoeValueSpecificationOption"
        ],
        "analysis_type": ["EnumWithSelectedValue_AnalysisType"],
        "bar_model_export_type": ["EnumWithSelectedValue_BarModelExportType"],
        "dynamics_response_3d_chart_type": [
            "EnumWithSelectedValue_DynamicsResponse3DChartType"
        ],
        "complex_part_display_option": [
            "EnumWithSelectedValue_ComplexPartDisplayOption"
        ],
        "bearing_stiffness_model": ["EnumWithSelectedValue_BearingStiffnessModel"],
        "gear_mesh_stiffness_model": ["EnumWithSelectedValue_GearMeshStiffnessModel"],
        "shaft_and_housing_flexibility_option": [
            "EnumWithSelectedValue_ShaftAndHousingFlexibilityOption"
        ],
        "export_output_type": ["EnumWithSelectedValue_ExportOutputType"],
        "complex_number_output": [
            "EnumWithSelectedValue_HarmonicAnalysisFEExportOptions_ComplexNumberOutput"
        ],
        "damping_specification": ["EnumWithSelectedValue_DampingSpecification"],
        "modal_correction_method": ["EnumWithSelectedValue_ModalCorrectionMethod"],
        "step_creation": [
            "EnumWithSelectedValue_StiffnessOptionsForHarmonicAnalysis_StepCreation"
        ],
        "harmonic_analysis_torque_input_type": [
            "EnumWithSelectedValue_HarmonicAnalysisTorqueInputType"
        ],
        "friction_model_for_gyroscopic_moment": [
            "EnumWithSelectedValue_FrictionModelForGyroscopicMoment"
        ],
        "mesh_stiffness_model": ["EnumWithSelectedValue_MeshStiffnessModel"],
        "shear_area_factor_method": ["EnumWithSelectedValue_ShearAreaFactorMethod"],
        "stress_concentration_method": [
            "EnumWithSelectedValue_StressConcentrationMethod"
        ],
        "ball_bearing_analysis_method": [
            "EnumWithSelectedValue_BallBearingAnalysisMethod"
        ],
        "hertzian_contact_deflection_calculation_method": [
            "EnumWithSelectedValue_HertzianContactDeflectionCalculationMethod"
        ],
        "load_case_override_option": ["EnumWithSelectedValue_LoadCaseOverrideOption"],
        "torque_ripple_input_type": ["EnumWithSelectedValue_TorqueRippleInputType"],
        "harmonic_excitation_type": ["EnumWithSelectedValue_HarmonicExcitationType"],
        "force_specification": [
            "EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification"
        ],
        "torque_specification_for_system_deflection": [
            "EnumWithSelectedValue_TorqueSpecificationForSystemDeflection"
        ],
        "power_load_input_torque_specification_method": [
            "EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod"
        ],
        "torque_converter_lockup_rule": [
            "EnumWithSelectedValue_TorqueConverterLockupRule"
        ],
        "degree_of_freedom": ["EnumWithSelectedValue_DegreeOfFreedom"],
        "destination_design_state": ["EnumWithSelectedValue_DestinationDesignState"],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "EnumWithSelectedValue_ShaftRatingMethod",
    "EnumWithSelectedValue_SurfaceFinishes",
    "EnumWithSelectedValue_IntegrationMethod",
    "EnumWithSelectedValue_ValueInputOption",
    "EnumWithSelectedValue_SinglePointSelectionMethod",
    "EnumWithSelectedValue_ExtrapolationOptions",
    "EnumWithSelectedValue_PropertySpecificationMethod",
    "EnumWithSelectedValue_ResultOptionsFor3DVector",
    "EnumWithSelectedValue_ElmerResultType",
    "EnumWithSelectedValue_ModeInputType",
    "EnumWithSelectedValue_MaterialPropertyClass",
    "EnumWithSelectedValue_LubricantDefinition",
    "EnumWithSelectedValue_LubricantViscosityClassISO",
    "EnumWithSelectedValue_MicroGeometryModel",
    "EnumWithSelectedValue_CoefficientOfFrictionCalculationMethod",
    "EnumWithSelectedValue_CylindricalGearRatingMethods",
    "EnumWithSelectedValue_ScuffingFlashTemperatureRatingMethod",
    "EnumWithSelectedValue_ScuffingIntegralTemperatureRatingMethod",
    "EnumWithSelectedValue_LocationOfEvaluationLowerLimit",
    "EnumWithSelectedValue_LocationOfEvaluationUpperLimit",
    "EnumWithSelectedValue_LocationOfRootReliefEvaluation",
    "EnumWithSelectedValue_LocationOfTipReliefEvaluation",
    "EnumWithSelectedValue_CylindricalMftFinishingMethods",
    "EnumWithSelectedValue_CylindricalMftRoughingMethods",
    "EnumWithSelectedValue_MicroGeometryDefinitionMethod",
    "EnumWithSelectedValue_MicroGeometryDefinitionType",
    "EnumWithSelectedValue_ChartType",
    "EnumWithSelectedValue_Flank",
    "EnumWithSelectedValue_ActiveProcessMethod",
    "EnumWithSelectedValue_CutterFlankSections",
    "EnumWithSelectedValue_BasicCurveTypes",
    "EnumWithSelectedValue_ThicknessType",
    "EnumWithSelectedValue_ConicalMachineSettingCalculationMethods",
    "EnumWithSelectedValue_ConicalManufactureMethods",
    "EnumWithSelectedValue_ContactResultType",
    "EnumWithSelectedValue_CandidateDisplayChoice",
    "EnumWithSelectedValue_Severity",
    "EnumWithSelectedValue_GeometrySpecificationType",
    "EnumWithSelectedValue_StatusItemSeverity",
    "EnumWithSelectedValue_LubricationMethods",
    "EnumWithSelectedValue_GearMeshEfficiencyRatingMethod",
    "EnumWithSelectedValue_MicropittingCoefficientOfFrictionCalculationMethod",
    "EnumWithSelectedValue_ScuffingCoefficientOfFrictionMethods",
    "EnumWithSelectedValue_ResidualStressCalculationMethod",
    "EnumWithSelectedValue_StressResultsType",
    "EnumWithSelectedValue_CylindricalGearPairCreationOptions_DerivedParameterOption",
    "EnumWithSelectedValue_ToothThicknessSpecificationMethod",
    "EnumWithSelectedValue_LoadDistributionFactorMethods",
    "EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods",
    "EnumWithSelectedValue_ProSolveMpcType",
    "EnumWithSelectedValue_ProSolveSolverType",
    "EnumWithSelectedValue_CoilPositionInSlot",
    "EnumWithSelectedValue_EndWindingCoolingFlowSource",
    "EnumWithSelectedValue_ElectricMachineAnalysisPeriod",
    "EnumWithSelectedValue_SpecifyTorqueOrCurrent",
    "EnumWithSelectedValue_LoadCaseType",
    "EnumWithSelectedValue_HarmonicLoadDataType",
    "EnumWithSelectedValue_ForceDisplayOption",
    "EnumWithSelectedValue_ITDesignation",
    "EnumWithSelectedValue_DudleyEffectiveLengthApproximationOption",
    "EnumWithSelectedValue_SplineRatingTypes",
    "EnumWithSelectedValue_Modules",
    "EnumWithSelectedValue_PressureAngleTypes",
    "EnumWithSelectedValue_SplineFitClassType",
    "EnumWithSelectedValue_SplineToleranceClassTypes",
    "EnumWithSelectedValue_Table4JointInterfaceTypes",
    "EnumWithSelectedValue_DynamicsResponseScaling",
    "EnumWithSelectedValue_CadPageOrientation",
    "EnumWithSelectedValue_FluidFilmTemperatureOptions",
    "EnumWithSelectedValue_SupportToleranceLocationDesignation",
    "EnumWithSelectedValue_LoadedBallElementPropertyType",
    "EnumWithSelectedValue_RollerBearingProfileTypes",
    "EnumWithSelectedValue_RollingBearingArrangement",
    "EnumWithSelectedValue_BasicDynamicLoadRatingCalculationMethod",
    "EnumWithSelectedValue_BasicStaticLoadRatingCalculationMethod",
    "EnumWithSelectedValue_FatigueLoadLimitCalculationMethodEnum",
    "EnumWithSelectedValue_RollingBearingRaceType",
    "EnumWithSelectedValue_RotationalDirections",
    "EnumWithSelectedValue_BearingEfficiencyRatingMethod",
    "EnumWithSelectedValue_ShaftDiameterModificationDueToRollingBearingRing",
    "EnumWithSelectedValue_GearWindageAndChurningLossCalculationMethod",
    "EnumWithSelectedValue_DynamicsResponseType",
    "EnumWithSelectedValue_ExcitationAnalysisViewOption",
    "EnumWithSelectedValue_ThreeDViewContourOptionFirstSelection",
    "EnumWithSelectedValue_ThreeDViewContourOptionSecondSelection",
    "EnumWithSelectedValue_ComponentOrientationOption",
    "EnumWithSelectedValue_Axis",
    "EnumWithSelectedValue_AlignmentAxis",
    "EnumWithSelectedValue_DesignEntityId",
    "EnumWithSelectedValue_ThermalExpansionOption",
    "EnumWithSelectedValue_FESubstructureType",
    "EnumWithSelectedValue_FESubstructuringFileFormat",
    "EnumWithSelectedValue_ThreeDViewContourOption",
    "EnumWithSelectedValue_BoundaryConditionType",
    "EnumWithSelectedValue_FEExportFormat",
    "EnumWithSelectedValue_BearingNodeOption",
    "EnumWithSelectedValue_LinkNodeSource",
    "EnumWithSelectedValue_BearingToleranceClass",
    "EnumWithSelectedValue_BearingModel",
    "EnumWithSelectedValue_PreloadType",
    "EnumWithSelectedValue_RaceAxialMountingType",
    "EnumWithSelectedValue_RaceRadialMountingType",
    "EnumWithSelectedValue_InternalClearanceClass",
    "EnumWithSelectedValue_BearingToleranceDefinitionOptions",
    "EnumWithSelectedValue_OilSealLossCalculationMethod",
    "EnumWithSelectedValue_DxfVersionWithName",
    "EnumWithSelectedValue_ProfileToothDrawingMethod",
    "EnumWithSelectedValue_PowerLoadType",
    "EnumWithSelectedValue_RigidConnectorStiffnessType",
    "EnumWithSelectedValue_RigidConnectorToothSpacingType",
    "EnumWithSelectedValue_RigidConnectorTypes",
    "EnumWithSelectedValue_DoeValueSpecificationOption",
    "EnumWithSelectedValue_AnalysisType",
    "EnumWithSelectedValue_BarModelExportType",
    "EnumWithSelectedValue_DynamicsResponse3DChartType",
    "EnumWithSelectedValue_ComplexPartDisplayOption",
    "EnumWithSelectedValue_BearingStiffnessModel",
    "EnumWithSelectedValue_GearMeshStiffnessModel",
    "EnumWithSelectedValue_ShaftAndHousingFlexibilityOption",
    "EnumWithSelectedValue_ExportOutputType",
    "EnumWithSelectedValue_HarmonicAnalysisFEExportOptions_ComplexNumberOutput",
    "EnumWithSelectedValue_DampingSpecification",
    "EnumWithSelectedValue_ModalCorrectionMethod",
    "EnumWithSelectedValue_StiffnessOptionsForHarmonicAnalysis_StepCreation",
    "EnumWithSelectedValue_HarmonicAnalysisTorqueInputType",
    "EnumWithSelectedValue_FrictionModelForGyroscopicMoment",
    "EnumWithSelectedValue_MeshStiffnessModel",
    "EnumWithSelectedValue_ShearAreaFactorMethod",
    "EnumWithSelectedValue_StressConcentrationMethod",
    "EnumWithSelectedValue_BallBearingAnalysisMethod",
    "EnumWithSelectedValue_HertzianContactDeflectionCalculationMethod",
    "EnumWithSelectedValue_LoadCaseOverrideOption",
    "EnumWithSelectedValue_TorqueRippleInputType",
    "EnumWithSelectedValue_HarmonicExcitationType",
    "EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification",
    "EnumWithSelectedValue_TorqueSpecificationForSystemDeflection",
    "EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod",
    "EnumWithSelectedValue_TorqueConverterLockupRule",
    "EnumWithSelectedValue_DegreeOfFreedom",
    "EnumWithSelectedValue_DestinationDesignState",
)
