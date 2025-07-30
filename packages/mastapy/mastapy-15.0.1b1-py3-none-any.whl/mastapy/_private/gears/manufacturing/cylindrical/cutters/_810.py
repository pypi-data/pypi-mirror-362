"""CylindricalGearFormGrindingWheel"""

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
from mastapy._private.gears.manufacturing.cylindrical.cutters import _816

_CYLINDRICAL_GEAR_FORM_GRINDING_WHEEL = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters",
    "CylindricalGearFormGrindingWheel",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical.cutters import _809
    from mastapy._private.math_utility import _1718
    from mastapy._private.utility.databases import _2028

    Self = TypeVar("Self", bound="CylindricalGearFormGrindingWheel")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearFormGrindingWheel._Cast_CylindricalGearFormGrindingWheel",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearFormGrindingWheel",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearFormGrindingWheel:
    """Special nested class for casting CylindricalGearFormGrindingWheel to subclasses."""

    __parent__: "CylindricalGearFormGrindingWheel"

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
    def cylindrical_gear_form_grinding_wheel(
        self: "CastSelf",
    ) -> "CylindricalGearFormGrindingWheel":
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
class CylindricalGearFormGrindingWheel(_816.CylindricalGearRealCutterDesign):
    """CylindricalGearFormGrindingWheel

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_FORM_GRINDING_WHEEL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Radius")

        if temp is None:
            return 0.0

        return temp

    @radius.setter
    @exception_bridge
    @enforce_parameter_types
    def radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Radius", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def right_hand_cutting_edge_shape(self: "Self") -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "RightHandCuttingEdgeShape")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @right_hand_cutting_edge_shape.setter
    @exception_bridge
    @enforce_parameter_types
    def right_hand_cutting_edge_shape(
        self: "Self", value: "_1718.Vector2DListAccessor"
    ) -> None:
        pythonnet_property_set(self.wrapped, "RightHandCuttingEdgeShape", value.wrapped)

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearFormGrindingWheel":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearFormGrindingWheel
        """
        return _Cast_CylindricalGearFormGrindingWheel(self)
