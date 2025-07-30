"""FEInterfaceThermalFace"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import _219

_FE_INTERFACE_THERMAL_FACE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.LumpedParameterThermalAnalysis",
    "FEInterfaceThermalFace",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FEInterfaceThermalFace")
    CastSelf = TypeVar(
        "CastSelf", bound="FEInterfaceThermalFace._Cast_FEInterfaceThermalFace"
    )


__docformat__ = "restructuredtext en"
__all__ = ("FEInterfaceThermalFace",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FEInterfaceThermalFace:
    """Special nested class for casting FEInterfaceThermalFace to subclasses."""

    __parent__: "FEInterfaceThermalFace"

    @property
    def thermal_face(self: "CastSelf") -> "_219.ThermalFace":
        return self.__parent__._cast(_219.ThermalFace)

    @property
    def fe_interface_thermal_face(self: "CastSelf") -> "FEInterfaceThermalFace":
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
class FEInterfaceThermalFace(_219.ThermalFace):
    """FEInterfaceThermalFace

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_INTERFACE_THERMAL_FACE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_FEInterfaceThermalFace":
        """Cast to another type.

        Returns:
            _Cast_FEInterfaceThermalFace
        """
        return _Cast_FEInterfaceThermalFace(self)
