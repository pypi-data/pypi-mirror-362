"""RigidlyConnectedDesignEntityGroupForSingleExcitationModalAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
    _4996,
)

_RIGIDLY_CONNECTED_DESIGN_ENTITY_GROUP_FOR_SINGLE_EXCITATION_MODAL_ANALYSIS = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Reporting",
        "RigidlyConnectedDesignEntityGroupForSingleExcitationModalAnalysis",
    )
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar(
        "Self",
        bound="RigidlyConnectedDesignEntityGroupForSingleExcitationModalAnalysis",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="RigidlyConnectedDesignEntityGroupForSingleExcitationModalAnalysis._Cast_RigidlyConnectedDesignEntityGroupForSingleExcitationModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RigidlyConnectedDesignEntityGroupForSingleExcitationModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RigidlyConnectedDesignEntityGroupForSingleExcitationModalAnalysis:
    """Special nested class for casting RigidlyConnectedDesignEntityGroupForSingleExcitationModalAnalysis to subclasses."""

    __parent__: "RigidlyConnectedDesignEntityGroupForSingleExcitationModalAnalysis"

    @property
    def rigidly_connected_design_entity_group_for_single_mode_modal_analysis(
        self: "CastSelf",
    ) -> "_4996.RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis":
        return self.__parent__._cast(
            _4996.RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis
        )

    @property
    def rigidly_connected_design_entity_group_for_single_excitation_modal_analysis(
        self: "CastSelf",
    ) -> "RigidlyConnectedDesignEntityGroupForSingleExcitationModalAnalysis":
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
class RigidlyConnectedDesignEntityGroupForSingleExcitationModalAnalysis(
    _4996.RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis
):
    """RigidlyConnectedDesignEntityGroupForSingleExcitationModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _RIGIDLY_CONNECTED_DESIGN_ENTITY_GROUP_FOR_SINGLE_EXCITATION_MODAL_ANALYSIS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def reference_speed_of_crossing(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReferenceSpeedOfCrossing")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_RigidlyConnectedDesignEntityGroupForSingleExcitationModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_RigidlyConnectedDesignEntityGroupForSingleExcitationModalAnalysis
        """
        return _Cast_RigidlyConnectedDesignEntityGroupForSingleExcitationModalAnalysis(
            self
        )
