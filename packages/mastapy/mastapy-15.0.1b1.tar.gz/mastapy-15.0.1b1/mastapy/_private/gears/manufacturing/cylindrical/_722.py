"""CylindricalManufacturedGearMeshLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.analysis import _1343

_CYLINDRICAL_MANUFACTURED_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical",
    "CylindricalManufacturedGearMeshLoadCase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1336, _1342

    Self = TypeVar("Self", bound="CylindricalManufacturedGearMeshLoadCase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalManufacturedGearMeshLoadCase._Cast_CylindricalManufacturedGearMeshLoadCase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalManufacturedGearMeshLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalManufacturedGearMeshLoadCase:
    """Special nested class for casting CylindricalManufacturedGearMeshLoadCase to subclasses."""

    __parent__: "CylindricalManufacturedGearMeshLoadCase"

    @property
    def gear_mesh_implementation_analysis(
        self: "CastSelf",
    ) -> "_1343.GearMeshImplementationAnalysis":
        return self.__parent__._cast(_1343.GearMeshImplementationAnalysis)

    @property
    def gear_mesh_design_analysis(self: "CastSelf") -> "_1342.GearMeshDesignAnalysis":
        from mastapy._private.gears.analysis import _1342

        return self.__parent__._cast(_1342.GearMeshDesignAnalysis)

    @property
    def abstract_gear_mesh_analysis(
        self: "CastSelf",
    ) -> "_1336.AbstractGearMeshAnalysis":
        from mastapy._private.gears.analysis import _1336

        return self.__parent__._cast(_1336.AbstractGearMeshAnalysis)

    @property
    def cylindrical_manufactured_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "CylindricalManufacturedGearMeshLoadCase":
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
class CylindricalManufacturedGearMeshLoadCase(_1343.GearMeshImplementationAnalysis):
    """CylindricalManufacturedGearMeshLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_MANUFACTURED_GEAR_MESH_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalManufacturedGearMeshLoadCase":
        """Cast to another type.

        Returns:
            _Cast_CylindricalManufacturedGearMeshLoadCase
        """
        return _Cast_CylindricalManufacturedGearMeshLoadCase(self)
