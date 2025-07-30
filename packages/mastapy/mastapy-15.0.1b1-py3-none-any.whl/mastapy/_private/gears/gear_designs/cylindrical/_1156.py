"""FinishToothThicknessDesignSpecification"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.gear_designs.cylindrical import _1199

_FINISH_TOOTH_THICKNESS_DESIGN_SPECIFICATION = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical",
    "FinishToothThicknessDesignSpecification",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FinishToothThicknessDesignSpecification")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FinishToothThicknessDesignSpecification._Cast_FinishToothThicknessDesignSpecification",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FinishToothThicknessDesignSpecification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FinishToothThicknessDesignSpecification:
    """Special nested class for casting FinishToothThicknessDesignSpecification to subclasses."""

    __parent__: "FinishToothThicknessDesignSpecification"

    @property
    def tooth_thickness_specification_base(
        self: "CastSelf",
    ) -> "_1199.ToothThicknessSpecificationBase":
        return self.__parent__._cast(_1199.ToothThicknessSpecificationBase)

    @property
    def finish_tooth_thickness_design_specification(
        self: "CastSelf",
    ) -> "FinishToothThicknessDesignSpecification":
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
class FinishToothThicknessDesignSpecification(_1199.ToothThicknessSpecificationBase):
    """FinishToothThicknessDesignSpecification

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FINISH_TOOTH_THICKNESS_DESIGN_SPECIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_FinishToothThicknessDesignSpecification":
        """Cast to another type.

        Returns:
            _Cast_FinishToothThicknessDesignSpecification
        """
        return _Cast_FinishToothThicknessDesignSpecification(self)
