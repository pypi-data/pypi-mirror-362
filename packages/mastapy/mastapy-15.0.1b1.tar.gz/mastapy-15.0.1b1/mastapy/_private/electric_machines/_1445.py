"""TwoDimensionalFEModelForAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_TWO_DIMENSIONAL_FE_MODEL_FOR_ANALYSIS = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "TwoDimensionalFEModelForAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.electric_machines import _1393, _1446, _1447

    Self = TypeVar("Self", bound="TwoDimensionalFEModelForAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="TwoDimensionalFEModelForAnalysis._Cast_TwoDimensionalFEModelForAnalysis",
    )

T = TypeVar("T", bound="_1393.ElectricMachineMeshingOptionsBase")

__docformat__ = "restructuredtext en"
__all__ = ("TwoDimensionalFEModelForAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TwoDimensionalFEModelForAnalysis:
    """Special nested class for casting TwoDimensionalFEModelForAnalysis to subclasses."""

    __parent__: "TwoDimensionalFEModelForAnalysis"

    @property
    def two_dimensional_fe_model_for_electromagnetic_analysis(
        self: "CastSelf",
    ) -> "_1446.TwoDimensionalFEModelForElectromagneticAnalysis":
        from mastapy._private.electric_machines import _1446

        return self.__parent__._cast(
            _1446.TwoDimensionalFEModelForElectromagneticAnalysis
        )

    @property
    def two_dimensional_fe_model_for_mechanical_analysis(
        self: "CastSelf",
    ) -> "_1447.TwoDimensionalFEModelForMechanicalAnalysis":
        from mastapy._private.electric_machines import _1447

        return self.__parent__._cast(_1447.TwoDimensionalFEModelForMechanicalAnalysis)

    @property
    def two_dimensional_fe_model_for_analysis(
        self: "CastSelf",
    ) -> "TwoDimensionalFEModelForAnalysis":
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
class TwoDimensionalFEModelForAnalysis(_0.APIBase, Generic[T]):
    """TwoDimensionalFEModelForAnalysis

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _TWO_DIMENSIONAL_FE_MODEL_FOR_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def number_of_elements(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfElements")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_nodes(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfNodes")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def meshing_options(self: "Self") -> "T":
        """T

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshingOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_TwoDimensionalFEModelForAnalysis":
        """Cast to another type.

        Returns:
            _Cast_TwoDimensionalFEModelForAnalysis
        """
        return _Cast_TwoDimensionalFEModelForAnalysis(self)
