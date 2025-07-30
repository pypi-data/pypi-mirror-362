"""CylindricalGearMicroGeometry"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1214

_CYLINDRICAL_GEAR_MICRO_GEOMETRY = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry",
    "CylindricalGearMicroGeometry",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1335, _1338, _1341
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import (
        _1208,
        _1236,
    )

    Self = TypeVar("Self", bound="CylindricalGearMicroGeometry")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearMicroGeometry._Cast_CylindricalGearMicroGeometry",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearMicroGeometry",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearMicroGeometry:
    """Special nested class for casting CylindricalGearMicroGeometry to subclasses."""

    __parent__: "CylindricalGearMicroGeometry"

    @property
    def cylindrical_gear_micro_geometry_base(
        self: "CastSelf",
    ) -> "_1214.CylindricalGearMicroGeometryBase":
        return self.__parent__._cast(_1214.CylindricalGearMicroGeometryBase)

    @property
    def gear_implementation_detail(
        self: "CastSelf",
    ) -> "_1341.GearImplementationDetail":
        from mastapy._private.gears.analysis import _1341

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
    def cylindrical_gear_micro_geometry(
        self: "CastSelf",
    ) -> "CylindricalGearMicroGeometry":
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
class CylindricalGearMicroGeometry(_1214.CylindricalGearMicroGeometryBase):
    """CylindricalGearMicroGeometry

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_MICRO_GEOMETRY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def left_flank(self: "Self") -> "_1208.CylindricalGearFlankMicroGeometry":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearFlankMicroGeometry

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeftFlank")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def right_flank(self: "Self") -> "_1208.CylindricalGearFlankMicroGeometry":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearFlankMicroGeometry

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RightFlank")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def flanks(self: "Self") -> "List[_1208.CylindricalGearFlankMicroGeometry]":
        """List[mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearFlankMicroGeometry]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Flanks")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def meshed_gears(self: "Self") -> "List[_1236.MeshedCylindricalGearMicroGeometry]":
        """List[mastapy.gears.gear_designs.cylindrical.micro_geometry.MeshedCylindricalGearMicroGeometry]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshedGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def both_flanks(self: "Self") -> "_1208.CylindricalGearFlankMicroGeometry":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearFlankMicroGeometry

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BothFlanks")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    def swap_flanks(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SwapFlanks")

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearMicroGeometry":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearMicroGeometry
        """
        return _Cast_CylindricalGearMicroGeometry(self)
