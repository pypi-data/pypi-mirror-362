"""CycloidalDiscCentralBearingConnectionCompoundParametricStudyTool"""

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
    _4735,
)

_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_COMPOUND_PARAMETRIC_STUDY_TOOL = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound",
        "CycloidalDiscCentralBearingConnectionCompoundParametricStudyTool",
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
        _4605,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
        _4714,
        _4746,
        _4810,
    )

    Self = TypeVar(
        "Self", bound="CycloidalDiscCentralBearingConnectionCompoundParametricStudyTool"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="CycloidalDiscCentralBearingConnectionCompoundParametricStudyTool._Cast_CycloidalDiscCentralBearingConnectionCompoundParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CycloidalDiscCentralBearingConnectionCompoundParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CycloidalDiscCentralBearingConnectionCompoundParametricStudyTool:
    """Special nested class for casting CycloidalDiscCentralBearingConnectionCompoundParametricStudyTool to subclasses."""

    __parent__: "CycloidalDiscCentralBearingConnectionCompoundParametricStudyTool"

    @property
    def coaxial_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4735.CoaxialConnectionCompoundParametricStudyTool":
        return self.__parent__._cast(_4735.CoaxialConnectionCompoundParametricStudyTool)

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
    ) -> "_4714.AbstractShaftToMountableComponentConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4714,
        )

        return self.__parent__._cast(
            _4714.AbstractShaftToMountableComponentConnectionCompoundParametricStudyTool
        )

    @property
    def connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4746.ConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4746,
        )

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
    def cycloidal_disc_central_bearing_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "CycloidalDiscCentralBearingConnectionCompoundParametricStudyTool":
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
class CycloidalDiscCentralBearingConnectionCompoundParametricStudyTool(
    _4735.CoaxialConnectionCompoundParametricStudyTool
):
    """CycloidalDiscCentralBearingConnectionCompoundParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_COMPOUND_PARAMETRIC_STUDY_TOOL
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4605.CycloidalDiscCentralBearingConnectionParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.CycloidalDiscCentralBearingConnectionParametricStudyTool]

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
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_4605.CycloidalDiscCentralBearingConnectionParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.CycloidalDiscCentralBearingConnectionParametricStudyTool]

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_CycloidalDiscCentralBearingConnectionCompoundParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_CycloidalDiscCentralBearingConnectionCompoundParametricStudyTool
        """
        return _Cast_CycloidalDiscCentralBearingConnectionCompoundParametricStudyTool(
            self
        )
