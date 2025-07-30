"""GearMeshDirectSingleFlankContact"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_GEAR_MESH_DIRECT_SINGLE_FLANK_CONTACT = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.NodalEntities.ExternalForce",
    "GearMeshDirectSingleFlankContact",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="GearMeshDirectSingleFlankContact")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearMeshDirectSingleFlankContact._Cast_GearMeshDirectSingleFlankContact",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshDirectSingleFlankContact",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMeshDirectSingleFlankContact:
    """Special nested class for casting GearMeshDirectSingleFlankContact to subclasses."""

    __parent__: "GearMeshDirectSingleFlankContact"

    @property
    def gear_mesh_direct_single_flank_contact(
        self: "CastSelf",
    ) -> "GearMeshDirectSingleFlankContact":
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
class GearMeshDirectSingleFlankContact(_0.APIBase):
    """GearMeshDirectSingleFlankContact

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESH_DIRECT_SINGLE_FLANK_CONTACT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def centre_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CentreDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def working_transverse_pressure_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WorkingTransversePressureAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_GearMeshDirectSingleFlankContact":
        """Cast to another type.

        Returns:
            _Cast_GearMeshDirectSingleFlankContact
        """
        return _Cast_GearMeshDirectSingleFlankContact(self)
