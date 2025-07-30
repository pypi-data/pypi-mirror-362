"""ShaftModalComplexShapeAtSpeeds"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.rotor_dynamics import _4290

_SHAFT_MODAL_COMPLEX_SHAPE_AT_SPEEDS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.RotorDynamics",
    "ShaftModalComplexShapeAtSpeeds",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.rotor_dynamics import _4288

    Self = TypeVar("Self", bound="ShaftModalComplexShapeAtSpeeds")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ShaftModalComplexShapeAtSpeeds._Cast_ShaftModalComplexShapeAtSpeeds",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftModalComplexShapeAtSpeeds",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftModalComplexShapeAtSpeeds:
    """Special nested class for casting ShaftModalComplexShapeAtSpeeds to subclasses."""

    __parent__: "ShaftModalComplexShapeAtSpeeds"

    @property
    def shaft_modal_complex_shape(self: "CastSelf") -> "_4290.ShaftModalComplexShape":
        return self.__parent__._cast(_4290.ShaftModalComplexShape)

    @property
    def shaft_complex_shape(self: "CastSelf") -> "_4288.ShaftComplexShape":
        pass

        from mastapy._private.system_model.analyses_and_results.rotor_dynamics import (
            _4288,
        )

        return self.__parent__._cast(_4288.ShaftComplexShape)

    @property
    def shaft_modal_complex_shape_at_speeds(
        self: "CastSelf",
    ) -> "ShaftModalComplexShapeAtSpeeds":
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
class ShaftModalComplexShapeAtSpeeds(_4290.ShaftModalComplexShape):
    """ShaftModalComplexShapeAtSpeeds

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_MODAL_COMPLEX_SHAPE_AT_SPEEDS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftModalComplexShapeAtSpeeds":
        """Cast to another type.

        Returns:
            _Cast_ShaftModalComplexShapeAtSpeeds
        """
        return _Cast_ShaftModalComplexShapeAtSpeeds(self)
