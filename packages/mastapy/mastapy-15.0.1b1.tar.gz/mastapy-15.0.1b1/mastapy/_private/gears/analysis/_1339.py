"""GearImplementationAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.analysis import _1338

_GEAR_IMPLEMENTATION_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.Analysis", "GearImplementationAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1335
    from mastapy._private.gears.ltca import _943
    from mastapy._private.gears.ltca.conical import _970
    from mastapy._private.gears.ltca.cylindrical import _959
    from mastapy._private.gears.manufacturing.bevel import _878
    from mastapy._private.gears.manufacturing.cylindrical import _720

    Self = TypeVar("Self", bound="GearImplementationAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="GearImplementationAnalysis._Cast_GearImplementationAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearImplementationAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearImplementationAnalysis:
    """Special nested class for casting GearImplementationAnalysis to subclasses."""

    __parent__: "GearImplementationAnalysis"

    @property
    def gear_design_analysis(self: "CastSelf") -> "_1338.GearDesignAnalysis":
        return self.__parent__._cast(_1338.GearDesignAnalysis)

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1335.AbstractGearAnalysis":
        from mastapy._private.gears.analysis import _1335

        return self.__parent__._cast(_1335.AbstractGearAnalysis)

    @property
    def cylindrical_manufactured_gear_load_case(
        self: "CastSelf",
    ) -> "_720.CylindricalManufacturedGearLoadCase":
        from mastapy._private.gears.manufacturing.cylindrical import _720

        return self.__parent__._cast(_720.CylindricalManufacturedGearLoadCase)

    @property
    def conical_gear_manufacturing_analysis(
        self: "CastSelf",
    ) -> "_878.ConicalGearManufacturingAnalysis":
        from mastapy._private.gears.manufacturing.bevel import _878

        return self.__parent__._cast(_878.ConicalGearManufacturingAnalysis)

    @property
    def gear_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_943.GearLoadDistributionAnalysis":
        from mastapy._private.gears.ltca import _943

        return self.__parent__._cast(_943.GearLoadDistributionAnalysis)

    @property
    def cylindrical_gear_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_959.CylindricalGearLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.cylindrical import _959

        return self.__parent__._cast(_959.CylindricalGearLoadDistributionAnalysis)

    @property
    def conical_gear_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_970.ConicalGearLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.conical import _970

        return self.__parent__._cast(_970.ConicalGearLoadDistributionAnalysis)

    @property
    def gear_implementation_analysis(self: "CastSelf") -> "GearImplementationAnalysis":
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
class GearImplementationAnalysis(_1338.GearDesignAnalysis):
    """GearImplementationAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_IMPLEMENTATION_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_GearImplementationAnalysis":
        """Cast to another type.

        Returns:
            _Cast_GearImplementationAnalysis
        """
        return _Cast_GearImplementationAnalysis(self)
