"""RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_RIGIDLY_CONNECTED_DESIGN_ENTITY_GROUP_FOR_SINGLE_MODE_MODAL_ANALYSIS = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Reporting",
        "RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis",
    )
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
        _4991,
        _4995,
    )

    Self = TypeVar(
        "Self", bound="RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis._Cast_RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis:
    """Special nested class for casting RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis to subclasses."""

    __parent__: "RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis"

    @property
    def rigidly_connected_design_entity_group_for_single_excitation_modal_analysis(
        self: "CastSelf",
    ) -> "_4995.RigidlyConnectedDesignEntityGroupForSingleExcitationModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
            _4995,
        )

        return self.__parent__._cast(
            _4995.RigidlyConnectedDesignEntityGroupForSingleExcitationModalAnalysis
        )

    @property
    def rigidly_connected_design_entity_group_for_single_mode_modal_analysis(
        self: "CastSelf",
    ) -> "RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis":
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
class RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis(_0.APIBase):
    """RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _RIGIDLY_CONNECTED_DESIGN_ENTITY_GROUP_FOR_SINGLE_MODE_MODAL_ANALYSIS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def mode_frequency(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModeFrequency")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mode_id(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModeID")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def percentage_kinetic_energy(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PercentageKineticEnergy")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def percentage_strain_energy(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PercentageStrainEnergy")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def shaft_names(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftNames")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def component_results(self: "Self") -> "List[_4991.ComponentPerModeResult]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.reporting.ComponentPerModeResult]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis
        """
        return _Cast_RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis(self)
