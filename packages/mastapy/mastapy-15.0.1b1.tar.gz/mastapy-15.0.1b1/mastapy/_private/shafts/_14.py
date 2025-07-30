"""GenericStressConcentrationFactor"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.shafts import _21

_GENERIC_STRESS_CONCENTRATION_FACTOR = python_net_import(
    "SMT.MastaAPI.Shafts", "GenericStressConcentrationFactor"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="GenericStressConcentrationFactor")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GenericStressConcentrationFactor._Cast_GenericStressConcentrationFactor",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GenericStressConcentrationFactor",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GenericStressConcentrationFactor:
    """Special nested class for casting GenericStressConcentrationFactor to subclasses."""

    __parent__: "GenericStressConcentrationFactor"

    @property
    def shaft_feature(self: "CastSelf") -> "_21.ShaftFeature":
        return self.__parent__._cast(_21.ShaftFeature)

    @property
    def generic_stress_concentration_factor(
        self: "CastSelf",
    ) -> "GenericStressConcentrationFactor":
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
class GenericStressConcentrationFactor(_21.ShaftFeature):
    """GenericStressConcentrationFactor

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GENERIC_STRESS_CONCENTRATION_FACTOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def bending_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BendingFactor")

        if temp is None:
            return 0.0

        return temp

    @bending_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def bending_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "BendingFactor", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Length")

        if temp is None:
            return 0.0

        return temp

    @length.setter
    @exception_bridge
    @enforce_parameter_types
    def length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Length", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def tension_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TensionFactor")

        if temp is None:
            return 0.0

        return temp

    @tension_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def tension_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "TensionFactor", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def torsion_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TorsionFactor")

        if temp is None:
            return 0.0

        return temp

    @torsion_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def torsion_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "TorsionFactor", float(value) if value is not None else 0.0
        )

    @exception_bridge
    def add_new_generic_scf(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddNewGenericSCF")

    @property
    def cast_to(self: "Self") -> "_Cast_GenericStressConcentrationFactor":
        """Cast to another type.

        Returns:
            _Cast_GenericStressConcentrationFactor
        """
        return _Cast_GenericStressConcentrationFactor(self)
