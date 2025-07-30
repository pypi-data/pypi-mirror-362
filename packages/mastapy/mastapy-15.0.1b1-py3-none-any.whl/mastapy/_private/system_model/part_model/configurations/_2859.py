"""ActiveShaftDesignSelection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.shafts import _46
from mastapy._private.system_model.part_model.configurations import _2865
from mastapy._private.system_model.part_model.shaft_model import _2714

_ACTIVE_SHAFT_DESIGN_SELECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Configurations", "ActiveShaftDesignSelection"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ActiveShaftDesignSelection")
    CastSelf = TypeVar(
        "CastSelf", bound="ActiveShaftDesignSelection._Cast_ActiveShaftDesignSelection"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ActiveShaftDesignSelection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ActiveShaftDesignSelection:
    """Special nested class for casting ActiveShaftDesignSelection to subclasses."""

    __parent__: "ActiveShaftDesignSelection"

    @property
    def part_detail_selection(self: "CastSelf") -> "_2865.PartDetailSelection":
        return self.__parent__._cast(_2865.PartDetailSelection)

    @property
    def active_shaft_design_selection(self: "CastSelf") -> "ActiveShaftDesignSelection":
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
class ActiveShaftDesignSelection(
    _2865.PartDetailSelection[_2714.Shaft, _46.SimpleShaftDefinition]
):
    """ActiveShaftDesignSelection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ACTIVE_SHAFT_DESIGN_SELECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ActiveShaftDesignSelection":
        """Cast to another type.

        Returns:
            _Cast_ActiveShaftDesignSelection
        """
        return _Cast_ActiveShaftDesignSelection(self)
