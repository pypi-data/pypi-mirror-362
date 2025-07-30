"""CylindricalGearShaver"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.manufacturing.cylindrical.cutters import _821

_CYLINDRICAL_GEAR_SHAVER = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters", "CylindricalGearShaver"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.gears.manufacturing.cylindrical.cutters import (
        _809,
        _813,
        _816,
    )
    from mastapy._private.utility.databases import _2028

    Self = TypeVar("Self", bound="CylindricalGearShaver")
    CastSelf = TypeVar(
        "CastSelf", bound="CylindricalGearShaver._Cast_CylindricalGearShaver"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearShaver",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearShaver:
    """Special nested class for casting CylindricalGearShaver to subclasses."""

    __parent__: "CylindricalGearShaver"

    @property
    def involute_cutter_design(self: "CastSelf") -> "_821.InvoluteCutterDesign":
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
    ) -> "_813.CylindricalGearPlungeShaver":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _813

        return self.__parent__._cast(_813.CylindricalGearPlungeShaver)

    @property
    def cylindrical_gear_shaver(self: "CastSelf") -> "CylindricalGearShaver":
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
class CylindricalGearShaver(_821.InvoluteCutterDesign):
    """CylindricalGearShaver

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_SHAVER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def base_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BaseDiameter")

        if temp is None:
            return 0.0

        return temp

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
    def normal_tip_thickness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalTipThickness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def root_form_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RootFormDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @root_form_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def root_form_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RootFormDiameter", value)

    @property
    @exception_bridge
    def tip_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TipDiameter")

        if temp is None:
            return 0.0

        return temp

    @tip_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def tip_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "TipDiameter", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearShaver":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearShaver
        """
        return _Cast_CylindricalGearShaver(self)
