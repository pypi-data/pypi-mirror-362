"""ConicalGearMicroGeometryConfigBase"""

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
from mastapy._private.gears.analysis import _1341

_CONICAL_GEAR_MICRO_GEOMETRY_CONFIG_BASE = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel", "ConicalGearMicroGeometryConfigBase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1335, _1338
    from mastapy._private.gears.manufacturing.bevel import (
        _879,
        _880,
        _891,
        _892,
        _897,
        _899,
    )

    Self = TypeVar("Self", bound="ConicalGearMicroGeometryConfigBase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearMicroGeometryConfigBase._Cast_ConicalGearMicroGeometryConfigBase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearMicroGeometryConfigBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearMicroGeometryConfigBase:
    """Special nested class for casting ConicalGearMicroGeometryConfigBase to subclasses."""

    __parent__: "ConicalGearMicroGeometryConfigBase"

    @property
    def gear_implementation_detail(
        self: "CastSelf",
    ) -> "_1341.GearImplementationDetail":
        return self.__parent__._cast(_1341.GearImplementationDetail)

    @property
    def gear_design_analysis(self: "CastSelf") -> "_1338.GearDesignAnalysis":
        from mastapy._private.gears.analysis import _1338

        return self.__parent__._cast(_1338.GearDesignAnalysis)

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1335.AbstractGearAnalysis":
        from mastapy._private.gears.analysis import _1335

        return self.__parent__._cast(_1335.AbstractGearAnalysis)

    @property
    def conical_gear_manufacturing_config(
        self: "CastSelf",
    ) -> "_879.ConicalGearManufacturingConfig":
        from mastapy._private.gears.manufacturing.bevel import _879

        return self.__parent__._cast(_879.ConicalGearManufacturingConfig)

    @property
    def conical_gear_micro_geometry_config(
        self: "CastSelf",
    ) -> "_880.ConicalGearMicroGeometryConfig":
        from mastapy._private.gears.manufacturing.bevel import _880

        return self.__parent__._cast(_880.ConicalGearMicroGeometryConfig)

    @property
    def conical_pinion_manufacturing_config(
        self: "CastSelf",
    ) -> "_891.ConicalPinionManufacturingConfig":
        from mastapy._private.gears.manufacturing.bevel import _891

        return self.__parent__._cast(_891.ConicalPinionManufacturingConfig)

    @property
    def conical_pinion_micro_geometry_config(
        self: "CastSelf",
    ) -> "_892.ConicalPinionMicroGeometryConfig":
        from mastapy._private.gears.manufacturing.bevel import _892

        return self.__parent__._cast(_892.ConicalPinionMicroGeometryConfig)

    @property
    def conical_wheel_manufacturing_config(
        self: "CastSelf",
    ) -> "_897.ConicalWheelManufacturingConfig":
        from mastapy._private.gears.manufacturing.bevel import _897

        return self.__parent__._cast(_897.ConicalWheelManufacturingConfig)

    @property
    def conical_gear_micro_geometry_config_base(
        self: "CastSelf",
    ) -> "ConicalGearMicroGeometryConfigBase":
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
class ConicalGearMicroGeometryConfigBase(_1341.GearImplementationDetail):
    """ConicalGearMicroGeometryConfigBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_MICRO_GEOMETRY_CONFIG_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def flank_measurement_border(self: "Self") -> "_899.FlankMeasurementBorder":
        """mastapy.gears.manufacturing.bevel.FlankMeasurementBorder

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FlankMeasurementBorder")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearMicroGeometryConfigBase":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearMicroGeometryConfigBase
        """
        return _Cast_ConicalGearMicroGeometryConfigBase(self)
