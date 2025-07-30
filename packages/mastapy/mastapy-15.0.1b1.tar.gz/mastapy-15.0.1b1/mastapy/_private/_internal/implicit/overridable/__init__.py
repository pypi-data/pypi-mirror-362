"""__init__.py"""

import sys
from typing import TYPE_CHECKING

from lazy_imports import LazyImporter

if TYPE_CHECKING:
    from .ball_bearing_contact_calculation import (
        Overridable_BallBearingContactCalculation,
    )
    from .bearing_efficiency_rating_method import (
        Overridable_BearingEfficiencyRatingMethod,
    )
    from .bearing_element_orbit_model import Overridable_BearingElementOrbitModel
    from .bearing_f0_input_method import Overridable_BearingF0InputMethod
    from .bool import Overridable_bool
    from .boundary_condition_type import Overridable_BoundaryConditionType
    from .coefficient_of_friction_calculation_method import (
        Overridable_CoefficientOfFrictionCalculationMethod,
    )
    from .contact_damping_model import Overridable_ContactDampingModel
    from .contact_ratio_requirements import Overridable_ContactRatioRequirements
    from .cooling_channel_shape import Overridable_CoolingChannelShape
    from .cylindrical_gear_rating_methods import (
        Overridable_CylindricalGearRatingMethods,
    )
    from .cylindrical_roller_max_axial_load_method import (
        Overridable_CylindricalRollerMaxAxialLoadMethod,
    )
    from .diameter_series import Overridable_DiameterSeries
    from .dq_axis_convention import Overridable_DQAxisConvention
    from .float import Overridable_float
    from .friction_model_for_gyroscopic_moment import (
        Overridable_FrictionModelForGyroscopicMoment,
    )
    from .gear_mesh_efficiency_rating_method import (
        Overridable_GearMeshEfficiencyRatingMethod,
    )
    from .gear_windage_and_churning_loss_calculation_method import (
        Overridable_GearWindageAndChurningLossCalculationMethod,
    )
    from .height_series import Overridable_HeightSeries
    from .helical_gear_micro_geometry_option import (
        Overridable_HelicalGearMicroGeometryOption,
    )
    from .int import Overridable_int
    from .iso_tolerance_standard import Overridable_ISOToleranceStandard
    from .mesh_stiffness_source import Overridable_MeshStiffnessSource
    from .micro_geometry_model import Overridable_MicroGeometryModel
    from .node_selection_depth_option import Overridable_NodeSelectionDepthOption
    from .planetary_rating_load_sharing_option import (
        Overridable_PlanetaryRatingLoadSharingOption,
    )
    from .pro_solve_eigenmethod import Overridable_ProSolveEigenmethod
    from .rigid_coupling_type import Overridable_RigidCouplingType
    from .roller_analysis_method import Overridable_RollerAnalysisMethod
    from .seal_location import Overridable_SealLocation
    from .spline_pitch_error_input_type import Overridable_SplinePitchErrorInputType
    from .t import Overridable_T
    from .unbalanced_mass_inclusion_option import (
        Overridable_UnbalancedMassInclusionOption,
    )
    from .width_series import Overridable_WidthSeries
