"""CycloidalDiscModificationsSpecification"""

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
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_CYCLOIDAL_DISC_MODIFICATIONS_SPECIFICATION = python_net_import(
    "SMT.MastaAPI.Cycloidal", "CycloidalDiscModificationsSpecification"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.cycloidal import _1637, _1644
    from mastapy._private.math_utility import _1718

    Self = TypeVar("Self", bound="CycloidalDiscModificationsSpecification")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CycloidalDiscModificationsSpecification._Cast_CycloidalDiscModificationsSpecification",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CycloidalDiscModificationsSpecification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CycloidalDiscModificationsSpecification:
    """Special nested class for casting CycloidalDiscModificationsSpecification to subclasses."""

    __parent__: "CycloidalDiscModificationsSpecification"

    @property
    def cycloidal_disc_modifications_specification(
        self: "CastSelf",
    ) -> "CycloidalDiscModificationsSpecification":
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
class CycloidalDiscModificationsSpecification(_0.APIBase):
    """CycloidalDiscModificationsSpecification

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYCLOIDAL_DISC_MODIFICATIONS_SPECIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def angular_offset_modification(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AngularOffsetModification")

        if temp is None:
            return 0.0

        return temp

    @angular_offset_modification.setter
    @exception_bridge
    @enforce_parameter_types
    def angular_offset_modification(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AngularOffsetModification",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def coefficient_for_logarithmic_modification_along_the_face_width(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "CoefficientForLogarithmicModificationAlongTheFaceWidth"
        )

        if temp is None:
            return 0.0

        return temp

    @coefficient_for_logarithmic_modification_along_the_face_width.setter
    @exception_bridge
    @enforce_parameter_types
    def coefficient_for_logarithmic_modification_along_the_face_width(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "CoefficientForLogarithmicModificationAlongTheFaceWidth",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def crowning_radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CrowningRadius")

        if temp is None:
            return 0.0

        return temp

    @crowning_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def crowning_radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "CrowningRadius", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def crowning_specification_method(
        self: "Self",
    ) -> "_1637.CrowningSpecificationMethod":
        """mastapy.cycloidal.CrowningSpecificationMethod"""
        temp = pythonnet_property_get(self.wrapped, "CrowningSpecificationMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Cycloidal.CrowningSpecificationMethod"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.cycloidal._1637", "CrowningSpecificationMethod"
        )(value)

    @crowning_specification_method.setter
    @exception_bridge
    @enforce_parameter_types
    def crowning_specification_method(
        self: "Self", value: "_1637.CrowningSpecificationMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Cycloidal.CrowningSpecificationMethod"
        )
        pythonnet_property_set(self.wrapped, "CrowningSpecificationMethod", value)

    @property
    @exception_bridge
    def direction_of_measured_modifications(
        self: "Self",
    ) -> "_1644.DirectionOfMeasuredModifications":
        """mastapy.cycloidal.DirectionOfMeasuredModifications"""
        temp = pythonnet_property_get(self.wrapped, "DirectionOfMeasuredModifications")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Cycloidal.DirectionOfMeasuredModifications"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.cycloidal._1644", "DirectionOfMeasuredModifications"
        )(value)

    @direction_of_measured_modifications.setter
    @exception_bridge
    @enforce_parameter_types
    def direction_of_measured_modifications(
        self: "Self", value: "_1644.DirectionOfMeasuredModifications"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Cycloidal.DirectionOfMeasuredModifications"
        )
        pythonnet_property_set(self.wrapped, "DirectionOfMeasuredModifications", value)

    @property
    @exception_bridge
    def distance_to_where_crowning_starts_from_lobe_centre(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "DistanceToWhereCrowningStartsFromLobeCentre"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @distance_to_where_crowning_starts_from_lobe_centre.setter
    @exception_bridge
    @enforce_parameter_types
    def distance_to_where_crowning_starts_from_lobe_centre(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "DistanceToWhereCrowningStartsFromLobeCentre", value
        )

    @property
    @exception_bridge
    def generating_wheel_centre_circle_diameter_modification(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "GeneratingWheelCentreCircleDiameterModification"
        )

        if temp is None:
            return 0.0

        return temp

    @generating_wheel_centre_circle_diameter_modification.setter
    @exception_bridge
    @enforce_parameter_types
    def generating_wheel_centre_circle_diameter_modification(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "GeneratingWheelCentreCircleDiameterModification",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def generating_wheel_diameter_modification(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "GeneratingWheelDiameterModification"
        )

        if temp is None:
            return 0.0

        return temp

    @generating_wheel_diameter_modification.setter
    @exception_bridge
    @enforce_parameter_types
    def generating_wheel_diameter_modification(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "GeneratingWheelDiameterModification",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def measured_profile_modification(self: "Self") -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "MeasuredProfileModification")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @measured_profile_modification.setter
    @exception_bridge
    @enforce_parameter_types
    def measured_profile_modification(
        self: "Self", value: "_1718.Vector2DListAccessor"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "MeasuredProfileModification", value.wrapped
        )

    @property
    @exception_bridge
    def specify_measured_profile_modification(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "SpecifyMeasuredProfileModification"
        )

        if temp is None:
            return False

        return temp

    @specify_measured_profile_modification.setter
    @exception_bridge
    @enforce_parameter_types
    def specify_measured_profile_modification(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifyMeasuredProfileModification",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CycloidalDiscModificationsSpecification":
        """Cast to another type.

        Returns:
            _Cast_CycloidalDiscModificationsSpecification
        """
        return _Cast_CycloidalDiscModificationsSpecification(self)
