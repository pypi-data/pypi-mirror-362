"""DegreeOfFreedomBoundaryConditionLinear"""

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
from mastapy._private.system_model.fe import _2592

_DEGREE_OF_FREEDOM_BOUNDARY_CONDITION_LINEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "DegreeOfFreedomBoundaryConditionLinear"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    Self = TypeVar("Self", bound="DegreeOfFreedomBoundaryConditionLinear")
    CastSelf = TypeVar(
        "CastSelf",
        bound="DegreeOfFreedomBoundaryConditionLinear._Cast_DegreeOfFreedomBoundaryConditionLinear",
    )


__docformat__ = "restructuredtext en"
__all__ = ("DegreeOfFreedomBoundaryConditionLinear",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DegreeOfFreedomBoundaryConditionLinear:
    """Special nested class for casting DegreeOfFreedomBoundaryConditionLinear to subclasses."""

    __parent__: "DegreeOfFreedomBoundaryConditionLinear"

    @property
    def degree_of_freedom_boundary_condition(
        self: "CastSelf",
    ) -> "_2592.DegreeOfFreedomBoundaryCondition":
        return self.__parent__._cast(_2592.DegreeOfFreedomBoundaryCondition)

    @property
    def degree_of_freedom_boundary_condition_linear(
        self: "CastSelf",
    ) -> "DegreeOfFreedomBoundaryConditionLinear":
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
class DegreeOfFreedomBoundaryConditionLinear(_2592.DegreeOfFreedomBoundaryCondition):
    """DegreeOfFreedomBoundaryConditionLinear

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DEGREE_OF_FREEDOM_BOUNDARY_CONDITION_LINEAR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def displacement(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Displacement")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @displacement.setter
    @exception_bridge
    @enforce_parameter_types
    def displacement(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Displacement", value)

    @property
    @exception_bridge
    def force(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Force")

        if temp is None:
            return 0.0

        return temp

    @force.setter
    @exception_bridge
    @enforce_parameter_types
    def force(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Force", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_DegreeOfFreedomBoundaryConditionLinear":
        """Cast to another type.

        Returns:
            _Cast_DegreeOfFreedomBoundaryConditionLinear
        """
        return _Cast_DegreeOfFreedomBoundaryConditionLinear(self)
