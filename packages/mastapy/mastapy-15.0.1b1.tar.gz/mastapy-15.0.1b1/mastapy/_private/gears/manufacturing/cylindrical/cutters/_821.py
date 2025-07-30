"""InvoluteCutterDesign"""

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
from mastapy._private.gears.manufacturing.cylindrical.cutters import _816

_INVOLUTE_CUTTER_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters", "InvoluteCutterDesign"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears import _423
    from mastapy._private.gears.gear_designs.cylindrical import _1199
    from mastapy._private.gears.manufacturing.cylindrical.cutters import (
        _809,
        _813,
        _817,
        _818,
    )
    from mastapy._private.utility.databases import _2028

    Self = TypeVar("Self", bound="InvoluteCutterDesign")
    CastSelf = TypeVar(
        "CastSelf", bound="InvoluteCutterDesign._Cast_InvoluteCutterDesign"
    )


__docformat__ = "restructuredtext en"
__all__ = ("InvoluteCutterDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InvoluteCutterDesign:
    """Special nested class for casting InvoluteCutterDesign to subclasses."""

    __parent__: "InvoluteCutterDesign"

    @property
    def cylindrical_gear_real_cutter_design(
        self: "CastSelf",
    ) -> "_816.CylindricalGearRealCutterDesign":
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
    ) -> "_813.CylindricalGearPlungeShaver":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _813

        return self.__parent__._cast(_813.CylindricalGearPlungeShaver)

    @property
    def cylindrical_gear_shaper(self: "CastSelf") -> "_817.CylindricalGearShaper":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _817

        return self.__parent__._cast(_817.CylindricalGearShaper)

    @property
    def cylindrical_gear_shaver(self: "CastSelf") -> "_818.CylindricalGearShaver":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _818

        return self.__parent__._cast(_818.CylindricalGearShaver)

    @property
    def involute_cutter_design(self: "CastSelf") -> "InvoluteCutterDesign":
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
class InvoluteCutterDesign(_816.CylindricalGearRealCutterDesign):
    """InvoluteCutterDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INVOLUTE_CUTTER_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def hand(self: "Self") -> "_423.Hand":
        """mastapy.gears.Hand"""
        temp = pythonnet_property_get(self.wrapped, "Hand")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Gears.Hand")

        if value is None:
            return None

        return constructor.new_from_mastapy("mastapy._private.gears._423", "Hand")(
            value
        )

    @hand.setter
    @exception_bridge
    @enforce_parameter_types
    def hand(self: "Self", value: "_423.Hand") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.Gears.Hand")
        pythonnet_property_set(self.wrapped, "Hand", value)

    @property
    @exception_bridge
    def helix_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "HelixAngle")

        if temp is None:
            return 0.0

        return temp

    @helix_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def helix_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "HelixAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def number_of_teeth(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfTeeth")

        if temp is None:
            return 0.0

        return temp

    @number_of_teeth.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_teeth(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfTeeth", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def tooth_thickness(self: "Self") -> "_1199.ToothThicknessSpecificationBase":
        """mastapy.gears.gear_designs.cylindrical.ToothThicknessSpecificationBase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothThickness")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_InvoluteCutterDesign":
        """Cast to another type.

        Returns:
            _Cast_InvoluteCutterDesign
        """
        return _Cast_InvoluteCutterDesign(self)
