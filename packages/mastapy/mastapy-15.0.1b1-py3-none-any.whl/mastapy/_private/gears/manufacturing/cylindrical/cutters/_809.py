"""CylindricalGearAbstractCutterDesign"""

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
from mastapy._private.utility.databases import _2028

_CYLINDRICAL_GEAR_ABSTRACT_CUTTER_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters",
    "CylindricalGearAbstractCutterDesign",
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.gears.manufacturing.cylindrical.cutters import (
        _810,
        _811,
        _812,
        _813,
        _815,
        _816,
        _817,
        _818,
        _821,
    )

    Self = TypeVar("Self", bound="CylindricalGearAbstractCutterDesign")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearAbstractCutterDesign._Cast_CylindricalGearAbstractCutterDesign",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearAbstractCutterDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearAbstractCutterDesign:
    """Special nested class for casting CylindricalGearAbstractCutterDesign to subclasses."""

    __parent__: "CylindricalGearAbstractCutterDesign"

    @property
    def named_database_item(self: "CastSelf") -> "_2028.NamedDatabaseItem":
        return self.__parent__._cast(_2028.NamedDatabaseItem)

    @property
    def cylindrical_gear_form_grinding_wheel(
        self: "CastSelf",
    ) -> "_810.CylindricalGearFormGrindingWheel":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _810

        return self.__parent__._cast(_810.CylindricalGearFormGrindingWheel)

    @property
    def cylindrical_gear_grinding_worm(
        self: "CastSelf",
    ) -> "_811.CylindricalGearGrindingWorm":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _811

        return self.__parent__._cast(_811.CylindricalGearGrindingWorm)

    @property
    def cylindrical_gear_hob_design(
        self: "CastSelf",
    ) -> "_812.CylindricalGearHobDesign":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _812

        return self.__parent__._cast(_812.CylindricalGearHobDesign)

    @property
    def cylindrical_gear_plunge_shaver(
        self: "CastSelf",
    ) -> "_813.CylindricalGearPlungeShaver":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _813

        return self.__parent__._cast(_813.CylindricalGearPlungeShaver)

    @property
    def cylindrical_gear_rack_design(
        self: "CastSelf",
    ) -> "_815.CylindricalGearRackDesign":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _815

        return self.__parent__._cast(_815.CylindricalGearRackDesign)

    @property
    def cylindrical_gear_real_cutter_design(
        self: "CastSelf",
    ) -> "_816.CylindricalGearRealCutterDesign":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _816

        return self.__parent__._cast(_816.CylindricalGearRealCutterDesign)

    @property
    def cylindrical_gear_shaper(self: "CastSelf") -> "_817.CylindricalGearShaper":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _817

        return self.__parent__._cast(_817.CylindricalGearShaper)

    @property
    def cylindrical_gear_shaver(self: "CastSelf") -> "_818.CylindricalGearShaver":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _818

        return self.__parent__._cast(_818.CylindricalGearShaver)

    @property
    def involute_cutter_design(self: "CastSelf") -> "_821.InvoluteCutterDesign":
        from mastapy._private.gears.manufacturing.cylindrical.cutters import _821

        return self.__parent__._cast(_821.InvoluteCutterDesign)

    @property
    def cylindrical_gear_abstract_cutter_design(
        self: "CastSelf",
    ) -> "CylindricalGearAbstractCutterDesign":
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
class CylindricalGearAbstractCutterDesign(_2028.NamedDatabaseItem):
    """CylindricalGearAbstractCutterDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_ABSTRACT_CUTTER_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def cutter_type(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CutterType")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def edge_radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EdgeRadius")

        if temp is None:
            return 0.0

        return temp

    @edge_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def edge_radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "EdgeRadius", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def nominal_normal_pressure_angle(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "NominalNormalPressureAngle")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @nominal_normal_pressure_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def nominal_normal_pressure_angle(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "NominalNormalPressureAngle", value)

    @property
    @exception_bridge
    def normal_module(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NormalModule")

        if temp is None:
            return 0.0

        return temp

    @normal_module.setter
    @exception_bridge
    @enforce_parameter_types
    def normal_module(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "NormalModule", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def normal_pressure_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NormalPressureAngle")

        if temp is None:
            return 0.0

        return temp

    @normal_pressure_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def normal_pressure_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NormalPressureAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearAbstractCutterDesign":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearAbstractCutterDesign
        """
        return _Cast_CylindricalGearAbstractCutterDesign(self)
