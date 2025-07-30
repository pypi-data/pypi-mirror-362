"""ConicalGearManufacturingAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.analysis import _1339

_CONICAL_GEAR_MANUFACTURING_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel", "ConicalGearManufacturingAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1335, _1338

    Self = TypeVar("Self", bound="ConicalGearManufacturingAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearManufacturingAnalysis._Cast_ConicalGearManufacturingAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearManufacturingAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearManufacturingAnalysis:
    """Special nested class for casting ConicalGearManufacturingAnalysis to subclasses."""

    __parent__: "ConicalGearManufacturingAnalysis"

    @property
    def gear_implementation_analysis(
        self: "CastSelf",
    ) -> "_1339.GearImplementationAnalysis":
        return self.__parent__._cast(_1339.GearImplementationAnalysis)

    @property
    def gear_design_analysis(self: "CastSelf") -> "_1338.GearDesignAnalysis":
        from mastapy._private.gears.analysis import _1338

        return self.__parent__._cast(_1338.GearDesignAnalysis)

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1335.AbstractGearAnalysis":
        from mastapy._private.gears.analysis import _1335

        return self.__parent__._cast(_1335.AbstractGearAnalysis)

    @property
    def conical_gear_manufacturing_analysis(
        self: "CastSelf",
    ) -> "ConicalGearManufacturingAnalysis":
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
class ConicalGearManufacturingAnalysis(_1339.GearImplementationAnalysis):
    """ConicalGearManufacturingAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_MANUFACTURING_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearManufacturingAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearManufacturingAnalysis
        """
        return _Cast_ConicalGearManufacturingAnalysis(self)
