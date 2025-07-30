"""GearMeshImplementationAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.analysis import _1342

_GEAR_MESH_IMPLEMENTATION_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.Analysis", "GearMeshImplementationAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1336
    from mastapy._private.gears.ltca import _944
    from mastapy._private.gears.ltca.conical import _973
    from mastapy._private.gears.ltca.cylindrical import _960
    from mastapy._private.gears.manufacturing.bevel import _887
    from mastapy._private.gears.manufacturing.cylindrical import _722

    Self = TypeVar("Self", bound="GearMeshImplementationAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearMeshImplementationAnalysis._Cast_GearMeshImplementationAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshImplementationAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMeshImplementationAnalysis:
    """Special nested class for casting GearMeshImplementationAnalysis to subclasses."""

    __parent__: "GearMeshImplementationAnalysis"

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
    def cylindrical_manufactured_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_722.CylindricalManufacturedGearMeshLoadCase":
        from mastapy._private.gears.manufacturing.cylindrical import _722

        return self.__parent__._cast(_722.CylindricalManufacturedGearMeshLoadCase)

    @property
    def conical_mesh_manufacturing_analysis(
        self: "CastSelf",
    ) -> "_887.ConicalMeshManufacturingAnalysis":
        from mastapy._private.gears.manufacturing.bevel import _887

        return self.__parent__._cast(_887.ConicalMeshManufacturingAnalysis)

    @property
    def gear_mesh_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_944.GearMeshLoadDistributionAnalysis":
        from mastapy._private.gears.ltca import _944

        return self.__parent__._cast(_944.GearMeshLoadDistributionAnalysis)

    @property
    def cylindrical_gear_mesh_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_960.CylindricalGearMeshLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.cylindrical import _960

        return self.__parent__._cast(_960.CylindricalGearMeshLoadDistributionAnalysis)

    @property
    def conical_mesh_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_973.ConicalMeshLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.conical import _973

        return self.__parent__._cast(_973.ConicalMeshLoadDistributionAnalysis)

    @property
    def gear_mesh_implementation_analysis(
        self: "CastSelf",
    ) -> "GearMeshImplementationAnalysis":
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
class GearMeshImplementationAnalysis(_1342.GearMeshDesignAnalysis):
    """GearMeshImplementationAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESH_IMPLEMENTATION_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_GearMeshImplementationAnalysis":
        """Cast to another type.

        Returns:
            _Cast_GearMeshImplementationAnalysis
        """
        return _Cast_GearMeshImplementationAnalysis(self)
