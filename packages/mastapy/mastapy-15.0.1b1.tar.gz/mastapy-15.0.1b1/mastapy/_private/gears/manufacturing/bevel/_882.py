"""ConicalMeshedGearManufacturingAnalysis"""

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

_CONICAL_MESHED_GEAR_MANUFACTURING_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel", "ConicalMeshedGearManufacturingAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ConicalMeshedGearManufacturingAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalMeshedGearManufacturingAnalysis._Cast_ConicalMeshedGearManufacturingAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalMeshedGearManufacturingAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalMeshedGearManufacturingAnalysis:
    """Special nested class for casting ConicalMeshedGearManufacturingAnalysis to subclasses."""

    __parent__: "ConicalMeshedGearManufacturingAnalysis"

    @property
    def conical_meshed_gear_manufacturing_analysis(
        self: "CastSelf",
    ) -> "ConicalMeshedGearManufacturingAnalysis":
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
class ConicalMeshedGearManufacturingAnalysis(_0.APIBase):
    """ConicalMeshedGearManufacturingAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_MESHED_GEAR_MANUFACTURING_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    @exception_bridge
    def torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Torque")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalMeshedGearManufacturingAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConicalMeshedGearManufacturingAnalysis
        """
        return _Cast_ConicalMeshedGearManufacturingAnalysis(self)
