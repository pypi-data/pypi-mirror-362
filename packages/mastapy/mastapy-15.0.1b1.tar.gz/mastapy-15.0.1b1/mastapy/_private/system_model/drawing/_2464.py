"""AbstractSystemDeflectionViewable"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private.system_model.drawing import _2474

_ABSTRACT_SYSTEM_DEFLECTION_VIEWABLE = python_net_import(
    "SMT.MastaAPI.SystemModel.Drawing", "AbstractSystemDeflectionViewable"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _3069,
    )
    from mastapy._private.system_model.drawing import _2465, _2467, _2481

    Self = TypeVar("Self", bound="AbstractSystemDeflectionViewable")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractSystemDeflectionViewable._Cast_AbstractSystemDeflectionViewable",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractSystemDeflectionViewable",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractSystemDeflectionViewable:
    """Special nested class for casting AbstractSystemDeflectionViewable to subclasses."""

    __parent__: "AbstractSystemDeflectionViewable"

    @property
    def part_analysis_case_with_contour_viewable(
        self: "CastSelf",
    ) -> "_2474.PartAnalysisCaseWithContourViewable":
        return self.__parent__._cast(_2474.PartAnalysisCaseWithContourViewable)

    @property
    def advanced_system_deflection_viewable(
        self: "CastSelf",
    ) -> "_2465.AdvancedSystemDeflectionViewable":
        from mastapy._private.system_model.drawing import _2465

        return self.__parent__._cast(_2465.AdvancedSystemDeflectionViewable)

    @property
    def system_deflection_viewable(
        self: "CastSelf",
    ) -> "_2481.SystemDeflectionViewable":
        from mastapy._private.system_model.drawing import _2481

        return self.__parent__._cast(_2481.SystemDeflectionViewable)

    @property
    def abstract_system_deflection_viewable(
        self: "CastSelf",
    ) -> "AbstractSystemDeflectionViewable":
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
class AbstractSystemDeflectionViewable(_2474.PartAnalysisCaseWithContourViewable):
    """AbstractSystemDeflectionViewable

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_SYSTEM_DEFLECTION_VIEWABLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def contour_draw_style(self: "Self") -> "_2467.ContourDrawStyle":
        """mastapy.system_model.drawing.ContourDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContourDrawStyle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def system_deflection_draw_style(self: "Self") -> "_3069.SystemDeflectionDrawStyle":
        """mastapy.system_model.analyses_and_results.system_deflections.SystemDeflectionDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionDrawStyle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    def fe_results(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "FEResults")

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractSystemDeflectionViewable":
        """Cast to another type.

        Returns:
            _Cast_AbstractSystemDeflectionViewable
        """
        return _Cast_AbstractSystemDeflectionViewable(self)
