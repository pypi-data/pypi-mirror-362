"""FESubstructure"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import (
    enum_with_selected_value,
    list_with_selected_item,
    overridable,
)
from mastapy._private._internal.list_with_selected_item import (
    promote_to_list_with_selected_item,
)
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_method_call_overload,
    pythonnet_property_get,
    pythonnet_property_get_with_method,
    pythonnet_property_set,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.nodal_analysis import _69
from mastapy._private.system_model.fe import _2610, _2636
from mastapy._private.system_model.part_model import _2670, _2674
from mastapy._private.utility.units_and_measurements import _1802

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_TASK_PROGRESS = python_net_import("SMT.MastaAPIUtility", "TaskProgress")
_FE_SUBSTRUCTURE = python_net_import("SMT.MastaAPI.SystemModel.FE", "FESubstructure")

if TYPE_CHECKING:
    from typing import Any, List, Optional, Tuple, Type, TypeVar, Union

    from mastapy._private import _7901
    from mastapy._private._internal.typing import PathLike
    from mastapy._private.materials import _324, _372
    from mastapy._private.math_utility import _1683
    from mastapy._private.math_utility.measured_vectors import _1748
    from mastapy._private.nodal_analysis import _63, _73, _91
    from mastapy._private.nodal_analysis.component_mode_synthesis import _312, _320
    from mastapy._private.nodal_analysis.fe_export_utility import _246
    from mastapy._private.nodal_analysis.geometry_modeller_link import _233, _235
    from mastapy._private.system_model import _2431
    from mastapy._private.system_model.fe import (
        _2577,
        _2579,
        _2583,
        _2603,
        _2606,
        _2607,
        _2613,
        _2614,
        _2615,
        _2616,
        _2617,
        _2618,
        _2621,
        _2634,
    )
    from mastapy._private.system_model.fe.links import _2643
    from mastapy._private.system_model.part_model import _2680
    from mastapy._private.system_model.part_model.shaft_model import _2714

    Self = TypeVar("Self", bound="FESubstructure")
    CastSelf = TypeVar("CastSelf", bound="FESubstructure._Cast_FESubstructure")


__docformat__ = "restructuredtext en"
__all__ = ("FESubstructure",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FESubstructure:
    """Special nested class for casting FESubstructure to subclasses."""

    __parent__: "FESubstructure"

    @property
    def fe_stiffness(self: "CastSelf") -> "_69.FEStiffness":
        return self.__parent__._cast(_69.FEStiffness)

    @property
    def fe_substructure(self: "CastSelf") -> "FESubstructure":
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
class FESubstructure(_69.FEStiffness):
    """FESubstructure

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_SUBSTRUCTURE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def actual_number_of_rigid_body_modes(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActualNumberOfRigidBodyModes")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def alignment_method(self: "Self") -> "_2577.AlignmentMethod":
        """mastapy.system_model.fe.AlignmentMethod"""
        temp = pythonnet_property_get(self.wrapped, "AlignmentMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.SystemModel.FE.AlignmentMethod"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.fe._2577", "AlignmentMethod"
        )(value)

    @alignment_method.setter
    @exception_bridge
    @enforce_parameter_types
    def alignment_method(self: "Self", value: "_2577.AlignmentMethod") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.SystemModel.FE.AlignmentMethod"
        )
        pythonnet_property_set(self.wrapped, "AlignmentMethod", value)

    @property
    @exception_bridge
    def angle_span(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AngleSpan")

        if temp is None:
            return 0.0

        return temp

    @angle_span.setter
    @exception_bridge
    @enforce_parameter_types
    def angle_span(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "AngleSpan", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def angular_alignment_tolerance(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "AngularAlignmentTolerance")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @angular_alignment_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def angular_alignment_tolerance(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "AngularAlignmentTolerance", value)

    @property
    @exception_bridge
    def apply_translation_and_rotation_for_planetary_duplicates(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "ApplyTranslationAndRotationForPlanetaryDuplicates"
        )

        if temp is None:
            return False

        return temp

    @apply_translation_and_rotation_for_planetary_duplicates.setter
    @exception_bridge
    @enforce_parameter_types
    def apply_translation_and_rotation_for_planetary_duplicates(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ApplyTranslationAndRotationForPlanetaryDuplicates",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def are_vectors_loaded(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AreVectorsLoaded")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def bearing_node_alignment(self: "Self") -> "_2583.BearingNodeAlignmentOption":
        """mastapy.system_model.fe.BearingNodeAlignmentOption"""
        temp = pythonnet_property_get(self.wrapped, "BearingNodeAlignment")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.SystemModel.FE.BearingNodeAlignmentOption"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.fe._2583", "BearingNodeAlignmentOption"
        )(value)

    @bearing_node_alignment.setter
    @exception_bridge
    @enforce_parameter_types
    def bearing_node_alignment(
        self: "Self", value: "_2583.BearingNodeAlignmentOption"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.SystemModel.FE.BearingNodeAlignmentOption"
        )
        pythonnet_property_set(self.wrapped, "BearingNodeAlignment", value)

    @property
    @exception_bridge
    def bearing_rings_in_fe(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "BearingRingsInFE")

        if temp is None:
            return False

        return temp

    @bearing_rings_in_fe.setter
    @exception_bridge
    @enforce_parameter_types
    def bearing_rings_in_fe(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "BearingRingsInFE",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def check_fe_has_internal_modes_before_nvh_analysis(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "CheckFEHasInternalModesBeforeNVHAnalysis"
        )

        if temp is None:
            return False

        return temp

    @check_fe_has_internal_modes_before_nvh_analysis.setter
    @exception_bridge
    @enforce_parameter_types
    def check_fe_has_internal_modes_before_nvh_analysis(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "CheckFEHasInternalModesBeforeNVHAnalysis",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def comment(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Comment")

        if temp is None:
            return ""

        return temp

    @comment.setter
    @exception_bridge
    @enforce_parameter_types
    def comment(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Comment", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def component_to_align_to(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_Component":
        """ListWithSelectedItem[mastapy.system_model.part_model.Component]"""
        temp = pythonnet_property_get(self.wrapped, "ComponentToAlignTo")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_Component",
        )(temp)

    @component_to_align_to.setter
    @exception_bridge
    @enforce_parameter_types
    def component_to_align_to(self: "Self", value: "_2670.Component") -> None:
        generic_type = (
            list_with_selected_item.ListWithSelectedItem_Component.implicit_type()
        )
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "ComponentToAlignTo", value)

    @property
    @exception_bridge
    def condensation_node_size(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CondensationNodeSize")

        if temp is None:
            return 0.0

        return temp

    @condensation_node_size.setter
    @exception_bridge
    @enforce_parameter_types
    def condensation_node_size(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CondensationNodeSize",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def datum(self: "Self") -> "list_with_selected_item.ListWithSelectedItem_Datum":
        """ListWithSelectedItem[mastapy.system_model.part_model.Datum]"""
        temp = pythonnet_property_get(self.wrapped, "Datum")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_Datum",
        )(temp)

    @datum.setter
    @exception_bridge
    @enforce_parameter_types
    def datum(self: "Self", value: "_2674.Datum") -> None:
        generic_type = (
            list_with_selected_item.ListWithSelectedItem_Datum.implicit_type()
        )
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "Datum", value)

    @property
    @exception_bridge
    def default_fe_surface_group(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "DefaultFESurfaceGroup")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @default_fe_surface_group.setter
    @exception_bridge
    @enforce_parameter_types
    def default_fe_surface_group(self: "Self", value: "str") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "DefaultFESurfaceGroup", value)

    @property
    @exception_bridge
    def distance_display_unit(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_Unit":
        """ListWithSelectedItem[mastapy.utility.units_and_measurements.Unit]"""
        temp = pythonnet_property_get(self.wrapped, "DistanceDisplayUnit")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_Unit",
        )(temp)

    @distance_display_unit.setter
    @exception_bridge
    @enforce_parameter_types
    def distance_display_unit(self: "Self", value: "_1802.Unit") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "DistanceDisplayUnit", value)

    @property
    @exception_bridge
    def expected_number_of_rigid_body_modes(
        self: "Self",
    ) -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "ExpectedNumberOfRigidBodyModes")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @expected_number_of_rigid_body_modes.setter
    @exception_bridge
    @enforce_parameter_types
    def expected_number_of_rigid_body_modes(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ExpectedNumberOfRigidBodyModes", value)

    @property
    @exception_bridge
    def external_fe_forces_are_from_gravity_only(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "ExternalFEForcesAreFromGravityOnly"
        )

        if temp is None:
            return False

        return temp

    @external_fe_forces_are_from_gravity_only.setter
    @exception_bridge
    @enforce_parameter_types
    def external_fe_forces_are_from_gravity_only(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ExternalFEForcesAreFromGravityOnly",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def force_display_unit(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_Unit":
        """ListWithSelectedItem[mastapy.utility.units_and_measurements.Unit]"""
        temp = pythonnet_property_get(self.wrapped, "ForceDisplayUnit")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_Unit",
        )(temp)

    @force_display_unit.setter
    @exception_bridge
    @enforce_parameter_types
    def force_display_unit(self: "Self", value: "_1802.Unit") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "ForceDisplayUnit", value)

    @property
    @exception_bridge
    def full_fe_model_mesh_path(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FullFEModelMeshPath")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def full_fe_model_mesh_size(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FullFEModelMeshSize")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def full_fe_model_vectors_path(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FullFEModelVectorsPath")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def full_fe_model_vectors_size(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FullFEModelVectorsSize")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def geometry_meshing_material(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "GeometryMeshingMaterial", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @geometry_meshing_material.setter
    @exception_bridge
    @enforce_parameter_types
    def geometry_meshing_material(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "GeometryMeshingMaterial",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def gravity_force_can_be_rotated(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GravityForceCanBeRotated")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def gravity_force_source(self: "Self") -> "_73.GravityForceSource":
        """mastapy.nodal_analysis.GravityForceSource

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GravityForceSource")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.NodalAnalysis.GravityForceSource"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.nodal_analysis._73", "GravityForceSource"
        )(value)

    @property
    @exception_bridge
    def gravity_magnitude_used_for_reduced_forces(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "GravityMagnitudeUsedForReducedForces"
        )

        if temp is None:
            return 0.0

        return temp

    @gravity_magnitude_used_for_reduced_forces.setter
    @exception_bridge
    @enforce_parameter_types
    def gravity_magnitude_used_for_reduced_forces(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "GravityMagnitudeUsedForReducedForces",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def housing_is_grounded(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "HousingIsGrounded")

        if temp is None:
            return False

        return temp

    @housing_is_grounded.setter
    @exception_bridge
    @enforce_parameter_types
    def housing_is_grounded(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "HousingIsGrounded",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def is_housing(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsHousing")

        if temp is None:
            return False

        return temp

    @is_housing.setter
    @exception_bridge
    @enforce_parameter_types
    def is_housing(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "IsHousing", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def is_mesh_loaded(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsMeshLoaded")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def material(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "Material", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @material.setter
    @exception_bridge
    @enforce_parameter_types
    def material(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "Material",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def non_condensation_node_size(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NonCondensationNodeSize")

        if temp is None:
            return 0

        return temp

    @non_condensation_node_size.setter
    @exception_bridge
    @enforce_parameter_types
    def non_condensation_node_size(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NonCondensationNodeSize",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def number_of_angles(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfAngles")

        if temp is None:
            return 0

        return temp

    @number_of_angles.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_angles(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfAngles", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def number_of_condensation_nodes(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfCondensationNodes")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_condensation_nodes_in_reduced_model(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfCondensationNodesInReducedModel"
        )

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def polar_inertia(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PolarInertia")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def reduced_stiffness_file(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReducedStiffnessFile")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def reduced_stiffness_file_editable(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "ReducedStiffnessFileEditable")

        if temp is None:
            return ""

        return temp

    @reduced_stiffness_file_editable.setter
    @exception_bridge
    @enforce_parameter_types
    def reduced_stiffness_file_editable(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ReducedStiffnessFileEditable",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def reduction_mode_type(self: "Self") -> "_320.ReductionModeType":
        """mastapy.nodal_analysis.component_mode_synthesis.ReductionModeType"""
        temp = pythonnet_property_get(self.wrapped, "ReductionModeType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.NodalAnalysis.ComponentModeSynthesis.ReductionModeType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.nodal_analysis.component_mode_synthesis._320",
            "ReductionModeType",
        )(value)

    @reduction_mode_type.setter
    @exception_bridge
    @enforce_parameter_types
    def reduction_mode_type(self: "Self", value: "_320.ReductionModeType") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.NodalAnalysis.ComponentModeSynthesis.ReductionModeType"
        )
        pythonnet_property_set(self.wrapped, "ReductionModeType", value)

    @property
    @exception_bridge
    def thermal_expansion_option(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ThermalExpansionOption":
        """EnumWithSelectedValue[mastapy.system_model.fe.ThermalExpansionOption]"""
        temp = pythonnet_property_get(self.wrapped, "ThermalExpansionOption")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ThermalExpansionOption.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @thermal_expansion_option.setter
    @exception_bridge
    @enforce_parameter_types
    def thermal_expansion_option(
        self: "Self", value: "_2636.ThermalExpansionOption"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ThermalExpansionOption.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ThermalExpansionOption", value)

    @property
    @exception_bridge
    def torque_transmission_relative_tolerance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "TorqueTransmissionRelativeTolerance"
        )

        if temp is None:
            return 0.0

        return temp

    @torque_transmission_relative_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def torque_transmission_relative_tolerance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TorqueTransmissionRelativeTolerance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def type_(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_FESubstructureType":
        """EnumWithSelectedValue[mastapy.system_model.fe.FESubstructureType]"""
        temp = pythonnet_property_get(self.wrapped, "Type")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_FESubstructureType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @type_.setter
    @exception_bridge
    @enforce_parameter_types
    def type_(self: "Self", value: "_2610.FESubstructureType") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_FESubstructureType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "Type", value)

    @property
    @exception_bridge
    def acoustic_radiation_efficiency(
        self: "Self",
    ) -> "_324.AcousticRadiationEfficiency":
        """mastapy.materials.AcousticRadiationEfficiency

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AcousticRadiationEfficiency")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def alignment_using_axial_node_positions(
        self: "Self",
    ) -> "_2579.AlignmentUsingAxialNodePositions":
        """mastapy.system_model.fe.AlignmentUsingAxialNodePositions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AlignmentUsingAxialNodePositions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def alignment_to_component(
        self: "Self",
    ) -> "_2431.RelativeComponentAlignment[_2670.Component]":
        """mastapy.system_model.RelativeComponentAlignment[mastapy.system_model.part_model.Component]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AlignmentToComponent")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_2670.Component](temp)

    @property
    @exception_bridge
    def cms_model(self: "Self") -> "_312.CMSModel":
        """mastapy.nodal_analysis.component_mode_synthesis.CMSModel

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CMSModel")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def coordinate_system(self: "Self") -> "_1683.CoordinateSystem3D":
        """mastapy.math_utility.CoordinateSystem3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CoordinateSystem")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def export(self: "Self") -> "_2606.FESubstructureExportOptions":
        """mastapy.system_model.fe.FESubstructureExportOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Export")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def fe_meshing_options(self: "Self") -> "_91.ShaftFEMeshingOptions":
        """mastapy.nodal_analysis.ShaftFEMeshingOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FEMeshingOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def fe_part(self: "Self") -> "_2680.FEPart":
        """mastapy.system_model.part_model.FEPart

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FEPart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def geometry_modeller_design_information(
        self: "Self",
    ) -> "_233.GeometryModellerDesignInformation":
        """mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDesignInformation

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GeometryModellerDesignInformation")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def geometry_modeller_dimensions(self: "Self") -> "_235.GeometryModellerDimensions":
        """mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDimensions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GeometryModellerDimensions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def sound_pressure_enclosure(self: "Self") -> "_372.SoundPressureEnclosure":
        """mastapy.materials.SoundPressureEnclosure

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SoundPressureEnclosure")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear_meshing_options(self: "Self") -> "List[_2617.GearMeshingOptions]":
        """List[mastapy.system_model.fe.GearMeshingOptions]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearMeshingOptions")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def geometries(self: "Self") -> "List[_2603.FEStiffnessGeometry]":
        """List[mastapy.system_model.fe.FEStiffnessGeometry]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Geometries")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def independent_masta_created_condensation_nodes(
        self: "Self",
    ) -> "List[_2618.IndependentMASTACreatedCondensationNode]":
        """List[mastapy.system_model.fe.IndependentMASTACreatedCondensationNode]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "IndependentMastaCreatedCondensationNodes"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def independent_masta_created_rigid_nodes(
        self: "Self",
    ) -> "List[_2621.IndependentMASTACreatedRigidlyConnectedNodeGroup]":
        """List[mastapy.system_model.fe.IndependentMASTACreatedRigidlyConnectedNodeGroup]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IndependentMastaCreatedRigidNodes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def links(self: "Self") -> "List[_2643.FELink]":
        """List[mastapy.system_model.fe.links.FELink]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Links")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def nodes(self: "Self") -> "List[_2607.FESubstructureNode]":
        """List[mastapy.system_model.fe.FESubstructureNode]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Nodes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def replaced_shafts(self: "Self") -> "List[_2714.Shaft]":
        """List[mastapy.system_model.part_model.shaft_model.Shaft]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReplacedShafts")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def shafts_that_can_be_replaced(
        self: "Self",
    ) -> "List[_2634.ReplacedShaftSelectionHelper]":
        """List[mastapy.system_model.fe.ReplacedShaftSelectionHelper]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftsThatCanBeReplaced")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def thermal_expansion_displacements(
        self: "Self",
    ) -> "List[_1748.VectorWithLinearAndAngularComponents]":
        """List[mastapy.math_utility.measured_vectors.VectorWithLinearAndAngularComponents]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThermalExpansionDisplacements")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def thermal_expansion_forces(
        self: "Self",
    ) -> "List[_1748.VectorWithLinearAndAngularComponents]":
        """List[mastapy.math_utility.measured_vectors.VectorWithLinearAndAngularComponents]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThermalExpansionForces")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

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

    @exception_bridge
    def add_geometry(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddGeometry")

    @exception_bridge
    def auto_connect_external_nodes(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AutoConnectExternalNodes")

    @exception_bridge
    def calculate_maximum_gear_tip_diameters(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CalculateMaximumGearTipDiameters")

    @exception_bridge
    def copy_datum_to_manual(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CopyDatumToManual")

    @exception_bridge
    def create_datum_from_manual_alignment(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CreateDatumFromManualAlignment")

    @exception_bridge
    def create_fe_volume_mesh(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CreateFEVolumeMesh")

    @exception_bridge
    def default_node_creation_options(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "DefaultNodeCreationOptions")

    @exception_bridge
    def delete_all_links(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "DeleteAllLinks")

    @exception_bridge
    def embed_fe_model_mesh_in_masta_file(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "EmbedFEModelMeshInMASTAFile")

    @exception_bridge
    def embed_fe_model_vectors_in_masta_file(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "EmbedFEModelVectorsInMASTAFile")

    @exception_bridge
    def perform_reduction(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "PerformReduction")

    @exception_bridge
    def re_import_external_fe_mesh(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ReImportExternalFEMesh")

    @exception_bridge
    def remove_full_fe_mesh(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "RemoveFullFEMesh")

    @exception_bridge
    def reread_mesh_from_geometry_modeller(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "RereadMeshFromGeometryModeller")

    @exception_bridge
    def unload_external_mesh_file(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "UnloadExternalMeshFile")

    @exception_bridge
    def unload_external_vectors_file(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "UnloadExternalVectorsFile")

    @exception_bridge
    def update_gear_teeth_mesh(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "UpdateGearTeethMesh")

    @exception_bridge
    @enforce_parameter_types
    def convert_shafts_to_fe(
        self: "Self", operation: "_63.FEMeshingOperation", export_file_name: "str"
    ) -> None:
        """Method does not return.

        Args:
            operation (mastapy.nodal_analysis.FEMeshingOperation)
            export_file_name (str)
        """
        operation = conversion.mp_to_pn_enum(
            operation, "SMT.MastaAPI.NodalAnalysis.FEMeshingOperation"
        )
        export_file_name = str(export_file_name)
        pythonnet_method_call(
            self.wrapped,
            "ConvertShaftsToFE",
            operation,
            export_file_name if export_file_name else "",
        )

    @exception_bridge
    def create_fe_substructure_with_selection_components(
        self: "Self",
    ) -> "_2613.FESubstructureWithSelectionComponents":
        """mastapy.system_model.fe.FESubstructureWithSelectionComponents"""
        method_result = pythonnet_method_call(
            self.wrapped, "CreateFESubstructureWithSelectionComponents"
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def create_fe_substructure_with_selection_for_harmonic_analysis(
        self: "Self",
    ) -> "_2614.FESubstructureWithSelectionForHarmonicAnalysis":
        """mastapy.system_model.fe.FESubstructureWithSelectionForHarmonicAnalysis"""
        method_result = pythonnet_method_call(
            self.wrapped, "CreateFESubstructureWithSelectionForHarmonicAnalysis"
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def create_fe_substructure_with_selection_for_modal_analysis(
        self: "Self",
    ) -> "_2615.FESubstructureWithSelectionForModalAnalysis":
        """mastapy.system_model.fe.FESubstructureWithSelectionForModalAnalysis"""
        method_result = pythonnet_method_call(
            self.wrapped, "CreateFESubstructureWithSelectionForModalAnalysis"
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def create_fe_substructure_with_selection_for_static_analysis(
        self: "Self",
    ) -> "_2616.FESubstructureWithSelectionForStaticAnalysis":
        """mastapy.system_model.fe.FESubstructureWithSelectionForStaticAnalysis"""
        method_result = pythonnet_method_call(
            self.wrapped, "CreateFESubstructureWithSelectionForStaticAnalysis"
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def duplicate(self: "Self", name: "str") -> "FESubstructure":
        """mastapy.system_model.fe.FESubstructure

        Args:
            name (str)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "Duplicate", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def import_fe_mesh(
        self: "Self",
        file_path: "PathLike",
        format_: "_246.FEExportFormat",
        length_scale: "float" = 1.0,
        force_scale: "float" = 1.0,
        progress: Optional["_7901.TaskProgress"] = None,
    ) -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
            format_ (mastapy.nodal_analysis.fe_export_utility.FEExportFormat)
            length_scale (float, optional)
            force_scale (float, optional)
            progress (mastapy.TaskProgress, optional)
        """
        file_path = str(file_path)
        format_ = conversion.mp_to_pn_enum(
            format_, "SMT.MastaAPI.NodalAnalysis.FeExportUtility.FEExportFormat"
        )
        length_scale = float(length_scale)
        force_scale = float(force_scale)
        pythonnet_method_call(
            self.wrapped,
            "ImportFEMesh",
            file_path,
            format_,
            length_scale if length_scale else 0.0,
            force_scale if force_scale else 0.0,
            progress.wrapped if progress else None,
        )

    @exception_bridge
    @enforce_parameter_types
    def import_node_positions(
        self: "Self", file_name: "PathLike", distance_unit: "_1802.Unit"
    ) -> None:
        """Method does not return.

        Args:
            file_name (PathLike)
            distance_unit (mastapy.utility.units_and_measurements.Unit)
        """
        file_name = str(file_name)
        pythonnet_method_call(
            self.wrapped,
            "ImportNodePositions",
            file_name,
            distance_unit.wrapped if distance_unit else None,
        )

    @exception_bridge
    @enforce_parameter_types
    def import_reduced_stiffness(
        self: "Self",
        file_name: "PathLike",
        distance_unit: "_1802.Unit",
        force_unit: "_1802.Unit",
    ) -> None:
        """Method does not return.

        Args:
            file_name (PathLike)
            distance_unit (mastapy.utility.units_and_measurements.Unit)
            force_unit (mastapy.utility.units_and_measurements.Unit)
        """
        file_name = str(file_name)
        pythonnet_method_call(
            self.wrapped,
            "ImportReducedStiffness",
            file_name,
            distance_unit.wrapped if distance_unit else None,
            force_unit.wrapped if force_unit else None,
        )

    @exception_bridge
    @enforce_parameter_types
    def links_for(
        self: "Self", node: "_2607.FESubstructureNode"
    ) -> "List[_2643.FELink]":
        """List[mastapy.system_model.fe.links.FELink]

        Args:
            node (mastapy.system_model.fe.FESubstructureNode)
        """
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call(
                self.wrapped, "LinksFor", node.wrapped if node else None
            )
        )

    @exception_bridge
    @enforce_parameter_types
    def load_existing_masta_fe_file(self: "Self", file_name: "PathLike") -> None:
        """Method does not return.

        Args:
            file_name (PathLike)
        """
        file_name = str(file_name)
        pythonnet_method_call_overload(
            self.wrapped, "LoadExistingMastaFEFile", [str], file_name
        )

    @exception_bridge
    @enforce_parameter_types
    def load_existing_masta_fe_file_with_progress(
        self: "Self", file_name: "PathLike", progress: "_7901.TaskProgress"
    ) -> None:
        """Method does not return.

        Args:
            file_name (PathLike)
            progress (mastapy.TaskProgress)
        """
        file_name = str(file_name)
        pythonnet_method_call_overload(
            self.wrapped,
            "LoadExistingMastaFEFile",
            [str, _TASK_PROGRESS],
            file_name,
            progress.wrapped if progress else None,
        )

    @exception_bridge
    @enforce_parameter_types
    def load_external_mesh(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "LoadExternalMesh", file_path)

    @exception_bridge
    @enforce_parameter_types
    def load_external_vectors(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "LoadExternalVectors", file_path)

    @exception_bridge
    @enforce_parameter_types
    def load_stl_geometry(
        self: "Self", length_unit: "_1802.Unit", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            length_unit (mastapy.utility.units_and_measurements.Unit)
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "LoadStlGeometry",
            length_unit.wrapped if length_unit else None,
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def store_full_fe_mesh_in_external_file(
        self: "Self", external_fe_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            external_fe_path (str)
        """
        external_fe_path = str(external_fe_path)
        pythonnet_method_call(
            self.wrapped,
            "StoreFullFeMeshInExternalFile",
            external_fe_path if external_fe_path else "",
        )

    @exception_bridge
    @enforce_parameter_types
    def store_full_fe_model_vectors_in_external_file(
        self: "Self", external_fe_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            external_fe_path (str)
        """
        external_fe_path = str(external_fe_path)
        pythonnet_method_call(
            self.wrapped,
            "StoreFullFeModelVectorsInExternalFile",
            external_fe_path if external_fe_path else "",
        )

    @property
    def cast_to(self: "Self") -> "_Cast_FESubstructure":
        """Cast to another type.

        Returns:
            _Cast_FESubstructure
        """
        return _Cast_FESubstructure(self)
