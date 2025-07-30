"""CylindricalGearMeshLoadedContactLine"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.ltca import _946

_CYLINDRICAL_GEAR_MESH_LOADED_CONTACT_LINE = python_net_import(
    "SMT.MastaAPI.Gears.LTCA.Cylindrical", "CylindricalGearMeshLoadedContactLine"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.ltca.cylindrical import _962

    Self = TypeVar("Self", bound="CylindricalGearMeshLoadedContactLine")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearMeshLoadedContactLine._Cast_CylindricalGearMeshLoadedContactLine",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearMeshLoadedContactLine",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearMeshLoadedContactLine:
    """Special nested class for casting CylindricalGearMeshLoadedContactLine to subclasses."""

    __parent__: "CylindricalGearMeshLoadedContactLine"

    @property
    def gear_mesh_loaded_contact_line(
        self: "CastSelf",
    ) -> "_946.GearMeshLoadedContactLine":
        return self.__parent__._cast(_946.GearMeshLoadedContactLine)

    @property
    def cylindrical_gear_mesh_loaded_contact_line(
        self: "CastSelf",
    ) -> "CylindricalGearMeshLoadedContactLine":
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
class CylindricalGearMeshLoadedContactLine(_946.GearMeshLoadedContactLine):
    """CylindricalGearMeshLoadedContactLine

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_MESH_LOADED_CONTACT_LINE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def loaded_contact_strip_end_points(
        self: "Self",
    ) -> "List[_962.CylindricalGearMeshLoadedContactPoint]":
        """List[mastapy.gears.ltca.cylindrical.CylindricalGearMeshLoadedContactPoint]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadedContactStripEndPoints")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearMeshLoadedContactLine":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearMeshLoadedContactLine
        """
        return _Cast_CylindricalGearMeshLoadedContactLine(self)
