"""RoundnessSpecification"""

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
from mastapy._private.utility import _1779

_ROUNDNESS_SPECIFICATION = python_net_import(
    "SMT.MastaAPI.Bearings.Tolerances", "RoundnessSpecification"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.bearings.tolerances import _2117, _2122, _2128
    from mastapy._private.math_utility import _1718

    Self = TypeVar("Self", bound="RoundnessSpecification")
    CastSelf = TypeVar(
        "CastSelf", bound="RoundnessSpecification._Cast_RoundnessSpecification"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RoundnessSpecification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RoundnessSpecification:
    """Special nested class for casting RoundnessSpecification to subclasses."""

    __parent__: "RoundnessSpecification"

    @property
    def independent_reportable_properties_base(
        self: "CastSelf",
    ) -> "_1779.IndependentReportablePropertiesBase":
        pass

        return self.__parent__._cast(_1779.IndependentReportablePropertiesBase)

    @property
    def roundness_specification(self: "CastSelf") -> "RoundnessSpecification":
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
class RoundnessSpecification(
    _1779.IndependentReportablePropertiesBase["RoundnessSpecification"]
):
    """RoundnessSpecification

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROUNDNESS_SPECIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def angle_of_first_max_deviation_from_round(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AngleOfFirstMaxDeviationFromRound")

        if temp is None:
            return 0.0

        return temp

    @angle_of_first_max_deviation_from_round.setter
    @exception_bridge
    @enforce_parameter_types
    def angle_of_first_max_deviation_from_round(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AngleOfFirstMaxDeviationFromRound",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def maximum_deviation_from_round(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumDeviationFromRound")

        if temp is None:
            return 0.0

        return temp

    @maximum_deviation_from_round.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_deviation_from_round(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumDeviationFromRound",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def number_of_lobes(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfLobes")

        if temp is None:
            return 0

        return temp

    @number_of_lobes.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_lobes(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfLobes", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def specification_type(self: "Self") -> "_2122.RoundnessSpecificationType":
        """mastapy.bearings.tolerances.RoundnessSpecificationType"""
        temp = pythonnet_property_get(self.wrapped, "SpecificationType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.Tolerances.RoundnessSpecificationType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings.tolerances._2122", "RoundnessSpecificationType"
        )(value)

    @specification_type.setter
    @exception_bridge
    @enforce_parameter_types
    def specification_type(
        self: "Self", value: "_2122.RoundnessSpecificationType"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Bearings.Tolerances.RoundnessSpecificationType"
        )
        pythonnet_property_set(self.wrapped, "SpecificationType", value)

    @property
    @exception_bridge
    def type_of_fit(self: "Self") -> "_2128.TypeOfFit":
        """mastapy.bearings.tolerances.TypeOfFit"""
        temp = pythonnet_property_get(self.wrapped, "TypeOfFit")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.Tolerances.TypeOfFit"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings.tolerances._2128", "TypeOfFit"
        )(value)

    @type_of_fit.setter
    @exception_bridge
    @enforce_parameter_types
    def type_of_fit(self: "Self", value: "_2128.TypeOfFit") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Bearings.Tolerances.TypeOfFit"
        )
        pythonnet_property_set(self.wrapped, "TypeOfFit", value)

    @property
    @exception_bridge
    def user_specified_deviation(self: "Self") -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "UserSpecifiedDeviation")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @user_specified_deviation.setter
    @exception_bridge
    @enforce_parameter_types
    def user_specified_deviation(
        self: "Self", value: "_1718.Vector2DListAccessor"
    ) -> None:
        pythonnet_property_set(self.wrapped, "UserSpecifiedDeviation", value.wrapped)

    @property
    @exception_bridge
    def roundness_distribution(self: "Self") -> "List[_2117.RaceRoundnessAtAngle]":
        """List[mastapy.bearings.tolerances.RaceRoundnessAtAngle]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RoundnessDistribution")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_RoundnessSpecification":
        """Cast to another type.

        Returns:
            _Cast_RoundnessSpecification
        """
        return _Cast_RoundnessSpecification(self)
