"""CylindricalGearSetTIFFAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.analysis import _1346

_CYLINDRICAL_GEAR_SET_TIFF_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.GearTwoDFEAnalysis", "CylindricalGearSetTIFFAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1337
    from mastapy._private.gears.gear_two_d_fe_analysis import _1001

    Self = TypeVar("Self", bound="CylindricalGearSetTIFFAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearSetTIFFAnalysis._Cast_CylindricalGearSetTIFFAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearSetTIFFAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearSetTIFFAnalysis:
    """Special nested class for casting CylindricalGearSetTIFFAnalysis to subclasses."""

    __parent__: "CylindricalGearSetTIFFAnalysis"

    @property
    def gear_set_design_analysis(self: "CastSelf") -> "_1346.GearSetDesignAnalysis":
        return self.__parent__._cast(_1346.GearSetDesignAnalysis)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1337.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1337

        return self.__parent__._cast(_1337.AbstractGearSetAnalysis)

    @property
    def cylindrical_gear_set_tiff_analysis(
        self: "CastSelf",
    ) -> "CylindricalGearSetTIFFAnalysis":
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
class CylindricalGearSetTIFFAnalysis(_1346.GearSetDesignAnalysis):
    """CylindricalGearSetTIFFAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_SET_TIFF_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def gears(self: "Self") -> "List[_1001.CylindricalGearTIFFAnalysis]":
        """List[mastapy.gears.gear_two_d_fe_analysis.CylindricalGearTIFFAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Gears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearSetTIFFAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearSetTIFFAnalysis
        """
        return _Cast_CylindricalGearSetTIFFAnalysis(self)
