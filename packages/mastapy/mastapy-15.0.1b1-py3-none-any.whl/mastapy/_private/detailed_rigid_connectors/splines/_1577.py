"""DIN5480SplineHalfDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.detailed_rigid_connectors.splines import _1604

_DIN5480_SPLINE_HALF_DESIGN = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines", "DIN5480SplineHalfDesign"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.detailed_rigid_connectors import _1573
    from mastapy._private.detailed_rigid_connectors.splines import _1587, _1596, _1599

    Self = TypeVar("Self", bound="DIN5480SplineHalfDesign")
    CastSelf = TypeVar(
        "CastSelf", bound="DIN5480SplineHalfDesign._Cast_DIN5480SplineHalfDesign"
    )


__docformat__ = "restructuredtext en"
__all__ = ("DIN5480SplineHalfDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DIN5480SplineHalfDesign:
    """Special nested class for casting DIN5480SplineHalfDesign to subclasses."""

    __parent__: "DIN5480SplineHalfDesign"

    @property
    def standard_spline_half_design(
        self: "CastSelf",
    ) -> "_1604.StandardSplineHalfDesign":
        return self.__parent__._cast(_1604.StandardSplineHalfDesign)

    @property
    def spline_half_design(self: "CastSelf") -> "_1599.SplineHalfDesign":
        from mastapy._private.detailed_rigid_connectors.splines import _1599

        return self.__parent__._cast(_1599.SplineHalfDesign)

    @property
    def detailed_rigid_connector_half_design(
        self: "CastSelf",
    ) -> "_1573.DetailedRigidConnectorHalfDesign":
        from mastapy._private.detailed_rigid_connectors import _1573

        return self.__parent__._cast(_1573.DetailedRigidConnectorHalfDesign)

    @property
    def din5480_spline_half_design(self: "CastSelf") -> "DIN5480SplineHalfDesign":
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
class DIN5480SplineHalfDesign(_1604.StandardSplineHalfDesign):
    """DIN5480SplineHalfDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DIN5480_SPLINE_HALF_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def addendum_modification(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AddendumModification")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def addendum_of_basic_rack(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AddendumOfBasicRack")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def base_form_circle_diameter_limit(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BaseFormCircleDiameterLimit")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def basic_rack_addendum_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasicRackAddendumFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def basic_rack_dedendum_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasicRackDedendumFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def bottom_clearance_of_basic_rack(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BottomClearanceOfBasicRack")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def dedendum_of_basic_rack(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DedendumOfBasicRack")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def finishing_method(self: "Self") -> "_1596.FinishingMethods":
        """mastapy.detailed_rigid_connectors.splines.FinishingMethods"""
        temp = pythonnet_property_get(self.wrapped, "FinishingMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.DetailedRigidConnectors.Splines.FinishingMethods"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.detailed_rigid_connectors.splines._1596",
            "FinishingMethods",
        )(value)

    @finishing_method.setter
    @exception_bridge
    @enforce_parameter_types
    def finishing_method(self: "Self", value: "_1596.FinishingMethods") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.DetailedRigidConnectors.Splines.FinishingMethods"
        )
        pythonnet_property_set(self.wrapped, "FinishingMethod", value)

    @property
    @exception_bridge
    def form_clearance_of_basic_rack(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FormClearanceOfBasicRack")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def manufacturing_type(self: "Self") -> "_1587.ManufacturingTypes":
        """mastapy.detailed_rigid_connectors.splines.ManufacturingTypes"""
        temp = pythonnet_property_get(self.wrapped, "ManufacturingType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.DetailedRigidConnectors.Splines.ManufacturingTypes"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.detailed_rigid_connectors.splines._1587",
            "ManufacturingTypes",
        )(value)

    @manufacturing_type.setter
    @exception_bridge
    @enforce_parameter_types
    def manufacturing_type(self: "Self", value: "_1587.ManufacturingTypes") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.DetailedRigidConnectors.Splines.ManufacturingTypes"
        )
        pythonnet_property_set(self.wrapped, "ManufacturingType", value)

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
    def maximum_effective_root_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumEffectiveRootDiameter")

        if temp is None:
            return 0.0

        return temp

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
    def minimum_effective_root_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumEffectiveRootDiameter")

        if temp is None:
            return 0.0

        return temp

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
    def root_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RootDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def root_fillet_radius_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RootFilletRadiusFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tip_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TipDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tooth_height_of_basic_rack(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothHeightOfBasicRack")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_DIN5480SplineHalfDesign":
        """Cast to another type.

        Returns:
            _Cast_DIN5480SplineHalfDesign
        """
        return _Cast_DIN5480SplineHalfDesign(self)
