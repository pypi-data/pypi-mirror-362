"""FEModelInstanceDrawStyle"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_FE_MODEL_INSTANCE_DRAW_STYLE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses", "FEModelInstanceDrawStyle"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.dev_tools_analyses import _262

    Self = TypeVar("Self", bound="FEModelInstanceDrawStyle")
    CastSelf = TypeVar(
        "CastSelf", bound="FEModelInstanceDrawStyle._Cast_FEModelInstanceDrawStyle"
    )


__docformat__ = "restructuredtext en"
__all__ = ("FEModelInstanceDrawStyle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FEModelInstanceDrawStyle:
    """Special nested class for casting FEModelInstanceDrawStyle to subclasses."""

    __parent__: "FEModelInstanceDrawStyle"

    @property
    def fe_model_instance_draw_style(self: "CastSelf") -> "FEModelInstanceDrawStyle":
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
class FEModelInstanceDrawStyle(_0.APIBase):
    """FEModelInstanceDrawStyle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_MODEL_INSTANCE_DRAW_STYLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def model_draw_style(self: "Self") -> "_262.DrawStyleForFE":
        """mastapy.nodal_analysis.dev_tools_analyses.DrawStyleForFE

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModelDrawStyle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_FEModelInstanceDrawStyle":
        """Cast to another type.

        Returns:
            _Cast_FEModelInstanceDrawStyle
        """
        return _Cast_FEModelInstanceDrawStyle(self)
