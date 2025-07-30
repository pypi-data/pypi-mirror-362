"""LoadCaseConstraint"""

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
from mastapy._private.system_model.optimization.machine_learning import _2459

_LOAD_CASE_CONSTRAINT = python_net_import(
    "SMT.MastaAPI.SystemModel.Optimization.MachineLearning", "LoadCaseConstraint"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    Self = TypeVar("Self", bound="LoadCaseConstraint")
    CastSelf = TypeVar("CastSelf", bound="LoadCaseConstraint._Cast_LoadCaseConstraint")


__docformat__ = "restructuredtext en"
__all__ = ("LoadCaseConstraint",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadCaseConstraint:
    """Special nested class for casting LoadCaseConstraint to subclasses."""

    __parent__: "LoadCaseConstraint"

    @property
    def load_case_settings(self: "CastSelf") -> "_2459.LoadCaseSettings":
        return self.__parent__._cast(_2459.LoadCaseSettings)

    @property
    def load_case_constraint(self: "CastSelf") -> "LoadCaseConstraint":
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
class LoadCaseConstraint(_2459.LoadCaseSettings):
    """LoadCaseConstraint

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOAD_CASE_CONSTRAINT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def maximum(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Maximum")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @maximum.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Maximum", value)

    @property
    @exception_bridge
    def minimum(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Minimum")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @minimum.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Minimum", value)

    @property
    def cast_to(self: "Self") -> "_Cast_LoadCaseConstraint":
        """Cast to another type.

        Returns:
            _Cast_LoadCaseConstraint
        """
        return _Cast_LoadCaseConstraint(self)
