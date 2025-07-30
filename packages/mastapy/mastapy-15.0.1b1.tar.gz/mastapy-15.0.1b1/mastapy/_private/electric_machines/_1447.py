"""TwoDimensionalFEModelForMechanicalAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.electric_machines import _1391, _1445

_TWO_DIMENSIONAL_FE_MODEL_FOR_MECHANICAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "TwoDimensionalFEModelForMechanicalAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="TwoDimensionalFEModelForMechanicalAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="TwoDimensionalFEModelForMechanicalAnalysis._Cast_TwoDimensionalFEModelForMechanicalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("TwoDimensionalFEModelForMechanicalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TwoDimensionalFEModelForMechanicalAnalysis:
    """Special nested class for casting TwoDimensionalFEModelForMechanicalAnalysis to subclasses."""

    __parent__: "TwoDimensionalFEModelForMechanicalAnalysis"

    @property
    def two_dimensional_fe_model_for_analysis(
        self: "CastSelf",
    ) -> "_1445.TwoDimensionalFEModelForAnalysis":
        return self.__parent__._cast(_1445.TwoDimensionalFEModelForAnalysis)

    @property
    def two_dimensional_fe_model_for_mechanical_analysis(
        self: "CastSelf",
    ) -> "TwoDimensionalFEModelForMechanicalAnalysis":
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
class TwoDimensionalFEModelForMechanicalAnalysis(
    _1445.TwoDimensionalFEModelForAnalysis[
        _1391.ElectricMachineMechanicalAnalysisMeshingOptions
    ]
):
    """TwoDimensionalFEModelForMechanicalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TWO_DIMENSIONAL_FE_MODEL_FOR_MECHANICAL_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_TwoDimensionalFEModelForMechanicalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_TwoDimensionalFEModelForMechanicalAnalysis
        """
        return _Cast_TwoDimensionalFEModelForMechanicalAnalysis(self)
