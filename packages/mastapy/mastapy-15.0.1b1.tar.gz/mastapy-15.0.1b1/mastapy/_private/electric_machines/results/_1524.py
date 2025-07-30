"""LinearDQModel"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.electric_machines.results import _1507

_LINEAR_DQ_MODEL = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Results", "LinearDQModel"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="LinearDQModel")
    CastSelf = TypeVar("CastSelf", bound="LinearDQModel._Cast_LinearDQModel")


__docformat__ = "restructuredtext en"
__all__ = ("LinearDQModel",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LinearDQModel:
    """Special nested class for casting LinearDQModel to subclasses."""

    __parent__: "LinearDQModel"

    @property
    def electric_machine_dq_model(self: "CastSelf") -> "_1507.ElectricMachineDQModel":
        return self.__parent__._cast(_1507.ElectricMachineDQModel)

    @property
    def linear_dq_model(self: "CastSelf") -> "LinearDQModel":
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
class LinearDQModel(_1507.ElectricMachineDQModel):
    """LinearDQModel

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LINEAR_DQ_MODEL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def apparent_d_axis_inductance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ApparentDAxisInductance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def apparent_mutual_field_armature_inductance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ApparentMutualFieldArmatureInductance"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def apparent_q_axis_inductance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ApparentQAxisInductance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def base_speed_from_mtpa_at_reference_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BaseSpeedFromMTPAAtReferenceTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def field_winding_current(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FieldWindingCurrent")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def field_winding_flux_linkage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FieldWindingFluxLinkage")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def max_speed_at_reference_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaxSpeedAtReferenceTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_LinearDQModel":
        """Cast to another type.

        Returns:
            _Cast_LinearDQModel
        """
        return _Cast_LinearDQModel(self)
