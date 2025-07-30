"""TwoDimensionalFEModelForElectromagneticAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.electric_machines import _1392, _1445

_TWO_DIMENSIONAL_FE_MODEL_FOR_ELECTROMAGNETIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "TwoDimensionalFEModelForElectromagneticAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="TwoDimensionalFEModelForElectromagneticAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="TwoDimensionalFEModelForElectromagneticAnalysis._Cast_TwoDimensionalFEModelForElectromagneticAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("TwoDimensionalFEModelForElectromagneticAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TwoDimensionalFEModelForElectromagneticAnalysis:
    """Special nested class for casting TwoDimensionalFEModelForElectromagneticAnalysis to subclasses."""

    __parent__: "TwoDimensionalFEModelForElectromagneticAnalysis"

    @property
    def two_dimensional_fe_model_for_analysis(
        self: "CastSelf",
    ) -> "_1445.TwoDimensionalFEModelForAnalysis":
        return self.__parent__._cast(_1445.TwoDimensionalFEModelForAnalysis)

    @property
    def two_dimensional_fe_model_for_electromagnetic_analysis(
        self: "CastSelf",
    ) -> "TwoDimensionalFEModelForElectromagneticAnalysis":
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
class TwoDimensionalFEModelForElectromagneticAnalysis(
    _1445.TwoDimensionalFEModelForAnalysis[_1392.ElectricMachineMeshingOptions]
):
    """TwoDimensionalFEModelForElectromagneticAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TWO_DIMENSIONAL_FE_MODEL_FOR_ELECTROMAGNETIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_TwoDimensionalFEModelForElectromagneticAnalysis":
        """Cast to another type.

        Returns:
            _Cast_TwoDimensionalFEModelForElectromagneticAnalysis
        """
        return _Cast_TwoDimensionalFEModelForElectromagneticAnalysis(self)
