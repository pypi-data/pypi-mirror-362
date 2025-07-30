"""TwoBodyConnectionNodalComponent"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.nodal_entities import _141

_TWO_BODY_CONNECTION_NODAL_COMPONENT = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.NodalEntities", "TwoBodyConnectionNodalComponent"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.nodal_entities import (
        _142,
        _143,
        _149,
        _154,
        _155,
        _161,
        _167,
        _168,
        _169,
    )

    Self = TypeVar("Self", bound="TwoBodyConnectionNodalComponent")
    CastSelf = TypeVar(
        "CastSelf",
        bound="TwoBodyConnectionNodalComponent._Cast_TwoBodyConnectionNodalComponent",
    )


__docformat__ = "restructuredtext en"
__all__ = ("TwoBodyConnectionNodalComponent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TwoBodyConnectionNodalComponent:
    """Special nested class for casting TwoBodyConnectionNodalComponent to subclasses."""

    __parent__: "TwoBodyConnectionNodalComponent"

    @property
    def component_nodal_composite_base(
        self: "CastSelf",
    ) -> "_141.ComponentNodalCompositeBase":
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
    ) -> "_142.ConcentricConnectionNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _142

        return self.__parent__._cast(_142.ConcentricConnectionNodalComponent)

    @property
    def concentric_connection_nodal_component_base(
        self: "CastSelf",
    ) -> "_143.ConcentricConnectionNodalComponentBase":
        from mastapy._private.nodal_analysis.nodal_entities import _143

        return self.__parent__._cast(_143.ConcentricConnectionNodalComponentBase)

    @property
    def gear_mesh_point_on_flank_contact(
        self: "CastSelf",
    ) -> "_149.GearMeshPointOnFlankContact":
        from mastapy._private.nodal_analysis.nodal_entities import _149

        return self.__parent__._cast(_149.GearMeshPointOnFlankContact)

    @property
    def simple_bar(self: "CastSelf") -> "_161.SimpleBar":
        from mastapy._private.nodal_analysis.nodal_entities import _161

        return self.__parent__._cast(_161.SimpleBar)

    @property
    def torsional_friction_node_pair(
        self: "CastSelf",
    ) -> "_167.TorsionalFrictionNodePair":
        from mastapy._private.nodal_analysis.nodal_entities import _167

        return self.__parent__._cast(_167.TorsionalFrictionNodePair)

    @property
    def torsional_friction_node_pair_base(
        self: "CastSelf",
    ) -> "_168.TorsionalFrictionNodePairBase":
        from mastapy._private.nodal_analysis.nodal_entities import _168

        return self.__parent__._cast(_168.TorsionalFrictionNodePairBase)

    @property
    def torsional_friction_node_pair_simple_locked_stiffness(
        self: "CastSelf",
    ) -> "_169.TorsionalFrictionNodePairSimpleLockedStiffness":
        from mastapy._private.nodal_analysis.nodal_entities import _169

        return self.__parent__._cast(
            _169.TorsionalFrictionNodePairSimpleLockedStiffness
        )

    @property
    def two_body_connection_nodal_component(
        self: "CastSelf",
    ) -> "TwoBodyConnectionNodalComponent":
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
class TwoBodyConnectionNodalComponent(_141.ComponentNodalCompositeBase):
    """TwoBodyConnectionNodalComponent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TWO_BODY_CONNECTION_NODAL_COMPONENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_TwoBodyConnectionNodalComponent":
        """Cast to another type.

        Returns:
            _Cast_TwoBodyConnectionNodalComponent
        """
        return _Cast_TwoBodyConnectionNodalComponent(self)
