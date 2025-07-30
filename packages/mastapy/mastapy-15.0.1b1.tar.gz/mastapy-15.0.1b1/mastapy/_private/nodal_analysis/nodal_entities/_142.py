"""ConcentricConnectionNodalComponent"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.nodal_entities import _143

_CONCENTRIC_CONNECTION_NODAL_COMPONENT = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.NodalEntities", "ConcentricConnectionNodalComponent"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.nodal_entities import _141, _154, _155, _170

    Self = TypeVar("Self", bound="ConcentricConnectionNodalComponent")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConcentricConnectionNodalComponent._Cast_ConcentricConnectionNodalComponent",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConcentricConnectionNodalComponent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConcentricConnectionNodalComponent:
    """Special nested class for casting ConcentricConnectionNodalComponent to subclasses."""

    __parent__: "ConcentricConnectionNodalComponent"

    @property
    def concentric_connection_nodal_component_base(
        self: "CastSelf",
    ) -> "_143.ConcentricConnectionNodalComponentBase":
        return self.__parent__._cast(_143.ConcentricConnectionNodalComponentBase)

    @property
    def two_body_connection_nodal_component(
        self: "CastSelf",
    ) -> "_170.TwoBodyConnectionNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _170

        return self.__parent__._cast(_170.TwoBodyConnectionNodalComponent)

    @property
    def component_nodal_composite_base(
        self: "CastSelf",
    ) -> "_141.ComponentNodalCompositeBase":
        from mastapy._private.nodal_analysis.nodal_entities import _141

        return self.__parent__._cast(_141.ComponentNodalCompositeBase)

    @property
    def nodal_composite(self: "CastSelf") -> "_154.NodalComposite":
        from mastapy._private.nodal_analysis.nodal_entities import _154

        return self.__parent__._cast(_154.NodalComposite)

    @property
    def nodal_entity(self: "CastSelf") -> "_155.NodalEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _155

        return self.__parent__._cast(_155.NodalEntity)

    @property
    def concentric_connection_nodal_component(
        self: "CastSelf",
    ) -> "ConcentricConnectionNodalComponent":
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
class ConcentricConnectionNodalComponent(_143.ConcentricConnectionNodalComponentBase):
    """ConcentricConnectionNodalComponent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONCENTRIC_CONNECTION_NODAL_COMPONENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConcentricConnectionNodalComponent":
        """Cast to another type.

        Returns:
            _Cast_ConcentricConnectionNodalComponent
        """
        return _Cast_ConcentricConnectionNodalComponent(self)
