"""RigidlyConnectedDesignEntityGroupModalAnalysis"""

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
from mastapy._private.system_model.analyses_and_results import _2893

_RIGIDLY_CONNECTED_DESIGN_ENTITY_GROUP_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Reporting",
    "RigidlyConnectedDesignEntityGroupModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.utility.modal_analysis import _1993

    Self = TypeVar("Self", bound="RigidlyConnectedDesignEntityGroupModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RigidlyConnectedDesignEntityGroupModalAnalysis._Cast_RigidlyConnectedDesignEntityGroupModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RigidlyConnectedDesignEntityGroupModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RigidlyConnectedDesignEntityGroupModalAnalysis:
    """Special nested class for casting RigidlyConnectedDesignEntityGroupModalAnalysis to subclasses."""

    __parent__: "RigidlyConnectedDesignEntityGroupModalAnalysis"

    @property
    def design_entity_group_analysis(
        self: "CastSelf",
    ) -> "_2893.DesignEntityGroupAnalysis":
        return self.__parent__._cast(_2893.DesignEntityGroupAnalysis)

    @property
    def rigidly_connected_design_entity_group_modal_analysis(
        self: "CastSelf",
    ) -> "RigidlyConnectedDesignEntityGroupModalAnalysis":
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
class RigidlyConnectedDesignEntityGroupModalAnalysis(_2893.DesignEntityGroupAnalysis):
    """RigidlyConnectedDesignEntityGroupModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RIGIDLY_CONNECTED_DESIGN_ENTITY_GROUP_MODAL_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def excitation_frequencies_at_reference_speed(
        self: "Self",
    ) -> "List[_1993.DesignEntityExcitationDescription]":
        """List[mastapy.utility.modal_analysis.DesignEntityExcitationDescription]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ExcitationFrequenciesAtReferenceSpeed"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_RigidlyConnectedDesignEntityGroupModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_RigidlyConnectedDesignEntityGroupModalAnalysis
        """
        return _Cast_RigidlyConnectedDesignEntityGroupModalAnalysis(self)
