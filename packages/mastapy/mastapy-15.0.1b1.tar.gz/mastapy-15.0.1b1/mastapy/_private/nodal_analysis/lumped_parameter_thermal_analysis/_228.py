"""UserDefinedThermalConnectorWithResistance"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import _217

_USER_DEFINED_THERMAL_CONNECTOR_WITH_RESISTANCE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.LumpedParameterThermalAnalysis",
    "UserDefinedThermalConnectorWithResistance",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import _215

    Self = TypeVar("Self", bound="UserDefinedThermalConnectorWithResistance")
    CastSelf = TypeVar(
        "CastSelf",
        bound="UserDefinedThermalConnectorWithResistance._Cast_UserDefinedThermalConnectorWithResistance",
    )


__docformat__ = "restructuredtext en"
__all__ = ("UserDefinedThermalConnectorWithResistance",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_UserDefinedThermalConnectorWithResistance:
    """Special nested class for casting UserDefinedThermalConnectorWithResistance to subclasses."""

    __parent__: "UserDefinedThermalConnectorWithResistance"

    @property
    def thermal_connector_with_resistance(
        self: "CastSelf",
    ) -> "_217.ThermalConnectorWithResistance":
        return self.__parent__._cast(_217.ThermalConnectorWithResistance)

    @property
    def thermal_connector(self: "CastSelf") -> "_215.ThermalConnector":
        from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
            _215,
        )

        return self.__parent__._cast(_215.ThermalConnector)

    @property
    def user_defined_thermal_connector_with_resistance(
        self: "CastSelf",
    ) -> "UserDefinedThermalConnectorWithResistance":
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
class UserDefinedThermalConnectorWithResistance(_217.ThermalConnectorWithResistance):
    """UserDefinedThermalConnectorWithResistance

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _USER_DEFINED_THERMAL_CONNECTOR_WITH_RESISTANCE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_UserDefinedThermalConnectorWithResistance":
        """Cast to another type.

        Returns:
            _Cast_UserDefinedThermalConnectorWithResistance
        """
        return _Cast_UserDefinedThermalConnectorWithResistance(self)
