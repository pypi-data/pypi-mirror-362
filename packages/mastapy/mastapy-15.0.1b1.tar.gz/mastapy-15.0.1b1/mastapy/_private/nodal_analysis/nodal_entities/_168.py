"""TorsionalFrictionNodePairBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.nodal_entities import _143

_TORSIONAL_FRICTION_NODE_PAIR_BASE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.NodalEntities", "TorsionalFrictionNodePairBase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.nodal_entities import (
        _141,
        _154,
        _155,
        _167,
        _169,
        _170,
    )

    Self = TypeVar("Self", bound="TorsionalFrictionNodePairBase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="TorsionalFrictionNodePairBase._Cast_TorsionalFrictionNodePairBase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("TorsionalFrictionNodePairBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TorsionalFrictionNodePairBase:
    """Special nested class for casting TorsionalFrictionNodePairBase to subclasses."""

    __parent__: "TorsionalFrictionNodePairBase"

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
    def torsional_friction_node_pair(
        self: "CastSelf",
    ) -> "_167.TorsionalFrictionNodePair":
        from mastapy._private.nodal_analysis.nodal_entities import _167

        return self.__parent__._cast(_167.TorsionalFrictionNodePair)

    @property
    def torsional_friction_node_pair_simple_locked_stiffness(
        self: "CastSelf",
    ) -> "_169.TorsionalFrictionNodePairSimpleLockedStiffness":
        from mastapy._private.nodal_analysis.nodal_entities import _169

        return self.__parent__._cast(
            _169.TorsionalFrictionNodePairSimpleLockedStiffness
        )

    @property
    def torsional_friction_node_pair_base(
        self: "CastSelf",
    ) -> "TorsionalFrictionNodePairBase":
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
class TorsionalFrictionNodePairBase(_143.ConcentricConnectionNodalComponentBase):
    """TorsionalFrictionNodePairBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TORSIONAL_FRICTION_NODE_PAIR_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_TorsionalFrictionNodePairBase":
        """Cast to another type.

        Returns:
            _Cast_TorsionalFrictionNodePairBase
        """
        return _Cast_TorsionalFrictionNodePairBase(self)
