"""ActiveGearSetDesignSelection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.gear_designs import _1054
from mastapy._private.system_model.part_model.configurations import _2865
from mastapy._private.system_model.part_model.gears import _2769

_ACTIVE_GEAR_SET_DESIGN_SELECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ActiveGearSetDesignSelection"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.part_model.gears import _2747

    Self = TypeVar("Self", bound="ActiveGearSetDesignSelection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ActiveGearSetDesignSelection._Cast_ActiveGearSetDesignSelection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ActiveGearSetDesignSelection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ActiveGearSetDesignSelection:
    """Special nested class for casting ActiveGearSetDesignSelection to subclasses."""

    __parent__: "ActiveGearSetDesignSelection"

    @property
    def part_detail_selection(self: "CastSelf") -> "_2865.PartDetailSelection":
        return self.__parent__._cast(_2865.PartDetailSelection)

    @property
    def active_cylindrical_gear_set_design_selection(
        self: "CastSelf",
    ) -> "_2747.ActiveCylindricalGearSetDesignSelection":
        from mastapy._private.system_model.part_model.gears import _2747

        return self.__parent__._cast(_2747.ActiveCylindricalGearSetDesignSelection)

    @property
    def active_gear_set_design_selection(
        self: "CastSelf",
    ) -> "ActiveGearSetDesignSelection":
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
class ActiveGearSetDesignSelection(
    _2865.PartDetailSelection[_2769.GearSet, _1054.GearSetDesign]
):
    """ActiveGearSetDesignSelection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ACTIVE_GEAR_SET_DESIGN_SELECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ActiveGearSetDesignSelection":
        """Cast to another type.

        Returns:
            _Cast_ActiveGearSetDesignSelection
        """
        return _Cast_ActiveGearSetDesignSelection(self)
