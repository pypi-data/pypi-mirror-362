"""ML1OptimizerSettings"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_ML1_OPTIMIZER_SETTINGS = python_net_import(
    "SMT.MastaAPI.MathUtility.BayesianOptimization", "ML1OptimizerSettings"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility.bayesian_optimization import _1768

    Self = TypeVar("Self", bound="ML1OptimizerSettings")
    CastSelf = TypeVar(
        "CastSelf", bound="ML1OptimizerSettings._Cast_ML1OptimizerSettings"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ML1OptimizerSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ML1OptimizerSettings:
    """Special nested class for casting ML1OptimizerSettings to subclasses."""

    __parent__: "ML1OptimizerSettings"

    @property
    def ml1_optimizer_settings(self: "CastSelf") -> "ML1OptimizerSettings":
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
class ML1OptimizerSettings(_0.APIBase):
    """ML1OptimizerSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ML1_OPTIMIZER_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def initial_capacity(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "InitialCapacity")

        if temp is None:
            return 0

        return temp

    @initial_capacity.setter
    @exception_bridge
    @enforce_parameter_types
    def initial_capacity(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "InitialCapacity", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def number_of_initial_samples(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfInitialSamples")

        if temp is None:
            return 0

        return temp

    @number_of_initial_samples.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_initial_samples(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfInitialSamples",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def random_seed(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "RandomSeed")

        if temp is None:
            return 0

        return temp

    @random_seed.setter
    @exception_bridge
    @enforce_parameter_types
    def random_seed(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "RandomSeed", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def result_storage_option(
        self: "Self",
    ) -> "_1768.BayesianOptimizationResultsStorageOption":
        """mastapy.math_utility.bayesian_optimization.BayesianOptimizationResultsStorageOption"""
        temp = pythonnet_property_get(self.wrapped, "ResultStorageOption")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.MathUtility.BayesianOptimization.BayesianOptimizationResultsStorageOption",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.math_utility.bayesian_optimization._1768",
            "BayesianOptimizationResultsStorageOption",
        )(value)

    @result_storage_option.setter
    @exception_bridge
    @enforce_parameter_types
    def result_storage_option(
        self: "Self", value: "_1768.BayesianOptimizationResultsStorageOption"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.MathUtility.BayesianOptimization.BayesianOptimizationResultsStorageOption",
        )
        pythonnet_property_set(self.wrapped, "ResultStorageOption", value)

    @property
    def cast_to(self: "Self") -> "_Cast_ML1OptimizerSettings":
        """Cast to another type.

        Returns:
            _Cast_ML1OptimizerSettings
        """
        return _Cast_ML1OptimizerSettings(self)
