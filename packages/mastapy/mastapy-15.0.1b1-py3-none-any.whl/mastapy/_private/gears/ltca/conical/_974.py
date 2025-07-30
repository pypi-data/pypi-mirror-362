"""ConicalMeshLoadDistributionAtRotation"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.ltca import _945

_CONICAL_MESH_LOAD_DISTRIBUTION_AT_ROTATION = python_net_import(
    "SMT.MastaAPI.Gears.LTCA.Conical", "ConicalMeshLoadDistributionAtRotation"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ConicalMeshLoadDistributionAtRotation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalMeshLoadDistributionAtRotation._Cast_ConicalMeshLoadDistributionAtRotation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalMeshLoadDistributionAtRotation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalMeshLoadDistributionAtRotation:
    """Special nested class for casting ConicalMeshLoadDistributionAtRotation to subclasses."""

    __parent__: "ConicalMeshLoadDistributionAtRotation"

    @property
    def gear_mesh_load_distribution_at_rotation(
        self: "CastSelf",
    ) -> "_945.GearMeshLoadDistributionAtRotation":
        return self.__parent__._cast(_945.GearMeshLoadDistributionAtRotation)

    @property
    def conical_mesh_load_distribution_at_rotation(
        self: "CastSelf",
    ) -> "ConicalMeshLoadDistributionAtRotation":
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
class ConicalMeshLoadDistributionAtRotation(_945.GearMeshLoadDistributionAtRotation):
    """ConicalMeshLoadDistributionAtRotation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_MESH_LOAD_DISTRIBUTION_AT_ROTATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalMeshLoadDistributionAtRotation":
        """Cast to another type.

        Returns:
            _Cast_ConicalMeshLoadDistributionAtRotation
        """
        return _Cast_ConicalMeshLoadDistributionAtRotation(self)
