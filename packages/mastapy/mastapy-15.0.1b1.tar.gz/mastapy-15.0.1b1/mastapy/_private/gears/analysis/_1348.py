"""GearSetImplementationAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.analysis import _1349

_GEAR_SET_IMPLEMENTATION_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.Analysis", "GearSetImplementationAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private import _7901
    from mastapy._private.gears.analysis import _1337, _1346
    from mastapy._private.gears.ltca import _949
    from mastapy._private.gears.ltca.conical import _971
    from mastapy._private.gears.ltca.cylindrical import _963, _965
    from mastapy._private.gears.manufacturing.bevel import _893
    from mastapy._private.gears.manufacturing.cylindrical import _724

    Self = TypeVar("Self", bound="GearSetImplementationAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearSetImplementationAnalysis._Cast_GearSetImplementationAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearSetImplementationAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetImplementationAnalysis:
    """Special nested class for casting GearSetImplementationAnalysis to subclasses."""

    __parent__: "GearSetImplementationAnalysis"

    @property
    def gear_set_implementation_analysis_abstract(
        self: "CastSelf",
    ) -> "_1349.GearSetImplementationAnalysisAbstract":
        return self.__parent__._cast(_1349.GearSetImplementationAnalysisAbstract)

    @property
    def gear_set_design_analysis(self: "CastSelf") -> "_1346.GearSetDesignAnalysis":
        from mastapy._private.gears.analysis import _1346

        return self.__parent__._cast(_1346.GearSetDesignAnalysis)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1337.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1337

        return self.__parent__._cast(_1337.AbstractGearSetAnalysis)

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
    def gear_set_implementation_analysis(
        self: "CastSelf",
    ) -> "GearSetImplementationAnalysis":
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
class GearSetImplementationAnalysis(_1349.GearSetImplementationAnalysisAbstract):
    """GearSetImplementationAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_IMPLEMENTATION_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def valid_results_ready(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ValidResultsReady")

        if temp is None:
            return False

        return temp

    @exception_bridge
    @enforce_parameter_types
    def perform_analysis(self: "Self", run_all_planetary_meshes: "bool" = True) -> None:
        """Method does not return.

        Args:
            run_all_planetary_meshes (bool, optional)
        """
        run_all_planetary_meshes = bool(run_all_planetary_meshes)
        pythonnet_method_call(
            self.wrapped,
            "PerformAnalysis",
            run_all_planetary_meshes if run_all_planetary_meshes else False,
        )

    @exception_bridge
    @enforce_parameter_types
    def perform_analysis_with_progress(
        self: "Self", run_all_planetary_meshes: "bool", progress: "_7901.TaskProgress"
    ) -> None:
        """Method does not return.

        Args:
            run_all_planetary_meshes (bool)
            progress (mastapy.TaskProgress)
        """
        run_all_planetary_meshes = bool(run_all_planetary_meshes)
        pythonnet_method_call(
            self.wrapped,
            "PerformAnalysisWithProgress",
            run_all_planetary_meshes if run_all_planetary_meshes else False,
            progress.wrapped if progress else None,
        )

    @exception_bridge
    @enforce_parameter_types
    def results_ready_for(
        self: "Self", run_all_planetary_meshes: "bool" = True
    ) -> "bool":
        """bool

        Args:
            run_all_planetary_meshes (bool, optional)
        """
        run_all_planetary_meshes = bool(run_all_planetary_meshes)
        method_result = pythonnet_method_call(
            self.wrapped,
            "ResultsReadyFor",
            run_all_planetary_meshes if run_all_planetary_meshes else False,
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_GearSetImplementationAnalysis":
        """Cast to another type.

        Returns:
            _Cast_GearSetImplementationAnalysis
        """
        return _Cast_GearSetImplementationAnalysis(self)
