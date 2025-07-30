"""CylindricalMeshLoadDistributionAtRotation"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.ltca import _945

_CYLINDRICAL_MESH_LOAD_DISTRIBUTION_AT_ROTATION = python_net_import(
    "SMT.MastaAPI.Gears.LTCA.Cylindrical", "CylindricalMeshLoadDistributionAtRotation"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1234
    from mastapy._private.gears.ltca.cylindrical import _961

    Self = TypeVar("Self", bound="CylindricalMeshLoadDistributionAtRotation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalMeshLoadDistributionAtRotation._Cast_CylindricalMeshLoadDistributionAtRotation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalMeshLoadDistributionAtRotation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalMeshLoadDistributionAtRotation:
    """Special nested class for casting CylindricalMeshLoadDistributionAtRotation to subclasses."""

    __parent__: "CylindricalMeshLoadDistributionAtRotation"

    @property
    def gear_mesh_load_distribution_at_rotation(
        self: "CastSelf",
    ) -> "_945.GearMeshLoadDistributionAtRotation":
        return self.__parent__._cast(_945.GearMeshLoadDistributionAtRotation)

    @property
    def cylindrical_mesh_load_distribution_at_rotation(
        self: "CastSelf",
    ) -> "CylindricalMeshLoadDistributionAtRotation":
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
class CylindricalMeshLoadDistributionAtRotation(
    _945.GearMeshLoadDistributionAtRotation
):
    """CylindricalMeshLoadDistributionAtRotation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_MESH_LOAD_DISTRIBUTION_AT_ROTATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def mesh_alignment(self: "Self") -> "_1234.MeshAlignment":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.MeshAlignment

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshAlignment")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def loaded_contact_lines(
        self: "Self",
    ) -> "List[_961.CylindricalGearMeshLoadedContactLine]":
        """List[mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactLine]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadedContactLines")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalMeshLoadDistributionAtRotation":
        """Cast to another type.

        Returns:
            _Cast_CylindricalMeshLoadDistributionAtRotation
        """
        return _Cast_CylindricalMeshLoadDistributionAtRotation(self)
