"""FEModelStaticAnalysisDrawStyle"""

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
from mastapy._private.nodal_analysis.dev_tools_analyses import _277

_FE_MODEL_STATIC_ANALYSIS_DRAW_STYLE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses", "FEModelStaticAnalysisDrawStyle"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FEModelStaticAnalysisDrawStyle")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FEModelStaticAnalysisDrawStyle._Cast_FEModelStaticAnalysisDrawStyle",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FEModelStaticAnalysisDrawStyle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FEModelStaticAnalysisDrawStyle:
    """Special nested class for casting FEModelStaticAnalysisDrawStyle to subclasses."""

    __parent__: "FEModelStaticAnalysisDrawStyle"

    @property
    def fe_model_tab_draw_style(self: "CastSelf") -> "_277.FEModelTabDrawStyle":
        return self.__parent__._cast(_277.FEModelTabDrawStyle)

    @property
    def fe_model_static_analysis_draw_style(
        self: "CastSelf",
    ) -> "FEModelStaticAnalysisDrawStyle":
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
class FEModelStaticAnalysisDrawStyle(_277.FEModelTabDrawStyle):
    """FEModelStaticAnalysisDrawStyle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_MODEL_STATIC_ANALYSIS_DRAW_STYLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def show_force_arrows(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowForceArrows")

        if temp is None:
            return False

        return temp

    @show_force_arrows.setter
    @exception_bridge
    @enforce_parameter_types
    def show_force_arrows(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ShowForceArrows", bool(value) if value is not None else False
        )

    @property
    def cast_to(self: "Self") -> "_Cast_FEModelStaticAnalysisDrawStyle":
        """Cast to another type.

        Returns:
            _Cast_FEModelStaticAnalysisDrawStyle
        """
        return _Cast_FEModelStaticAnalysisDrawStyle(self)
