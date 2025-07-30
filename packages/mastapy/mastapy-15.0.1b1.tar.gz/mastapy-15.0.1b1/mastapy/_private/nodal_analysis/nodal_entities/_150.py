"""GearMeshSingleFlankContact"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.nodal_entities import _154

_GEAR_MESH_SINGLE_FLANK_CONTACT = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.NodalEntities", "GearMeshSingleFlankContact"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.nodal_entities import _155

    Self = TypeVar("Self", bound="GearMeshSingleFlankContact")
    CastSelf = TypeVar(
        "CastSelf", bound="GearMeshSingleFlankContact._Cast_GearMeshSingleFlankContact"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshSingleFlankContact",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMeshSingleFlankContact:
    """Special nested class for casting GearMeshSingleFlankContact to subclasses."""

    __parent__: "GearMeshSingleFlankContact"

    @property
    def nodal_composite(self: "CastSelf") -> "_154.NodalComposite":
        return self.__parent__._cast(_154.NodalComposite)

    @property
    def nodal_entity(self: "CastSelf") -> "_155.NodalEntity":
        from mastapy._private.nodal_analysis.nodal_entities import _155

        return self.__parent__._cast(_155.NodalEntity)

    @property
    def gear_mesh_single_flank_contact(
        self: "CastSelf",
    ) -> "GearMeshSingleFlankContact":
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
class GearMeshSingleFlankContact(_154.NodalComposite):
    """GearMeshSingleFlankContact

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESH_SINGLE_FLANK_CONTACT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_GearMeshSingleFlankContact":
        """Cast to another type.

        Returns:
            _Cast_GearMeshSingleFlankContact
        """
        return _Cast_GearMeshSingleFlankContact(self)
