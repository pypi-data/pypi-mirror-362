"""CylindricalMeshedGearLoadDistributionAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_method_call_overload,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_CONTACT_RESULT_TYPE = python_net_import("SMT.MastaAPI.Gears.LTCA", "ContactResultType")
_CYLINDRICAL_MESHED_GEAR_LOAD_DISTRIBUTION_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.LTCA", "CylindricalMeshedGearLoadDistributionAnalysis"
)
_BOOLEAN = python_net_import("System", "Boolean")
_INT_32 = python_net_import("System", "Int32")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.cylindrical import _1328, _1329, _1330, _1331
    from mastapy._private.gears.ltca import _930
    from mastapy._private.gears.ltca.cylindrical import _959
    from mastapy._private.math_utility import _1699

    Self = TypeVar("Self", bound="CylindricalMeshedGearLoadDistributionAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalMeshedGearLoadDistributionAnalysis._Cast_CylindricalMeshedGearLoadDistributionAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalMeshedGearLoadDistributionAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalMeshedGearLoadDistributionAnalysis:
    """Special nested class for casting CylindricalMeshedGearLoadDistributionAnalysis to subclasses."""

    __parent__: "CylindricalMeshedGearLoadDistributionAnalysis"

    @property
    def cylindrical_meshed_gear_load_distribution_analysis(
        self: "CastSelf",
    ) -> "CylindricalMeshedGearLoadDistributionAnalysis":
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
class CylindricalMeshedGearLoadDistributionAnalysis(_0.APIBase):
    """CylindricalMeshedGearLoadDistributionAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_MESHED_GEAR_LOAD_DISTRIBUTION_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def contact_patch_left_and_right_edge_loading_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ContactPatchLeftAndRightEdgeLoadingFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_patch_offset_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactPatchOffsetFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_patch_tip_and_root_loading_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ContactPatchTipAndRootLoadingFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def extended_edge_loading_factor_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExtendedEdgeLoadingFactorLeft")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def extended_edge_loading_factor_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExtendedEdgeLoadingFactorRight")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def extended_edge_loading_factor_root(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExtendedEdgeLoadingFactorRoot")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def extended_edge_loading_factor_tip(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExtendedEdgeLoadingFactorTip")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def is_loaded_on_tip(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsLoadedOnTip")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def maximum_principal_root_stress_compression(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumPrincipalRootStressCompression"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_principal_root_stress_tension(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumPrincipalRootStressTension")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_von_mises_root_stress_compression(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumVonMisesRootStressCompression"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_von_mises_root_stress_tension(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumVonMisesRootStressTension")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def nominal_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def percentage_of_effective_face_width_utilized(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PercentageOfEffectiveFaceWidthUtilized"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def percentage_of_effective_profile_utilized(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PercentageOfEffectiveProfileUtilized"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def percentage_of_potential_contact_area_loaded(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PercentageOfPotentialContactAreaLoaded"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def percentage_of_potential_contact_area_utilized(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PercentageOfPotentialContactAreaUtilized"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def torque_scaled_by_application_and_dynamic_factors(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TorqueScaledByApplicationAndDynamicFactors"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_load_distribution_analysis(
        self: "Self",
    ) -> "_959.CylindricalGearLoadDistributionAnalysis":
        """mastapy.gears.ltca.cylindrical.CylindricalGearLoadDistributionAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearLoadDistributionAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def other_gear_load_distribution_analysis(
        self: "Self",
    ) -> "_959.CylindricalGearLoadDistributionAnalysis":
        """mastapy.gears.ltca.cylindrical.CylindricalGearLoadDistributionAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OtherGearLoadDistributionAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def worst_contact_charts(
        self: "Self",
    ) -> "_1331.CylindricalGearWorstLTCAContactCharts":
        """mastapy.gears.cylindrical.CylindricalGearWorstLTCAContactCharts

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WorstContactCharts")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def worst_contact_charts_as_text_files(
        self: "Self",
    ) -> "_1330.CylindricalGearWorstLTCAContactChartDataAsTextFile":
        """mastapy.gears.cylindrical.CylindricalGearWorstLTCAContactChartDataAsTextFile

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WorstContactChartsAsTextFiles")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def contact_charts(self: "Self") -> "List[_1329.CylindricalGearLTCAContactCharts]":
        """List[mastapy.gears.cylindrical.CylindricalGearLTCAContactCharts]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactCharts")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def contact_charts_as_text_files(
        self: "Self",
    ) -> "List[_1328.CylindricalGearLTCAContactChartDataAsTextFile]":
        """List[mastapy.gears.cylindrical.CylindricalGearLTCAContactChartDataAsTextFile]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactChartsAsTextFiles")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    @enforce_parameter_types
    def contact_patch_as_text(
        self: "Self",
        result_type: "_930.ContactResultType",
        include_tip_contact: "bool",
        file_name_with_path: "str",
        start_rotation_index: "int" = 0,
    ) -> None:
        """Method does not return.

        Args:
            result_type (mastapy.gears.ltca.ContactResultType)
            include_tip_contact (bool)
            file_name_with_path (str)
            start_rotation_index (int, optional)
        """
        result_type = conversion.mp_to_pn_enum(
            result_type, "SMT.MastaAPI.Gears.LTCA.ContactResultType"
        )
        include_tip_contact = bool(include_tip_contact)
        file_name_with_path = str(file_name_with_path)
        start_rotation_index = int(start_rotation_index)
        pythonnet_method_call(
            self.wrapped,
            "ContactPatchAsText",
            result_type,
            include_tip_contact if include_tip_contact else False,
            file_name_with_path if file_name_with_path else "",
            start_rotation_index if start_rotation_index else 0,
        )

    @exception_bridge
    @enforce_parameter_types
    def contact_patch(
        self: "Self",
        result_type: "_930.ContactResultType",
        include_tip_contact: "bool",
        start_rotation_index: "int" = 0,
    ) -> "_1699.GriddedSurface":
        """mastapy.math_utility.GriddedSurface

        Args:
            result_type (mastapy.gears.ltca.ContactResultType)
            include_tip_contact (bool)
            start_rotation_index (int, optional)
        """
        result_type = conversion.mp_to_pn_enum(
            result_type, "SMT.MastaAPI.Gears.LTCA.ContactResultType"
        )
        include_tip_contact = bool(include_tip_contact)
        start_rotation_index = int(start_rotation_index)
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ContactPatch",
            [_CONTACT_RESULT_TYPE, _BOOLEAN, _INT_32],
            result_type,
            include_tip_contact if include_tip_contact else False,
            start_rotation_index if start_rotation_index else 0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def contact_patch_detailed(
        self: "Self",
        result_type: "_930.ContactResultType",
        number_of_face_width_steps: "int",
        number_of_roll_distance_steps: "int",
        start_rotation_index: "int" = 0,
    ) -> "_1699.GriddedSurface":
        """mastapy.math_utility.GriddedSurface

        Args:
            result_type (mastapy.gears.ltca.ContactResultType)
            number_of_face_width_steps (int)
            number_of_roll_distance_steps (int)
            start_rotation_index (int, optional)
        """
        result_type = conversion.mp_to_pn_enum(
            result_type, "SMT.MastaAPI.Gears.LTCA.ContactResultType"
        )
        number_of_face_width_steps = int(number_of_face_width_steps)
        number_of_roll_distance_steps = int(number_of_roll_distance_steps)
        start_rotation_index = int(start_rotation_index)
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ContactPatch",
            [_CONTACT_RESULT_TYPE, _INT_32, _INT_32, _INT_32],
            result_type,
            number_of_face_width_steps if number_of_face_width_steps else 0,
            number_of_roll_distance_steps if number_of_roll_distance_steps else 0,
            start_rotation_index if start_rotation_index else 0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalMeshedGearLoadDistributionAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CylindricalMeshedGearLoadDistributionAnalysis
        """
        return _Cast_CylindricalMeshedGearLoadDistributionAnalysis(self)
