"""ExternalForceEntity"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.nodal_entities import _153

_EXTERNAL_FORCE_ENTITY = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.NodalEntities.ExternalForce", "ExternalForceEntity"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.nodal_entities import _155
    from mastapy._private.nodal_analysis.nodal_entities.external_force import _172, _173

    Self = TypeVar("Self", bound="ExternalForceEntity")
    CastSelf = TypeVar(
        "CastSelf", bound="ExternalForceEntity._Cast_ExternalForceEntity"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ExternalForceEntity",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ExternalForceEntity:
    """Special nested class for casting ExternalForceEntity to subclasses."""

    __parent__: "ExternalForceEntity"

    @property
    def nodal_component(self: "CastSelf") -> "_153.NodalComponent":
        return self.__parent__._cast(_153.NodalComponent)

    @property
    def nodal_entity(self: "CastSelf") -> "_155.NodalEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _155

        return self.__parent__._cast(_155.NodalEntity)

    @property
    def external_force_line_contact_entity(
        self: "CastSelf",
    ) -> "_172.ExternalForceLineContactEntity":
        from mastapy._private.nodal_analysis.nodal_entities.external_force import _172

        return self.__parent__._cast(_172.ExternalForceLineContactEntity)

    @property
    def external_force_single_point_entity(
        self: "CastSelf",
    ) -> "_173.ExternalForceSinglePointEntity":
        from mastapy._private.nodal_analysis.nodal_entities.external_force import _173

        return self.__parent__._cast(_173.ExternalForceSinglePointEntity)

    @property
    def external_force_entity(self: "CastSelf") -> "ExternalForceEntity":
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
class ExternalForceEntity(_153.NodalComponent):
    """ExternalForceEntity

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _EXTERNAL_FORCE_ENTITY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ExternalForceEntity":
        """Cast to another type.

        Returns:
            _Cast_ExternalForceEntity
        """
        return _Cast_ExternalForceEntity(self)
