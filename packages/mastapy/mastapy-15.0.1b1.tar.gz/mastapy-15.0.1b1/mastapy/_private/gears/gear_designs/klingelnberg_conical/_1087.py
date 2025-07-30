"""KlingelnbergConicalGearSetDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import list_with_selected_item
from mastapy._private._internal.list_with_selected_item import (
    promote_to_list_with_selected_item,
)
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs.conical import _1276

_KLINGELNBERG_CONICAL_GEAR_SET_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.KlingelnbergConical",
    "KlingelnbergConicalGearSetDesign",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs import _1052, _1054
    from mastapy._private.gears.gear_designs.conical import _1288
    from mastapy._private.gears.gear_designs.klingelnberg_conical import _1086
    from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1083
    from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1079

    Self = TypeVar("Self", bound="KlingelnbergConicalGearSetDesign")
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergConicalGearSetDesign._Cast_KlingelnbergConicalGearSetDesign",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergConicalGearSetDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergConicalGearSetDesign:
    """Special nested class for casting KlingelnbergConicalGearSetDesign to subclasses."""

    __parent__: "KlingelnbergConicalGearSetDesign"

    @property
    def conical_gear_set_design(self: "CastSelf") -> "_1276.ConicalGearSetDesign":
        return self.__parent__._cast(_1276.ConicalGearSetDesign)

    @property
    def gear_set_design(self: "CastSelf") -> "_1054.GearSetDesign":
        from mastapy._private.gears.gear_designs import _1054

        return self.__parent__._cast(_1054.GearSetDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_1052.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _1052

        return self.__parent__._cast(_1052.GearDesignComponent)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_design(
        self: "CastSelf",
    ) -> "_1079.KlingelnbergCycloPalloidSpiralBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1079

        return self.__parent__._cast(
            _1079.KlingelnbergCycloPalloidSpiralBevelGearSetDesign
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_design(
        self: "CastSelf",
    ) -> "_1083.KlingelnbergCycloPalloidHypoidGearSetDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1083

        return self.__parent__._cast(_1083.KlingelnbergCycloPalloidHypoidGearSetDesign)

    @property
    def klingelnberg_conical_gear_set_design(
        self: "CastSelf",
    ) -> "KlingelnbergConicalGearSetDesign":
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
class KlingelnbergConicalGearSetDesign(_1276.ConicalGearSetDesign):
    """KlingelnbergConicalGearSetDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _KLINGELNBERG_CONICAL_GEAR_SET_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def addendum_modification_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AddendumModificationFactor")

        if temp is None:
            return 0.0

        return temp

    @addendum_modification_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def addendum_modification_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AddendumModificationFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def addendum_of_tool(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AddendumOfTool")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def angle_modification(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AngleModification")

        if temp is None:
            return 0.0

        return temp

    @angle_modification.setter
    @exception_bridge
    @enforce_parameter_types
    def angle_modification(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AngleModification",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def auxiliary_value_for_angle_modification(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AuxiliaryValueForAngleModification"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def auxiliary_angle_at_re(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AuxiliaryAngleAtRe")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def auxiliary_angle_at_ri(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AuxiliaryAngleAtRi")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def auxilliary_angle_at_re_2(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AuxilliaryAngleAtRe2")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def auxilliary_angle_at_ri_2(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AuxilliaryAngleAtRi2")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def base_circle_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BaseCircleRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def cone_distance_maximum_tooth_gap(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConeDistanceMaximumToothGap")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def cutter_blade_tip_width_causes_cut_off(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CutterBladeTipWidthCausesCutOff")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def cutter_blade_tip_width_causes_ridge(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CutterBladeTipWidthCausesRidge")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def cutter_module(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CutterModule")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def cutter_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CutterRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def effective_face_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EffectiveFaceWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def face_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceContactRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_cutting_machine_options(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "GearCuttingMachineOptions")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @gear_cutting_machine_options.setter
    @exception_bridge
    @enforce_parameter_types
    def gear_cutting_machine_options(self: "Self", value: "str") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "GearCuttingMachineOptions", value)

    @property
    @exception_bridge
    def gear_finish(self: "Self") -> "_1288.KlingelnbergFinishingMethods":
        """mastapy.gears.gear_designs.conical.KlingelnbergFinishingMethods"""
        temp = pythonnet_property_get(self.wrapped, "GearFinish")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.GearDesigns.Conical.KlingelnbergFinishingMethods"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.conical._1288",
            "KlingelnbergFinishingMethods",
        )(value)

    @gear_finish.setter
    @exception_bridge
    @enforce_parameter_types
    def gear_finish(self: "Self", value: "_1288.KlingelnbergFinishingMethods") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.GearDesigns.Conical.KlingelnbergFinishingMethods"
        )
        pythonnet_property_set(self.wrapped, "GearFinish", value)

    @property
    @exception_bridge
    def lead_angle_on_cutter_head(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeadAngleOnCutterHead")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def machine_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MachineDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def module(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Module")

        if temp is None:
            return 0.0

        return temp

    @module.setter
    @exception_bridge
    @enforce_parameter_types
    def module(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Module", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def normal_module_at_inner_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalModuleAtInnerDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_module_at_outer_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalModuleAtOuterDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_pressure_angle_at_tooth_tip(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalPressureAngleAtToothTip")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def number_of_starts(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfStarts")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_generating_cone_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionGeneratingConeAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_number_of_teeth(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "PinionNumberOfTeeth")

        if temp is None:
            return 0

        return temp

    @pinion_number_of_teeth.setter
    @exception_bridge
    @enforce_parameter_types
    def pinion_number_of_teeth(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "PinionNumberOfTeeth", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def shaft_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def spiral_angle_at_wheel_inner_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpiralAngleAtWheelInnerDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def spiral_angle_at_wheel_outer_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpiralAngleAtWheelOuterDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stub_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StubFactor")

        if temp is None:
            return 0.0

        return temp

    @stub_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def stub_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "StubFactor", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def tip_circle_diameter_of_virtual_gear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TipCircleDiameterOfVirtualGear")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tip_cone_angle_from_tooth_tip_chamfering_reduction(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TipConeAngleFromToothTipChamferingReduction"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tooth_thickness_half_angle_on_pitch_cone(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ToothThicknessHalfAngleOnPitchCone"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tooth_thickness_half_angle_on_tooth_tip(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothThicknessHalfAngleOnToothTip")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tooth_thickness_modification_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ToothThicknessModificationFactor")

        if temp is None:
            return 0.0

        return temp

    @tooth_thickness_modification_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def tooth_thickness_modification_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ToothThicknessModificationFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def tooth_tip_chamfering_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ToothTipChamferingFactor")

        if temp is None:
            return 0.0

        return temp

    @tooth_tip_chamfering_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def tooth_tip_chamfering_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ToothTipChamferingFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def tooth_tip_thickness_at_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothTipThicknessAtInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tooth_tip_thickness_at_mean_cone_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ToothTipThicknessAtMeanConeDistance"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def use_minimum_addendum_modification_factor(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseMinimumAddendumModificationFactor"
        )

        if temp is None:
            return False

        return temp

    @use_minimum_addendum_modification_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def use_minimum_addendum_modification_factor(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseMinimumAddendumModificationFactor",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_required_tooth_tip_chamfering_factor(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseRequiredToothTipChamferingFactor"
        )

        if temp is None:
            return False

        return temp

    @use_required_tooth_tip_chamfering_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def use_required_tooth_tip_chamfering_factor(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseRequiredToothTipChamferingFactor",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def wheel_face_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WheelFaceWidth")

        if temp is None:
            return 0.0

        return temp

    @wheel_face_width.setter
    @exception_bridge
    @enforce_parameter_types
    def wheel_face_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "WheelFaceWidth", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def wheel_generating_cone_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelGeneratingConeAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_mean_spiral_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WheelMeanSpiralAngle")

        if temp is None:
            return 0.0

        return temp

    @wheel_mean_spiral_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def wheel_mean_spiral_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "WheelMeanSpiralAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def wheel_number_of_teeth(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "WheelNumberOfTeeth")

        if temp is None:
            return 0

        return temp

    @wheel_number_of_teeth.setter
    @exception_bridge
    @enforce_parameter_types
    def wheel_number_of_teeth(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "WheelNumberOfTeeth", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def wheel_pitch_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WheelPitchDiameter")

        if temp is None:
            return 0.0

        return temp

    @wheel_pitch_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def wheel_pitch_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "WheelPitchDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def whole_depth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WholeDepth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def conical_meshes(self: "Self") -> "List[_1086.KlingelnbergConicalGearMeshDesign]":
        """List[mastapy.gears.gear_designs.klingelnberg_conical.KlingelnbergConicalGearMeshDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalMeshes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def klingelnberg_conical_meshes(
        self: "Self",
    ) -> "List[_1086.KlingelnbergConicalGearMeshDesign]":
        """List[mastapy.gears.gear_designs.klingelnberg_conical.KlingelnbergConicalGearMeshDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "KlingelnbergConicalMeshes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_KlingelnbergConicalGearSetDesign":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergConicalGearSetDesign
        """
        return _Cast_KlingelnbergConicalGearSetDesign(self)
