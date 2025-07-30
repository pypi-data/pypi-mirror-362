"""CylindricalGearPlungeShaver"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.manufacturing.cylindrical.cutters import _818

_CYLINDRICAL_GEAR_PLUNGE_SHAVER = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters",
    "CylindricalGearPlungeShaver",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical import _716
    from mastapy._private.gears.manufacturing.cylindrical.cutters import (
        _809,
        _816,
        _821,
    )
    from mastapy._private.utility.databases import _2028

    Self = TypeVar("Self", bound="CylindricalGearPlungeShaver")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearPlungeShaver._Cast_CylindricalGearPlungeShaver",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearPlungeShaver",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearPlungeShaver:
    """Special nested class for casting CylindricalGearPlungeShaver to subclasses."""

    __parent__: "CylindricalGearPlungeShaver"

    @property
    def cylindrical_gear_shaver(self: "CastSelf") -> "_818.CylindricalGearShaver":
        return self.__parent__._cast(_818.CylindricalGearShaver)

    @property
    def involute_cutter_design(self: "CastSelf") -> "_821.InvoluteCutterDesign":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _821

        return self.__parent__._cast(_821.InvoluteCutterDesign)

    @property
    def cylindrical_gear_real_cutter_design(
        self: "CastSelf",
    ) -> "_816.CylindricalGearRealCutterDesign":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _816

        return self.__parent__._cast(_816.CylindricalGearRealCutterDesign)

    @property
    def cylindrical_gear_abstract_cutter_design(
        self: "CastSelf",
    ) -> "_809.CylindricalGearAbstractCutterDesign":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _809

        return self.__parent__._cast(_809.CylindricalGearAbstractCutterDesign)

    @property
    def named_database_item(self: "CastSelf") -> "_2028.NamedDatabaseItem":
        from mastapy._private.utility.databases import _2028

        return self.__parent__._cast(_2028.NamedDatabaseItem)

    @property
    def cylindrical_gear_plunge_shaver(
        self: "CastSelf",
    ) -> "CylindricalGearPlungeShaver":
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
class CylindricalGearPlungeShaver(_818.CylindricalGearShaver):
    """CylindricalGearPlungeShaver

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_PLUNGE_SHAVER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def face_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FaceWidth")

        if temp is None:
            return 0.0

        return temp

    @face_width.setter
    @exception_bridge
    @enforce_parameter_types
    def face_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FaceWidth", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def has_tolerances(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "HasTolerances")

        if temp is None:
            return False

        return temp

    @has_tolerances.setter
    @exception_bridge
    @enforce_parameter_types
    def has_tolerances(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "HasTolerances", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def left_flank_micro_geometry(
        self: "Self",
    ) -> "_716.CylindricalGearSpecifiedMicroGeometry":
        """mastapy.gears.manufacturing.cylindrical.CylindricalGearSpecifiedMicroGeometry

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeftFlankMicroGeometry")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def right_flank_micro_geometry(
        self: "Self",
    ) -> "_716.CylindricalGearSpecifiedMicroGeometry":
        """mastapy.gears.manufacturing.cylindrical.CylindricalGearSpecifiedMicroGeometry

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RightFlankMicroGeometry")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def micro_geometry(
        self: "Self",
    ) -> "List[_716.CylindricalGearSpecifiedMicroGeometry]":
        """List[mastapy.gears.manufacturing.cylindrical.CylindricalGearSpecifiedMicroGeometry]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MicroGeometry")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearPlungeShaver":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearPlungeShaver
        """
        return _Cast_CylindricalGearPlungeShaver(self)
