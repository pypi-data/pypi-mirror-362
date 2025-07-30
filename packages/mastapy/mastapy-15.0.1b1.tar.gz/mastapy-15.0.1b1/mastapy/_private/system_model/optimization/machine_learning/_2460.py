"""LoadCaseTarget"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.optimization.machine_learning import _2459

_LOAD_CASE_TARGET = python_net_import(
    "SMT.MastaAPI.SystemModel.Optimization.MachineLearning", "LoadCaseTarget"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="LoadCaseTarget")
    CastSelf = TypeVar("CastSelf", bound="LoadCaseTarget._Cast_LoadCaseTarget")


__docformat__ = "restructuredtext en"
__all__ = ("LoadCaseTarget",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadCaseTarget:
    """Special nested class for casting LoadCaseTarget to subclasses."""

    __parent__: "LoadCaseTarget"

    @property
    def load_case_settings(self: "CastSelf") -> "_2459.LoadCaseSettings":
        return self.__parent__._cast(_2459.LoadCaseSettings)

    @property
    def load_case_target(self: "CastSelf") -> "LoadCaseTarget":
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
class LoadCaseTarget(_2459.LoadCaseSettings):
    """LoadCaseTarget

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOAD_CASE_TARGET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def weighting(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Weighting")

        if temp is None:
            return 0.0

        return temp

    @weighting.setter
    @exception_bridge
    @enforce_parameter_types
    def weighting(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Weighting", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_LoadCaseTarget":
        """Cast to another type.

        Returns:
            _Cast_LoadCaseTarget
        """
        return _Cast_LoadCaseTarget(self)
