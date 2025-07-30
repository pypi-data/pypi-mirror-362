"""IndependentReportablePropertiesBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import

_INDEPENDENT_REPORTABLE_PROPERTIES_BASE = python_net_import(
    "SMT.MastaAPI.Utility", "IndependentReportablePropertiesBase"
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.bearings.bearing_results import _2151
    from mastapy._private.bearings.bearing_results.rolling import _2183, _2279
    from mastapy._private.bearings.tolerances import _2121
    from mastapy._private.electric_machines import _1385
    from mastapy._private.electric_machines.load_cases_and_analyses import _1561
    from mastapy._private.gears import _436
    from mastapy._private.gears.gear_designs.cylindrical import (
        _1130,
        _1161,
        _1169,
        _1170,
        _1173,
        _1174,
        _1183,
        _1191,
        _1193,
        _1197,
        _1201,
    )
    from mastapy._private.geometry import _398
    from mastapy._private.materials import _376
    from mastapy._private.materials.efficiency import _387
    from mastapy._private.math_utility.measured_data import _1750, _1751, _1752
    from mastapy._private.system_model.analyses_and_results.static_loads import _7679
    from mastapy._private.utility import _1791

    Self = TypeVar("Self", bound="IndependentReportablePropertiesBase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="IndependentReportablePropertiesBase._Cast_IndependentReportablePropertiesBase",
    )

T = TypeVar("T", bound="IndependentReportablePropertiesBase")

__docformat__ = "restructuredtext en"
__all__ = ("IndependentReportablePropertiesBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_IndependentReportablePropertiesBase:
    """Special nested class for casting IndependentReportablePropertiesBase to subclasses."""

    __parent__: "IndependentReportablePropertiesBase"

    @property
    def temperature_dependent_property(
        self: "CastSelf",
    ) -> "_376.TemperatureDependentProperty":
        from mastapy._private.materials import _376

        return self.__parent__._cast(_376.TemperatureDependentProperty)

    @property
    def oil_pump_detail(self: "CastSelf") -> "_387.OilPumpDetail":
        from mastapy._private.materials.efficiency import _387

        return self.__parent__._cast(_387.OilPumpDetail)

    @property
    def packaging_limits(self: "CastSelf") -> "_398.PackagingLimits":
        from mastapy._private.geometry import _398

        return self.__parent__._cast(_398.PackagingLimits)

    @property
    def specification_for_the_effect_of_oil_kinematic_viscosity(
        self: "CastSelf",
    ) -> "_436.SpecificationForTheEffectOfOilKinematicViscosity":
        from mastapy._private.gears import _436

        return self.__parent__._cast(
            _436.SpecificationForTheEffectOfOilKinematicViscosity
        )

    @property
    def cylindrical_gear_micro_geometry_settings(
        self: "CastSelf",
    ) -> "_1130.CylindricalGearMicroGeometrySettings":
        from mastapy._private.gears.gear_designs.cylindrical import _1130

        return self.__parent__._cast(_1130.CylindricalGearMicroGeometrySettings)

    @property
    def hardened_material_properties(
        self: "CastSelf",
    ) -> "_1161.HardenedMaterialProperties":
        from mastapy._private.gears.gear_designs.cylindrical import _1161

        return self.__parent__._cast(_1161.HardenedMaterialProperties)

    @property
    def ltca_load_case_modifiable_settings(
        self: "CastSelf",
    ) -> "_1169.LTCALoadCaseModifiableSettings":
        from mastapy._private.gears.gear_designs.cylindrical import _1169

        return self.__parent__._cast(_1169.LTCALoadCaseModifiableSettings)

    @property
    def ltca_settings(self: "CastSelf") -> "_1170.LTCASettings":
        from mastapy._private.gears.gear_designs.cylindrical import _1170

        return self.__parent__._cast(_1170.LTCASettings)

    @property
    def micropitting(self: "CastSelf") -> "_1173.Micropitting":
        from mastapy._private.gears.gear_designs.cylindrical import _1173

        return self.__parent__._cast(_1173.Micropitting)

    @property
    def muller_residual_stress_definition(
        self: "CastSelf",
    ) -> "_1174.MullerResidualStressDefinition":
        from mastapy._private.gears.gear_designs.cylindrical import _1174

        return self.__parent__._cast(_1174.MullerResidualStressDefinition)

    @property
    def scuffing(self: "CastSelf") -> "_1183.Scuffing":
        from mastapy._private.gears.gear_designs.cylindrical import _1183

        return self.__parent__._cast(_1183.Scuffing)

    @property
    def surface_roughness(self: "CastSelf") -> "_1191.SurfaceRoughness":
        from mastapy._private.gears.gear_designs.cylindrical import _1191

        return self.__parent__._cast(_1191.SurfaceRoughness)

    @property
    def tiff_analysis_settings(self: "CastSelf") -> "_1193.TiffAnalysisSettings":
        from mastapy._private.gears.gear_designs.cylindrical import _1193

        return self.__parent__._cast(_1193.TiffAnalysisSettings)

    @property
    def tooth_flank_fracture_analysis_settings(
        self: "CastSelf",
    ) -> "_1197.ToothFlankFractureAnalysisSettings":
        from mastapy._private.gears.gear_designs.cylindrical import _1197

        return self.__parent__._cast(_1197.ToothFlankFractureAnalysisSettings)

    @property
    def usage(self: "CastSelf") -> "_1201.Usage":
        from mastapy._private.gears.gear_designs.cylindrical import _1201

        return self.__parent__._cast(_1201.Usage)

    @property
    def eccentricity(self: "CastSelf") -> "_1385.Eccentricity":
        from mastapy._private.electric_machines import _1385

        return self.__parent__._cast(_1385.Eccentricity)

    @property
    def temperatures(self: "CastSelf") -> "_1561.Temperatures":
        from mastapy._private.electric_machines.load_cases_and_analyses import _1561

        return self.__parent__._cast(_1561.Temperatures)

    @property
    def lookup_table_base(self: "CastSelf") -> "_1750.LookupTableBase":
        from mastapy._private.math_utility.measured_data import _1750

        return self.__parent__._cast(_1750.LookupTableBase)

    @property
    def onedimensional_function_lookup_table(
        self: "CastSelf",
    ) -> "_1751.OnedimensionalFunctionLookupTable":
        from mastapy._private.math_utility.measured_data import _1751

        return self.__parent__._cast(_1751.OnedimensionalFunctionLookupTable)

    @property
    def twodimensional_function_lookup_table(
        self: "CastSelf",
    ) -> "_1752.TwodimensionalFunctionLookupTable":
        from mastapy._private.math_utility.measured_data import _1752

        return self.__parent__._cast(_1752.TwodimensionalFunctionLookupTable)

    @property
    def skf_loss_moment_multipliers(
        self: "CastSelf",
    ) -> "_1791.SKFLossMomentMultipliers":
        from mastapy._private.utility import _1791

        return self.__parent__._cast(_1791.SKFLossMomentMultipliers)

    @property
    def roundness_specification(self: "CastSelf") -> "_2121.RoundnessSpecification":
        from mastapy._private.bearings.tolerances import _2121

        return self.__parent__._cast(_2121.RoundnessSpecification)

    @property
    def equivalent_load_factors(self: "CastSelf") -> "_2151.EquivalentLoadFactors":
        from mastapy._private.bearings.bearing_results import _2151

        return self.__parent__._cast(_2151.EquivalentLoadFactors)

    @property
    def iso14179_settings_per_bearing_type(
        self: "CastSelf",
    ) -> "_2183.ISO14179SettingsPerBearingType":
        from mastapy._private.bearings.bearing_results.rolling import _2183

        return self.__parent__._cast(_2183.ISO14179SettingsPerBearingType)

    @property
    def rolling_bearing_friction_coefficients(
        self: "CastSelf",
    ) -> "_2279.RollingBearingFrictionCoefficients":
        from mastapy._private.bearings.bearing_results.rolling import _2279

        return self.__parent__._cast(_2279.RollingBearingFrictionCoefficients)

    @property
    def additional_acceleration_options(
        self: "CastSelf",
    ) -> "_7679.AdditionalAccelerationOptions":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7679,
        )

        return self.__parent__._cast(_7679.AdditionalAccelerationOptions)

    @property
    def independent_reportable_properties_base(
        self: "CastSelf",
    ) -> "IndependentReportablePropertiesBase":
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
class IndependentReportablePropertiesBase(_0.APIBase, Generic[T]):
    """IndependentReportablePropertiesBase

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _INDEPENDENT_REPORTABLE_PROPERTIES_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_IndependentReportablePropertiesBase":
        """Cast to another type.

        Returns:
            _Cast_IndependentReportablePropertiesBase
        """
        return _Cast_IndependentReportablePropertiesBase(self)
