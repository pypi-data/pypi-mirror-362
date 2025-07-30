"""ArbitraryNodalComponentBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.nodal_entities import _153

_ARBITRARY_NODAL_COMPONENT_BASE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.NodalEntities", "ArbitraryNodalComponentBase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.nodal_entities import (
        _130,
        _138,
        _139,
        _148,
        _152,
        _155,
        _163,
    )

    Self = TypeVar("Self", bound="ArbitraryNodalComponentBase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ArbitraryNodalComponentBase._Cast_ArbitraryNodalComponentBase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ArbitraryNodalComponentBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ArbitraryNodalComponentBase:
    """Special nested class for casting ArbitraryNodalComponentBase to subclasses."""

    __parent__: "ArbitraryNodalComponentBase"

    @property
    def nodal_component(self: "CastSelf") -> "_153.NodalComponent":
        return self.__parent__._cast(_153.NodalComponent)

    @property
    def nodal_entity(self: "CastSelf") -> "_155.NodalEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _155

        return self.__parent__._cast(_155.NodalEntity)

    @property
    def arbitrary_nodal_component(self: "CastSelf") -> "_130.ArbitraryNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _130

        return self.__parent__._cast(_130.ArbitraryNodalComponent)

    @property
    def bearing_axial_mounting_clearance(
        self: "CastSelf",
    ) -> "_138.BearingAxialMountingClearance":
        from mastapy._private.nodal_analysis.nodal_entities import _138

        return self.__parent__._cast(_138.BearingAxialMountingClearance)

    @property
    def cms_nodal_component(self: "CastSelf") -> "_139.CMSNodalComponent":
        from mastapy._private.nodal_analysis.nodal_entities import _139

        return self.__parent__._cast(_139.CMSNodalComponent)

    @property
    def gear_mesh_node_pair(self: "CastSelf") -> "_148.GearMeshNodePair":
        from mastapy._private.nodal_analysis.nodal_entities import _148

        return self.__parent__._cast(_148.GearMeshNodePair)

    @property
    def line_contact_stiffness_entity(
        self: "CastSelf",
    ) -> "_152.LineContactStiffnessEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _152

        return self.__parent__._cast(_152.LineContactStiffnessEntity)

    @property
    def surface_to_surface_contact_stiffness_entity(
        self: "CastSelf",
    ) -> "_163.SurfaceToSurfaceContactStiffnessEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _163

        return self.__parent__._cast(_163.SurfaceToSurfaceContactStiffnessEntity)

    @property
    def arbitrary_nodal_component_base(
        self: "CastSelf",
    ) -> "ArbitraryNodalComponentBase":
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
class ArbitraryNodalComponentBase(_153.NodalComponent):
    """ArbitraryNodalComponentBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ARBITRARY_NODAL_COMPONENT_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ArbitraryNodalComponentBase":
        """Cast to another type.

        Returns:
            _Cast_ArbitraryNodalComponentBase
        """
        return _Cast_ArbitraryNodalComponentBase(self)
