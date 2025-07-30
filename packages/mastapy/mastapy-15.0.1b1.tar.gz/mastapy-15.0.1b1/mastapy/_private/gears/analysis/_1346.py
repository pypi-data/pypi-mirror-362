"""GearSetDesignAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.analysis import _1337

_GEAR_SET_DESIGN_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.Analysis", "GearSetDesignAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1348, _1349, _1350, _1351
    from mastapy._private.gears.fe_model import _1320
    from mastapy._private.gears.fe_model.conical import _1326
    from mastapy._private.gears.fe_model.cylindrical import _1323
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import (
        _1220,
        _1221,
    )
    from mastapy._private.gears.gear_designs.face import _1100
    from mastapy._private.gears.gear_two_d_fe_analysis import _999, _1000
    from mastapy._private.gears.load_case import _977
    from mastapy._private.gears.load_case.bevel import _996
    from mastapy._private.gears.load_case.concept import _992
    from mastapy._private.gears.load_case.conical import _989
    from mastapy._private.gears.load_case.cylindrical import _986
    from mastapy._private.gears.load_case.face import _983
    from mastapy._private.gears.load_case.worm import _980
    from mastapy._private.gears.ltca import _949
    from mastapy._private.gears.ltca.conical import _971
    from mastapy._private.gears.ltca.cylindrical import _963, _965
    from mastapy._private.gears.manufacturing.bevel import _893, _894, _895, _896
    from mastapy._private.gears.manufacturing.cylindrical import _723, _724, _728

    Self = TypeVar("Self", bound="GearSetDesignAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="GearSetDesignAnalysis._Cast_GearSetDesignAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearSetDesignAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetDesignAnalysis:
    """Special nested class for casting GearSetDesignAnalysis to subclasses."""

    __parent__: "GearSetDesignAnalysis"

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1337.AbstractGearSetAnalysis":
        return self.__parent__._cast(_1337.AbstractGearSetAnalysis)

    @property
    def cylindrical_manufactured_gear_set_duty_cycle(
        self: "CastSelf",
    ) -> "_723.CylindricalManufacturedGearSetDutyCycle":
        from mastapy._private.gears.manufacturing.cylindrical import _723

        return self.__parent__._cast(_723.CylindricalManufacturedGearSetDutyCycle)

    @property
    def cylindrical_manufactured_gear_set_load_case(
        self: "CastSelf",
    ) -> "_724.CylindricalManufacturedGearSetLoadCase":
        from mastapy._private.gears.manufacturing.cylindrical import _724

        return self.__parent__._cast(_724.CylindricalManufacturedGearSetLoadCase)

    @property
    def cylindrical_set_manufacturing_config(
        self: "CastSelf",
    ) -> "_728.CylindricalSetManufacturingConfig":
        from mastapy._private.gears.manufacturing.cylindrical import _728

        return self.__parent__._cast(_728.CylindricalSetManufacturingConfig)

    @property
    def conical_set_manufacturing_analysis(
        self: "CastSelf",
    ) -> "_893.ConicalSetManufacturingAnalysis":
        from mastapy._private.gears.manufacturing.bevel import _893

        return self.__parent__._cast(_893.ConicalSetManufacturingAnalysis)

    @property
    def conical_set_manufacturing_config(
        self: "CastSelf",
    ) -> "_894.ConicalSetManufacturingConfig":
        from mastapy._private.gears.manufacturing.bevel import _894

        return self.__parent__._cast(_894.ConicalSetManufacturingConfig)

    @property
    def conical_set_micro_geometry_config(
        self: "CastSelf",
    ) -> "_895.ConicalSetMicroGeometryConfig":
        from mastapy._private.gears.manufacturing.bevel import _895

        return self.__parent__._cast(_895.ConicalSetMicroGeometryConfig)

    @property
    def conical_set_micro_geometry_config_base(
        self: "CastSelf",
    ) -> "_896.ConicalSetMicroGeometryConfigBase":
        from mastapy._private.gears.manufacturing.bevel import _896

        return self.__parent__._cast(_896.ConicalSetMicroGeometryConfigBase)

    @property
    def gear_set_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_949.GearSetLoadDistributionAnalysis":
        from mastapy._private.gears.ltca import _949

        return self.__parent__._cast(_949.GearSetLoadDistributionAnalysis)

    @property
    def cylindrical_gear_set_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_963.CylindricalGearSetLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.cylindrical import _963

        return self.__parent__._cast(_963.CylindricalGearSetLoadDistributionAnalysis)

    @property
    def face_gear_set_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_965.FaceGearSetLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.cylindrical import _965

        return self.__parent__._cast(_965.FaceGearSetLoadDistributionAnalysis)

    @property
    def conical_gear_set_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_971.ConicalGearSetLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.conical import _971

        return self.__parent__._cast(_971.ConicalGearSetLoadDistributionAnalysis)

    @property
    def gear_set_load_case_base(self: "CastSelf") -> "_977.GearSetLoadCaseBase":
        from mastapy._private.gears.load_case import _977

        return self.__parent__._cast(_977.GearSetLoadCaseBase)

    @property
    def worm_gear_set_load_case(self: "CastSelf") -> "_980.WormGearSetLoadCase":
        from mastapy._private.gears.load_case.worm import _980

        return self.__parent__._cast(_980.WormGearSetLoadCase)

    @property
    def face_gear_set_load_case(self: "CastSelf") -> "_983.FaceGearSetLoadCase":
        from mastapy._private.gears.load_case.face import _983

        return self.__parent__._cast(_983.FaceGearSetLoadCase)

    @property
    def cylindrical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_986.CylindricalGearSetLoadCase":
        from mastapy._private.gears.load_case.cylindrical import _986

        return self.__parent__._cast(_986.CylindricalGearSetLoadCase)

    @property
    def conical_gear_set_load_case(self: "CastSelf") -> "_989.ConicalGearSetLoadCase":
        from mastapy._private.gears.load_case.conical import _989

        return self.__parent__._cast(_989.ConicalGearSetLoadCase)

    @property
    def concept_gear_set_load_case(self: "CastSelf") -> "_992.ConceptGearSetLoadCase":
        from mastapy._private.gears.load_case.concept import _992

        return self.__parent__._cast(_992.ConceptGearSetLoadCase)

    @property
    def bevel_set_load_case(self: "CastSelf") -> "_996.BevelSetLoadCase":
        from mastapy._private.gears.load_case.bevel import _996

        return self.__parent__._cast(_996.BevelSetLoadCase)

    @property
    def cylindrical_gear_set_tiff_analysis(
        self: "CastSelf",
    ) -> "_999.CylindricalGearSetTIFFAnalysis":
        from mastapy._private.gears.gear_two_d_fe_analysis import _999

        return self.__parent__._cast(_999.CylindricalGearSetTIFFAnalysis)

    @property
    def cylindrical_gear_set_tiff_analysis_duty_cycle(
        self: "CastSelf",
    ) -> "_1000.CylindricalGearSetTIFFAnalysisDutyCycle":
        from mastapy._private.gears.gear_two_d_fe_analysis import _1000

        return self.__parent__._cast(_1000.CylindricalGearSetTIFFAnalysisDutyCycle)

    @property
    def face_gear_set_micro_geometry(
        self: "CastSelf",
    ) -> "_1100.FaceGearSetMicroGeometry":
        from mastapy._private.gears.gear_designs.face import _1100

        return self.__parent__._cast(_1100.FaceGearSetMicroGeometry)

    @property
    def cylindrical_gear_set_micro_geometry(
        self: "CastSelf",
    ) -> "_1220.CylindricalGearSetMicroGeometry":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1220

        return self.__parent__._cast(_1220.CylindricalGearSetMicroGeometry)

    @property
    def cylindrical_gear_set_micro_geometry_duty_cycle(
        self: "CastSelf",
    ) -> "_1221.CylindricalGearSetMicroGeometryDutyCycle":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1221

        return self.__parent__._cast(_1221.CylindricalGearSetMicroGeometryDutyCycle)

    @property
    def gear_set_fe_model(self: "CastSelf") -> "_1320.GearSetFEModel":
        from mastapy._private.gears.fe_model import _1320

        return self.__parent__._cast(_1320.GearSetFEModel)

    @property
    def cylindrical_gear_set_fe_model(
        self: "CastSelf",
    ) -> "_1323.CylindricalGearSetFEModel":
        from mastapy._private.gears.fe_model.cylindrical import _1323

        return self.__parent__._cast(_1323.CylindricalGearSetFEModel)

    @property
    def conical_set_fe_model(self: "CastSelf") -> "_1326.ConicalSetFEModel":
        from mastapy._private.gears.fe_model.conical import _1326

        return self.__parent__._cast(_1326.ConicalSetFEModel)

    @property
    def gear_set_implementation_analysis(
        self: "CastSelf",
    ) -> "_1348.GearSetImplementationAnalysis":
        from mastapy._private.gears.analysis import _1348

        return self.__parent__._cast(_1348.GearSetImplementationAnalysis)

    @property
    def gear_set_implementation_analysis_abstract(
        self: "CastSelf",
    ) -> "_1349.GearSetImplementationAnalysisAbstract":
        from mastapy._private.gears.analysis import _1349

        return self.__parent__._cast(_1349.GearSetImplementationAnalysisAbstract)

    @property
    def gear_set_implementation_analysis_duty_cycle(
        self: "CastSelf",
    ) -> "_1350.GearSetImplementationAnalysisDutyCycle":
        from mastapy._private.gears.analysis import _1350

        return self.__parent__._cast(_1350.GearSetImplementationAnalysisDutyCycle)

    @property
    def gear_set_implementation_detail(
        self: "CastSelf",
    ) -> "_1351.GearSetImplementationDetail":
        from mastapy._private.gears.analysis import _1351

        return self.__parent__._cast(_1351.GearSetImplementationDetail)

    @property
    def gear_set_design_analysis(self: "CastSelf") -> "GearSetDesignAnalysis":
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
class GearSetDesignAnalysis(_1337.AbstractGearSetAnalysis):
    """GearSetDesignAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_DESIGN_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_GearSetDesignAnalysis":
        """Cast to another type.

        Returns:
            _Cast_GearSetDesignAnalysis
        """
        return _Cast_GearSetDesignAnalysis(self)
