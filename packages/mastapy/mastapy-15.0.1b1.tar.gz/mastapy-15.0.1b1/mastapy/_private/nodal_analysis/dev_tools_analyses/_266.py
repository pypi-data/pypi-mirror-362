"""ElementGroup"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.nodal_analysis.dev_tools_analyses import _268

_ELEMENT_GROUP = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses", "ElementGroup"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.dev_tools_analyses import _267

    Self = TypeVar("Self", bound="ElementGroup")
    CastSelf = TypeVar("CastSelf", bound="ElementGroup._Cast_ElementGroup")


__docformat__ = "restructuredtext en"
__all__ = ("ElementGroup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElementGroup:
    """Special nested class for casting ElementGroup to subclasses."""

    __parent__: "ElementGroup"

    @property
    def fe_entity_group_integer(self: "CastSelf") -> "_268.FEEntityGroupInteger":
        return self.__parent__._cast(_268.FEEntityGroupInteger)

    @property
    def fe_entity_group(self: "CastSelf") -> "_267.FEEntityGroup":
        from mastapy._private.nodal_analysis.dev_tools_analyses import _267

        return self.__parent__._cast(_267.FEEntityGroup)

    @property
    def element_group(self: "CastSelf") -> "ElementGroup":
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
class ElementGroup(_268.FEEntityGroupInteger):
    """ElementGroup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELEMENT_GROUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ElementGroup":
        """Cast to another type.

        Returns:
            _Cast_ElementGroup
        """
        return _Cast_ElementGroup(self)
