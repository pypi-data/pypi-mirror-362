"""AbstractShaftMultibodyDynamicsAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5661

_ABSTRACT_SHAFT_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses",
    "AbstractShaftMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7891,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
        _5688,
        _5708,
        _5753,
        _5772,
    )
    from mastapy._private.system_model.part_model import _2660

    Self = TypeVar("Self", bound="AbstractShaftMultibodyDynamicsAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractShaftMultibodyDynamicsAnalysis._Cast_AbstractShaftMultibodyDynamicsAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractShaftMultibodyDynamicsAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftMultibodyDynamicsAnalysis:
    """Special nested class for casting AbstractShaftMultibodyDynamicsAnalysis to subclasses."""

    __parent__: "AbstractShaftMultibodyDynamicsAnalysis"

    @property
    def abstract_shaft_or_housing_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5661.AbstractShaftOrHousingMultibodyDynamicsAnalysis":
        return self.__parent__._cast(
            _5661.AbstractShaftOrHousingMultibodyDynamicsAnalysis
        )

    @property
    def component_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5688.ComponentMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5688,
        )

        return self.__parent__._cast(_5688.ComponentMultibodyDynamicsAnalysis)

    @property
    def part_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5753.PartMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5753,
        )

        return self.__parent__._cast(_5753.PartMultibodyDynamicsAnalysis)

    @property
    def part_time_series_load_analysis_case(
        self: "CastSelf",
    ) -> "_7891.PartTimeSeriesLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7891,
        )

        return self.__parent__._cast(_7891.PartTimeSeriesLoadAnalysisCase)

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
    def cycloidal_disc_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5708.CycloidalDiscMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5708,
        )

        return self.__parent__._cast(_5708.CycloidalDiscMultibodyDynamicsAnalysis)

    @property
    def shaft_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5772.ShaftMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5772,
        )

        return self.__parent__._cast(_5772.ShaftMultibodyDynamicsAnalysis)

    @property
    def abstract_shaft_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "AbstractShaftMultibodyDynamicsAnalysis":
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
class AbstractShaftMultibodyDynamicsAnalysis(
    _5661.AbstractShaftOrHousingMultibodyDynamicsAnalysis
):
    """AbstractShaftMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_SHAFT_MULTIBODY_DYNAMICS_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2660.AbstractShaft":
        """mastapy.system_model.part_model.AbstractShaft

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractShaftMultibodyDynamicsAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftMultibodyDynamicsAnalysis
        """
        return _Cast_AbstractShaftMultibodyDynamicsAnalysis(self)
