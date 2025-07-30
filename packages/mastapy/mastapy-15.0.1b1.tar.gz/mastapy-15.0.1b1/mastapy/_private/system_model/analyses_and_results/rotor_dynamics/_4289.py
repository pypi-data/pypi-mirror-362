"""ShaftForcedComplexShape"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.rotor_dynamics import _4288
from mastapy._private.utility.units_and_measurements.measurements import _1807, _1863

_SHAFT_FORCED_COMPLEX_SHAPE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.RotorDynamics",
    "ShaftForcedComplexShape",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ShaftForcedComplexShape")
    CastSelf = TypeVar(
        "CastSelf", bound="ShaftForcedComplexShape._Cast_ShaftForcedComplexShape"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftForcedComplexShape",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftForcedComplexShape:
    """Special nested class for casting ShaftForcedComplexShape to subclasses."""

    __parent__: "ShaftForcedComplexShape"

    @property
    def shaft_complex_shape(self: "CastSelf") -> "_4288.ShaftComplexShape":
        return self.__parent__._cast(_4288.ShaftComplexShape)

    @property
    def shaft_forced_complex_shape(self: "CastSelf") -> "ShaftForcedComplexShape":
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
class ShaftForcedComplexShape(
    _4288.ShaftComplexShape[_1863.LengthVeryShort, _1807.AngleSmall]
):
    """ShaftForcedComplexShape

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_FORCED_COMPLEX_SHAPE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftForcedComplexShape":
        """Cast to another type.

        Returns:
            _Cast_ShaftForcedComplexShape
        """
        return _Cast_ShaftForcedComplexShape(self)
