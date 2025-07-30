"""StraightBevelDiffGearMeshModalAnalysis"""

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
from mastapy._private.system_model.analyses_and_results.modal_analyses import _4858

_STRAIGHT_BEVEL_DIFF_GEAR_MESH_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses",
    "StraightBevelDiffGearMeshModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7883,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import (
        _4846,
        _4874,
        _4877,
        _4905,
        _4912,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7831
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _3056,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2546

    Self = TypeVar("Self", bound="StraightBevelDiffGearMeshModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelDiffGearMeshModalAnalysis._Cast_StraightBevelDiffGearMeshModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelDiffGearMeshModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelDiffGearMeshModalAnalysis:
    """Special nested class for casting StraightBevelDiffGearMeshModalAnalysis to subclasses."""

    __parent__: "StraightBevelDiffGearMeshModalAnalysis"

    @property
    def bevel_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4858.BevelGearMeshModalAnalysis":
        return self.__parent__._cast(_4858.BevelGearMeshModalAnalysis)

    @property
    def agma_gleason_conical_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4846.AGMAGleasonConicalGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4846,
        )

        return self.__parent__._cast(_4846.AGMAGleasonConicalGearMeshModalAnalysis)

    @property
    def conical_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4874.ConicalGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4874,
        )

        return self.__parent__._cast(_4874.ConicalGearMeshModalAnalysis)

    @property
    def gear_mesh_modal_analysis(self: "CastSelf") -> "_4905.GearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4905,
        )

        return self.__parent__._cast(_4905.GearMeshModalAnalysis)

    @property
    def inter_mountable_component_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4912.InterMountableComponentConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4912,
        )

        return self.__parent__._cast(
            _4912.InterMountableComponentConnectionModalAnalysis
        )

    @property
    def connection_modal_analysis(self: "CastSelf") -> "_4877.ConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4877,
        )

        return self.__parent__._cast(_4877.ConnectionModalAnalysis)

    @property
    def connection_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7883.ConnectionStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7883,
        )

        return self.__parent__._cast(_7883.ConnectionStaticLoadAnalysisCase)

    @property
    def connection_analysis_case(self: "CastSelf") -> "_7880.ConnectionAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7880,
        )

        return self.__parent__._cast(_7880.ConnectionAnalysisCase)

    @property
    def connection_analysis(self: "CastSelf") -> "_2890.ConnectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2890

        return self.__parent__._cast(_2890.ConnectionAnalysis)

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
    def straight_bevel_diff_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "StraightBevelDiffGearMeshModalAnalysis":
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
class StraightBevelDiffGearMeshModalAnalysis(_4858.BevelGearMeshModalAnalysis):
    """StraightBevelDiffGearMeshModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_DIFF_GEAR_MESH_MODAL_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_design(self: "Self") -> "_2546.StraightBevelDiffGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh

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
    def connection_load_case(self: "Self") -> "_7831.StraightBevelDiffGearMeshLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearMeshLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def system_deflection_results(
        self: "Self",
    ) -> "_3056.StraightBevelDiffGearMeshSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.StraightBevelDiffGearMeshSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_StraightBevelDiffGearMeshModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelDiffGearMeshModalAnalysis
        """
        return _Cast_StraightBevelDiffGearMeshModalAnalysis(self)
