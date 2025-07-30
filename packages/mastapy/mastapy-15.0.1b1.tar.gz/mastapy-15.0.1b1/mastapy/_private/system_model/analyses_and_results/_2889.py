"""AnalysisCaseVariable"""

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
)

_ANALYSIS_CASE_VARIABLE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults", "AnalysisCaseVariable"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4660,
    )

    Self = TypeVar("Self", bound="AnalysisCaseVariable")
    CastSelf = TypeVar(
        "CastSelf", bound="AnalysisCaseVariable._Cast_AnalysisCaseVariable"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AnalysisCaseVariable",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AnalysisCaseVariable:
    """Special nested class for casting AnalysisCaseVariable to subclasses."""

    __parent__: "AnalysisCaseVariable"

    @property
    def parametric_study_variable(self: "CastSelf") -> "_4660.ParametricStudyVariable":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4660,
        )

        return self.__parent__._cast(_4660.ParametricStudyVariable)

    @property
    def analysis_case_variable(self: "CastSelf") -> "AnalysisCaseVariable":
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
class AnalysisCaseVariable(_0.APIBase):
    """AnalysisCaseVariable

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ANALYSIS_CASE_VARIABLE

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
    def cast_to(self: "Self") -> "_Cast_AnalysisCaseVariable":
        """Cast to another type.

        Returns:
            _Cast_AnalysisCaseVariable
        """
        return _Cast_AnalysisCaseVariable(self)
