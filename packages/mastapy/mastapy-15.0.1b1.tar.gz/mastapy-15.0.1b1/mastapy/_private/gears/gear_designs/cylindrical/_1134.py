"""CylindricalGearPinionTypeCutterFlank"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs.cylindrical import _1117

_CYLINDRICAL_GEAR_PINION_TYPE_CUTTER_FLANK = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "CylindricalGearPinionTypeCutterFlank"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1133

    Self = TypeVar("Self", bound="CylindricalGearPinionTypeCutterFlank")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearPinionTypeCutterFlank._Cast_CylindricalGearPinionTypeCutterFlank",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearPinionTypeCutterFlank",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearPinionTypeCutterFlank:
    """Special nested class for casting CylindricalGearPinionTypeCutterFlank to subclasses."""

    __parent__: "CylindricalGearPinionTypeCutterFlank"

    @property
    def cylindrical_gear_abstract_rack_flank(
        self: "CastSelf",
    ) -> "_1117.CylindricalGearAbstractRackFlank":
        return self.__parent__._cast(_1117.CylindricalGearAbstractRackFlank)

    @property
    def cylindrical_gear_pinion_type_cutter_flank(
        self: "CastSelf",
    ) -> "CylindricalGearPinionTypeCutterFlank":
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
class CylindricalGearPinionTypeCutterFlank(_1117.CylindricalGearAbstractRackFlank):
    """CylindricalGearPinionTypeCutterFlank

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_PINION_TYPE_CUTTER_FLANK

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def residual_fillet_undercut(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ResidualFilletUndercut")

        if temp is None:
            return 0.0

        return temp

    @residual_fillet_undercut.setter
    @exception_bridge
    @enforce_parameter_types
    def residual_fillet_undercut(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ResidualFilletUndercut",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def cutter(self: "Self") -> "_1133.CylindricalGearPinionTypeCutter":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearPinionTypeCutter

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Cutter")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearPinionTypeCutterFlank":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearPinionTypeCutterFlank
        """
        return _Cast_CylindricalGearPinionTypeCutterFlank(self)
