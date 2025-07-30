"""FaceGearSetCompoundSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
    _3155,
)

_FACE_GEAR_SET_COMPOUND_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound",
    "FaceGearSetCompoundSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2996,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
        _3094,
        _3148,
        _3149,
        _3176,
        _3196,
    )
    from mastapy._private.system_model.part_model.gears import _2766

    Self = TypeVar("Self", bound="FaceGearSetCompoundSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FaceGearSetCompoundSystemDeflection._Cast_FaceGearSetCompoundSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FaceGearSetCompoundSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FaceGearSetCompoundSystemDeflection:
    """Special nested class for casting FaceGearSetCompoundSystemDeflection to subclasses."""

    __parent__: "FaceGearSetCompoundSystemDeflection"

    @property
    def gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3155.GearSetCompoundSystemDeflection":
        return self.__parent__._cast(_3155.GearSetCompoundSystemDeflection)

    @property
    def specialised_assembly_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3196.SpecialisedAssemblyCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3196,
        )

        return self.__parent__._cast(_3196.SpecialisedAssemblyCompoundSystemDeflection)

    @property
    def abstract_assembly_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3094.AbstractAssemblyCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3094,
        )

        return self.__parent__._cast(_3094.AbstractAssemblyCompoundSystemDeflection)

    @property
    def part_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3176.PartCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3176,
        )

        return self.__parent__._cast(_3176.PartCompoundSystemDeflection)

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7888.PartCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7888,
        )

        return self.__parent__._cast(_7888.PartCompoundAnalysis)

    @property
    def design_entity_compound_analysis(
        self: "CastSelf",
    ) -> "_7885.DesignEntityCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7885,
        )

        return self.__parent__._cast(_7885.DesignEntityCompoundAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2892.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2892

        return self.__parent__._cast(_2892.DesignEntityAnalysis)

    @property
    def face_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "FaceGearSetCompoundSystemDeflection":
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
class FaceGearSetCompoundSystemDeflection(_3155.GearSetCompoundSystemDeflection):
    """FaceGearSetCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FACE_GEAR_SET_COMPOUND_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2766.FaceGearSet":
        """mastapy.system_model.part_model.gears.FaceGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def assembly_design(self: "Self") -> "_2766.FaceGearSet":
        """mastapy.system_model.part_model.gears.FaceGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_2996.FaceGearSetSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.FaceGearSetSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def face_gears_compound_system_deflection(
        self: "Self",
    ) -> "List[_3148.FaceGearCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.FaceGearCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceGearsCompoundSystemDeflection")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def face_meshes_compound_system_deflection(
        self: "Self",
    ) -> "List[_3149.FaceGearMeshCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.FaceGearMeshCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "FaceMeshesCompoundSystemDeflection"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_2996.FaceGearSetSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.FaceGearSetSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_FaceGearSetCompoundSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_FaceGearSetCompoundSystemDeflection
        """
        return _Cast_FaceGearSetCompoundSystemDeflection(self)