else:
    import_structure = {
        "float": ["Overridable_float"],
        "int": ["Overridable_int"],
        "pro_solve_eigenmethod": ["Overridable_ProSolveEigenmethod"],
        "iso_tolerance_standard": ["Overridable_ISOToleranceStandard"],
        "cylindrical_gear_rating_methods": ["Overridable_CylindricalGearRatingMethods"],
        "coefficient_of_friction_calculation_method": [
            "Overridable_CoefficientOfFrictionCalculationMethod"
        ],
        "bool": ["Overridable_bool"],
        "dq_axis_convention": ["Overridable_DQAxisConvention"],
        "cooling_channel_shape": ["Overridable_CoolingChannelShape"],
        "t": ["Overridable_T"],
        "diameter_series": ["Overridable_DiameterSeries"],
        "height_series": ["Overridable_HeightSeries"],
        "width_series": ["Overridable_WidthSeries"],
        "seal_location": ["Overridable_SealLocation"],
        "rigid_coupling_type": ["Overridable_RigidCouplingType"],
        "boundary_condition_type": ["Overridable_BoundaryConditionType"],
        "node_selection_depth_option": ["Overridable_NodeSelectionDepthOption"],
        "bearing_efficiency_rating_method": [
            "Overridable_BearingEfficiencyRatingMethod"
        ],
        "cylindrical_roller_max_axial_load_method": [
            "Overridable_CylindricalRollerMaxAxialLoadMethod"
        ],
        "contact_ratio_requirements": ["Overridable_ContactRatioRequirements"],
        "spline_pitch_error_input_type": ["Overridable_SplinePitchErrorInputType"],
        "contact_damping_model": ["Overridable_ContactDampingModel"],
        "micro_geometry_model": ["Overridable_MicroGeometryModel"],
        "unbalanced_mass_inclusion_option": [
            "Overridable_UnbalancedMassInclusionOption"
        ],
        "ball_bearing_contact_calculation": [
            "Overridable_BallBearingContactCalculation"
        ],
        "friction_model_for_gyroscopic_moment": [
            "Overridable_FrictionModelForGyroscopicMoment"
        ],
        "bearing_element_orbit_model": ["Overridable_BearingElementOrbitModel"],
        "bearing_f0_input_method": ["Overridable_BearingF0InputMethod"],
        "roller_analysis_method": ["Overridable_RollerAnalysisMethod"],
        "helical_gear_micro_geometry_option": [
            "Overridable_HelicalGearMicroGeometryOption"
        ],
        "gear_mesh_efficiency_rating_method": [
            "Overridable_GearMeshEfficiencyRatingMethod"
        ],
        "planetary_rating_load_sharing_option": [
            "Overridable_PlanetaryRatingLoadSharingOption"
        ],
        "mesh_stiffness_source": ["Overridable_MeshStiffnessSource"],
        "gear_windage_and_churning_loss_calculation_method": [
            "Overridable_GearWindageAndChurningLossCalculationMethod"
        ],
    }

    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        import_structure,
    )

__all__ = (
    "Overridable_float",
    "Overridable_int",
    "Overridable_ProSolveEigenmethod",
    "Overridable_ISOToleranceStandard",
    "Overridable_CylindricalGearRatingMethods",
    "Overridable_CoefficientOfFrictionCalculationMethod",
    "Overridable_bool",
    "Overridable_DQAxisConvention",
    "Overridable_CoolingChannelShape",
    "Overridable_T",
    "Overridable_DiameterSeries",
    "Overridable_HeightSeries",
    "Overridable_WidthSeries",
    "Overridable_SealLocation",
    "Overridable_RigidCouplingType",
    "Overridable_BoundaryConditionType",
    "Overridable_NodeSelectionDepthOption",
    "Overridable_BearingEfficiencyRatingMethod",
    "Overridable_CylindricalRollerMaxAxialLoadMethod",
    "Overridable_ContactRatioRequirements",
    "Overridable_SplinePitchErrorInputType",
    "Overridable_ContactDampingModel",
    "Overridable_MicroGeometryModel",
    "Overridable_UnbalancedMassInclusionOption",
    "Overridable_BallBearingContactCalculation",
    "Overridable_FrictionModelForGyroscopicMoment",
    "Overridable_BearingElementOrbitModel",
    "Overridable_BearingF0InputMethod",
    "Overridable_RollerAnalysisMethod",
    "Overridable_HelicalGearMicroGeometryOption",
    "Overridable_GearMeshEfficiencyRatingMethod",
    "Overridable_PlanetaryRatingLoadSharingOption",
    "Overridable_MeshStiffnessSource",
    "Overridable_GearWindageAndChurningLossCalculationMethod",
)
