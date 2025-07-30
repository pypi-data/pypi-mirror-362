"""WindageLossCalculationOilParameters"""

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
)

_WINDAGE_LOSS_CALCULATION_OIL_PARAMETERS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.ShaftModel",
    "WindageLossCalculationOilParameters",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="WindageLossCalculationOilParameters")
    CastSelf = TypeVar(
        "CastSelf",
        bound="WindageLossCalculationOilParameters._Cast_WindageLossCalculationOilParameters",
    )


__docformat__ = "restructuredtext en"
__all__ = ("WindageLossCalculationOilParameters",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WindageLossCalculationOilParameters:
    """Special nested class for casting WindageLossCalculationOilParameters to subclasses."""

    __parent__: "WindageLossCalculationOilParameters"

    @property
    def windage_loss_calculation_oil_parameters(
        self: "CastSelf",
    ) -> "WindageLossCalculationOilParameters":
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
class WindageLossCalculationOilParameters(_0.APIBase):
    """WindageLossCalculationOilParameters

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WINDAGE_LOSS_CALCULATION_OIL_PARAMETERS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def dynamic_viscosity_at_oil_sump_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DynamicViscosityAtOilSumpTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def kinematic_viscosity_at_oil_sump_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KinematicViscosityAtOilSumpTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def oil_density_at_oil_sump_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OilDensityAtOilSumpTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def oil_dip_coefficient(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OilDipCoefficient")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def volumetric_oil_air_mixture_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VolumetricOilAirMixtureRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_WindageLossCalculationOilParameters":
        """Cast to another type.

        Returns:
            _Cast_WindageLossCalculationOilParameters
        """
        return _Cast_WindageLossCalculationOilParameters(self)
