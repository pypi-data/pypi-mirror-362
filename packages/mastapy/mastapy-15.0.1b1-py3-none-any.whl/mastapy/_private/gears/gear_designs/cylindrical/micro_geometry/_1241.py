"""ProfileFormReliefWithDeviation"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1244

_PROFILE_FORM_RELIEF_WITH_DEVIATION = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry",
    "ProfileFormReliefWithDeviation",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1246

    Self = TypeVar("Self", bound="ProfileFormReliefWithDeviation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ProfileFormReliefWithDeviation._Cast_ProfileFormReliefWithDeviation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ProfileFormReliefWithDeviation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ProfileFormReliefWithDeviation:
    """Special nested class for casting ProfileFormReliefWithDeviation to subclasses."""

    __parent__: "ProfileFormReliefWithDeviation"

    @property
    def profile_relief_with_deviation(
        self: "CastSelf",
    ) -> "_1244.ProfileReliefWithDeviation":
        return self.__parent__._cast(_1244.ProfileReliefWithDeviation)

    @property
    def relief_with_deviation(self: "CastSelf") -> "_1246.ReliefWithDeviation":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1246

        return self.__parent__._cast(_1246.ReliefWithDeviation)

    @property
    def profile_form_relief_with_deviation(
        self: "CastSelf",
    ) -> "ProfileFormReliefWithDeviation":
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
class ProfileFormReliefWithDeviation(_1244.ProfileReliefWithDeviation):
    """ProfileFormReliefWithDeviation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PROFILE_FORM_RELIEF_WITH_DEVIATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ProfileFormReliefWithDeviation":
        """Cast to another type.

        Returns:
            _Cast_ProfileFormReliefWithDeviation
        """
        return _Cast_ProfileFormReliefWithDeviation(self)
