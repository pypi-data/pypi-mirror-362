"""GearMeshImplementationAnalysisDutyCycle"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.analysis import _1342

_GEAR_MESH_IMPLEMENTATION_ANALYSIS_DUTY_CYCLE = python_net_import(
    "SMT.MastaAPI.Gears.Analysis", "GearMeshImplementationAnalysisDutyCycle"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1336
    from mastapy._private.gears.manufacturing.cylindrical import _721

    Self = TypeVar("Self", bound="GearMeshImplementationAnalysisDutyCycle")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearMeshImplementationAnalysisDutyCycle._Cast_GearMeshImplementationAnalysisDutyCycle",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshImplementationAnalysisDutyCycle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMeshImplementationAnalysisDutyCycle:
    """Special nested class for casting GearMeshImplementationAnalysisDutyCycle to subclasses."""

    __parent__: "GearMeshImplementationAnalysisDutyCycle"

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
    def cylindrical_manufactured_gear_mesh_duty_cycle(
        self: "CastSelf",
    ) -> "_721.CylindricalManufacturedGearMeshDutyCycle":
        from mastapy._private.gears.manufacturing.cylindrical import _721

        return self.__parent__._cast(_721.CylindricalManufacturedGearMeshDutyCycle)

    @property
    def gear_mesh_implementation_analysis_duty_cycle(
        self: "CastSelf",
    ) -> "GearMeshImplementationAnalysisDutyCycle":
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
class GearMeshImplementationAnalysisDutyCycle(_1342.GearMeshDesignAnalysis):
    """GearMeshImplementationAnalysisDutyCycle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESH_IMPLEMENTATION_ANALYSIS_DUTY_CYCLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_GearMeshImplementationAnalysisDutyCycle":
        """Cast to another type.

        Returns:
            _Cast_GearMeshImplementationAnalysisDutyCycle
        """
        return _Cast_GearMeshImplementationAnalysisDutyCycle(self)
