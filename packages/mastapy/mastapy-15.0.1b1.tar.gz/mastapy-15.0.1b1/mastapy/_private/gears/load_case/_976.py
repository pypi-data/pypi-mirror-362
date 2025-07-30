"""GearLoadCaseBase"""

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
from mastapy._private.gears.analysis import _1338

_GEAR_LOAD_CASE_BASE = python_net_import(
    "SMT.MastaAPI.Gears.LoadCase", "GearLoadCaseBase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1335
    from mastapy._private.gears.load_case.bevel import _994
    from mastapy._private.gears.load_case.concept import _991
    from mastapy._private.gears.load_case.conical import _988
    from mastapy._private.gears.load_case.cylindrical import _985
    from mastapy._private.gears.load_case.face import _982
    from mastapy._private.gears.load_case.worm import _979

    Self = TypeVar("Self", bound="GearLoadCaseBase")
    CastSelf = TypeVar("CastSelf", bound="GearLoadCaseBase._Cast_GearLoadCaseBase")


__docformat__ = "restructuredtext en"
__all__ = ("GearLoadCaseBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearLoadCaseBase:
    """Special nested class for casting GearLoadCaseBase to subclasses."""

    __parent__: "GearLoadCaseBase"

    @property
    def gear_design_analysis(self: "CastSelf") -> "_1338.GearDesignAnalysis":
        return self.__parent__._cast(_1338.GearDesignAnalysis)

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1335.AbstractGearAnalysis":
        from mastapy._private.gears.analysis import _1335

        return self.__parent__._cast(_1335.AbstractGearAnalysis)

    @property
    def worm_gear_load_case(self: "CastSelf") -> "_979.WormGearLoadCase":
        from mastapy._private.gears.load_case.worm import _979

        return self.__parent__._cast(_979.WormGearLoadCase)

    @property
    def face_gear_load_case(self: "CastSelf") -> "_982.FaceGearLoadCase":
        from mastapy._private.gears.load_case.face import _982

        return self.__parent__._cast(_982.FaceGearLoadCase)

    @property
    def cylindrical_gear_load_case(self: "CastSelf") -> "_985.CylindricalGearLoadCase":
        from mastapy._private.gears.load_case.cylindrical import _985

        return self.__parent__._cast(_985.CylindricalGearLoadCase)

    @property
    def conical_gear_load_case(self: "CastSelf") -> "_988.ConicalGearLoadCase":
        from mastapy._private.gears.load_case.conical import _988

        return self.__parent__._cast(_988.ConicalGearLoadCase)

    @property
    def concept_gear_load_case(self: "CastSelf") -> "_991.ConceptGearLoadCase":
        from mastapy._private.gears.load_case.concept import _991

        return self.__parent__._cast(_991.ConceptGearLoadCase)

    @property
    def bevel_load_case(self: "CastSelf") -> "_994.BevelLoadCase":
        from mastapy._private.gears.load_case.bevel import _994

        return self.__parent__._cast(_994.BevelLoadCase)

    @property
    def gear_load_case_base(self: "CastSelf") -> "GearLoadCaseBase":
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
class GearLoadCaseBase(_1338.GearDesignAnalysis):
    """GearLoadCaseBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_LOAD_CASE_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def duration(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Duration")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "GearTemperature")

        if temp is None:
            return 0.0

        return temp

    @gear_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def gear_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "GearTemperature", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def rotation_speed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RotationSpeed")

        if temp is None:
            return 0.0

        return temp

    @rotation_speed.setter
    @exception_bridge
    @enforce_parameter_types
    def rotation_speed(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RotationSpeed", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def sump_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SumpTemperature")

        if temp is None:
            return 0.0

        return temp

    @sump_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def sump_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "SumpTemperature", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_GearLoadCaseBase":
        """Cast to another type.

        Returns:
            _Cast_GearLoadCaseBase
        """
        return _Cast_GearLoadCaseBase(self)
