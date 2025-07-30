"""Design"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.class_property import classproperty
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
    pythonnet_method_call_generic,
    pythonnet_method_call_overload,
    pythonnet_property_get,
    pythonnet_property_get_with_method,
    pythonnet_property_set,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private._math.vector_3d import Vector3D
from mastapy._private.gears import _422
from mastapy._private.materials.efficiency import _382
from mastapy._private.system_model.part_model import _2703, _2707
from mastapy._private.system_model.part_model.gears import _2749
from mastapy._private.utility import _1774

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_ARRAY = python_net_import("System", "Array")
_STRING = python_net_import("System", "String")
_BOOLEAN = python_net_import("System", "Boolean")
_TASK_PROGRESS = python_net_import("SMT.MastaAPIUtility", "TaskProgress")
_DESIGN = python_net_import("SMT.MastaAPI.SystemModel", "Design")

if TYPE_CHECKING:
    from typing import Any, List, Optional, Tuple, Type, TypeVar, Union

    from mastapy._private import _7901
    from mastapy._private._internal.example_name import ExampleName
    from mastapy._private._internal.typing import PathLike
    from mastapy._private.bearings.bearing_designs.rolling import _2375
    from mastapy._private.bearings.bearing_results.rolling import _2183
    from mastapy._private.detailed_rigid_connectors.splines import _1576
    from mastapy._private.gears import _411, _417
    from mastapy._private.gears.gear_designs.creation_options import _1265, _1268, _1269
    from mastapy._private.gears.materials import _698
    from mastapy._private.nodal_analysis import _82
    from mastapy._private.shafts import _38
    from mastapy._private.system_model import _2416, _2422, _2423, _2433, _2434, _2435
    from mastapy._private.system_model.analyses_and_results.load_case_groups import (
        _5953,
        _5954,
        _5961,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7673,
        _7674,
    )
    from mastapy._private.system_model.analyses_and_results.synchroniser_analysis import (
        _3227,
    )
    from mastapy._private.system_model.database_access import _2485
    from mastapy._private.system_model.fe import _2582
    from mastapy._private.system_model.optimization.system_optimiser import _2451, _2452
    from mastapy._private.system_model.part_model import (
        _2658,
        _2659,
        _2660,
        _2661,
        _2664,
        _2667,
        _2668,
        _2670,
        _2673,
        _2674,
        _2679,
        _2680,
        _2681,
        _2682,
        _2689,
        _2690,
        _2691,
        _2692,
        _2693,
        _2695,
        _2698,
        _2700,
        _2702,
        _2706,
        _2708,
        _2709,
        _2710,
        _2711,
    )
    from mastapy._private.system_model.part_model.acoustics import _2869
    from mastapy._private.system_model.part_model.configurations import (
        _2858,
        _2860,
        _2861,
        _2863,
    )
    from mastapy._private.system_model.part_model.couplings import (
        _2815,
        _2817,
        _2818,
        _2820,
        _2821,
        _2823,
        _2824,
        _2826,
        _2827,
        _2828,
        _2829,
        _2831,
        _2838,
        _2839,
        _2840,
        _2846,
        _2847,
        _2848,
        _2850,
        _2851,
        _2852,
        _2853,
        _2854,
        _2856,
    )
    from mastapy._private.system_model.part_model.creation_options import (
        _2809,
        _2810,
        _2811,
        _2813,
        _2814,
    )
    from mastapy._private.system_model.part_model.cycloidal import _2806, _2807, _2808
    from mastapy._private.system_model.part_model.gears import (
        _2750,
        _2751,
        _2752,
        _2753,
        _2754,
        _2755,
        _2756,
        _2757,
        _2758,
        _2759,
        _2760,
        _2761,
        _2762,
        _2763,
        _2764,
        _2765,
        _2766,
        _2767,
        _2769,
        _2770,
        _2771,
        _2772,
        _2773,
        _2774,
        _2775,
        _2776,
        _2777,
        _2778,
        _2779,
        _2781,
        _2782,
        _2783,
        _2784,
        _2785,
        _2786,
        _2787,
        _2788,
        _2789,
        _2790,
        _2791,
        _2792,
    )
    from mastapy._private.system_model.part_model.shaft_model import _2714
    from mastapy._private.system_model_gui import _2049
    from mastapy._private.utility import _1775, _1776, _1791
    from mastapy._private.utility.model_validation import _1988

    T_all_parts = TypeVar("T_all_parts", bound="_2698.Part")
    Self = TypeVar("Self", bound="Design")
    CastSelf = TypeVar("CastSelf", bound="Design._Cast_Design")


__docformat__ = "restructuredtext en"
__all__ = ("Design",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Design:
    """Special nested class for casting Design to subclasses."""

    __parent__: "Design"

    @property
    def design(self: "CastSelf") -> "Design":
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
class Design(_0.APIBase):
    """Design

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DESIGN

    wrapped: "Any" = None

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if self.wrapped is None:
            object.__setattr__(self, "wrapped", Design.TYPE())

        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @classproperty
    @exception_bridge
    def available_examples(cls) -> "List[str]":
        """List[str]"""
        temp = pythonnet_property_get(Design.TYPE, "AvailableExamples")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def masta_gui(self: "Self") -> "_2049.MASTAGUI":
        """mastapy.system_model_gui.MASTAGUI

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MastaGUI")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def axial_contact_ratio_requirement(
        self: "Self",
    ) -> "_411.ContactRatioRequirements":
        """mastapy.gears.ContactRatioRequirements"""
        temp = pythonnet_property_get(self.wrapped, "AxialContactRatioRequirement")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.ContactRatioRequirements"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears._411", "ContactRatioRequirements"
        )(value)

    @axial_contact_ratio_requirement.setter
    @exception_bridge
    @enforce_parameter_types
    def axial_contact_ratio_requirement(
        self: "Self", value: "_411.ContactRatioRequirements"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.ContactRatioRequirements"
        )
        pythonnet_property_set(self.wrapped, "AxialContactRatioRequirement", value)

    @property
    @exception_bridge
    def bearing_configuration(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "BearingConfiguration")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @bearing_configuration.setter
    @exception_bridge
    @enforce_parameter_types
    def bearing_configuration(self: "Self", value: "str") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "BearingConfiguration", value)

    @property
    @exception_bridge
    def coefficient_of_friction(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CoefficientOfFriction")

        if temp is None:
            return 0.0

        return temp

    @coefficient_of_friction.setter
    @exception_bridge
    @enforce_parameter_types
    def coefficient_of_friction(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CoefficientOfFriction",
            float(value) if value is not None else 0.0,
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
    def default_save_location_path(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DefaultSaveLocationPath")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def design_configuration(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "DesignConfiguration")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @design_configuration.setter
    @exception_bridge
    @enforce_parameter_types
    def design_configuration(self: "Self", value: "str") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "DesignConfiguration", value)

    @property
    @exception_bridge
    def design_name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "DesignName")

        if temp is None:
            return ""

        return temp

    @design_name.setter
    @exception_bridge
    @enforce_parameter_types
    def design_name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "DesignName", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def efficiency_rating_method_for_bearings(
        self: "Self",
    ) -> "_382.BearingEfficiencyRatingMethod":
        """mastapy.materials.efficiency.BearingEfficiencyRatingMethod"""
        temp = pythonnet_property_get(self.wrapped, "EfficiencyRatingMethodForBearings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Materials.Efficiency.BearingEfficiencyRatingMethod"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials.efficiency._382",
            "BearingEfficiencyRatingMethod",
        )(value)

    @efficiency_rating_method_for_bearings.setter
    @exception_bridge
    @enforce_parameter_types
    def efficiency_rating_method_for_bearings(
        self: "Self", value: "_382.BearingEfficiencyRatingMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Materials.Efficiency.BearingEfficiencyRatingMethod"
        )
        pythonnet_property_set(self.wrapped, "EfficiencyRatingMethodForBearings", value)

    @property
    @exception_bridge
    def efficiency_rating_method_if_skf_loss_model_does_not_provide_losses(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_BearingEfficiencyRatingMethod":
        """EnumWithSelectedValue[mastapy.materials.efficiency.BearingEfficiencyRatingMethod]"""
        temp = pythonnet_property_get(
            self.wrapped, "EfficiencyRatingMethodIfSKFLossModelDoesNotProvideLosses"
        )

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_BearingEfficiencyRatingMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @efficiency_rating_method_if_skf_loss_model_does_not_provide_losses.setter
    @exception_bridge
    @enforce_parameter_types
    def efficiency_rating_method_if_skf_loss_model_does_not_provide_losses(
        self: "Self", value: "_382.BearingEfficiencyRatingMethod"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_BearingEfficiencyRatingMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(
            self.wrapped,
            "EfficiencyRatingMethodIfSKFLossModelDoesNotProvideLosses",
            value,
        )

    @property
    @exception_bridge
    def fe_substructure_configuration(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "FESubstructureConfiguration")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @fe_substructure_configuration.setter
    @exception_bridge
    @enforce_parameter_types
    def fe_substructure_configuration(self: "Self", value: "str") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "FESubstructureConfiguration", value)

    @property
    @exception_bridge
    def file_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FileName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def gear_set_configuration(
        self: "Self",
    ) -> (
        "list_with_selected_item.ListWithSelectedItem_ActiveGearSetDesignSelectionGroup"
    ):
        """ListWithSelectedItem[mastapy.system_model.part_model.gears.ActiveGearSetDesignSelectionGroup]"""
        temp = pythonnet_property_get(self.wrapped, "GearSetConfiguration")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_ActiveGearSetDesignSelectionGroup",
        )(temp)

    @gear_set_configuration.setter
    @exception_bridge
    @enforce_parameter_types
    def gear_set_configuration(
        self: "Self", value: "_2749.ActiveGearSetDesignSelectionGroup"
    ) -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_ActiveGearSetDesignSelectionGroup.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "GearSetConfiguration", value)

    @property
    @exception_bridge
    def gravity_magnitude(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "GravityMagnitude")

        if temp is None:
            return 0.0

        return temp

    @gravity_magnitude.setter
    @exception_bridge
    @enforce_parameter_types
    def gravity_magnitude(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "GravityMagnitude", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def housing_material_for_grounded_connections(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "HousingMaterialForGroundedConnections", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @housing_material_for_grounded_connections.setter
    @exception_bridge
    @enforce_parameter_types
    def housing_material_for_grounded_connections(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "HousingMaterialForGroundedConnections",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def iso14179_part_1_coefficient_of_friction_constants_and_exponents_for_external_external_meshes_database(
        self: "Self",
    ) -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped,
            "ISO14179Part1CoefficientOfFrictionConstantsAndExponentsForExternalExternalMeshesDatabase",
            "SelectedItemName",
        )

        if temp is None:
            return ""

        return temp

    @iso14179_part_1_coefficient_of_friction_constants_and_exponents_for_external_external_meshes_database.setter
    @exception_bridge
    @enforce_parameter_types
    def iso14179_part_1_coefficient_of_friction_constants_and_exponents_for_external_external_meshes_database(
        self: "Self", value: "str"
    ) -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "ISO14179Part1CoefficientOfFrictionConstantsAndExponentsForExternalExternalMeshesDatabase",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def iso14179_part_1_coefficient_of_friction_constants_and_exponents_for_internal_external_meshes_database(
        self: "Self",
    ) -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped,
            "ISO14179Part1CoefficientOfFrictionConstantsAndExponentsForInternalExternalMeshesDatabase",
            "SelectedItemName",
        )

        if temp is None:
            return ""

        return temp

    @iso14179_part_1_coefficient_of_friction_constants_and_exponents_for_internal_external_meshes_database.setter
    @exception_bridge
    @enforce_parameter_types
    def iso14179_part_1_coefficient_of_friction_constants_and_exponents_for_internal_external_meshes_database(
        self: "Self", value: "str"
    ) -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "ISO14179Part1CoefficientOfFrictionConstantsAndExponentsForInternalExternalMeshesDatabase",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def input_power_load(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_PowerLoad":
        """ListWithSelectedItem[mastapy.system_model.part_model.PowerLoad]"""
        temp = pythonnet_property_get(self.wrapped, "InputPowerLoad")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_PowerLoad",
        )(temp)

    @input_power_load.setter
    @exception_bridge
    @enforce_parameter_types
    def input_power_load(self: "Self", value: "_2703.PowerLoad") -> None:
        generic_type = (
            list_with_selected_item.ListWithSelectedItem_PowerLoad.implicit_type()
        )
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "InputPowerLoad", value)

    @property
    @exception_bridge
    def manufacturer(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Manufacturer")

        if temp is None:
            return ""

        return temp

    @manufacturer.setter
    @exception_bridge
    @enforce_parameter_types
    def manufacturer(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Manufacturer", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def maximum_acceptable_axial_contact_ratio(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumAcceptableAxialContactRatio"
        )

        if temp is None:
            return 0.0

        return temp

    @maximum_acceptable_axial_contact_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_acceptable_axial_contact_ratio(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumAcceptableAxialContactRatio",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def maximum_acceptable_transverse_contact_ratio(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumAcceptableTransverseContactRatio"
        )

        if temp is None:
            return 0.0

        return temp

    @maximum_acceptable_transverse_contact_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_acceptable_transverse_contact_ratio(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumAcceptableTransverseContactRatio",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def maximum_number_of_teeth(self: "Self") -> "Optional[int]":
        """Optional[int]"""
        temp = pythonnet_property_get(self.wrapped, "MaximumNumberOfTeeth")

        if temp is None:
            return None

        return temp

    @maximum_number_of_teeth.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_number_of_teeth(self: "Self", value: "Optional[int]") -> None:
        pythonnet_property_set(self.wrapped, "MaximumNumberOfTeeth", value)

    @property
    @exception_bridge
    def maximum_number_of_teeth_external_gears(self: "Self") -> "Optional[int]":
        """Optional[int]"""
        temp = pythonnet_property_get(self.wrapped, "MaximumNumberOfTeethExternalGears")

        if temp is None:
            return None

        return temp

    @maximum_number_of_teeth_external_gears.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_number_of_teeth_external_gears(
        self: "Self", value: "Optional[int]"
    ) -> None:
        pythonnet_property_set(self.wrapped, "MaximumNumberOfTeethExternalGears", value)

    @property
    @exception_bridge
    def maximum_number_of_teeth_internal_gears(self: "Self") -> "Optional[int]":
        """Optional[int]"""
        temp = pythonnet_property_get(self.wrapped, "MaximumNumberOfTeethInternalGears")

        if temp is None:
            return None

        return temp

    @maximum_number_of_teeth_internal_gears.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_number_of_teeth_internal_gears(
        self: "Self", value: "Optional[int]"
    ) -> None:
        pythonnet_property_set(self.wrapped, "MaximumNumberOfTeethInternalGears", value)

    @property
    @exception_bridge
    def minimum_acceptable_axial_contact_ratio(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MinimumAcceptableAxialContactRatio"
        )

        if temp is None:
            return 0.0

        return temp

    @minimum_acceptable_axial_contact_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_acceptable_axial_contact_ratio(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumAcceptableAxialContactRatio",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def minimum_acceptable_transverse_contact_ratio(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MinimumAcceptableTransverseContactRatio"
        )

        if temp is None:
            return 0.0

        return temp

    @minimum_acceptable_transverse_contact_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_acceptable_transverse_contact_ratio(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumAcceptableTransverseContactRatio",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def minimum_number_of_teeth(self: "Self") -> "Optional[int]":
        """Optional[int]"""
        temp = pythonnet_property_get(self.wrapped, "MinimumNumberOfTeeth")

        if temp is None:
            return None

        return temp

    @minimum_number_of_teeth.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_number_of_teeth(self: "Self", value: "Optional[int]") -> None:
        pythonnet_property_set(self.wrapped, "MinimumNumberOfTeeth", value)

    @property
    @exception_bridge
    def minimum_number_of_teeth_external_gears(self: "Self") -> "Optional[int]":
        """Optional[int]"""
        temp = pythonnet_property_get(self.wrapped, "MinimumNumberOfTeethExternalGears")

        if temp is None:
            return None

        return temp

    @minimum_number_of_teeth_external_gears.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_number_of_teeth_external_gears(
        self: "Self", value: "Optional[int]"
    ) -> None:
        pythonnet_property_set(self.wrapped, "MinimumNumberOfTeethExternalGears", value)

    @property
    @exception_bridge
    def minimum_number_of_teeth_internal_gears(self: "Self") -> "Optional[int]":
        """Optional[int]"""
        temp = pythonnet_property_get(self.wrapped, "MinimumNumberOfTeethInternalGears")

        if temp is None:
            return None

        return temp

    @minimum_number_of_teeth_internal_gears.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_number_of_teeth_internal_gears(
        self: "Self", value: "Optional[int]"
    ) -> None:
        pythonnet_property_set(self.wrapped, "MinimumNumberOfTeethInternalGears", value)

    @property
    @exception_bridge
    def node_size(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "NodeSize")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @node_size.setter
    @exception_bridge
    @enforce_parameter_types
    def node_size(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "NodeSize", value)

    @property
    @exception_bridge
    def number_of_gear_set_configurations(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfGearSetConfigurations")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def output_power_load(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_PowerLoad":
        """ListWithSelectedItem[mastapy.system_model.part_model.PowerLoad]"""
        temp = pythonnet_property_get(self.wrapped, "OutputPowerLoad")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_PowerLoad",
        )(temp)

    @output_power_load.setter
    @exception_bridge
    @enforce_parameter_types
    def output_power_load(self: "Self", value: "_2703.PowerLoad") -> None:
        generic_type = (
            list_with_selected_item.ListWithSelectedItem_PowerLoad.implicit_type()
        )
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "OutputPowerLoad", value)

    @property
    @exception_bridge
    def required_clearance_between_gear_tip_and_housing(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "RequiredClearanceBetweenGearTipAndHousing"
        )

        if temp is None:
            return 0.0

        return temp

    @required_clearance_between_gear_tip_and_housing.setter
    @exception_bridge
    @enforce_parameter_types
    def required_clearance_between_gear_tip_and_housing(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "RequiredClearanceBetweenGearTipAndHousing",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def save_external_fe_files_in_the_default_subfolder(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "SaveExternalFEFilesInTheDefaultSubfolder"
        )

        if temp is None:
            return False

        return temp

    @save_external_fe_files_in_the_default_subfolder.setter
    @exception_bridge
    @enforce_parameter_types
    def save_external_fe_files_in_the_default_subfolder(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "SaveExternalFEFilesInTheDefaultSubfolder",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def shaft_detail_configuration(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "ShaftDetailConfiguration")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @shaft_detail_configuration.setter
    @exception_bridge
    @enforce_parameter_types
    def shaft_detail_configuration(self: "Self", value: "str") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "ShaftDetailConfiguration", value)

    @property
    @exception_bridge
    def shaft_diameter_modification_due_to_rolling_bearing_rings(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ShaftDiameterModificationDueToRollingBearingRing":
        """EnumWithSelectedValue[mastapy.system_model.part_model.ShaftDiameterModificationDueToRollingBearingRing]"""
        temp = pythonnet_property_get(
            self.wrapped, "ShaftDiameterModificationDueToRollingBearingRings"
        )

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ShaftDiameterModificationDueToRollingBearingRing.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @shaft_diameter_modification_due_to_rolling_bearing_rings.setter
    @exception_bridge
    @enforce_parameter_types
    def shaft_diameter_modification_due_to_rolling_bearing_rings(
        self: "Self", value: "_2707.ShaftDiameterModificationDueToRollingBearingRing"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ShaftDiameterModificationDueToRollingBearingRing.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(
            self.wrapped, "ShaftDiameterModificationDueToRollingBearingRings", value
        )

    @property
    @exception_bridge
    def shaft_gear_windage_and_churning_loss_calculation_method(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_GearWindageAndChurningLossCalculationMethod":
        """EnumWithSelectedValue[mastapy.gears.GearWindageAndChurningLossCalculationMethod]"""
        temp = pythonnet_property_get(
            self.wrapped, "ShaftGearWindageAndChurningLossCalculationMethod"
        )

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_GearWindageAndChurningLossCalculationMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @shaft_gear_windage_and_churning_loss_calculation_method.setter
    @exception_bridge
    @enforce_parameter_types
    def shaft_gear_windage_and_churning_loss_calculation_method(
        self: "Self", value: "_422.GearWindageAndChurningLossCalculationMethod"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_GearWindageAndChurningLossCalculationMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(
            self.wrapped, "ShaftGearWindageAndChurningLossCalculationMethod", value
        )

    @property
    @exception_bridge
    def thermal_expansion_for_grounded_nodes(
        self: "Self",
    ) -> "_2434.ThermalExpansionOptionForGroundedNodes":
        """mastapy.system_model.ThermalExpansionOptionForGroundedNodes"""
        temp = pythonnet_property_get(self.wrapped, "ThermalExpansionForGroundedNodes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.SystemModel.ThermalExpansionOptionForGroundedNodes"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model._2434",
            "ThermalExpansionOptionForGroundedNodes",
        )(value)

    @thermal_expansion_for_grounded_nodes.setter
    @exception_bridge
    @enforce_parameter_types
    def thermal_expansion_for_grounded_nodes(
        self: "Self", value: "_2434.ThermalExpansionOptionForGroundedNodes"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.SystemModel.ThermalExpansionOptionForGroundedNodes"
        )
        pythonnet_property_set(self.wrapped, "ThermalExpansionForGroundedNodes", value)

    @property
    @exception_bridge
    def transverse_contact_ratio_requirement(
        self: "Self",
    ) -> "_411.ContactRatioRequirements":
        """mastapy.gears.ContactRatioRequirements"""
        temp = pythonnet_property_get(self.wrapped, "TransverseContactRatioRequirement")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.ContactRatioRequirements"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears._411", "ContactRatioRequirements"
        )(value)

    @transverse_contact_ratio_requirement.setter
    @exception_bridge
    @enforce_parameter_types
    def transverse_contact_ratio_requirement(
        self: "Self", value: "_411.ContactRatioRequirements"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.ContactRatioRequirements"
        )
        pythonnet_property_set(self.wrapped, "TransverseContactRatioRequirement", value)

    @property
    @exception_bridge
    def unbalanced_mass_inclusion(
        self: "Self",
    ) -> "_2710.UnbalancedMassInclusionOption":
        """mastapy.system_model.part_model.UnbalancedMassInclusionOption"""
        temp = pythonnet_property_get(self.wrapped, "UnbalancedMassInclusion")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.SystemModel.PartModel.UnbalancedMassInclusionOption"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.part_model._2710",
            "UnbalancedMassInclusionOption",
        )(value)

    @unbalanced_mass_inclusion.setter
    @exception_bridge
    @enforce_parameter_types
    def unbalanced_mass_inclusion(
        self: "Self", value: "_2710.UnbalancedMassInclusionOption"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.SystemModel.PartModel.UnbalancedMassInclusionOption"
        )
        pythonnet_property_set(self.wrapped, "UnbalancedMassInclusion", value)

    @property
    @exception_bridge
    def use_element_contact_angles_for_angular_velocities_in_ball_bearings(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseElementContactAnglesForAngularVelocitiesInBallBearings"
        )

        if temp is None:
            return False

        return temp

    @use_element_contact_angles_for_angular_velocities_in_ball_bearings.setter
    @exception_bridge
    @enforce_parameter_types
    def use_element_contact_angles_for_angular_velocities_in_ball_bearings(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseElementContactAnglesForAngularVelocitiesInBallBearings",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_expanded_2d_projection_mode(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseExpanded2DProjectionMode")

        if temp is None:
            return False

        return temp

    @use_expanded_2d_projection_mode.setter
    @exception_bridge
    @enforce_parameter_types
    def use_expanded_2d_projection_mode(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseExpanded2DProjectionMode",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def volumetric_oil_air_mixture_ratio(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "VolumetricOilAirMixtureRatio")

        if temp is None:
            return 0.0

        return temp

    @volumetric_oil_air_mixture_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def volumetric_oil_air_mixture_ratio(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "VolumetricOilAirMixtureRatio",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def acoustic_analysis_setups(
        self: "Self",
    ) -> "_2869.AcousticAnalysisSetupCollection":
        """mastapy.system_model.part_model.acoustics.AcousticAnalysisSetupCollection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AcousticAnalysisSetups")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def default_system_temperatures(self: "Self") -> "_2435.TransmissionTemperatureSet":
        """mastapy.system_model.TransmissionTemperatureSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DefaultSystemTemperatures")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def detailed_spline_settings(self: "Self") -> "_1576.DetailedSplineJointSettings":
        """mastapy.detailed_rigid_connectors.splines.DetailedSplineJointSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DetailedSplineSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def electric_machine_group(self: "Self") -> "_2422.MAAElectricMachineGroup":
        """mastapy.system_model.MAAElectricMachineGroup

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElectricMachineGroup")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def fe_batch_operations(self: "Self") -> "_2582.BatchOperations":
        """mastapy.system_model.fe.BatchOperations

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FEBatchOperations")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def file_save_details_all(self: "Self") -> "_1775.FileHistory":
        """mastapy.utility.FileHistory

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FileSaveDetailsAll")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def file_save_details_most_recent(self: "Self") -> "_1776.FileHistoryItem":
        """mastapy.utility.FileHistoryItem

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FileSaveDetailsMostRecent")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear_set_design_group(self: "Self") -> "_417.GearSetDesignGroup":
        """mastapy.gears.GearSetDesignGroup

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSetDesignGroup")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gravity_orientation(self: "Self") -> "Vector3D":
        """Vector3D"""
        temp = pythonnet_property_get(self.wrapped, "GravityOrientation")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @gravity_orientation.setter
    @exception_bridge
    @enforce_parameter_types
    def gravity_orientation(self: "Self", value: "Vector3D") -> None:
        value = conversion.mp_to_pn_vector3d(value)
        pythonnet_property_set(self.wrapped, "GravityOrientation", value)

    @property
    @exception_bridge
    def gravity_vector_components(self: "Self") -> "Vector3D":
        """Vector3D"""
        temp = pythonnet_property_get(self.wrapped, "GravityVectorComponents")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @gravity_vector_components.setter
    @exception_bridge
    @enforce_parameter_types
    def gravity_vector_components(self: "Self", value: "Vector3D") -> None:
        value = conversion.mp_to_pn_vector3d(value)
        pythonnet_property_set(self.wrapped, "GravityVectorComponents", value)

    @property
    @exception_bridge
    def iso14179_coefficient_of_friction_constants_and_exponents_for_external_external_meshes(
        self: "Self",
    ) -> "_698.ISOTR1417912001CoefficientOfFrictionConstants":
        """mastapy.gears.materials.ISOTR1417912001CoefficientOfFrictionConstants

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "ISO14179CoefficientOfFrictionConstantsAndExponentsForExternalExternalMeshes",
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def iso14179_coefficient_of_friction_constants_and_exponents_for_internal_external_meshes(
        self: "Self",
    ) -> "_698.ISOTR1417912001CoefficientOfFrictionConstants":
        """mastapy.gears.materials.ISOTR1417912001CoefficientOfFrictionConstants

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "ISO14179CoefficientOfFrictionConstantsAndExponentsForInternalExternalMeshes",
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def skf_loss_moment_multipliers(self: "Self") -> "_1791.SKFLossMomentMultipliers":
        """mastapy.utility.SKFLossMomentMultipliers

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SKFLossMomentMultipliers")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def selected_gear_set_selection_group(
        self: "Self",
    ) -> "_2749.ActiveGearSetDesignSelectionGroup":
        """mastapy.system_model.part_model.gears.ActiveGearSetDesignSelectionGroup

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SelectedGearSetSelectionGroup")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def settings(self: "Self") -> "_2416.DesignSettings":
        """mastapy.system_model.DesignSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Settings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def shafts(self: "Self") -> "_38.ShaftSafetyFactorSettings":
        """mastapy.shafts.ShaftSafetyFactorSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Shafts")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def system(self: "Self") -> "_2433.SystemReporting":
        """mastapy.system_model.SystemReporting

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "System")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def system_optimiser_details(self: "Self") -> "_2452.SystemOptimiserDetails":
        """mastapy.system_model.optimization.system_optimiser.SystemOptimiserDetails

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemOptimiserDetails")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def bearing_detail_configurations(
        self: "Self",
    ) -> "List[_2861.BearingDetailConfiguration]":
        """List[mastapy.system_model.part_model.configurations.BearingDetailConfiguration]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BearingDetailConfigurations")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def design_configurations(self: "Self") -> "List[_2863.DesignConfiguration]":
        """List[mastapy.system_model.part_model.configurations.DesignConfiguration]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DesignConfigurations")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def fe_parts(self: "Self") -> "List[_2680.FEPart]":
        """List[mastapy.system_model.part_model.FEPart]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FEParts")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def fe_substructure_configurations(
        self: "Self",
    ) -> "List[_2858.ActiveFESubstructureSelectionGroup]":
        """List[mastapy.system_model.part_model.configurations.ActiveFESubstructureSelectionGroup]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FESubstructureConfigurations")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def gear_set_configurations(
        self: "Self",
    ) -> "List[_2749.ActiveGearSetDesignSelectionGroup]":
        """List[mastapy.system_model.part_model.gears.ActiveGearSetDesignSelectionGroup]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSetConfigurations")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def iso14179_settings_per_bearing_type(
        self: "Self",
    ) -> "List[_2183.ISO14179SettingsPerBearingType]":
        """List[mastapy.bearings.bearing_results.rolling.ISO14179SettingsPerBearingType]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISO14179SettingsPerBearingType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def shaft_detail_configurations(
        self: "Self",
    ) -> "List[_2860.ActiveShaftDesignSelectionGroup]":
        """List[mastapy.system_model.part_model.configurations.ActiveShaftDesignSelectionGroup]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftDetailConfigurations")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def databases(self: "Self") -> "_2485.Databases":
        """mastapy.system_model.database_access.Databases

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Databases")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def design_states(self: "Self") -> "List[_5953.DesignState]":
        """List[mastapy.system_model.analyses_and_results.load_case_groups.DesignState]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DesignStates")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def duty_cycles(self: "Self") -> "List[_5954.DutyCycle]":
        """List[mastapy.system_model.analyses_and_results.load_case_groups.DutyCycle]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DutyCycles")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def gear_set_config(self: "Self") -> "_2770.GearSetConfiguration":
        """mastapy.system_model.part_model.gears.GearSetConfiguration"""
        temp = pythonnet_property_get(self.wrapped, "GearSetConfig")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @gear_set_config.setter
    @exception_bridge
    @enforce_parameter_types
    def gear_set_config(self: "Self", value: "_2770.GearSetConfiguration") -> None:
        pythonnet_property_set(self.wrapped, "GearSetConfig", value.wrapped)

    @property
    @exception_bridge
    def masta_settings(self: "Self") -> "_2423.MASTASettings":
        """mastapy.system_model.MASTASettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MastaSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def root_assembly(self: "Self") -> "_2706.RootAssembly":
        """mastapy.system_model.part_model.RootAssembly

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RootAssembly")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def static_loads(self: "Self") -> "List[_7674.StaticLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StaticLoads")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def status(self: "Self") -> "_1988.Status":
        """mastapy.utility.model_validation.Status

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Status")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def system_optimiser(self: "Self") -> "_2451.SystemOptimiser":
        """mastapy.system_model.optimization.system_optimiser.SystemOptimiser

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemOptimiser")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def time_series_load_case_groups(
        self: "Self",
    ) -> "List[_5961.TimeSeriesLoadCaseGroup]":
        """List[mastapy.system_model.analyses_and_results.load_case_groups.TimeSeriesLoadCaseGroup]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TimeSeriesLoadCaseGroups")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    @enforce_parameter_types
    def add_design_state(
        self: "Self", name: "str" = "New Design State"
    ) -> "_5953.DesignState":
        """mastapy.system_model.analyses_and_results.load_case_groups.DesignState

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddDesignState", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_duty_cycle(
        self: "Self", name: "str" = "New Duty Cycle"
    ) -> "_5954.DutyCycle":
        """mastapy.system_model.analyses_and_results.load_case_groups.DutyCycle

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddDutyCycle", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_gear_set_selection_group(
        self: "Self", name: "str"
    ) -> "_2749.ActiveGearSetDesignSelectionGroup":
        """mastapy.system_model.part_model.gears.ActiveGearSetDesignSelectionGroup

        Args:
            name (str)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddGearSetSelectionGroup", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def add_synchroniser_shift_empty(self: "Self") -> "_3227.SynchroniserShift":
        """mastapy.system_model.analyses_and_results.synchroniser_analysis.SynchroniserShift"""
        method_result = pythonnet_method_call(self.wrapped, "AddSynchroniserShift")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_synchroniser_shift(self: "Self", name: "str") -> "_3227.SynchroniserShift":
        """mastapy.system_model.analyses_and_results.synchroniser_analysis.SynchroniserShift

        Args:
            name (str)
        """
        name = str(name)
        method_result = pythonnet_method_call_overload(
            self.wrapped, "AddSynchroniserShift", [_STRING], name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def clear_design(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ClearDesign")

    @exception_bridge
    def __copy__(self: "Self") -> "Design":
        """mastapy.system_model.Design"""
        method_result = pythonnet_method_call(self.wrapped, "Copy")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def __deepcopy__(self: "Self", memo) -> "Design":
        """mastapy.system_model.Design"""
        method_result = pythonnet_method_call(self.wrapped, "Copy")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def copy_with_results(self: "Self") -> "Design":
        """mastapy.system_model.Design"""
        method_result = pythonnet_method_call(self.wrapped, "CopyWithResults")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def design_state_load_case_group_named(
        self: "Self", name: "str"
    ) -> "_5953.DesignState":
        """mastapy.system_model.analyses_and_results.load_case_groups.DesignState

        Args:
            name (str)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "DesignStateLoadCaseGroupNamed", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def design_state_named(self: "Self", name: "str") -> "_5953.DesignState":
        """mastapy.system_model.analyses_and_results.load_case_groups.DesignState

        Args:
            name (str)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "DesignStateNamed", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def dispose(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Dispose")

    @exception_bridge
    @enforce_parameter_types
    def duty_cycle_named(self: "Self", name: "str") -> "_5954.DutyCycle":
        """mastapy.system_model.analyses_and_results.load_case_groups.DutyCycle

        Args:
            name (str)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "DutyCycleNamed", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def load_results(self: "Self", file_name: "PathLike") -> "Tuple[int, str]":
        """Tuple[int, str]

        Args:
            file_name (PathLike)
        """
        file_name = str(file_name)
        method_result = pythonnet_method_call(self.wrapped, "LoadResults", file_name)
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def new_belt_creation_options(
        self: "Self",
        centre_distance: "float" = 0.1,
        pulley_a_diameter: "float" = 0.08,
        pulley_b_diameter: "float" = 0.08,
        name: "str" = "Belt Drive",
    ) -> "_2809.BeltCreationOptions":
        """mastapy.system_model.part_model.creation_options.BeltCreationOptions

        Args:
            centre_distance (float, optional)
            pulley_a_diameter (float, optional)
            pulley_b_diameter (float, optional)
            name (str, optional)
        """
        centre_distance = float(centre_distance)
        pulley_a_diameter = float(pulley_a_diameter)
        pulley_b_diameter = float(pulley_b_diameter)
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "NewBeltCreationOptions",
            centre_distance if centre_distance else 0.0,
            pulley_a_diameter if pulley_a_diameter else 0.0,
            pulley_b_diameter if pulley_b_diameter else 0.0,
            name if name else "",
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def new_cycloidal_assembly_creation_options(
        self: "Self",
        number_of_discs: "int" = 1,
        number_of_pins: "int" = 10,
        name: "str" = "Cycloidal Assembly",
    ) -> "_2810.CycloidalAssemblyCreationOptions":
        """mastapy.system_model.part_model.creation_options.CycloidalAssemblyCreationOptions

        Args:
            number_of_discs (int, optional)
            number_of_pins (int, optional)
            name (str, optional)
        """
        number_of_discs = int(number_of_discs)
        number_of_pins = int(number_of_pins)
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "NewCycloidalAssemblyCreationOptions",
            number_of_discs if number_of_discs else 0,
            number_of_pins if number_of_pins else 0,
            name if name else "",
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def new_cylindrical_gear_linear_train_creation_options(
        self: "Self", number_of_gears: "int" = 3, name: "str" = "Gear Train"
    ) -> "_2811.CylindricalGearLinearTrainCreationOptions":
        """mastapy.system_model.part_model.creation_options.CylindricalGearLinearTrainCreationOptions

        Args:
            number_of_gears (int, optional)
            name (str, optional)
        """
        number_of_gears = int(number_of_gears)
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "NewCylindricalGearLinearTrainCreationOptions",
            number_of_gears if number_of_gears else 0,
            name if name else "",
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def new_cylindrical_gear_pair_creation_options(
        self: "Self",
    ) -> "_1265.CylindricalGearPairCreationOptions":
        """mastapy.gears.gear_designs.creation_options.CylindricalGearPairCreationOptions"""
        method_result = pythonnet_method_call(
            self.wrapped, "NewCylindricalGearPairCreationOptions"
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def new_hypoid_gear_set_creation_options(
        self: "Self",
    ) -> "_1268.HypoidGearSetCreationOptions":
        """mastapy.gears.gear_designs.creation_options.HypoidGearSetCreationOptions"""
        method_result = pythonnet_method_call(
            self.wrapped, "NewHypoidGearSetCreationOptions"
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def new_nodal_matrix(
        self: "Self", dense_matrix: "List[List[float]]"
    ) -> "_82.NodalMatrix":
        """mastapy.nodal_analysis.NodalMatrix

        Args:
            dense_matrix (List[List[float]])
        """
        dense_matrix = conversion.mp_to_pn_list_float_2d(dense_matrix)
        method_result = pythonnet_method_call(
            self.wrapped, "NewNodalMatrix", dense_matrix
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def new_planet_carrier_creation_options(
        self: "Self", number_of_planets: "int" = 3, diameter: "float" = 0.05
    ) -> "_2813.PlanetCarrierCreationOptions":
        """mastapy.system_model.part_model.creation_options.PlanetCarrierCreationOptions

        Args:
            number_of_planets (int, optional)
            diameter (float, optional)
        """
        number_of_planets = int(number_of_planets)
        diameter = float(diameter)
        method_result = pythonnet_method_call(
            self.wrapped,
            "NewPlanetCarrierCreationOptions",
            number_of_planets if number_of_planets else 0,
            diameter if diameter else 0.0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def new_shaft_creation_options(
        self: "Self",
        length: "float" = 0.1,
        outer_diameter: "float" = 0.025,
        bore: "float" = 0.0,
        name: "str" = "Shaft",
    ) -> "_2814.ShaftCreationOptions":
        """mastapy.system_model.part_model.creation_options.ShaftCreationOptions

        Args:
            length (float, optional)
            outer_diameter (float, optional)
            bore (float, optional)
            name (str, optional)
        """
        length = float(length)
        outer_diameter = float(outer_diameter)
        bore = float(bore)
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "NewShaftCreationOptions",
            length if length else 0.0,
            outer_diameter if outer_diameter else 0.0,
            bore if bore else 0.0,
            name if name else "",
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def new_spiral_bevel_gear_set_creation_options(
        self: "Self",
    ) -> "_1269.SpiralBevelGearSetCreationOptions":
        """mastapy.gears.gear_designs.creation_options.SpiralBevelGearSetCreationOptions"""
        method_result = pythonnet_method_call(
            self.wrapped, "NewSpiralBevelGearSetCreationOptions"
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def remove_all_gear_set_selection_group(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "RemoveAllGearSetSelectionGroup")

    @exception_bridge
    @enforce_parameter_types
    def remove_bearing_from_database(
        self: "Self", rolling_bearing: "_2375.RollingBearing"
    ) -> None:
        """Method does not return.

        Args:
            rolling_bearing (mastapy.bearings.bearing_designs.rolling.RollingBearing)
        """
        pythonnet_method_call(
            self.wrapped,
            "RemoveBearingFromDatabase",
            rolling_bearing.wrapped if rolling_bearing else None,
        )

    @exception_bridge
    @enforce_parameter_types
    def remove_design_configuration(
        self: "Self", config: "_2863.DesignConfiguration"
    ) -> None:
        """Method does not return.

        Args:
            config (mastapy.system_model.part_model.configurations.DesignConfiguration)
        """
        pythonnet_method_call(
            self.wrapped,
            "RemoveDesignConfiguration",
            config.wrapped if config else None,
        )

    @exception_bridge
    @enforce_parameter_types
    def remove_gear_set_selection_group(
        self: "Self", group: "_2749.ActiveGearSetDesignSelectionGroup"
    ) -> None:
        """Method does not return.

        Args:
            group (mastapy.system_model.part_model.gears.ActiveGearSetDesignSelectionGroup)
        """
        pythonnet_method_call(
            self.wrapped,
            "RemoveGearSetSelectionGroup",
            group.wrapped if group else None,
        )

    @exception_bridge
    @enforce_parameter_types
    def remove_synchroniser_shift(
        self: "Self", shift: "_3227.SynchroniserShift"
    ) -> None:
        """Method does not return.

        Args:
            shift (mastapy.system_model.analyses_and_results.synchroniser_analysis.SynchroniserShift)
        """
        pythonnet_method_call(
            self.wrapped, "RemoveSynchroniserShift", shift.wrapped if shift else None
        )

    @exception_bridge
    @enforce_parameter_types
    def save(
        self: "Self", file_name: "PathLike", save_results: "bool"
    ) -> "_1988.Status":
        """mastapy.utility.model_validation.Status

        Args:
            file_name (PathLike)
            save_results (bool)
        """
        file_name = str(file_name)
        save_results = bool(save_results)
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "Save",
            [str, _BOOLEAN],
            file_name,
            save_results if save_results else False,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def save_with_progress(
        self: "Self",
        file_name: "PathLike",
        save_results: "bool",
        progress: "_7901.TaskProgress",
    ) -> "_1988.Status":
        """mastapy.utility.model_validation.Status

        Args:
            file_name (PathLike)
            save_results (bool)
            progress (mastapy.TaskProgress)
        """
        file_name = str(file_name)
        save_results = bool(save_results)
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "Save",
            [str, _BOOLEAN, _TASK_PROGRESS],
            file_name,
            save_results if save_results else False,
            progress.wrapped if progress else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def save_load_case_results(
        self: "Self", file_name: "PathLike", load_cases: "List[_7673.LoadCase]"
    ) -> None:
        """Method does not return.

        Args:
            file_name (PathLike)
            load_cases (List[mastapy.system_model.analyses_and_results.static_loads.LoadCase])
        """
        file_name = str(file_name)
        load_cases = conversion.mp_to_pn_objects_in_dotnet_list(load_cases)
        pythonnet_method_call(
            self.wrapped, "SaveLoadCaseResults", file_name, load_cases
        )

    @exception_bridge
    @enforce_parameter_types
    def save_results(self: "Self", file_name: "PathLike") -> None:
        """Method does not return.

        Args:
            file_name (PathLike)
        """
        file_name = str(file_name)
        pythonnet_method_call(self.wrapped, "SaveResults", file_name)

    @exception_bridge
    @enforce_parameter_types
    def time_series_load_case_group_named(
        self: "Self", name: "str"
    ) -> "_5961.TimeSeriesLoadCaseGroup":
        """mastapy.system_model.analyses_and_results.load_case_groups.TimeSeriesLoadCaseGroup

        Args:
            name (str)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "TimeSeriesLoadCaseGroupNamed", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def all_parts(self: "Self") -> "List[_2698.Part]":
        """List[mastapy.system_model.part_model.Part]"""
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Part")
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_assembly(self: "Self") -> "List[_2658.Assembly]":
        """List[mastapy.system_model.part_model.Assembly]"""
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Assembly")
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_abstract_assembly(
        self: "Self",
    ) -> "List[_2659.AbstractAssembly]":
        """List[mastapy.system_model.part_model.AbstractAssembly]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "AbstractAssembly"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_abstract_shaft(self: "Self") -> "List[_2660.AbstractShaft]":
        """List[mastapy.system_model.part_model.AbstractShaft]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "AbstractShaft"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_abstract_shaft_or_housing(
        self: "Self",
    ) -> "List[_2661.AbstractShaftOrHousing]":
        """List[mastapy.system_model.part_model.AbstractShaftOrHousing]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "AbstractShaftOrHousing"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_bearing(self: "Self") -> "List[_2664.Bearing]":
        """List[mastapy.system_model.part_model.Bearing]"""
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Bearing")
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_bolt(self: "Self") -> "List[_2667.Bolt]":
        """List[mastapy.system_model.part_model.Bolt]"""
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Bolt")
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_bolted_joint(self: "Self") -> "List[_2668.BoltedJoint]":
        """List[mastapy.system_model.part_model.BoltedJoint]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "BoltedJoint"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_component(self: "Self") -> "List[_2670.Component]":
        """List[mastapy.system_model.part_model.Component]"""
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Component")
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_connector(self: "Self") -> "List[_2673.Connector]":
        """List[mastapy.system_model.part_model.Connector]"""
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Connector")
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_datum(self: "Self") -> "List[_2674.Datum]":
        """List[mastapy.system_model.part_model.Datum]"""
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Datum")
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_external_cad_model(
        self: "Self",
    ) -> "List[_2679.ExternalCADModel]":
        """List[mastapy.system_model.part_model.ExternalCADModel]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "ExternalCADModel"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_fe_part(self: "Self") -> "List[_2680.FEPart]":
        """List[mastapy.system_model.part_model.FEPart]"""
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "FEPart")
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_flexible_pin_assembly(
        self: "Self",
    ) -> "List[_2681.FlexiblePinAssembly]":
        """List[mastapy.system_model.part_model.FlexiblePinAssembly]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "FlexiblePinAssembly"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_guide_dxf_model(self: "Self") -> "List[_2682.GuideDxfModel]":
        """List[mastapy.system_model.part_model.GuideDxfModel]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "GuideDxfModel"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_mass_disc(self: "Self") -> "List[_2689.MassDisc]":
        """List[mastapy.system_model.part_model.MassDisc]"""
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "MassDisc")
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_measurement_component(
        self: "Self",
    ) -> "List[_2690.MeasurementComponent]":
        """List[mastapy.system_model.part_model.MeasurementComponent]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "MeasurementComponent"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_microphone(self: "Self") -> "List[_2691.Microphone]":
        """List[mastapy.system_model.part_model.Microphone]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "Microphone"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_microphone_array(
        self: "Self",
    ) -> "List[_2692.MicrophoneArray]":
        """List[mastapy.system_model.part_model.MicrophoneArray]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "MicrophoneArray"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_mountable_component(
        self: "Self",
    ) -> "List[_2693.MountableComponent]":
        """List[mastapy.system_model.part_model.MountableComponent]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "MountableComponent"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_oil_seal(self: "Self") -> "List[_2695.OilSeal]":
        """List[mastapy.system_model.part_model.OilSeal]"""
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "OilSeal")
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_part(self: "Self") -> "List[_2698.Part]":
        """List[mastapy.system_model.part_model.Part]"""
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Part")
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_planet_carrier(self: "Self") -> "List[_2700.PlanetCarrier]":
        """List[mastapy.system_model.part_model.PlanetCarrier]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "PlanetCarrier"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_point_load(self: "Self") -> "List[_2702.PointLoad]":
        """List[mastapy.system_model.part_model.PointLoad]"""
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "PointLoad")
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_power_load(self: "Self") -> "List[_2703.PowerLoad]":
        """List[mastapy.system_model.part_model.PowerLoad]"""
        cast_type = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "PowerLoad")
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_root_assembly(self: "Self") -> "List[_2706.RootAssembly]":
        """List[mastapy.system_model.part_model.RootAssembly]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "RootAssembly"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_specialised_assembly(
        self: "Self",
    ) -> "List[_2708.SpecialisedAssembly]":
        """List[mastapy.system_model.part_model.SpecialisedAssembly]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "SpecialisedAssembly"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_unbalanced_mass(self: "Self") -> "List[_2709.UnbalancedMass]":
        """List[mastapy.system_model.part_model.UnbalancedMass]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "UnbalancedMass"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_virtual_component(
        self: "Self",
    ) -> "List[_2711.VirtualComponent]":
        """List[mastapy.system_model.part_model.VirtualComponent]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel", "VirtualComponent"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_shaft(self: "Self") -> "List[_2714.Shaft]":
        """List[mastapy.system_model.part_model.shaft_model.Shaft]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.ShaftModel", "Shaft"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_agma_gleason_conical_gear(
        self: "Self",
    ) -> "List[_2750.AGMAGleasonConicalGear]":
        """List[mastapy.system_model.part_model.gears.AGMAGleasonConicalGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "AGMAGleasonConicalGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_agma_gleason_conical_gear_set(
        self: "Self",
    ) -> "List[_2751.AGMAGleasonConicalGearSet]":
        """List[mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "AGMAGleasonConicalGearSet"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_bevel_differential_gear(
        self: "Self",
    ) -> "List[_2752.BevelDifferentialGear]":
        """List[mastapy.system_model.part_model.gears.BevelDifferentialGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_bevel_differential_gear_set(
        self: "Self",
    ) -> "List[_2753.BevelDifferentialGearSet]":
        """List[mastapy.system_model.part_model.gears.BevelDifferentialGearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialGearSet"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_bevel_differential_planet_gear(
        self: "Self",
    ) -> "List[_2754.BevelDifferentialPlanetGear]":
        """List[mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialPlanetGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_bevel_differential_sun_gear(
        self: "Self",
    ) -> "List[_2755.BevelDifferentialSunGear]":
        """List[mastapy.system_model.part_model.gears.BevelDifferentialSunGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialSunGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_bevel_gear(self: "Self") -> "List[_2756.BevelGear]":
        """List[mastapy.system_model.part_model.gears.BevelGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_bevel_gear_set(self: "Self") -> "List[_2757.BevelGearSet]":
        """List[mastapy.system_model.part_model.gears.BevelGearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelGearSet"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_concept_gear(self: "Self") -> "List[_2758.ConceptGear]":
        """List[mastapy.system_model.part_model.gears.ConceptGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConceptGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_concept_gear_set(
        self: "Self",
    ) -> "List[_2759.ConceptGearSet]":
        """List[mastapy.system_model.part_model.gears.ConceptGearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConceptGearSet"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_conical_gear(self: "Self") -> "List[_2760.ConicalGear]":
        """List[mastapy.system_model.part_model.gears.ConicalGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConicalGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_conical_gear_set(
        self: "Self",
    ) -> "List[_2761.ConicalGearSet]":
        """List[mastapy.system_model.part_model.gears.ConicalGearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConicalGearSet"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_cylindrical_gear(
        self: "Self",
    ) -> "List[_2762.CylindricalGear]":
        """List[mastapy.system_model.part_model.gears.CylindricalGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "CylindricalGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_cylindrical_gear_set(
        self: "Self",
    ) -> "List[_2763.CylindricalGearSet]":
        """List[mastapy.system_model.part_model.gears.CylindricalGearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "CylindricalGearSet"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_cylindrical_planet_gear(
        self: "Self",
    ) -> "List[_2764.CylindricalPlanetGear]":
        """List[mastapy.system_model.part_model.gears.CylindricalPlanetGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "CylindricalPlanetGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_face_gear(self: "Self") -> "List[_2765.FaceGear]":
        """List[mastapy.system_model.part_model.gears.FaceGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "FaceGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_face_gear_set(self: "Self") -> "List[_2766.FaceGearSet]":
        """List[mastapy.system_model.part_model.gears.FaceGearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "FaceGearSet"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_gear(self: "Self") -> "List[_2767.Gear]":
        """List[mastapy.system_model.part_model.gears.Gear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "Gear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_gear_set(self: "Self") -> "List[_2769.GearSet]":
        """List[mastapy.system_model.part_model.gears.GearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "GearSet"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_hypoid_gear(self: "Self") -> "List[_2771.HypoidGear]":
        """List[mastapy.system_model.part_model.gears.HypoidGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "HypoidGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_hypoid_gear_set(self: "Self") -> "List[_2772.HypoidGearSet]":
        """List[mastapy.system_model.part_model.gears.HypoidGearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "HypoidGearSet"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_klingelnberg_cyclo_palloid_conical_gear(
        self: "Self",
    ) -> "List[_2773.KlingelnbergCycloPalloidConicalGear]":
        """List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears",
            "KlingelnbergCycloPalloidConicalGear",
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_klingelnberg_cyclo_palloid_conical_gear_set(
        self: "Self",
    ) -> "List[_2774.KlingelnbergCycloPalloidConicalGearSet]":
        """List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears",
            "KlingelnbergCycloPalloidConicalGearSet",
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_klingelnberg_cyclo_palloid_hypoid_gear(
        self: "Self",
    ) -> "List[_2775.KlingelnbergCycloPalloidHypoidGear]":
        """List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears",
            "KlingelnbergCycloPalloidHypoidGear",
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(
        self: "Self",
    ) -> "List[_2776.KlingelnbergCycloPalloidHypoidGearSet]":
        """List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears",
            "KlingelnbergCycloPalloidHypoidGearSet",
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(
        self: "Self",
    ) -> "List[_2777.KlingelnbergCycloPalloidSpiralBevelGear]":
        """List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears",
            "KlingelnbergCycloPalloidSpiralBevelGear",
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(
        self: "Self",
    ) -> "List[_2778.KlingelnbergCycloPalloidSpiralBevelGearSet]":
        """List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears",
            "KlingelnbergCycloPalloidSpiralBevelGearSet",
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_planetary_gear_set(
        self: "Self",
    ) -> "List[_2779.PlanetaryGearSet]":
        """List[mastapy.system_model.part_model.gears.PlanetaryGearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "PlanetaryGearSet"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_spiral_bevel_gear(
        self: "Self",
    ) -> "List[_2781.SpiralBevelGear]":
        """List[mastapy.system_model.part_model.gears.SpiralBevelGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "SpiralBevelGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_spiral_bevel_gear_set(
        self: "Self",
    ) -> "List[_2782.SpiralBevelGearSet]":
        """List[mastapy.system_model.part_model.gears.SpiralBevelGearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "SpiralBevelGearSet"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_straight_bevel_diff_gear(
        self: "Self",
    ) -> "List[_2783.StraightBevelDiffGear]":
        """List[mastapy.system_model.part_model.gears.StraightBevelDiffGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelDiffGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_straight_bevel_diff_gear_set(
        self: "Self",
    ) -> "List[_2784.StraightBevelDiffGearSet]":
        """List[mastapy.system_model.part_model.gears.StraightBevelDiffGearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelDiffGearSet"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_straight_bevel_gear(
        self: "Self",
    ) -> "List[_2785.StraightBevelGear]":
        """List[mastapy.system_model.part_model.gears.StraightBevelGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_straight_bevel_gear_set(
        self: "Self",
    ) -> "List[_2786.StraightBevelGearSet]":
        """List[mastapy.system_model.part_model.gears.StraightBevelGearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelGearSet"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_straight_bevel_planet_gear(
        self: "Self",
    ) -> "List[_2787.StraightBevelPlanetGear]":
        """List[mastapy.system_model.part_model.gears.StraightBevelPlanetGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelPlanetGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_straight_bevel_sun_gear(
        self: "Self",
    ) -> "List[_2788.StraightBevelSunGear]":
        """List[mastapy.system_model.part_model.gears.StraightBevelSunGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelSunGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_worm_gear(self: "Self") -> "List[_2789.WormGear]":
        """List[mastapy.system_model.part_model.gears.WormGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "WormGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_worm_gear_set(self: "Self") -> "List[_2790.WormGearSet]":
        """List[mastapy.system_model.part_model.gears.WormGearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "WormGearSet"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_zerol_bevel_gear(
        self: "Self",
    ) -> "List[_2791.ZerolBevelGear]":
        """List[mastapy.system_model.part_model.gears.ZerolBevelGear]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "ZerolBevelGear"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_zerol_bevel_gear_set(
        self: "Self",
    ) -> "List[_2792.ZerolBevelGearSet]":
        """List[mastapy.system_model.part_model.gears.ZerolBevelGearSet]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Gears", "ZerolBevelGearSet"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_cycloidal_assembly(
        self: "Self",
    ) -> "List[_2806.CycloidalAssembly]":
        """List[mastapy.system_model.part_model.cycloidal.CycloidalAssembly]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Cycloidal", "CycloidalAssembly"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_cycloidal_disc(self: "Self") -> "List[_2807.CycloidalDisc]":
        """List[mastapy.system_model.part_model.cycloidal.CycloidalDisc]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Cycloidal", "CycloidalDisc"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_ring_pins(self: "Self") -> "List[_2808.RingPins]":
        """List[mastapy.system_model.part_model.cycloidal.RingPins]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Cycloidal", "RingPins"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_belt_drive(self: "Self") -> "List[_2815.BeltDrive]":
        """List[mastapy.system_model.part_model.couplings.BeltDrive]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "BeltDrive"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_clutch(self: "Self") -> "List[_2817.Clutch]":
        """List[mastapy.system_model.part_model.couplings.Clutch]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "Clutch"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_clutch_half(self: "Self") -> "List[_2818.ClutchHalf]":
        """List[mastapy.system_model.part_model.couplings.ClutchHalf]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ClutchHalf"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_concept_coupling(
        self: "Self",
    ) -> "List[_2820.ConceptCoupling]":
        """List[mastapy.system_model.part_model.couplings.ConceptCoupling]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ConceptCoupling"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_concept_coupling_half(
        self: "Self",
    ) -> "List[_2821.ConceptCouplingHalf]":
        """List[mastapy.system_model.part_model.couplings.ConceptCouplingHalf]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ConceptCouplingHalf"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_coupling(self: "Self") -> "List[_2823.Coupling]":
        """List[mastapy.system_model.part_model.couplings.Coupling]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "Coupling"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_coupling_half(self: "Self") -> "List[_2824.CouplingHalf]":
        """List[mastapy.system_model.part_model.couplings.CouplingHalf]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "CouplingHalf"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_cvt(self: "Self") -> "List[_2826.CVT]":
        """List[mastapy.system_model.part_model.couplings.CVT]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "CVT"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_cvt_pulley(self: "Self") -> "List[_2827.CVTPulley]":
        """List[mastapy.system_model.part_model.couplings.CVTPulley]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "CVTPulley"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_part_to_part_shear_coupling(
        self: "Self",
    ) -> "List[_2828.PartToPartShearCoupling]":
        """List[mastapy.system_model.part_model.couplings.PartToPartShearCoupling]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "PartToPartShearCoupling"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_part_to_part_shear_coupling_half(
        self: "Self",
    ) -> "List[_2829.PartToPartShearCouplingHalf]":
        """List[mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings",
            "PartToPartShearCouplingHalf",
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_pulley(self: "Self") -> "List[_2831.Pulley]":
        """List[mastapy.system_model.part_model.couplings.Pulley]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "Pulley"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_rolling_ring(self: "Self") -> "List[_2838.RollingRing]":
        """List[mastapy.system_model.part_model.couplings.RollingRing]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "RollingRing"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_rolling_ring_assembly(
        self: "Self",
    ) -> "List[_2839.RollingRingAssembly]":
        """List[mastapy.system_model.part_model.couplings.RollingRingAssembly]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "RollingRingAssembly"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_shaft_hub_connection(
        self: "Self",
    ) -> "List[_2840.ShaftHubConnection]":
        """List[mastapy.system_model.part_model.couplings.ShaftHubConnection]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ShaftHubConnection"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_spring_damper(self: "Self") -> "List[_2846.SpringDamper]":
        """List[mastapy.system_model.part_model.couplings.SpringDamper]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SpringDamper"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_spring_damper_half(
        self: "Self",
    ) -> "List[_2847.SpringDamperHalf]":
        """List[mastapy.system_model.part_model.couplings.SpringDamperHalf]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SpringDamperHalf"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_synchroniser(self: "Self") -> "List[_2848.Synchroniser]":
        """List[mastapy.system_model.part_model.couplings.Synchroniser]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "Synchroniser"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_synchroniser_half(
        self: "Self",
    ) -> "List[_2850.SynchroniserHalf]":
        """List[mastapy.system_model.part_model.couplings.SynchroniserHalf]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SynchroniserHalf"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_synchroniser_part(
        self: "Self",
    ) -> "List[_2851.SynchroniserPart]":
        """List[mastapy.system_model.part_model.couplings.SynchroniserPart]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SynchroniserPart"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_synchroniser_sleeve(
        self: "Self",
    ) -> "List[_2852.SynchroniserSleeve]":
        """List[mastapy.system_model.part_model.couplings.SynchroniserSleeve]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SynchroniserSleeve"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_torque_converter(
        self: "Self",
    ) -> "List[_2853.TorqueConverter]":
        """List[mastapy.system_model.part_model.couplings.TorqueConverter]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "TorqueConverter"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_torque_converter_pump(
        self: "Self",
    ) -> "List[_2854.TorqueConverterPump]":
        """List[mastapy.system_model.part_model.couplings.TorqueConverterPump]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "TorqueConverterPump"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @exception_bridge
    def all_parts_of_type_torque_converter_turbine(
        self: "Self",
    ) -> "List[_2856.TorqueConverterTurbine]":
        """List[mastapy.system_model.part_model.couplings.TorqueConverterTurbine]"""
        cast_type = python_net_import(
            "SMT.MastaAPI.SystemModel.PartModel.Couplings", "TorqueConverterTurbine"
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call_generic(self.wrapped, "AllParts", cast_type)
        )

    @staticmethod
    @exception_bridge
    @enforce_parameter_types
    def load(
        file_path: "PathLike",
        load_full_fe_option: "_1774.ExternalFullFEFileOption" = _1774.ExternalFullFEFileOption.MESH_AND_EXPANSION_VECTORS,
    ) -> "Design":
        """mastapy.system_model.Design

        Args:
            file_path (PathLike)
            load_full_fe_option (mastapy.utility.ExternalFullFEFileOption, optional)
        """
        file_path = str(file_path)
        load_full_fe_option = conversion.mp_to_pn_enum(
            load_full_fe_option, "SMT.MastaAPI.Utility.ExternalFullFEFileOption"
        )
        method_result = pythonnet_method_call(
            Design.TYPE, "Load", file_path, load_full_fe_option
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @staticmethod
    @exception_bridge
    @enforce_parameter_types
    def load_example(example_string: "Union[ExampleName, str]") -> "Design":
        """mastapy.system_model.Design

        Args:
            example_string (Union[ExampleName, str])
        """
        example_string = str(example_string)
        method_result = pythonnet_method_call(
            Design.TYPE, "LoadExample", example_string
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def create_new_design(self: "Self") -> "Design":
        """mastapy.system_model.Design"""
        method_result = pythonnet_method_call(self.wrapped, "CreateNewDesign")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def load_new_design(
        self: "Self",
        file_path: "PathLike",
        load_full_fe_option: "_1774.ExternalFullFEFileOption" = _1774.ExternalFullFEFileOption.MESH_AND_EXPANSION_VECTORS,
    ) -> "Design":
        """mastapy.system_model.Design

        Args:
            file_path (PathLike)
            load_full_fe_option (mastapy.utility.ExternalFullFEFileOption, optional)
        """
        file_path = str(file_path)
        load_full_fe_option = conversion.mp_to_pn_enum(
            load_full_fe_option, "SMT.MastaAPI.Utility.ExternalFullFEFileOption"
        )
        method_result = pythonnet_method_call(
            self.wrapped, "LoadNewDesign", file_path, load_full_fe_option
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def create_from_example(
        self: "Self", example_string: "Union[ExampleName, str]"
    ) -> "Design":
        """mastapy.system_model.Design

        Args:
            example_string (Union[ExampleName, str])
        """
        example_string = str(example_string)
        method_result = pythonnet_method_call(
            self.wrapped, "CreateFromExample", example_string
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def compare_for_test_only(self: "Self", design: "Design", sb: "str") -> "bool":
        """bool

        Args:
            design (mastapy.system_model.Design)
            sb (str)
        """
        sb = str(sb)
        method_result = pythonnet_method_call(
            self.wrapped,
            "CompareForTestOnly",
            design.wrapped if design else None,
            sb if sb else "",
        )
        return method_result

    @exception_bridge
    def add_bearing_detail_configuration_all_bearings(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddBearingDetailConfigurationAllBearings")

    @exception_bridge
    def add_bearing_detail_configuration_rolling_bearings(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "AddBearingDetailConfigurationRollingBearings"
        )

    @exception_bridge
    def add_design_configuration(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddDesignConfiguration")

    @exception_bridge
    def add_fe_substructure_configuration(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddFESubstructureConfiguration")

    @exception_bridge
    def add_gear_set_configuration(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddGearSetConfiguration")

    @exception_bridge
    def add_shaft_detail_configuration(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddShaftDetailConfiguration")

    @exception_bridge
    def change_gears_to_clones_where_suitable(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ChangeGearsToClonesWhereSuitable")

    @exception_bridge
    def clear_undo_redo_stacks(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ClearUndoRedoStacks")

    @exception_bridge
    def compare_results_to_previous_masta_version(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CompareResultsToPreviousMASTAVersion")

    @exception_bridge
    def delete_all_gear_set_configurations_that_have_errors_or_warnings(
        self: "Self",
    ) -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "DeleteAllGearSetConfigurationsThatHaveErrorsOrWarnings"
        )

    @exception_bridge
    def delete_all_gear_sets_designs_that_are_not_used_in_configurations(
        self: "Self",
    ) -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "DeleteAllGearSetsDesignsThatAreNotUsedInConfigurations"
        )

    @exception_bridge
    def delete_all_inactive_gear_set_designs(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "DeleteAllInactiveGearSetDesigns")

    def __enter__(self: "Self") -> None:
        return self

    def __exit__(
        self: "Self", exception_type: "Any", exception_value: "Any", traceback: "Any"
    ) -> None:
        self.dispose()

    @property
    def cast_to(self: "Self") -> "_Cast_Design":
        """Cast to another type.

        Returns:
            _Cast_Design
        """
        return _Cast_Design(self)
