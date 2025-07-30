"""DetailedBoltDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_get_with_method,
    pythonnet_property_set,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private._math.vector_3d import Vector3D

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_DETAILED_BOLT_DESIGN = python_net_import("SMT.MastaAPI.Bolts", "DetailedBoltDesign")

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.bolts import _1651, _1653, _1655, _1660, _1665, _1668

    Self = TypeVar("Self", bound="DetailedBoltDesign")
    CastSelf = TypeVar("CastSelf", bound="DetailedBoltDesign._Cast_DetailedBoltDesign")


__docformat__ = "restructuredtext en"
__all__ = ("DetailedBoltDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DetailedBoltDesign:
    """Special nested class for casting DetailedBoltDesign to subclasses."""

    __parent__: "DetailedBoltDesign"

    @property
    def detailed_bolt_design(self: "CastSelf") -> "DetailedBoltDesign":
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
class DetailedBoltDesign(_0.APIBase):
    """DetailedBoltDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DETAILED_BOLT_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def appropriate_minimum_bolt_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AppropriateMinimumBoltDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def appropriate_minimum_cross_sectional_area_for_hollow_bolt(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AppropriateMinimumCrossSectionalAreaForHollowBolt"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def average_outside_diameter_of_clamped_parts(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AverageOutsideDiameterOfClampedParts"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def average_surface_roughness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AverageSurfaceRoughness")

        if temp is None:
            return 0.0

        return temp

    @average_surface_roughness.setter
    @exception_bridge
    @enforce_parameter_types
    def average_surface_roughness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AverageSurfaceRoughness",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def bearing_area_diameter_at_the_interface(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BearingAreaDiameterAtTheInterface")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def chamfer_diameter_at_the_clamped_parts(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ChamferDiameterAtTheClampedParts")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def clamped_parts(self: "Self") -> "List[_1660.ClampedSection]":
        """List[mastapy.bolts.ClampedSection]"""
        temp = pythonnet_property_get(self.wrapped, "ClampedParts")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @clamped_parts.setter
    @exception_bridge
    @enforce_parameter_types
    def clamped_parts(self: "Self", value: "List[_1660.ClampedSection]") -> None:
        value = conversion.mp_to_pn_objects_in_list(value)
        pythonnet_property_set(self.wrapped, "ClampedParts", value)

    @property
    @exception_bridge
    def clamping_length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ClampingLength")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def consider_this_tapped_thread_bolt_as_a_through_bolted_joint(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "ConsiderThisTappedThreadBoltAsAThroughBoltedJoint"
        )

        if temp is None:
            return False

        return temp

    @consider_this_tapped_thread_bolt_as_a_through_bolted_joint.setter
    @exception_bridge
    @enforce_parameter_types
    def consider_this_tapped_thread_bolt_as_a_through_bolted_joint(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ConsiderThisTappedThreadBoltAsAThroughBoltedJoint",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def counter_bore_depth(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CounterBoreDepth")

        if temp is None:
            return 0.0

        return temp

    @counter_bore_depth.setter
    @exception_bridge
    @enforce_parameter_types
    def counter_bore_depth(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "CounterBoreDepth", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def cross_section_of_thread(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CrossSectionOfThread")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def deformation_cone_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DeformationConeAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def diameter_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DiameterRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def diameter_for_the_specified_standard_size(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DiameterForTheSpecifiedStandardSize"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def diameter_of_shearing_cross_section(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DiameterOfShearingCrossSection")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def distance_of_bolt_axis_from_central_point(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "DistanceOfBoltAxisFromCentralPoint"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @distance_of_bolt_axis_from_central_point.setter
    @exception_bridge
    @enforce_parameter_types
    def distance_of_bolt_axis_from_central_point(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "DistanceOfBoltAxisFromCentralPoint", value
        )

    @property
    @exception_bridge
    def distance_of_the_bolt_axis_from_edge_of_interface(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "DistanceOfTheBoltAxisFromEdgeOfInterface"
        )

        if temp is None:
            return 0.0

        return temp

    @distance_of_the_bolt_axis_from_edge_of_interface.setter
    @exception_bridge
    @enforce_parameter_types
    def distance_of_the_bolt_axis_from_edge_of_interface(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "DistanceOfTheBoltAxisFromEdgeOfInterface",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def edit_bolt_geometry(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "EditBoltGeometry", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @edit_bolt_geometry.setter
    @exception_bridge
    @enforce_parameter_types
    def edit_bolt_geometry(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "EditBoltGeometry",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def edit_bolt_material(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "EditBoltMaterial", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @edit_bolt_material.setter
    @exception_bridge
    @enforce_parameter_types
    def edit_bolt_material(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "EditBoltMaterial",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def edit_nut_material(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "EditNutMaterial", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @edit_nut_material.setter
    @exception_bridge
    @enforce_parameter_types
    def edit_nut_material(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "EditNutMaterial",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def edit_tapped_thread_material(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "EditTappedThreadMaterial", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @edit_tapped_thread_material.setter
    @exception_bridge
    @enforce_parameter_types
    def edit_tapped_thread_material(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "EditTappedThreadMaterial",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def elastic_bending_resilience_of_clamped_parts(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ElasticBendingResilienceOfClampedParts"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def elastic_bending_resilience_of_concentric_clamped_parts(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ElasticBendingResilienceOfConcentricClampedParts"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def elastic_resilience_of_clamped_parts_eccentric_clamping(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ElasticResilienceOfClampedPartsEccentricClamping"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def elastic_resilience_of_clamped_parts(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElasticResilienceOfClampedParts")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def elastic_resilience_of_clamped_parts_eccentric_loading(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ElasticResilienceOfClampedPartsEccentricLoading"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def elastic_resilience_of_clamped_parts_in_operating_state(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ElasticResilienceOfClampedPartsInOperatingState"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def friction_radius(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "FrictionRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @friction_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def friction_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "FrictionRadius", value)

    @property
    @exception_bridge
    def height(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Height")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def inside_diameter_of_bearing_surface_of_washer(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "InsideDiameterOfBearingSurfaceOfWasher"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @inside_diameter_of_bearing_surface_of_washer.setter
    @exception_bridge
    @enforce_parameter_types
    def inside_diameter_of_bearing_surface_of_washer(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "InsideDiameterOfBearingSurfaceOfWasher", value
        )

    @property
    @exception_bridge
    def inside_diameter_of_head_bearing_area(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InsideDiameterOfHeadBearingArea")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def inside_diameter_of_plane_head_bearing_surface(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "InsideDiameterOfPlaneHeadBearingSurface"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def is_concentrically_clamped(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsConcentricallyClamped")

        if temp is None:
            return False

        return temp

    @is_concentrically_clamped.setter
    @exception_bridge
    @enforce_parameter_types
    def is_concentrically_clamped(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IsConcentricallyClamped",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def joint_coefficient(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "JointCoefficient")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def joint_geometry(self: "Self") -> "_1665.JointGeometries":
        """mastapy.bolts.JointGeometries"""
        temp = pythonnet_property_get(self.wrapped, "JointGeometry")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Bolts.JointGeometries")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bolts._1665", "JointGeometries"
        )(value)

    @joint_geometry.setter
    @exception_bridge
    @enforce_parameter_types
    def joint_geometry(self: "Self", value: "_1665.JointGeometries") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.Bolts.JointGeometries")
        pythonnet_property_set(self.wrapped, "JointGeometry", value)

    @property
    @exception_bridge
    def length_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LengthRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def length_of_deformation_cone(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LengthOfDeformationCone")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def length_of_deformation_sleeve(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LengthOfDeformationSleeve")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def length_of_free_loaded_thread(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LengthOfFreeLoadedThread")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def limiting_outside_diameter_maximum_diameter_of_deformation_cone(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LimitingOutsideDiameterMaximumDiameterOfDeformationCone"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def limiting_value_of_interface_dsv(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LimitingValueOfInterfaceDSV")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def limiting_value_of_interface_esv(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LimitingValueOfInterfaceESV")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def limiting_value_of_interface_esv_with_recessed_tapped_hole(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LimitingValueOfInterfaceESVWithRecessedTappedHole"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_coefficient_of_friction_of_bearing_area(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumCoefficientOfFrictionOfBearingArea"
        )

        if temp is None:
            return 0.0

        return temp

    @maximum_coefficient_of_friction_of_bearing_area.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_coefficient_of_friction_of_bearing_area(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumCoefficientOfFrictionOfBearingArea",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def maximum_coefficient_of_friction_of_thread(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumCoefficientOfFrictionOfThread"
        )

        if temp is None:
            return 0.0

        return temp

    @maximum_coefficient_of_friction_of_thread.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_coefficient_of_friction_of_thread(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumCoefficientOfFrictionOfThread",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def maximum_outside_diameter_of_deformation_cone(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumOutsideDiameterOfDeformationCone"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def measurement_interface_area_perpendicular_to_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MeasurementInterfaceAreaPerpendicularToWidth"
        )

        if temp is None:
            return 0.0

        return temp

    @measurement_interface_area_perpendicular_to_width.setter
    @exception_bridge
    @enforce_parameter_types
    def measurement_interface_area_perpendicular_to_width(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MeasurementInterfaceAreaPerpendicularToWidth",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def minimum_assembly_bearing_area_of_head(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumAssemblyBearingAreaOfHead")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_assembly_bearing_area_of_nut(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumAssemblyBearingAreaOfNut")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_bearing_area(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumBearingArea")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_coefficient_of_friction_at_interface(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MinimumCoefficientOfFrictionAtInterface"
        )

        if temp is None:
            return 0.0

        return temp

    @minimum_coefficient_of_friction_at_interface.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_coefficient_of_friction_at_interface(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumCoefficientOfFrictionAtInterface",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def minimum_coefficient_of_friction_of_bearing_area(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MinimumCoefficientOfFrictionOfBearingArea"
        )

        if temp is None:
            return 0.0

        return temp

    @minimum_coefficient_of_friction_of_bearing_area.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_coefficient_of_friction_of_bearing_area(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumCoefficientOfFrictionOfBearingArea",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def minimum_coefficient_of_friction_of_thread(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MinimumCoefficientOfFrictionOfThread"
        )

        if temp is None:
            return 0.0

        return temp

    @minimum_coefficient_of_friction_of_thread.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_coefficient_of_friction_of_thread(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumCoefficientOfFrictionOfThread",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def minimum_plate_thickness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumPlateThickness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def moment_of_gyration_of_cross_section_at_minor_thread_diameter(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MomentOfGyrationOfCrossSectionAtMinorThreadDiameter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @name.setter
    @exception_bridge
    @enforce_parameter_types
    def name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Name", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def nominal_cross_section(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalCrossSection")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def nominal_cross_section_of_hollow_bolt(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalCrossSectionOfHollowBolt")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def number_of_bolt_sections(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfBoltSections")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_force_transmitting_interfaces(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfForceTransmittingInterfaces"
        )

        if temp is None:
            return 0

        return temp

    @number_of_force_transmitting_interfaces.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_force_transmitting_interfaces(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfForceTransmittingInterfaces",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def number_of_torque_transmitting_interfaces(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfTorqueTransmittingInterfaces"
        )

        if temp is None:
            return 0

        return temp

    @number_of_torque_transmitting_interfaces.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_torque_transmitting_interfaces(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfTorqueTransmittingInterfaces",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def nut_chamfer_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NutChamferDiameter")

        if temp is None:
            return 0.0

        return temp

    @nut_chamfer_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def nut_chamfer_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NutChamferDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def outside_diameter_of_bearing_surface_of_washer(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "OutsideDiameterOfBearingSurfaceOfWasher"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @outside_diameter_of_bearing_surface_of_washer.setter
    @exception_bridge
    @enforce_parameter_types
    def outside_diameter_of_bearing_surface_of_washer(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "OutsideDiameterOfBearingSurfaceOfWasher", value
        )

    @property
    @exception_bridge
    def outside_diameter_of_nut(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OutsideDiameterOfNut")

        if temp is None:
            return 0.0

        return temp

    @outside_diameter_of_nut.setter
    @exception_bridge
    @enforce_parameter_types
    def outside_diameter_of_nut(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OutsideDiameterOfNut",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def reduction_coefficient(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ReductionCoefficient")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @reduction_coefficient.setter
    @exception_bridge
    @enforce_parameter_types
    def reduction_coefficient(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ReductionCoefficient", value)

    @property
    @exception_bridge
    def rolled_before_or_after_heat_treatment(
        self: "Self",
    ) -> "_1668.RolledBeforeOrAfterHeatTreatment":
        """mastapy.bolts.RolledBeforeOrAfterHeatTreatment"""
        temp = pythonnet_property_get(self.wrapped, "RolledBeforeOrAfterHeatTreatment")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bolts.RolledBeforeOrAfterHeatTreatment"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bolts._1668", "RolledBeforeOrAfterHeatTreatment"
        )(value)

    @rolled_before_or_after_heat_treatment.setter
    @exception_bridge
    @enforce_parameter_types
    def rolled_before_or_after_heat_treatment(
        self: "Self", value: "_1668.RolledBeforeOrAfterHeatTreatment"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Bolts.RolledBeforeOrAfterHeatTreatment"
        )
        pythonnet_property_set(self.wrapped, "RolledBeforeOrAfterHeatTreatment", value)

    @property
    @exception_bridge
    def sealing_area(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SealingArea")

        if temp is None:
            return 0.0

        return temp

    @sealing_area.setter
    @exception_bridge
    @enforce_parameter_types
    def sealing_area(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "SealingArea", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def section_radii_of_gyration(self: "Self") -> "List[float]":
        """List[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SectionRadiiOfGyration")

        if temp is None:
            return None

        value = conversion.to_list_any(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def shearing_area_transverse_loading(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShearingAreaTransverseLoading")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stress_cross_sectional_area(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StressCrossSectionalArea")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stress_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StressDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def substitutional_bending_length_of_bolt(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SubstitutionalBendingLengthOfBolt")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def substitutional_extension_length_of_engaged_nut_thread(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SubstitutionalExtensionLengthOfEngagedNutThread"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def substitutional_extension_length_of_engaged_thread(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SubstitutionalExtensionLengthOfEngagedThread"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def substitutional_extension_length_of_head(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SubstitutionalExtensionLengthOfHead"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def substitutional_moment_of_gyration_of_cone(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SubstitutionalMomentOfGyrationOfCone"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def substitutional_moment_of_gyration_of_plates(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SubstitutionalMomentOfGyrationOfPlates"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def substitutional_moment_of_gyration_of_plates_minus_bolt_area(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SubstitutionalMomentOfGyrationOfPlatesMinusBoltArea"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def substitutional_moment_of_gyration_of_sleeve(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SubstitutionalMomentOfGyrationOfSleeve"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def substitutional_outside_diameter_of_basic_solid(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "SubstitutionalOutsideDiameterOfBasicSolid"
        )

        if temp is None:
            return 0.0

        return temp

    @substitutional_outside_diameter_of_basic_solid.setter
    @exception_bridge
    @enforce_parameter_types
    def substitutional_outside_diameter_of_basic_solid(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "SubstitutionalOutsideDiameterOfBasicSolid",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def substitutional_outside_diameter_of_basic_solid_at_interface(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "SubstitutionalOutsideDiameterOfBasicSolidAtInterface"
        )

        if temp is None:
            return 0.0

        return temp

    @substitutional_outside_diameter_of_basic_solid_at_interface.setter
    @exception_bridge
    @enforce_parameter_types
    def substitutional_outside_diameter_of_basic_solid_at_interface(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "SubstitutionalOutsideDiameterOfBasicSolidAtInterface",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def total_axial_resilience(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalAxialResilience")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_bending_resilience(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalBendingResilience")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def utilization_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "UtilizationFactor")

        if temp is None:
            return 0.0

        return temp

    @utilization_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def utilization_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UtilizationFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def washer_thickness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WasherThickness")

        if temp is None:
            return 0.0

        return temp

    @washer_thickness.setter
    @exception_bridge
    @enforce_parameter_types
    def washer_thickness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "WasherThickness", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Width")

        if temp is None:
            return 0.0

        return temp

    @width.setter
    @exception_bridge
    @enforce_parameter_types
    def width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Width", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def bolt_geometry(self: "Self") -> "_1653.BoltGeometry":
        """mastapy.bolts.BoltGeometry

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BoltGeometry")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def material_of_bolt(self: "Self") -> "_1655.BoltMaterial":
        """mastapy.bolts.BoltMaterial

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaterialOfBolt")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def material_of_nut(self: "Self") -> "_1651.BoltedJointMaterial":
        """mastapy.bolts.BoltedJointMaterial

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaterialOfNut")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def material_of_tapped_thread(self: "Self") -> "_1651.BoltedJointMaterial":
        """mastapy.bolts.BoltedJointMaterial

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaterialOfTappedThread")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def orientation(self: "Self") -> "Vector3D":
        """Vector3D"""
        temp = pythonnet_property_get(self.wrapped, "Orientation")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @orientation.setter
    @exception_bridge
    @enforce_parameter_types
    def orientation(self: "Self", value: "Vector3D") -> None:
        value = conversion.mp_to_pn_vector3d(value)
        pythonnet_property_set(self.wrapped, "Orientation", value)

    @property
    @exception_bridge
    def clamped_sections(self: "Self") -> "List[_1660.ClampedSection]":
        """List[mastapy.bolts.ClampedSection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ClampedSections")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @exception_bridge
    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputDefaultReportTo", file_path)

    @exception_bridge
    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportTo", file_path)

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportAsTextTo", file_path)

    @exception_bridge
    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_DetailedBoltDesign":
        """Cast to another type.

        Returns:
            _Cast_DetailedBoltDesign
        """
        return _Cast_DetailedBoltDesign(self)
