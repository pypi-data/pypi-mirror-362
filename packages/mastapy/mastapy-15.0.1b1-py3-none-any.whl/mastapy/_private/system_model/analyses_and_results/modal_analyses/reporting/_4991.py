"""ComponentPerModeResult"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
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

_COMPONENT_PER_MODE_RESULT = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Reporting",
    "ComponentPerModeResult",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
        _4998,
    )

    Self = TypeVar("Self", bound="ComponentPerModeResult")
    CastSelf = TypeVar(
        "CastSelf", bound="ComponentPerModeResult._Cast_ComponentPerModeResult"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ComponentPerModeResult",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ComponentPerModeResult:
    """Special nested class for casting ComponentPerModeResult to subclasses."""

    __parent__: "ComponentPerModeResult"

    @property
    def shaft_per_mode_result(self: "CastSelf") -> "_4998.ShaftPerModeResult":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
            _4998,
        )

        return self.__parent__._cast(_4998.ShaftPerModeResult)

    @property
    def component_per_mode_result(self: "CastSelf") -> "ComponentPerModeResult":
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
class ComponentPerModeResult(_0.APIBase):
    """ComponentPerModeResult

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPONENT_PER_MODE_RESULT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def mode_frequency(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModeFrequency")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mode_id(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModeID")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def percentage_kinetic_energy(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PercentageKineticEnergy")

        if temp is None:
            return 0.0

        return temp

    @percentage_kinetic_energy.setter
    @exception_bridge
    @enforce_parameter_types
    def percentage_kinetic_energy(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PercentageKineticEnergy",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def percentage_strain_energy(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PercentageStrainEnergy")

        if temp is None:
            return 0.0

        return temp

    @percentage_strain_energy.setter
    @exception_bridge
    @enforce_parameter_types
    def percentage_strain_energy(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PercentageStrainEnergy",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ComponentPerModeResult":
        """Cast to another type.

        Returns:
            _Cast_ComponentPerModeResult
        """
        return _Cast_ComponentPerModeResult(self)
