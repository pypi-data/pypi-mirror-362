"""CylindricalGearMeshTIFFAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.analysis import _1342

_CYLINDRICAL_GEAR_MESH_TIFF_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.GearTwoDFEAnalysis", "CylindricalGearMeshTIFFAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1336

    Self = TypeVar("Self", bound="CylindricalGearMeshTIFFAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearMeshTIFFAnalysis._Cast_CylindricalGearMeshTIFFAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearMeshTIFFAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearMeshTIFFAnalysis:
    """Special nested class for casting CylindricalGearMeshTIFFAnalysis to subclasses."""

    __parent__: "CylindricalGearMeshTIFFAnalysis"

    @property
    def gear_mesh_design_analysis(self: "CastSelf") -> "_1342.GearMeshDesignAnalysis":
        return self.__parent__._cast(_1342.GearMeshDesignAnalysis)

    @property
    def abstract_gear_mesh_analysis(
        self: "CastSelf",
    ) -> "_1336.AbstractGearMeshAnalysis":
        from mastapy._private.gears.analysis import _1336

        return self.__parent__._cast(_1336.AbstractGearMeshAnalysis)

    @property
    def cylindrical_gear_mesh_tiff_analysis(
        self: "CastSelf",
    ) -> "CylindricalGearMeshTIFFAnalysis":
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
class CylindricalGearMeshTIFFAnalysis(_1342.GearMeshDesignAnalysis):
    """CylindricalGearMeshTIFFAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_MESH_TIFF_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearMeshTIFFAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearMeshTIFFAnalysis
        """
        return _Cast_CylindricalGearMeshTIFFAnalysis(self)
