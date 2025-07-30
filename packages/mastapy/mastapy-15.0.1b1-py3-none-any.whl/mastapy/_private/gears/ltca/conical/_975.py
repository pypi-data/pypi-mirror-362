"""ConicalMeshLoadedContactLine"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.ltca import _946

_CONICAL_MESH_LOADED_CONTACT_LINE = python_net_import(
    "SMT.MastaAPI.Gears.LTCA.Conical", "ConicalMeshLoadedContactLine"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ConicalMeshLoadedContactLine")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalMeshLoadedContactLine._Cast_ConicalMeshLoadedContactLine",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalMeshLoadedContactLine",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalMeshLoadedContactLine:
    """Special nested class for casting ConicalMeshLoadedContactLine to subclasses."""

    __parent__: "ConicalMeshLoadedContactLine"

    @property
    def gear_mesh_loaded_contact_line(
        self: "CastSelf",
    ) -> "_946.GearMeshLoadedContactLine":
        return self.__parent__._cast(_946.GearMeshLoadedContactLine)

    @property
    def conical_mesh_loaded_contact_line(
        self: "CastSelf",
    ) -> "ConicalMeshLoadedContactLine":
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
class ConicalMeshLoadedContactLine(_946.GearMeshLoadedContactLine):
    """ConicalMeshLoadedContactLine

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_MESH_LOADED_CONTACT_LINE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalMeshLoadedContactLine":
        """Cast to another type.

        Returns:
            _Cast_ConicalMeshLoadedContactLine
        """
        return _Cast_ConicalMeshLoadedContactLine(self)
