"""SplineHalfDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

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
from mastapy._private.detailed_rigid_connectors import _1573

_SPLINE_HALF_DESIGN = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines", "SplineHalfDesign"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.detailed_rigid_connectors.splines import (
        _1574,
        _1577,
        _1581,
        _1583,
        _1584,
        _1592,
        _1600,
        _1604,
    )
    from mastapy._private.detailed_rigid_connectors.splines.tolerances_and_deviations import (
        _1606,
    )

    Self = TypeVar("Self", bound="SplineHalfDesign")
    CastSelf = TypeVar("CastSelf", bound="SplineHalfDesign._Cast_SplineHalfDesign")


__docformat__ = "restructuredtext en"
__all__ = ("SplineHalfDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SplineHalfDesign:
    """Special nested class for casting SplineHalfDesign to subclasses."""

    __parent__: "SplineHalfDesign"

    @property
    def detailed_rigid_connector_half_design(
        self: "CastSelf",
    ) -> "_1573.DetailedRigidConnectorHalfDesign":
        return self.__parent__._cast(_1573.DetailedRigidConnectorHalfDesign)

    @property
    def custom_spline_half_design(self: "CastSelf") -> "_1574.CustomSplineHalfDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1574

        return self.__parent__._cast(_1574.CustomSplineHalfDesign)

    @property
    def din5480_spline_half_design(self: "CastSelf") -> "_1577.DIN5480SplineHalfDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1577

        return self.__parent__._cast(_1577.DIN5480SplineHalfDesign)

    @property
    def gbt3478_spline_half_design(self: "CastSelf") -> "_1581.GBT3478SplineHalfDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1581

        return self.__parent__._cast(_1581.GBT3478SplineHalfDesign)

    @property
    def iso4156_spline_half_design(self: "CastSelf") -> "_1584.ISO4156SplineHalfDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1584

        return self.__parent__._cast(_1584.ISO4156SplineHalfDesign)

    @property
    def sae_spline_half_design(self: "CastSelf") -> "_1592.SAESplineHalfDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1592

        return self.__parent__._cast(_1592.SAESplineHalfDesign)

    @property
    def standard_spline_half_design(
        self: "CastSelf",
    ) -> "_1604.StandardSplineHalfDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1604

        return self.__parent__._cast(_1604.StandardSplineHalfDesign)

    @property
    def spline_half_design(self: "CastSelf") -> "SplineHalfDesign":
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
class SplineHalfDesign(_1573.DetailedRigidConnectorHalfDesign):
    """SplineHalfDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPLINE_HALF_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def allowable_bending_stress(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AllowableBendingStress")

        if temp is None:
            return 0.0

        return temp

    @allowable_bending_stress.setter
    @exception_bridge
    @enforce_parameter_types
    def allowable_bending_stress(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AllowableBendingStress",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def allowable_bursting_stress(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AllowableBurstingStress")

        if temp is None:
            return 0.0

        return temp

    @allowable_bursting_stress.setter
    @exception_bridge
    @enforce_parameter_types
    def allowable_bursting_stress(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AllowableBurstingStress",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def allowable_compressive_stress(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AllowableCompressiveStress")

        if temp is None:
            return 0.0

        return temp

    @allowable_compressive_stress.setter
    @exception_bridge
    @enforce_parameter_types
    def allowable_compressive_stress(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AllowableCompressiveStress",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def allowable_contact_stress(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AllowableContactStress")

        if temp is None:
            return 0.0

        return temp

    @allowable_contact_stress.setter
    @exception_bridge
    @enforce_parameter_types
    def allowable_contact_stress(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AllowableContactStress",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def allowable_shear_stress(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AllowableShearStress")

        if temp is None:
            return 0.0

        return temp

    @allowable_shear_stress.setter
    @exception_bridge
    @enforce_parameter_types
    def allowable_shear_stress(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AllowableShearStress",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def ball_or_pin_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "BallOrPinDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @ball_or_pin_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def ball_or_pin_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "BallOrPinDiameter", value)

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
    def core_hardness_h_rc(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CoreHardnessHRc")

        if temp is None:
            return 0.0

        return temp

    @core_hardness_h_rc.setter
    @exception_bridge
    @enforce_parameter_types
    def core_hardness_h_rc(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "CoreHardnessHRc", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def designation(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Designation")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def form_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FormDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def heat_treatment(self: "Self") -> "_1583.HeatTreatmentTypes":
        """mastapy.detailed_rigid_connectors.splines.HeatTreatmentTypes"""
        temp = pythonnet_property_get(self.wrapped, "HeatTreatment")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.DetailedRigidConnectors.Splines.HeatTreatmentTypes"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.detailed_rigid_connectors.splines._1583",
            "HeatTreatmentTypes",
        )(value)

    @heat_treatment.setter
    @exception_bridge
    @enforce_parameter_types
    def heat_treatment(self: "Self", value: "_1583.HeatTreatmentTypes") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.DetailedRigidConnectors.Splines.HeatTreatmentTypes"
        )
        pythonnet_property_set(self.wrapped, "HeatTreatment", value)

    @property
    @exception_bridge
    def major_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MajorDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_actual_space_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumActualSpaceWidth")

        if temp is None:
            return 0.0

        return temp

    @maximum_actual_space_width.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_actual_space_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumActualSpaceWidth",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def maximum_actual_tooth_thickness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumActualToothThickness")

        if temp is None:
            return 0.0

        return temp

    @maximum_actual_tooth_thickness.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_actual_tooth_thickness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumActualToothThickness",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def maximum_chordal_span_over_teeth(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumChordalSpanOverTeeth")

        if temp is None:
            return 0.0

        return temp

    @maximum_chordal_span_over_teeth.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_chordal_span_over_teeth(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumChordalSpanOverTeeth",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def maximum_dimension_over_balls(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumDimensionOverBalls")

        if temp is None:
            return 0.0

        return temp

    @maximum_dimension_over_balls.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_dimension_over_balls(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumDimensionOverBalls",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def maximum_effective_tooth_thickness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumEffectiveToothThickness")

        if temp is None:
            return 0.0

        return temp

    @maximum_effective_tooth_thickness.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_effective_tooth_thickness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumEffectiveToothThickness",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def maximum_major_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumMajorDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_minor_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumMinorDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_actual_space_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanActualSpaceWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_actual_tooth_thickness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanActualToothThickness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_actual_space_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MinimumActualSpaceWidth")

        if temp is None:
            return 0.0

        return temp

    @minimum_actual_space_width.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_actual_space_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumActualSpaceWidth",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def minimum_actual_tooth_thickness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MinimumActualToothThickness")

        if temp is None:
            return 0.0

        return temp

    @minimum_actual_tooth_thickness.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_actual_tooth_thickness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumActualToothThickness",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def minimum_chordal_span_over_teeth(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MinimumChordalSpanOverTeeth")

        if temp is None:
            return 0.0

        return temp

    @minimum_chordal_span_over_teeth.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_chordal_span_over_teeth(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumChordalSpanOverTeeth",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def minimum_dimension_over_balls(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MinimumDimensionOverBalls")

        if temp is None:
            return 0.0

        return temp

    @minimum_dimension_over_balls.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_dimension_over_balls(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumDimensionOverBalls",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def minimum_effective_space_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MinimumEffectiveSpaceWidth")

        if temp is None:
            return 0.0

        return temp

    @minimum_effective_space_width.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_effective_space_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumEffectiveSpaceWidth",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def minimum_major_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumMajorDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_minor_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumMinorDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minor_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinorDiameter")

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
    def nominal_chordal_span_over_teeth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalChordalSpanOverTeeth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def nominal_dimension_over_balls(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalDimensionOverBalls")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def number_of_teeth_for_chordal_span_test(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfTeethForChordalSpanTest")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @number_of_teeth_for_chordal_span_test.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_teeth_for_chordal_span_test(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "NumberOfTeethForChordalSpanTest", value)

    @property
    @exception_bridge
    def pointed_flank_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PointedFlankDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def root_fillet_radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RootFilletRadius")

        if temp is None:
            return 0.0

        return temp

    @root_fillet_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def root_fillet_radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RootFilletRadius", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def root_fillet_radius_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RootFilletRadiusFactor")

        if temp is None:
            return 0.0

        return temp

    @root_fillet_radius_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def root_fillet_radius_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RootFilletRadiusFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def surface_hardness_h_rc(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SurfaceHardnessHRc")

        if temp is None:
            return 0.0

        return temp

    @surface_hardness_h_rc.setter
    @exception_bridge
    @enforce_parameter_types
    def surface_hardness_h_rc(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SurfaceHardnessHRc",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def theoretical_dimension_over_balls(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TheoreticalDimensionOverBalls")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tooth_height(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothHeight")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def fit_and_tolerance(self: "Self") -> "_1606.FitAndTolerance":
        """mastapy.detailed_rigid_connectors.splines.tolerances_and_deviations.FitAndTolerance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FitAndTolerance")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def spline_joint_design(self: "Self") -> "_1600.SplineJointDesign":
        """mastapy.detailed_rigid_connectors.splines.SplineJointDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SplineJointDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_SplineHalfDesign":
        """Cast to another type.

        Returns:
            _Cast_SplineHalfDesign
        """
        return _Cast_SplineHalfDesign(self)
