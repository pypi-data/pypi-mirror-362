"""CylindricalGearMeshCompoundSystemDeflection"""

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
    _3154,
)

_CYLINDRICAL_GEAR_MESH_COMPOUND_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound",
    "CylindricalGearMeshCompoundSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1212
    from mastapy._private.gears.rating.cylindrical import _557
    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7881,
        _7885,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2982,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
        _3129,
        _3160,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2530

    Self = TypeVar("Self", bound="CylindricalGearMeshCompoundSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearMeshCompoundSystemDeflection._Cast_CylindricalGearMeshCompoundSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearMeshCompoundSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearMeshCompoundSystemDeflection:
    """Special nested class for casting CylindricalGearMeshCompoundSystemDeflection to subclasses."""

    __parent__: "CylindricalGearMeshCompoundSystemDeflection"

    @property
    def gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3154.GearMeshCompoundSystemDeflection":
        return self.__parent__._cast(_3154.GearMeshCompoundSystemDeflection)

    @property
    def inter_mountable_component_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3160.InterMountableComponentConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3160,
        )

        return self.__parent__._cast(
            _3160.InterMountableComponentConnectionCompoundSystemDeflection
        )

    @property
    def connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3129.ConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3129,
        )

        return self.__parent__._cast(_3129.ConnectionCompoundSystemDeflection)

    @property
    def connection_compound_analysis(
        self: "CastSelf",
    ) -> "_7881.ConnectionCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7881,
        )

        return self.__parent__._cast(_7881.ConnectionCompoundAnalysis)

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
    def cylindrical_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "CylindricalGearMeshCompoundSystemDeflection":
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
class CylindricalGearMeshCompoundSystemDeflection(
    _3154.GearMeshCompoundSystemDeflection
):
    """CylindricalGearMeshCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_MESH_COMPOUND_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def maximum_operating_backlash(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumOperatingBacklash")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_operating_backlash(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumOperatingBacklash")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_operating_tip_root_clearance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumOperatingTipRootClearance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_operating_transverse_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumOperatingTransverseContactRatio"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def basic_ltca_results(
        self: "Self",
    ) -> "_1212.CylindricalGearMeshMicroGeometryDutyCycle":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearMeshMicroGeometryDutyCycle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasicLTCAResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2530.CylindricalGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh

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
    def connection_design(self: "Self") -> "_2530.CylindricalGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_mesh_rating(self: "Self") -> "_557.CylindricalMeshDutyCycleRating":
        """mastapy.gears.rating.cylindrical.CylindricalMeshDutyCycleRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalMeshRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_2982.CylindricalGearMeshSystemDeflectionWithLTCAResults]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.CylindricalGearMeshSystemDeflectionWithLTCAResults]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def planetaries(
        self: "Self",
    ) -> "List[CylindricalGearMeshCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.CylindricalGearMeshCompoundSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Planetaries")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_2982.CylindricalGearMeshSystemDeflectionWithLTCAResults]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.CylindricalGearMeshSystemDeflectionWithLTCAResults]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearMeshCompoundSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearMeshCompoundSystemDeflection
        """
        return _Cast_CylindricalGearMeshCompoundSystemDeflection(self)
