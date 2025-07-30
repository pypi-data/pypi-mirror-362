"""CouplingConnectionCompoundMultibodyDynamicsAnalysis"""

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
    _5882,
)

_COUPLING_CONNECTION_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound",
    "CouplingConnectionCompoundMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7881,
        _7885,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5700
    from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
        _5839,
        _5844,
        _5852,
        _5900,
        _5922,
        _5937,
    )

    Self = TypeVar("Self", bound="CouplingConnectionCompoundMultibodyDynamicsAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingConnectionCompoundMultibodyDynamicsAnalysis._Cast_CouplingConnectionCompoundMultibodyDynamicsAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingConnectionCompoundMultibodyDynamicsAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingConnectionCompoundMultibodyDynamicsAnalysis:
    """Special nested class for casting CouplingConnectionCompoundMultibodyDynamicsAnalysis to subclasses."""

    __parent__: "CouplingConnectionCompoundMultibodyDynamicsAnalysis"

    @property
    def inter_mountable_component_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5882.InterMountableComponentConnectionCompoundMultibodyDynamicsAnalysis":
        return self.__parent__._cast(
            _5882.InterMountableComponentConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5852.ConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5852,
        )

        return self.__parent__._cast(_5852.ConnectionCompoundMultibodyDynamicsAnalysis)

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
    def clutch_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5839.ClutchConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5839,
        )

        return self.__parent__._cast(
            _5839.ClutchConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def concept_coupling_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5844.ConceptCouplingConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5844,
        )

        return self.__parent__._cast(
            _5844.ConceptCouplingConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5900.PartToPartShearCouplingConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5900,
        )

        return self.__parent__._cast(
            _5900.PartToPartShearCouplingConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def spring_damper_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5922.SpringDamperConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5922,
        )

        return self.__parent__._cast(
            _5922.SpringDamperConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def torque_converter_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5937.TorqueConverterConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5937,
        )

        return self.__parent__._cast(
            _5937.TorqueConverterConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def coupling_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "CouplingConnectionCompoundMultibodyDynamicsAnalysis":
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
class CouplingConnectionCompoundMultibodyDynamicsAnalysis(
    _5882.InterMountableComponentConnectionCompoundMultibodyDynamicsAnalysis
):
    """CouplingConnectionCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_CONNECTION_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_5700.CouplingConnectionMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.CouplingConnectionMultibodyDynamicsAnalysis]

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
    @exception_bridge
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_5700.CouplingConnectionMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.CouplingConnectionMultibodyDynamicsAnalysis]

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_CouplingConnectionCompoundMultibodyDynamicsAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CouplingConnectionCompoundMultibodyDynamicsAnalysis
        """
        return _Cast_CouplingConnectionCompoundMultibodyDynamicsAnalysis(self)
