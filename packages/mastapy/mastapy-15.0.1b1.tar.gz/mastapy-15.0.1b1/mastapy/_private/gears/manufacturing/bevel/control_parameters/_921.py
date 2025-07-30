"""ConicalManufacturingSGMControlParameters"""

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
from mastapy._private.gears.manufacturing.bevel.control_parameters import _920

_CONICAL_MANUFACTURING_SGM_CONTROL_PARAMETERS = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel.ControlParameters",
    "ConicalManufacturingSGMControlParameters",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ConicalManufacturingSGMControlParameters")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalManufacturingSGMControlParameters._Cast_ConicalManufacturingSGMControlParameters",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalManufacturingSGMControlParameters",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalManufacturingSGMControlParameters:
    """Special nested class for casting ConicalManufacturingSGMControlParameters to subclasses."""

    __parent__: "ConicalManufacturingSGMControlParameters"

    @property
    def conical_gear_manufacturing_control_parameters(
        self: "CastSelf",
    ) -> "_920.ConicalGearManufacturingControlParameters":
        return self.__parent__._cast(_920.ConicalGearManufacturingControlParameters)

    @property
    def conical_manufacturing_sgm_control_parameters(
        self: "CastSelf",
    ) -> "ConicalManufacturingSGMControlParameters":
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
class ConicalManufacturingSGMControlParameters(
    _920.ConicalGearManufacturingControlParameters
):
    """ConicalManufacturingSGMControlParameters

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_MANUFACTURING_SGM_CONTROL_PARAMETERS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def delta_gamma(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DeltaGamma")

        if temp is None:
            return 0.0

        return temp

    @delta_gamma.setter
    @exception_bridge
    @enforce_parameter_types
    def delta_gamma(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DeltaGamma", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def profile_mismatch_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProfileMismatchFactor")

        if temp is None:
            return 0.0

        return temp

    @profile_mismatch_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def profile_mismatch_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProfileMismatchFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def work_head_offset_change(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WorkHeadOffsetChange")

        if temp is None:
            return 0.0

        return temp

    @work_head_offset_change.setter
    @exception_bridge
    @enforce_parameter_types
    def work_head_offset_change(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "WorkHeadOffsetChange",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalManufacturingSGMControlParameters":
        """Cast to another type.

        Returns:
            _Cast_ConicalManufacturingSGMControlParameters
        """
        return _Cast_ConicalManufacturingSGMControlParameters(self)
