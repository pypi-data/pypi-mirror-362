"""GearSetImplementationAnalysisAbstract"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.analysis import _1346

_GEAR_SET_IMPLEMENTATION_ANALYSIS_ABSTRACT = python_net_import(
    "SMT.MastaAPI.Gears.Analysis", "GearSetImplementationAnalysisAbstract"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1337, _1348, _1350
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1221
    from mastapy._private.gears.ltca import _949
    from mastapy._private.gears.ltca.conical import _971
    from mastapy._private.gears.ltca.cylindrical import _963, _965
    from mastapy._private.gears.manufacturing.bevel import _893
    from mastapy._private.gears.manufacturing.cylindrical import _723, _724

    Self = TypeVar("Self", bound="GearSetImplementationAnalysisAbstract")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearSetImplementationAnalysisAbstract._Cast_GearSetImplementationAnalysisAbstract",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearSetImplementationAnalysisAbstract",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetImplementationAnalysisAbstract:
    """Special nested class for casting GearSetImplementationAnalysisAbstract to subclasses."""

    __parent__: "GearSetImplementationAnalysisAbstract"

    @property
    def gear_set_design_analysis(self: "CastSelf") -> "_1346.GearSetDesignAnalysis":
        return self.__parent__._cast(_1346.GearSetDesignAnalysis)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1337.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1337

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
    def conical_set_manufacturing_analysis(
        self: "CastSelf",
    ) -> "_893.ConicalSetManufacturingAnalysis":
        from mastapy._private.gears.manufacturing.bevel import _893

        return self.__parent__._cast(_893.ConicalSetManufacturingAnalysis)

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
    def cylindrical_gear_set_micro_geometry_duty_cycle(
        self: "CastSelf",
    ) -> "_1221.CylindricalGearSetMicroGeometryDutyCycle":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1221

        return self.__parent__._cast(_1221.CylindricalGearSetMicroGeometryDutyCycle)

    @property
    def gear_set_implementation_analysis(
        self: "CastSelf",
    ) -> "_1348.GearSetImplementationAnalysis":
        from mastapy._private.gears.analysis import _1348

        return self.__parent__._cast(_1348.GearSetImplementationAnalysis)

    @property
    def gear_set_implementation_analysis_duty_cycle(
        self: "CastSelf",
    ) -> "_1350.GearSetImplementationAnalysisDutyCycle":
        from mastapy._private.gears.analysis import _1350

        return self.__parent__._cast(_1350.GearSetImplementationAnalysisDutyCycle)

    @property
    def gear_set_implementation_analysis_abstract(
        self: "CastSelf",
    ) -> "GearSetImplementationAnalysisAbstract":
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
class GearSetImplementationAnalysisAbstract(_1346.GearSetDesignAnalysis):
    """GearSetImplementationAnalysisAbstract

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_IMPLEMENTATION_ANALYSIS_ABSTRACT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_GearSetImplementationAnalysisAbstract":
        """Cast to another type.

        Returns:
            _Cast_GearSetImplementationAnalysisAbstract
        """
        return _Cast_GearSetImplementationAnalysisAbstract(self)
