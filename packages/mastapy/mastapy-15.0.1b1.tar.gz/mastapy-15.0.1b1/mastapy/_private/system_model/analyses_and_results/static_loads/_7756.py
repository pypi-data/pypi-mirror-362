"""FEPartLoadCase"""

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
from mastapy._private.system_model.analyses_and_results.static_loads import _7677
from mastapy._private.system_model.fe import _2605

_FE_PART_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "FEPartLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7704,
        _7706,
        _7799,
    )
    from mastapy._private.system_model.fe import _2580
    from mastapy._private.system_model.part_model import _2680

    Self = TypeVar("Self", bound="FEPartLoadCase")
    CastSelf = TypeVar("CastSelf", bound="FEPartLoadCase._Cast_FEPartLoadCase")


__docformat__ = "restructuredtext en"
__all__ = ("FEPartLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FEPartLoadCase:
    """Special nested class for casting FEPartLoadCase to subclasses."""

    __parent__: "FEPartLoadCase"

    @property
    def abstract_shaft_or_housing_load_case(
        self: "CastSelf",
    ) -> "_7677.AbstractShaftOrHousingLoadCase":
        return self.__parent__._cast(_7677.AbstractShaftOrHousingLoadCase)

    @property
    def component_load_case(self: "CastSelf") -> "_7706.ComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7706,
        )

        return self.__parent__._cast(_7706.ComponentLoadCase)

    @property
    def part_load_case(self: "CastSelf") -> "_7799.PartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7799,
        )

        return self.__parent__._cast(_7799.PartLoadCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2898.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2898

        return self.__parent__._cast(_2898.PartAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2894.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2894

        return self.__parent__._cast(_2894.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2892.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2892

        return self.__parent__._cast(_2892.DesignEntityAnalysis)

    @property
    def fe_part_load_case(self: "CastSelf") -> "FEPartLoadCase":
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
class FEPartLoadCase(_7677.AbstractShaftOrHousingLoadCase):
    """FEPartLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_PART_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def active_angle_index(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_int":
        """ListWithSelectedItem[int]"""
        temp = pythonnet_property_get(self.wrapped, "ActiveAngleIndex")

        if temp is None:
            return 0

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_int",
        )(temp)

    @active_angle_index.setter
    @exception_bridge
    @enforce_parameter_types
    def active_angle_index(self: "Self", value: "int") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_int.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "ActiveAngleIndex", value)

    @property
    @exception_bridge
    def angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Angle")

        if temp is None:
            return 0.0

        return temp

    @angle.setter
    @exception_bridge
    @enforce_parameter_types
    def angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Angle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def angle_source(self: "Self") -> "_2580.AngleSource":
        """mastapy.system_model.fe.AngleSource

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AngleSource")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.SystemModel.FE.AngleSource"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.fe._2580", "AngleSource"
        )(value)

    @property
    @exception_bridge
    def fe_substructure(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_FESubstructure":
        """ListWithSelectedItem[mastapy.system_model.fe.FESubstructure]"""
        temp = pythonnet_property_get(self.wrapped, "FESubstructure")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_FESubstructure",
        )(temp)

    @fe_substructure.setter
    @exception_bridge
    @enforce_parameter_types
    def fe_substructure(self: "Self", value: "_2605.FESubstructure") -> None:
        generic_type = (
            list_with_selected_item.ListWithSelectedItem_FESubstructure.implicit_type()
        )
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "FESubstructure", value)

    @property
    @exception_bridge
    def mass_scaling_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MassScalingFactor")

        if temp is None:
            return 0.0

        return temp

    @mass_scaling_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def mass_scaling_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MassScalingFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def override_default_fe_substructure(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "OverrideDefaultFESubstructure")

        if temp is None:
            return False

        return temp

    @override_default_fe_substructure.setter
    @exception_bridge
    @enforce_parameter_types
    def override_default_fe_substructure(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OverrideDefaultFESubstructure",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def stiffness_scaling_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StiffnessScalingFactor")

        if temp is None:
            return 0.0

        return temp

    @stiffness_scaling_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def stiffness_scaling_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StiffnessScalingFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2680.FEPart":
        """mastapy.system_model.part_model.FEPart

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def planetaries(self: "Self") -> "List[FEPartLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.FEPartLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Planetaries")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def surfaces_for_data_logging(
        self: "Self",
    ) -> "List[_7704.CMSElementFaceGroupWithSelectionOption]":
        """List[mastapy.system_model.analyses_and_results.static_loads.CMSElementFaceGroupWithSelectionOption]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SurfacesForDataLogging")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_FEPartLoadCase":
        """Cast to another type.

        Returns:
            _Cast_FEPartLoadCase
        """
        return _Cast_FEPartLoadCase(self)
