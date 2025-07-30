"""GearMeshBothFlankContacts"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_GEAR_MESH_BOTH_FLANK_CONTACTS = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.NodalEntities.ExternalForce",
    "GearMeshBothFlankContacts",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.nodal_entities.external_force import _172, _175

    Self = TypeVar("Self", bound="GearMeshBothFlankContacts")
    CastSelf = TypeVar(
        "CastSelf", bound="GearMeshBothFlankContacts._Cast_GearMeshBothFlankContacts"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshBothFlankContacts",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMeshBothFlankContacts:
    """Special nested class for casting GearMeshBothFlankContacts to subclasses."""

    __parent__: "GearMeshBothFlankContacts"

    @property
    def gear_mesh_both_flank_contacts(self: "CastSelf") -> "GearMeshBothFlankContacts":
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
class GearMeshBothFlankContacts(_0.APIBase):
    """GearMeshBothFlankContacts

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESH_BOTH_FLANK_CONTACTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def left_flank(self: "Self") -> "_172.ExternalForceLineContactEntity":
        """mastapy.nodal_analysis.nodal_entities.external_force.ExternalForceLineContactEntity

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeftFlank")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def left_flank_gear(self: "Self") -> "_175.GearMeshDirectSingleFlankContact":
        """mastapy.nodal_analysis.nodal_entities.external_force.GearMeshDirectSingleFlankContact

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeftFlankGear")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def right_flank(self: "Self") -> "_172.ExternalForceLineContactEntity":
        """mastapy.nodal_analysis.nodal_entities.external_force.ExternalForceLineContactEntity

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RightFlank")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def right_flank_gear(self: "Self") -> "_175.GearMeshDirectSingleFlankContact":
        """mastapy.nodal_analysis.nodal_entities.external_force.GearMeshDirectSingleFlankContact

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RightFlankGear")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_GearMeshBothFlankContacts":
        """Cast to another type.

        Returns:
            _Cast_GearMeshBothFlankContacts
        """
        return _Cast_GearMeshBothFlankContacts(self)
