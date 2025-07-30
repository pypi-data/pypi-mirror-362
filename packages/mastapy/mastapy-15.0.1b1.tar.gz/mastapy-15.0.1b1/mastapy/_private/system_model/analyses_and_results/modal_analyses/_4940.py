"""PlanetaryGearSetModalAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses import _4892

_PLANETARY_GEAR_SET_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses",
    "PlanetaryGearSetModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import (
        _4842,
        _4907,
        _4935,
        _4955,
    )
    from mastapy._private.system_model.part_model.gears import _2779

    Self = TypeVar("Self", bound="PlanetaryGearSetModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PlanetaryGearSetModalAnalysis._Cast_PlanetaryGearSetModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlanetaryGearSetModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlanetaryGearSetModalAnalysis:
    """Special nested class for casting PlanetaryGearSetModalAnalysis to subclasses."""

    __parent__: "PlanetaryGearSetModalAnalysis"

    @property
    def cylindrical_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4892.CylindricalGearSetModalAnalysis":
        return self.__parent__._cast(_4892.CylindricalGearSetModalAnalysis)

    @property
    def gear_set_modal_analysis(self: "CastSelf") -> "_4907.GearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4907,
        )

        return self.__parent__._cast(_4907.GearSetModalAnalysis)

    @property
    def specialised_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "_4955.SpecialisedAssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4955,
        )

        return self.__parent__._cast(_4955.SpecialisedAssemblyModalAnalysis)

    @property
    def abstract_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "_4842.AbstractAssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4842,
        )

        return self.__parent__._cast(_4842.AbstractAssemblyModalAnalysis)

    @property
    def part_modal_analysis(self: "CastSelf") -> "_4935.PartModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4935,
        )

        return self.__parent__._cast(_4935.PartModalAnalysis)

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7890.PartStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7890,
        )

        return self.__parent__._cast(_7890.PartStaticLoadAnalysisCase)

    @property
    def part_analysis_case(self: "CastSelf") -> "_7887.PartAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7887,
        )

        return self.__parent__._cast(_7887.PartAnalysisCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2898.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2898

        return self.__parent__._cast(_2898.PartAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2894.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2894

        return self.__parent__._cast(_2894.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2892.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2892

        return self.__parent__._cast(_2892.DesignEntityAnalysis)

    @property
    def planetary_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "PlanetaryGearSetModalAnalysis":
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
class PlanetaryGearSetModalAnalysis(_4892.CylindricalGearSetModalAnalysis):
    """PlanetaryGearSetModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLANETARY_GEAR_SET_MODAL_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_design(self: "Self") -> "_2779.PlanetaryGearSet":
        """mastapy.system_model.part_model.gears.PlanetaryGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_PlanetaryGearSetModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_PlanetaryGearSetModalAnalysis
        """
        return _Cast_PlanetaryGearSetModalAnalysis(self)
