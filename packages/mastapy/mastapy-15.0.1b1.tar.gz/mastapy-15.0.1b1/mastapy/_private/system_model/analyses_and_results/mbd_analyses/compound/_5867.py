"""CylindricalPlanetGearCompoundMultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
    _5864,
)

_CYLINDRICAL_PLANET_GEAR_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound",
    "CylindricalPlanetGearCompoundMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5713
    from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
        _5842,
        _5875,
        _5896,
        _5898,
    )

    Self = TypeVar(
        "Self", bound="CylindricalPlanetGearCompoundMultibodyDynamicsAnalysis"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalPlanetGearCompoundMultibodyDynamicsAnalysis._Cast_CylindricalPlanetGearCompoundMultibodyDynamicsAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalPlanetGearCompoundMultibodyDynamicsAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalPlanetGearCompoundMultibodyDynamicsAnalysis:
    """Special nested class for casting CylindricalPlanetGearCompoundMultibodyDynamicsAnalysis to subclasses."""

    __parent__: "CylindricalPlanetGearCompoundMultibodyDynamicsAnalysis"

    @property
    def cylindrical_gear_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5864.CylindricalGearCompoundMultibodyDynamicsAnalysis":
        return self.__parent__._cast(
            _5864.CylindricalGearCompoundMultibodyDynamicsAnalysis
        )

    @property
    def gear_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5875.GearCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5875,
        )

        return self.__parent__._cast(_5875.GearCompoundMultibodyDynamicsAnalysis)

    @property
    def mountable_component_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5896.MountableComponentCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5896,
        )

        return self.__parent__._cast(
            _5896.MountableComponentCompoundMultibodyDynamicsAnalysis
        )

    @property
    def component_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5842.ComponentCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5842,
        )

        return self.__parent__._cast(_5842.ComponentCompoundMultibodyDynamicsAnalysis)

    @property
    def part_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5898.PartCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5898,
        )

        return self.__parent__._cast(_5898.PartCompoundMultibodyDynamicsAnalysis)

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
    def cylindrical_planet_gear_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "CylindricalPlanetGearCompoundMultibodyDynamicsAnalysis":
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
class CylindricalPlanetGearCompoundMultibodyDynamicsAnalysis(
    _5864.CylindricalGearCompoundMultibodyDynamicsAnalysis
):
    """CylindricalPlanetGearCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _CYLINDRICAL_PLANET_GEAR_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_5713.CylindricalPlanetGearMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.CylindricalPlanetGearMultibodyDynamicsAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_5713.CylindricalPlanetGearMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.CylindricalPlanetGearMultibodyDynamicsAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_CylindricalPlanetGearCompoundMultibodyDynamicsAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CylindricalPlanetGearCompoundMultibodyDynamicsAnalysis
        """
        return _Cast_CylindricalPlanetGearCompoundMultibodyDynamicsAnalysis(self)
