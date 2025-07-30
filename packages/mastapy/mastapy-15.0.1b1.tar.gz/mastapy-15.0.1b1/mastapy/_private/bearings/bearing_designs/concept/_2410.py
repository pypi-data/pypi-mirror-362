"""ConceptRadialClearanceBearing"""

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
    pythonnet_property_get_with_method,
    pythonnet_property_set,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings.bearing_designs.concept import _2409

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_CONCEPT_RADIAL_CLEARANCE_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Concept", "ConceptRadialClearanceBearing"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.bearings import _2080
    from mastapy._private.bearings.bearing_designs import _2340, _2344

    Self = TypeVar("Self", bound="ConceptRadialClearanceBearing")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConceptRadialClearanceBearing._Cast_ConceptRadialClearanceBearing",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConceptRadialClearanceBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConceptRadialClearanceBearing:
    """Special nested class for casting ConceptRadialClearanceBearing to subclasses."""

    __parent__: "ConceptRadialClearanceBearing"

    @property
    def concept_clearance_bearing(self: "CastSelf") -> "_2409.ConceptClearanceBearing":
        return self.__parent__._cast(_2409.ConceptClearanceBearing)

    @property
    def non_linear_bearing(self: "CastSelf") -> "_2344.NonLinearBearing":
        from mastapy._private.bearings.bearing_designs import _2344

        return self.__parent__._cast(_2344.NonLinearBearing)

    @property
    def bearing_design(self: "CastSelf") -> "_2340.BearingDesign":
        from mastapy._private.bearings.bearing_designs import _2340

        return self.__parent__._cast(_2340.BearingDesign)

    @property
    def concept_radial_clearance_bearing(
        self: "CastSelf",
    ) -> "ConceptRadialClearanceBearing":
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
class ConceptRadialClearanceBearing(_2409.ConceptClearanceBearing):
    """ConceptRadialClearanceBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONCEPT_RADIAL_CLEARANCE_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def bore(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Bore")

        if temp is None:
            return 0.0

        return temp

    @bore.setter
    @exception_bridge
    @enforce_parameter_types
    def bore(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Bore", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def contact_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ContactAngle")

        if temp is None:
            return 0.0

        return temp

    @contact_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def contact_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ContactAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def contact_diameter_derived_from_connection_geometry(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "ContactDiameterDerivedFromConnectionGeometry"
        )

        if temp is None:
            return False

        return temp

    @contact_diameter_derived_from_connection_geometry.setter
    @exception_bridge
    @enforce_parameter_types
    def contact_diameter_derived_from_connection_geometry(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ContactDiameterDerivedFromConnectionGeometry",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def end_angle(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "EndAngle")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @end_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def end_angle(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "EndAngle", value)

    @property
    @exception_bridge
    def has_stiffness_only_in_eccentricity_direction(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "HasStiffnessOnlyInEccentricityDirection"
        )

        if temp is None:
            return False

        return temp

    @has_stiffness_only_in_eccentricity_direction.setter
    @exception_bridge
    @enforce_parameter_types
    def has_stiffness_only_in_eccentricity_direction(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "HasStiffnessOnlyInEccentricityDirection",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def inner_component_material_selector(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "InnerComponentMaterialSelector", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @inner_component_material_selector.setter
    @exception_bridge
    @enforce_parameter_types
    def inner_component_material_selector(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "InnerComponentMaterialSelector",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def model(self: "Self") -> "_2080.BearingModel":
        """mastapy.bearings.BearingModel

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Model")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Bearings.BearingModel")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings._2080", "BearingModel"
        )(value)

    @property
    @exception_bridge
    def outer_component_material_selector(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "OuterComponentMaterialSelector", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @outer_component_material_selector.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_component_material_selector(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "OuterComponentMaterialSelector",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def outer_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterDiameter")

        if temp is None:
            return 0.0

        return temp

    @outer_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "OuterDiameter", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def start_angle(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "StartAngle")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @start_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def start_angle(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "StartAngle", value)

    @property
    def cast_to(self: "Self") -> "_Cast_ConceptRadialClearanceBearing":
        """Cast to another type.

        Returns:
            _Cast_ConceptRadialClearanceBearing
        """
        return _Cast_ConceptRadialClearanceBearing(self)
