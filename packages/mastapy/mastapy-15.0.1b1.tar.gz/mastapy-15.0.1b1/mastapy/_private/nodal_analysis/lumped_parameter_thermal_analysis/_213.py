"""SimpleVolumetricFlowRateNode"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import _210

_SIMPLE_VOLUMETRIC_FLOW_RATE_NODE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.LumpedParameterThermalAnalysis",
    "SimpleVolumetricFlowRateNode",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SimpleVolumetricFlowRateNode")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SimpleVolumetricFlowRateNode._Cast_SimpleVolumetricFlowRateNode",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SimpleVolumetricFlowRateNode",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SimpleVolumetricFlowRateNode:
    """Special nested class for casting SimpleVolumetricFlowRateNode to subclasses."""

    __parent__: "SimpleVolumetricFlowRateNode"

    @property
    def simple_node(self: "CastSelf") -> "_210.SimpleNode":
        return self.__parent__._cast(_210.SimpleNode)

    @property
    def simple_volumetric_flow_rate_node(
        self: "CastSelf",
    ) -> "SimpleVolumetricFlowRateNode":
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
class SimpleVolumetricFlowRateNode(_210.SimpleNode):
    """SimpleVolumetricFlowRateNode

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SIMPLE_VOLUMETRIC_FLOW_RATE_NODE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_SimpleVolumetricFlowRateNode":
        """Cast to another type.

        Returns:
            _Cast_SimpleVolumetricFlowRateNode
        """
        return _Cast_SimpleVolumetricFlowRateNode(self)
