"""CylindricalGearMicroGeometryDutyCycle"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.analysis import _1338

_CYLINDRICAL_GEAR_MICRO_GEOMETRY_DUTY_CYCLE = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry",
    "CylindricalGearMicroGeometryDutyCycle",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1335
    from mastapy._private.gears.gear_two_d_fe_analysis import _1002

    Self = TypeVar("Self", bound="CylindricalGearMicroGeometryDutyCycle")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearMicroGeometryDutyCycle._Cast_CylindricalGearMicroGeometryDutyCycle",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearMicroGeometryDutyCycle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearMicroGeometryDutyCycle:
    """Special nested class for casting CylindricalGearMicroGeometryDutyCycle to subclasses."""

    __parent__: "CylindricalGearMicroGeometryDutyCycle"

    @property
    def gear_design_analysis(self: "CastSelf") -> "_1338.GearDesignAnalysis":
        return self.__parent__._cast(_1338.GearDesignAnalysis)

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1335.AbstractGearAnalysis":
        from mastapy._private.gears.analysis import _1335

        return self.__parent__._cast(_1335.AbstractGearAnalysis)

    @property
    def cylindrical_gear_micro_geometry_duty_cycle(
        self: "CastSelf",
    ) -> "CylindricalGearMicroGeometryDutyCycle":
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
class CylindricalGearMicroGeometryDutyCycle(_1338.GearDesignAnalysis):
    """CylindricalGearMicroGeometryDutyCycle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_MICRO_GEOMETRY_DUTY_CYCLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def tiff_analysis(self: "Self") -> "_1002.CylindricalGearTIFFAnalysisDutyCycle":
        """mastapy.gears.gear_two_d_fe_analysis.CylindricalGearTIFFAnalysisDutyCycle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TIFFAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearMicroGeometryDutyCycle":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearMicroGeometryDutyCycle
        """
        return _Cast_CylindricalGearMicroGeometryDutyCycle(self)
