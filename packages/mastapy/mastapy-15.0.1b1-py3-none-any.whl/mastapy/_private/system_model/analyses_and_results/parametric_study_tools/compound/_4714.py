"""AbstractShaftToMountableComponentConnectionCompoundParametricStudyTool"""

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
from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
    _4746,
)

_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_PARAMETRIC_STUDY_TOOL = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound",
        "AbstractShaftToMountableComponentConnectionCompoundParametricStudyTool",
    )
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7881,
        _7885,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4564,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
        _4735,
        _4755,
        _4757,
        _4796,
        _4810,
    )

    Self = TypeVar(
        "Self",
        bound="AbstractShaftToMountableComponentConnectionCompoundParametricStudyTool",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractShaftToMountableComponentConnectionCompoundParametricStudyTool._Cast_AbstractShaftToMountableComponentConnectionCompoundParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractShaftToMountableComponentConnectionCompoundParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftToMountableComponentConnectionCompoundParametricStudyTool:
    """Special nested class for casting AbstractShaftToMountableComponentConnectionCompoundParametricStudyTool to subclasses."""

    __parent__: "AbstractShaftToMountableComponentConnectionCompoundParametricStudyTool"

    @property
    def connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4746.ConnectionCompoundParametricStudyTool":
        return self.__parent__._cast(_4746.ConnectionCompoundParametricStudyTool)

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
    def coaxial_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4735.CoaxialConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4735,
        )

        return self.__parent__._cast(_4735.CoaxialConnectionCompoundParametricStudyTool)

    @property
    def cycloidal_disc_central_bearing_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4755.CycloidalDiscCentralBearingConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4755,
        )

        return self.__parent__._cast(
            _4755.CycloidalDiscCentralBearingConnectionCompoundParametricStudyTool
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4757.CycloidalDiscPlanetaryBearingConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4757,
        )

        return self.__parent__._cast(
            _4757.CycloidalDiscPlanetaryBearingConnectionCompoundParametricStudyTool
        )

    @property
    def planetary_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4796.PlanetaryConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4796,
        )

        return self.__parent__._cast(
            _4796.PlanetaryConnectionCompoundParametricStudyTool
        )

    @property
    def shaft_to_mountable_component_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4810.ShaftToMountableComponentConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4810,
        )

        return self.__parent__._cast(
            _4810.ShaftToMountableComponentConnectionCompoundParametricStudyTool
        )

    @property
    def abstract_shaft_to_mountable_component_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "AbstractShaftToMountableComponentConnectionCompoundParametricStudyTool":
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
class AbstractShaftToMountableComponentConnectionCompoundParametricStudyTool(
    _4746.ConnectionCompoundParametricStudyTool
):
    """AbstractShaftToMountableComponentConnectionCompoundParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_PARAMETRIC_STUDY_TOOL
    )

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
    ) -> "List[_4564.AbstractShaftToMountableComponentConnectionParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.AbstractShaftToMountableComponentConnectionParametricStudyTool]

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
    ) -> "List[_4564.AbstractShaftToMountableComponentConnectionParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.AbstractShaftToMountableComponentConnectionParametricStudyTool]

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
    ) -> "_Cast_AbstractShaftToMountableComponentConnectionCompoundParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftToMountableComponentConnectionCompoundParametricStudyTool
        """
        return _Cast_AbstractShaftToMountableComponentConnectionCompoundParametricStudyTool(
            self
        )
