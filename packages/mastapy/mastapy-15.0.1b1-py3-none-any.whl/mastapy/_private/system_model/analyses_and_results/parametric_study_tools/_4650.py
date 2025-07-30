"""ParametricStudyChartVariable"""

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
from mastapy._private.math_utility.optimisation import _1738

_PARAMETRIC_STUDY_CHART_VARIABLE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "ParametricStudyChartVariable",
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.math_utility.optimisation import _1739

    Self = TypeVar("Self", bound="ParametricStudyChartVariable")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ParametricStudyChartVariable._Cast_ParametricStudyChartVariable",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ParametricStudyChartVariable",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ParametricStudyChartVariable:
    """Special nested class for casting ParametricStudyChartVariable to subclasses."""

    __parent__: "ParametricStudyChartVariable"

    @property
    def pareto_optimisation_variable_base(
        self: "CastSelf",
    ) -> "_1738.ParetoOptimisationVariableBase":
        return self.__parent__._cast(_1738.ParetoOptimisationVariableBase)

    @property
    def parametric_study_chart_variable(
        self: "CastSelf",
    ) -> "ParametricStudyChartVariable":
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
class ParametricStudyChartVariable(_1738.ParetoOptimisationVariableBase):
    """ParametricStudyChartVariable

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PARAMETRIC_STUDY_CHART_VARIABLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def entity_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EntityName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def max(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Max")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @max.setter
    @exception_bridge
    @enforce_parameter_types
    def max(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Max", value)

    @property
    @exception_bridge
    def min(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Min")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @min.setter
    @exception_bridge
    @enforce_parameter_types
    def min(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Min", value)

    @property
    @exception_bridge
    def parameter_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ParameterName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def target_for_dominant_candidate_search(
        self: "Self",
    ) -> "_1739.PropertyTargetForDominantCandidateSearch":
        """mastapy.math_utility.optimisation.PropertyTargetForDominantCandidateSearch"""
        temp = pythonnet_property_get(self.wrapped, "TargetForDominantCandidateSearch")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.MathUtility.Optimisation.PropertyTargetForDominantCandidateSearch",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.math_utility.optimisation._1739",
            "PropertyTargetForDominantCandidateSearch",
        )(value)

    @target_for_dominant_candidate_search.setter
    @exception_bridge
    @enforce_parameter_types
    def target_for_dominant_candidate_search(
        self: "Self", value: "_1739.PropertyTargetForDominantCandidateSearch"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.MathUtility.Optimisation.PropertyTargetForDominantCandidateSearch",
        )
        pythonnet_property_set(self.wrapped, "TargetForDominantCandidateSearch", value)

    @property
    def cast_to(self: "Self") -> "_Cast_ParametricStudyChartVariable":
        """Cast to another type.

        Returns:
            _Cast_ParametricStudyChartVariable
        """
        return _Cast_ParametricStudyChartVariable(self)
