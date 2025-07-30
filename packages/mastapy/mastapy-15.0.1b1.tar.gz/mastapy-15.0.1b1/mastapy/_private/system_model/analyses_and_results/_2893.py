"""DesignEntityGroupAnalysis"""

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

_DESIGN_ENTITY_GROUP_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults", "DesignEntityGroupAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
        _4997,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting import (
        _3091,
    )

    Self = TypeVar("Self", bound="DesignEntityGroupAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="DesignEntityGroupAnalysis._Cast_DesignEntityGroupAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("DesignEntityGroupAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DesignEntityGroupAnalysis:
    """Special nested class for casting DesignEntityGroupAnalysis to subclasses."""

    __parent__: "DesignEntityGroupAnalysis"

    @property
    def rigidly_connected_component_group_system_deflection(
        self: "CastSelf",
    ) -> "_3091.RigidlyConnectedComponentGroupSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.reporting import (
            _3091,
        )

        return self.__parent__._cast(
            _3091.RigidlyConnectedComponentGroupSystemDeflection
        )

    @property
    def rigidly_connected_design_entity_group_modal_analysis(
        self: "CastSelf",
    ) -> "_4997.RigidlyConnectedDesignEntityGroupModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
            _4997,
        )

        return self.__parent__._cast(
            _4997.RigidlyConnectedDesignEntityGroupModalAnalysis
        )

    @property
    def design_entity_group_analysis(self: "CastSelf") -> "DesignEntityGroupAnalysis":
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
class DesignEntityGroupAnalysis(_0.APIBase):
    """DesignEntityGroupAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DESIGN_ENTITY_GROUP_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_DesignEntityGroupAnalysis":
        """Cast to another type.

        Returns:
            _Cast_DesignEntityGroupAnalysis
        """
        return _Cast_DesignEntityGroupAnalysis(self)
