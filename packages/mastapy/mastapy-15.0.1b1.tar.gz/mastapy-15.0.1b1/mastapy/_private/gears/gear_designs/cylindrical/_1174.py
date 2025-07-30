"""MullerResidualStressDefinition"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility import _1779

_MULLER_RESIDUAL_STRESS_DEFINITION = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "MullerResidualStressDefinition"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MullerResidualStressDefinition")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MullerResidualStressDefinition._Cast_MullerResidualStressDefinition",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MullerResidualStressDefinition",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MullerResidualStressDefinition:
    """Special nested class for casting MullerResidualStressDefinition to subclasses."""

    __parent__: "MullerResidualStressDefinition"

    @property
    def independent_reportable_properties_base(
        self: "CastSelf",
    ) -> "_1779.IndependentReportablePropertiesBase":
        pass

        return self.__parent__._cast(_1779.IndependentReportablePropertiesBase)

    @property
    def muller_residual_stress_definition(
        self: "CastSelf",
    ) -> "MullerResidualStressDefinition":
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
class MullerResidualStressDefinition(
    _1779.IndependentReportablePropertiesBase["MullerResidualStressDefinition"]
):
    """MullerResidualStressDefinition

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MULLER_RESIDUAL_STRESS_DEFINITION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def compressive_residual_stress_at_surface(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "CompressiveResidualStressAtSurface"
        )

        if temp is None:
            return 0.0

        return temp

    @compressive_residual_stress_at_surface.setter
    @exception_bridge
    @enforce_parameter_types
    def compressive_residual_stress_at_surface(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CompressiveResidualStressAtSurface",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def depth_of_maximum_compressive_residual_stress(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "DepthOfMaximumCompressiveResidualStress"
        )

        if temp is None:
            return 0.0

        return temp

    @depth_of_maximum_compressive_residual_stress.setter
    @exception_bridge
    @enforce_parameter_types
    def depth_of_maximum_compressive_residual_stress(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "DepthOfMaximumCompressiveResidualStress",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def depth_of_transition_from_compressive_to_tensile(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "DepthOfTransitionFromCompressiveToTensile"
        )

        if temp is None:
            return 0.0

        return temp

    @depth_of_transition_from_compressive_to_tensile.setter
    @exception_bridge
    @enforce_parameter_types
    def depth_of_transition_from_compressive_to_tensile(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "DepthOfTransitionFromCompressiveToTensile",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def maximum_compressive_residual_stress(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumCompressiveResidualStress")

        if temp is None:
            return 0.0

        return temp

    @maximum_compressive_residual_stress.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_compressive_residual_stress(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumCompressiveResidualStress",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def maximum_tensile_stress(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumTensileStress")

        if temp is None:
            return 0.0

        return temp

    @maximum_tensile_stress.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_tensile_stress(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumTensileStress",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def parameter_delta(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ParameterDelta")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def parameter_for_the_slope_in_the_transition_from_compressive_to_tensile_residual_stresses(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped,
            "ParameterForTheSlopeInTheTransitionFromCompressiveToTensileResidualStresses",
        )

        if temp is None:
            return 0.0

        return temp

    @parameter_for_the_slope_in_the_transition_from_compressive_to_tensile_residual_stresses.setter
    @exception_bridge
    @enforce_parameter_types
    def parameter_for_the_slope_in_the_transition_from_compressive_to_tensile_residual_stresses(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ParameterForTheSlopeInTheTransitionFromCompressiveToTensileResidualStresses",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def parameter_k(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ParameterK")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def parameter_to_adjust_the_compressive_residual_stresses(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ParameterToAdjustTheCompressiveResidualStresses"
        )

        if temp is None:
            return 0.0

        return temp

    @parameter_to_adjust_the_compressive_residual_stresses.setter
    @exception_bridge
    @enforce_parameter_types
    def parameter_to_adjust_the_compressive_residual_stresses(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ParameterToAdjustTheCompressiveResidualStresses",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def parameter_to_define_compressive_residual_stresses_at_surface(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ParameterToDefineCompressiveResidualStressesAtSurface"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_MullerResidualStressDefinition":
        """Cast to another type.

        Returns:
            _Cast_MullerResidualStressDefinition
        """
        return _Cast_MullerResidualStressDefinition(self)
