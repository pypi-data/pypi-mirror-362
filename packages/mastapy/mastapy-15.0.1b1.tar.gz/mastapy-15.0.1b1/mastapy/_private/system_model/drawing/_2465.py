"""AdvancedSystemDeflectionViewable"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.drawing import _2464

_ADVANCED_SYSTEM_DEFLECTION_VIEWABLE = python_net_import(
    "SMT.MastaAPI.SystemModel.Drawing", "AdvancedSystemDeflectionViewable"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.drawing import _2474

    Self = TypeVar("Self", bound="AdvancedSystemDeflectionViewable")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AdvancedSystemDeflectionViewable._Cast_AdvancedSystemDeflectionViewable",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AdvancedSystemDeflectionViewable",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AdvancedSystemDeflectionViewable:
    """Special nested class for casting AdvancedSystemDeflectionViewable to subclasses."""

    __parent__: "AdvancedSystemDeflectionViewable"

    @property
    def abstract_system_deflection_viewable(
        self: "CastSelf",
    ) -> "_2464.AbstractSystemDeflectionViewable":
        return self.__parent__._cast(_2464.AbstractSystemDeflectionViewable)

    @property
    def part_analysis_case_with_contour_viewable(
        self: "CastSelf",
    ) -> "_2474.PartAnalysisCaseWithContourViewable":
        from mastapy._private.system_model.drawing import _2474

        return self.__parent__._cast(_2474.PartAnalysisCaseWithContourViewable)

    @property
    def advanced_system_deflection_viewable(
        self: "CastSelf",
    ) -> "AdvancedSystemDeflectionViewable":
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
class AdvancedSystemDeflectionViewable(_2464.AbstractSystemDeflectionViewable):
    """AdvancedSystemDeflectionViewable

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ADVANCED_SYSTEM_DEFLECTION_VIEWABLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_AdvancedSystemDeflectionViewable":
        """Cast to another type.

        Returns:
            _Cast_AdvancedSystemDeflectionViewable
        """
        return _Cast_AdvancedSystemDeflectionViewable(self)
