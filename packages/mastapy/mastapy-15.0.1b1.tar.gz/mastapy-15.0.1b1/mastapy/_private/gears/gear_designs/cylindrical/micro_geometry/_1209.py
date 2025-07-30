"""CylindricalGearLeadModification"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.micro_geometry import _663

_CYLINDRICAL_GEAR_LEAD_MODIFICATION = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry",
    "CylindricalGearLeadModification",
)

if TYPE_CHECKING:
    from typing import Any, Optional, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import (
        _1210,
        _1228,
    )
    from mastapy._private.gears.micro_geometry import _670
    from mastapy._private.utility_gui.charts import _2070

    Self = TypeVar("Self", bound="CylindricalGearLeadModification")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearLeadModification._Cast_CylindricalGearLeadModification",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearLeadModification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearLeadModification:
    """Special nested class for casting CylindricalGearLeadModification to subclasses."""

    __parent__: "CylindricalGearLeadModification"

    @property
    def lead_modification(self: "CastSelf") -> "_663.LeadModification":
        return self.__parent__._cast(_663.LeadModification)

    @property
    def modification(self: "CastSelf") -> "_670.Modification":
        from mastapy._private.gears.micro_geometry import _670

        return self.__parent__._cast(_670.Modification)

    @property
    def cylindrical_gear_lead_modification_at_profile_position(
        self: "CastSelf",
    ) -> "_1210.CylindricalGearLeadModificationAtProfilePosition":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1210

        return self.__parent__._cast(
            _1210.CylindricalGearLeadModificationAtProfilePosition
        )

    @property
    def cylindrical_gear_lead_modification(
        self: "CastSelf",
    ) -> "CylindricalGearLeadModification":
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
class CylindricalGearLeadModification(_663.LeadModification):
    """CylindricalGearLeadModification

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_LEAD_MODIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def evaluation_left_limit(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EvaluationLeftLimit")

        if temp is None:
            return 0.0

        return temp

    @evaluation_left_limit.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_left_limit(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationLeftLimit",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_of_linear_left_relief(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EvaluationOfLinearLeftRelief")

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_linear_left_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_of_linear_left_relief(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationOfLinearLeftRelief",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_of_linear_right_relief(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EvaluationOfLinearRightRelief")

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_linear_right_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_of_linear_right_relief(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationOfLinearRightRelief",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_of_parabolic_left_relief(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EvaluationOfParabolicLeftRelief")

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_parabolic_left_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_of_parabolic_left_relief(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationOfParabolicLeftRelief",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_of_parabolic_right_relief(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EvaluationOfParabolicRightRelief")

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_parabolic_right_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_of_parabolic_right_relief(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationOfParabolicRightRelief",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_right_limit(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EvaluationRightLimit")

        if temp is None:
            return 0.0

        return temp

    @evaluation_right_limit.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_right_limit(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationRightLimit",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_side_limit(self: "Self") -> "Optional[float]":
        """Optional[float]"""
        temp = pythonnet_property_get(self.wrapped, "EvaluationSideLimit")

        if temp is None:
            return None

        return temp

    @evaluation_side_limit.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_side_limit(self: "Self", value: "Optional[float]") -> None:
        pythonnet_property_set(self.wrapped, "EvaluationSideLimit", value)

    @property
    @exception_bridge
    def evaluation_of_linear_side_relief(self: "Self") -> "Optional[float]":
        """Optional[float]"""
        temp = pythonnet_property_get(self.wrapped, "EvaluationOfLinearSideRelief")

        if temp is None:
            return None

        return temp

    @evaluation_of_linear_side_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_of_linear_side_relief(
        self: "Self", value: "Optional[float]"
    ) -> None:
        pythonnet_property_set(self.wrapped, "EvaluationOfLinearSideRelief", value)

    @property
    @exception_bridge
    def evaluation_of_parabolic_side_relief(self: "Self") -> "Optional[float]":
        """Optional[float]"""
        temp = pythonnet_property_get(self.wrapped, "EvaluationOfParabolicSideRelief")

        if temp is None:
            return None

        return temp

    @evaluation_of_parabolic_side_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_of_parabolic_side_relief(
        self: "Self", value: "Optional[float]"
    ) -> None:
        pythonnet_property_set(self.wrapped, "EvaluationOfParabolicSideRelief", value)

    @property
    @exception_bridge
    def helix_angle_modification_at_original_reference_diameter(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "HelixAngleModificationAtOriginalReferenceDiameter"
        )

        if temp is None:
            return 0.0

        return temp

    @helix_angle_modification_at_original_reference_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def helix_angle_modification_at_original_reference_diameter(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "HelixAngleModificationAtOriginalReferenceDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def lead_modification_chart(self: "Self") -> "_2070.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeadModificationChart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def linear_relief_isodinagmavdi(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LinearReliefISODINAGMAVDI")

        if temp is None:
            return 0.0

        return temp

    @linear_relief_isodinagmavdi.setter
    @exception_bridge
    @enforce_parameter_types
    def linear_relief_isodinagmavdi(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LinearReliefISODINAGMAVDI",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def linear_relief_isodinagmavdi_across_full_face_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "LinearReliefISODINAGMAVDIAcrossFullFaceWidth"
        )

        if temp is None:
            return 0.0

        return temp

    @linear_relief_isodinagmavdi_across_full_face_width.setter
    @exception_bridge
    @enforce_parameter_types
    def linear_relief_isodinagmavdi_across_full_face_width(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "LinearReliefISODINAGMAVDIAcrossFullFaceWidth",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def linear_relief_ldp(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LinearReliefLDP")

        if temp is None:
            return 0.0

        return temp

    @linear_relief_ldp.setter
    @exception_bridge
    @enforce_parameter_types
    def linear_relief_ldp(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "LinearReliefLDP", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def linear_relief_ldp_across_full_face_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "LinearReliefLDPAcrossFullFaceWidth"
        )

        if temp is None:
            return 0.0

        return temp

    @linear_relief_ldp_across_full_face_width.setter
    @exception_bridge
    @enforce_parameter_types
    def linear_relief_ldp_across_full_face_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LinearReliefLDPAcrossFullFaceWidth",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def linear_relief_across_full_face_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LinearReliefAcrossFullFaceWidth")

        if temp is None:
            return 0.0

        return temp

    @linear_relief_across_full_face_width.setter
    @exception_bridge
    @enforce_parameter_types
    def linear_relief_across_full_face_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LinearReliefAcrossFullFaceWidth",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def modified_base_helix_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ModifiedBaseHelixAngle")

        if temp is None:
            return 0.0

        return temp

    @modified_base_helix_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def modified_base_helix_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ModifiedBaseHelixAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def modified_helix_angle_assuming_unmodified_normal_module(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ModifiedHelixAngleAssumingUnmodifiedNormalModule"
        )

        if temp is None:
            return 0.0

        return temp

    @modified_helix_angle_assuming_unmodified_normal_module.setter
    @exception_bridge
    @enforce_parameter_types
    def modified_helix_angle_assuming_unmodified_normal_module(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ModifiedHelixAngleAssumingUnmodifiedNormalModule",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def modified_helix_angle_at_original_reference_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ModifiedHelixAngleAtOriginalReferenceDiameter"
        )

        if temp is None:
            return 0.0

        return temp

    @modified_helix_angle_at_original_reference_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def modified_helix_angle_at_original_reference_diameter(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ModifiedHelixAngleAtOriginalReferenceDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def modified_normal_pressure_angle_due_to_helix_angle_modification_assuming_unmodified_normal_module(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "ModifiedNormalPressureAngleDueToHelixAngleModificationAssumingUnmodifiedNormalModule",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def modified_normal_pressure_angle_due_to_helix_angle_modification_at_original_reference_diameter(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "ModifiedNormalPressureAngleDueToHelixAngleModificationAtOriginalReferenceDiameter",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def start_of_linear_left_relief(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StartOfLinearLeftRelief")

        if temp is None:
            return 0.0

        return temp

    @start_of_linear_left_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def start_of_linear_left_relief(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StartOfLinearLeftRelief",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def start_of_linear_right_relief(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StartOfLinearRightRelief")

        if temp is None:
            return 0.0

        return temp

    @start_of_linear_right_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def start_of_linear_right_relief(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StartOfLinearRightRelief",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def start_of_linear_side_relief(self: "Self") -> "Optional[float]":
        """Optional[float]"""
        temp = pythonnet_property_get(self.wrapped, "StartOfLinearSideRelief")

        if temp is None:
            return None

        return temp

    @start_of_linear_side_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def start_of_linear_side_relief(self: "Self", value: "Optional[float]") -> None:
        pythonnet_property_set(self.wrapped, "StartOfLinearSideRelief", value)

    @property
    @exception_bridge
    def start_of_parabolic_left_relief(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StartOfParabolicLeftRelief")

        if temp is None:
            return 0.0

        return temp

    @start_of_parabolic_left_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def start_of_parabolic_left_relief(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StartOfParabolicLeftRelief",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def start_of_parabolic_right_relief(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StartOfParabolicRightRelief")

        if temp is None:
            return 0.0

        return temp

    @start_of_parabolic_right_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def start_of_parabolic_right_relief(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StartOfParabolicRightRelief",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def start_of_parabolic_side_relief(self: "Self") -> "Optional[float]":
        """Optional[float]"""
        temp = pythonnet_property_get(self.wrapped, "StartOfParabolicSideRelief")

        if temp is None:
            return None

        return temp

    @start_of_parabolic_side_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def start_of_parabolic_side_relief(self: "Self", value: "Optional[float]") -> None:
        pythonnet_property_set(self.wrapped, "StartOfParabolicSideRelief", value)

    @property
    @exception_bridge
    def use_measured_data(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseMeasuredData")

        if temp is None:
            return False

        return temp

    @use_measured_data.setter
    @exception_bridge
    @enforce_parameter_types
    def use_measured_data(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "UseMeasuredData", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def lead_modification_for_customer_102cad(
        self: "Self",
    ) -> "_1228.LeadModificationForCustomer102CAD":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.LeadModificationForCustomer102CAD

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeadModificationForCustomer102CAD")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    @enforce_parameter_types
    def relief_of(self: "Self", face_width: "float") -> "float":
        """float

        Args:
            face_width (float)
        """
        face_width = float(face_width)
        method_result = pythonnet_method_call(
            self.wrapped, "ReliefOf", face_width if face_width else 0.0
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearLeadModification":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearLeadModification
        """
        return _Cast_CylindricalGearLeadModification(self)
