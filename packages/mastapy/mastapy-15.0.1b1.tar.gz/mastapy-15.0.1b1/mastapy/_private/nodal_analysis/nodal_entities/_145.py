"""FlowJunctionNodalComponent"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.nodal_entities import _153

_FLOW_JUNCTION_NODAL_COMPONENT = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.NodalEntities", "FlowJunctionNodalComponent"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.nodal_entities import _155

    Self = TypeVar("Self", bound="FlowJunctionNodalComponent")
    CastSelf = TypeVar(
        "CastSelf", bound="FlowJunctionNodalComponent._Cast_FlowJunctionNodalComponent"
    )


__docformat__ = "restructuredtext en"
__all__ = ("FlowJunctionNodalComponent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FlowJunctionNodalComponent:
    """Special nested class for casting FlowJunctionNodalComponent to subclasses."""

    __parent__: "FlowJunctionNodalComponent"

    @property
    def nodal_component(self: "CastSelf") -> "_153.NodalComponent":
        return self.__parent__._cast(_153.NodalComponent)

    @property
    def nodal_entity(self: "CastSelf") -> "_155.NodalEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _155

        return self.__parent__._cast(_155.NodalEntity)

    @property
    def flow_junction_nodal_component(self: "CastSelf") -> "FlowJunctionNodalComponent":
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
class FlowJunctionNodalComponent(_153.NodalComponent):
    """FlowJunctionNodalComponent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FLOW_JUNCTION_NODAL_COMPONENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_FlowJunctionNodalComponent":
        """Cast to another type.

        Returns:
            _Cast_FlowJunctionNodalComponent
        """
        return _Cast_FlowJunctionNodalComponent(self)
