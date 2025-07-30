"""CustomSplineHalfDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

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
from mastapy._private.detailed_rigid_connectors.splines import _1599

_CUSTOM_SPLINE_HALF_DESIGN = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines", "CustomSplineHalfDesign"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.detailed_rigid_connectors import _1573

    Self = TypeVar("Self", bound="CustomSplineHalfDesign")
    CastSelf = TypeVar(
        "CastSelf", bound="CustomSplineHalfDesign._Cast_CustomSplineHalfDesign"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CustomSplineHalfDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomSplineHalfDesign:
    """Special nested class for casting CustomSplineHalfDesign to subclasses."""

    __parent__: "CustomSplineHalfDesign"

    @property
    def spline_half_design(self: "CastSelf") -> "_1599.SplineHalfDesign":
        return self.__parent__._cast(_1599.SplineHalfDesign)

    @property
    def detailed_rigid_connector_half_design(
        self: "CastSelf",
    ) -> "_1573.DetailedRigidConnectorHalfDesign":
        from mastapy._private.detailed_rigid_connectors import _1573

        return self.__parent__._cast(_1573.DetailedRigidConnectorHalfDesign)

    @property
    def custom_spline_half_design(self: "CastSelf") -> "CustomSplineHalfDesign":
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
class CustomSplineHalfDesign(_1599.SplineHalfDesign):
    """CustomSplineHalfDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_SPLINE_HALF_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def actual_tooth_thickness_or_space_width_tolerance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ActualToothThicknessOrSpaceWidthTolerance"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def addendum_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AddendumFactor")

        if temp is None:
            return 0.0

        return temp

    @addendum_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def addendum_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "AddendumFactor", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def dedendum_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DedendumFactor")

        if temp is None:
            return 0.0

        return temp

    @dedendum_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def dedendum_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DedendumFactor", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def effective_tooth_thickness_or_space_width_tolerance(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "EffectiveToothThicknessOrSpaceWidthTolerance"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @effective_tooth_thickness_or_space_width_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def effective_tooth_thickness_or_space_width_tolerance(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "EffectiveToothThicknessOrSpaceWidthTolerance", value
        )

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
    def major_diameter_specified(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MajorDiameterSpecified")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @major_diameter_specified.setter
    @exception_bridge
    @enforce_parameter_types
    def major_diameter_specified(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MajorDiameterSpecified", value)

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
    def maximum_space_width_deviation(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumSpaceWidthDeviation")

        if temp is None:
            return 0.0

        return temp

    @maximum_space_width_deviation.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_space_width_deviation(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumSpaceWidthDeviation",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def maximum_tooth_thickness_deviation(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumToothThicknessDeviation")

        if temp is None:
            return 0.0

        return temp

    @maximum_tooth_thickness_deviation.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_tooth_thickness_deviation(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumToothThicknessDeviation",
            float(value) if value is not None else 0.0,
        )

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
    def minimum_space_width_deviation(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MinimumSpaceWidthDeviation")

        if temp is None:
            return 0.0

        return temp

    @minimum_space_width_deviation.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_space_width_deviation(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumSpaceWidthDeviation",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def minimum_tooth_thickness_deviation(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MinimumToothThicknessDeviation")

        if temp is None:
            return 0.0

        return temp

    @minimum_tooth_thickness_deviation.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_tooth_thickness_deviation(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumToothThicknessDeviation",
            float(value) if value is not None else 0.0,
        )

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
    def minor_diameter_specified(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MinorDiameterSpecified")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @minor_diameter_specified.setter
    @exception_bridge
    @enforce_parameter_types
    def minor_diameter_specified(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MinorDiameterSpecified", value)

    @property
    @exception_bridge
    def root_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RootDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @root_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def root_diameter(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RootDiameter", value)

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
    def tip_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "TipDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @tip_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def tip_diameter(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "TipDiameter", value)

    @property
    @exception_bridge
    def total_tooth_thickness_or_space_width_tolerance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "TotalToothThicknessOrSpaceWidthTolerance"
        )

        if temp is None:
            return 0.0

        return temp

    @total_tooth_thickness_or_space_width_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def total_tooth_thickness_or_space_width_tolerance(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "TotalToothThicknessOrSpaceWidthTolerance",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CustomSplineHalfDesign":
        """Cast to another type.

        Returns:
            _Cast_CustomSplineHalfDesign
        """
        return _Cast_CustomSplineHalfDesign(self)
