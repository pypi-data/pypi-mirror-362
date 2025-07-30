"""ActiveFESubstructureSelectionGroup"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.fe import _2605
from mastapy._private.system_model.part_model import _2680
from mastapy._private.system_model.part_model.configurations import _2857, _2864

_ACTIVE_FE_SUBSTRUCTURE_SELECTION_GROUP = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Configurations",
    "ActiveFESubstructureSelectionGroup",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ActiveFESubstructureSelectionGroup")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ActiveFESubstructureSelectionGroup._Cast_ActiveFESubstructureSelectionGroup",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ActiveFESubstructureSelectionGroup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ActiveFESubstructureSelectionGroup:
    """Special nested class for casting ActiveFESubstructureSelectionGroup to subclasses."""

    __parent__: "ActiveFESubstructureSelectionGroup"

    @property
    def part_detail_configuration(self: "CastSelf") -> "_2864.PartDetailConfiguration":
        return self.__parent__._cast(_2864.PartDetailConfiguration)

    @property
    def active_fe_substructure_selection_group(
        self: "CastSelf",
    ) -> "ActiveFESubstructureSelectionGroup":
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
class ActiveFESubstructureSelectionGroup(
    _2864.PartDetailConfiguration[
        _2857.ActiveFESubstructureSelection, _2680.FEPart, _2605.FESubstructure
    ]
):
    """ActiveFESubstructureSelectionGroup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ACTIVE_FE_SUBSTRUCTURE_SELECTION_GROUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ActiveFESubstructureSelectionGroup":
        """Cast to another type.

        Returns:
            _Cast_ActiveFESubstructureSelectionGroup
        """
        return _Cast_ActiveFESubstructureSelectionGroup(self)
