"""ParametricStudyToolStepResult"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
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

_PARAMETRIC_STUDY_TOOL_STEP_RESULT = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "ParametricStudyToolStepResult",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ParametricStudyToolStepResult")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ParametricStudyToolStepResult._Cast_ParametricStudyToolStepResult",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ParametricStudyToolStepResult",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ParametricStudyToolStepResult:
    """Special nested class for casting ParametricStudyToolStepResult to subclasses."""

    __parent__: "ParametricStudyToolStepResult"

    @property
    def parametric_study_tool_step_result(
        self: "CastSelf",
    ) -> "ParametricStudyToolStepResult":
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
class ParametricStudyToolStepResult(_0.APIBase):
    """ParametricStudyToolStepResult

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PARAMETRIC_STUDY_TOOL_STEP_RESULT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def failure_message(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "FailureMessage")

        if temp is None:
            return ""

        return temp

    @failure_message.setter
    @exception_bridge
    @enforce_parameter_types
    def failure_message(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "FailureMessage", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @name.setter
    @exception_bridge
    @enforce_parameter_types
    def name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Name", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def successful(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "Successful")

        if temp is None:
            return False

        return temp

    @successful.setter
    @exception_bridge
    @enforce_parameter_types
    def successful(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "Successful", bool(value) if value is not None else False
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ParametricStudyToolStepResult":
        """Cast to another type.

        Returns:
            _Cast_ParametricStudyToolStepResult
        """
        return _Cast_ParametricStudyToolStepResult(self)
