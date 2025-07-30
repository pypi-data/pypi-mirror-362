"""CylindricalGearRealCutterDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private._internal import constructor, conversion, utility
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
from mastapy._private.gears.manufacturing.cylindrical.cutters import _809

_CYLINDRICAL_GEAR_REAL_CUTTER_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters",
    "CylindricalGearRealCutterDesign",
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.gears.manufacturing.cylindrical.cutters import (
        _807,
        _810,
        _811,
        _812,
        _813,
        _815,
        _817,
        _818,
        _821,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles import _826
    from mastapy._private.utility.databases import _2028

    Self = TypeVar("Self", bound="CylindricalGearRealCutterDesign")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearRealCutterDesign._Cast_CylindricalGearRealCutterDesign",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearRealCutterDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearRealCutterDesign:
    """Special nested class for casting CylindricalGearRealCutterDesign to subclasses."""

    __parent__: "CylindricalGearRealCutterDesign"

    @property
    def cylindrical_gear_abstract_cutter_design(
        self: "CastSelf",
    ) -> "_809.CylindricalGearAbstractCutterDesign":
        return self.__parent__._cast(_809.CylindricalGearAbstractCutterDesign)

    @property
    def named_database_item(self: "CastSelf") -> "_2028.NamedDatabaseItem":
        from mastapy._private.utility.databases import _2028

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
    def cylindrical_gear_real_cutter_design(
        self: "CastSelf",
    ) -> "CylindricalGearRealCutterDesign":
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
class CylindricalGearRealCutterDesign(_809.CylindricalGearAbstractCutterDesign):
    """CylindricalGearRealCutterDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_REAL_CUTTER_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def cutter_and_gear_normal_base_pitch_comparison_tolerance(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "CutterAndGearNormalBasePitchComparisonTolerance"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @cutter_and_gear_normal_base_pitch_comparison_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def cutter_and_gear_normal_base_pitch_comparison_tolerance(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "CutterAndGearNormalBasePitchComparisonTolerance", value
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
    def nominal_cutter_drawing(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalCutterDrawing")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def normal_base_pitch(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalBasePitch")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_pitch(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalPitch")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_pressure_angle_constant_base_pitch(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "NormalPressureAngleConstantBasePitch"
        )

        if temp is None:
            return 0.0

        return temp

    @normal_pressure_angle_constant_base_pitch.setter
    @exception_bridge
    @enforce_parameter_types
    def normal_pressure_angle_constant_base_pitch(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NormalPressureAngleConstantBasePitch",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def number_of_points_for_reporting_fillet_shape(
        self: "Self",
    ) -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfPointsForReportingFilletShape"
        )

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @number_of_points_for_reporting_fillet_shape.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_points_for_reporting_fillet_shape(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "NumberOfPointsForReportingFilletShape", value
        )

    @property
    @exception_bridge
    def number_of_points_for_reporting_main_blade_shape(
        self: "Self",
    ) -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfPointsForReportingMainBladeShape"
        )

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @number_of_points_for_reporting_main_blade_shape.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_points_for_reporting_main_blade_shape(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "NumberOfPointsForReportingMainBladeShape", value
        )

    @property
    @exception_bridge
    def specify_custom_blade_shape(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "SpecifyCustomBladeShape")

        if temp is None:
            return False

        return temp

    @specify_custom_blade_shape.setter
    @exception_bridge
    @enforce_parameter_types
    def specify_custom_blade_shape(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifyCustomBladeShape",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def customised_cutting_edge_profile(self: "Self") -> "_807.CustomisableEdgeProfile":
        """mastapy.gears.manufacturing.cylindrical.cutters.CustomisableEdgeProfile

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CustomisedCuttingEdgeProfile")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def nominal_cutter_shape(self: "Self") -> "_826.CutterShapeDefinition":
        """mastapy.gears.manufacturing.cylindrical.cutters.tangibles.CutterShapeDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalCutterShape")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearRealCutterDesign":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearRealCutterDesign
        """
        return _Cast_CylindricalGearRealCutterDesign(self)
