"""FitAndTolerance"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import (
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import enum_with_selected_value
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.detailed_rigid_connectors.splines import _1597, _1603

_FIT_AND_TOLERANCE = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines.TolerancesAndDeviations",
    "FitAndTolerance",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FitAndTolerance")
    CastSelf = TypeVar("CastSelf", bound="FitAndTolerance._Cast_FitAndTolerance")


__docformat__ = "restructuredtext en"
__all__ = ("FitAndTolerance",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FitAndTolerance:
    """Special nested class for casting FitAndTolerance to subclasses."""

    __parent__: "FitAndTolerance"

    @property
    def fit_and_tolerance(self: "CastSelf") -> "FitAndTolerance":
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
class FitAndTolerance(_0.APIBase):
    """FitAndTolerance

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FIT_AND_TOLERANCE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def fit_class(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_SplineFitClassType":
        """EnumWithSelectedValue[mastapy.detailed_rigid_connectors.splines.SplineFitClassType]"""
        temp = pythonnet_property_get(self.wrapped, "FitClass")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_SplineFitClassType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @fit_class.setter
    @exception_bridge
    @enforce_parameter_types
    def fit_class(self: "Self", value: "_1597.SplineFitClassType") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_SplineFitClassType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "FitClass", value)

    @property
    @exception_bridge
    def tolerance_class(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_SplineToleranceClassTypes":
        """EnumWithSelectedValue[mastapy.detailed_rigid_connectors.splines.SplineToleranceClassTypes]"""
        temp = pythonnet_property_get(self.wrapped, "ToleranceClass")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_SplineToleranceClassTypes.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @tolerance_class.setter
    @exception_bridge
    @enforce_parameter_types
    def tolerance_class(self: "Self", value: "_1603.SplineToleranceClassTypes") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_SplineToleranceClassTypes.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ToleranceClass", value)

    @property
    def cast_to(self: "Self") -> "_Cast_FitAndTolerance":
        """Cast to another type.

        Returns:
            _Cast_FitAndTolerance
        """
        return _Cast_FitAndTolerance(self)
