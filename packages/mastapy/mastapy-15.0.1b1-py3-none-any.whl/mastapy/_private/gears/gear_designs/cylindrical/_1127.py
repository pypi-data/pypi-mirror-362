"""CylindricalGearFlankDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
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

_CYLINDRICAL_GEAR_FLANK_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "CylindricalGearFlankDesign"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.gears.gear_designs.cylindrical import _1135

    Self = TypeVar("Self", bound="CylindricalGearFlankDesign")
    CastSelf = TypeVar(
        "CastSelf", bound="CylindricalGearFlankDesign._Cast_CylindricalGearFlankDesign"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearFlankDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearFlankDesign:
    """Special nested class for casting CylindricalGearFlankDesign to subclasses."""

    __parent__: "CylindricalGearFlankDesign"

    @property
    def cylindrical_gear_flank_design(self: "CastSelf") -> "CylindricalGearFlankDesign":
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
class CylindricalGearFlankDesign(_0.APIBase):
    """CylindricalGearFlankDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_FLANK_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def absolute_base_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AbsoluteBaseDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def absolute_form_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AbsoluteFormDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def absolute_form_to_sap_diameter_clearance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AbsoluteFormToSAPDiameterClearance"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def absolute_tip_form_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AbsoluteTipFormDiameter")

        if temp is None:
            return 0.0

        return temp

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
    def base_thickness_half_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BaseThicknessHalfAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def base_to_form_diameter_clearance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BaseToFormDiameterClearance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def base_to_form_diameter_clearance_as_normal_module_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BaseToFormDiameterClearanceAsNormalModuleRatio"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def chamfer_angle_in_normal_plane(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ChamferAngleInNormalPlane")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def effective_tip_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EffectiveTipRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def flank_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FlankName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def form_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FormRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def form_to_sap_diameter_absolute_clearance_as_normal_module_ratio(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "FormToSAPDiameterAbsoluteClearanceAsNormalModuleRatio"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def has_chamfer(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HasChamfer")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def is_undercut_by_cutter(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsUndercutByCutter")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def lowest_sap_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LowestSAPDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_normal_thickness_at_root_form_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MeanNormalThicknessAtRootFormDiameter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_normal_thickness_at_tip_form_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MeanNormalThicknessAtTipFormDiameter"
        )

        if temp is None:
            return 0.0

        return temp

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
    def normal_pressure_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalPressureAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def radii_of_curvature_at_tip(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RadiiOfCurvatureAtTip")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @radii_of_curvature_at_tip.setter
    @exception_bridge
    @enforce_parameter_types
    def radii_of_curvature_at_tip(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RadiiOfCurvatureAtTip", value)

    @property
    @exception_bridge
    def root_form_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RootFormDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def root_form_roll_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RootFormRollAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def root_form_roll_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RootFormRollDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def signed_root_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SignedRootDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tip_form_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TipFormDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tip_form_roll_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TipFormRollAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tip_form_roll_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TipFormRollDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tooth_thickness_half_angle_at_reference_circle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ToothThicknessHalfAngleAtReferenceCircle"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transverse_base_pitch(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransverseBasePitch")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transverse_chamfer_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransverseChamferAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transverse_pressure_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransversePressureAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def highest_point_of_fewest_tooth_contacts(
        self: "Self",
    ) -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HighestPointOfFewestToothContacts")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def lowest_point_of_fewest_tooth_contacts(
        self: "Self",
    ) -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LowestPointOfFewestToothContacts")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def lowest_start_of_active_profile(
        self: "Self",
    ) -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LowestStartOfActiveProfile")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def root_diameter_reporting(
        self: "Self",
    ) -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RootDiameterReporting")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def root_form(self: "Self") -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RootForm")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def tip_diameter_reporting(
        self: "Self",
    ) -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TipDiameterReporting")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def tip_form(self: "Self") -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TipForm")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearFlankDesign":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearFlankDesign
        """
        return _Cast_CylindricalGearFlankDesign(self)
