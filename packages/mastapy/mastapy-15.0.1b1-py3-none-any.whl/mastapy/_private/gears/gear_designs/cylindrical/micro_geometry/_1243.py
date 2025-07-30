"""ProfileReliefSpecificationForCustomer102"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1244

_PROFILE_RELIEF_SPECIFICATION_FOR_CUSTOMER_102 = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry",
    "ProfileReliefSpecificationForCustomer102",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1246

    Self = TypeVar("Self", bound="ProfileReliefSpecificationForCustomer102")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ProfileReliefSpecificationForCustomer102._Cast_ProfileReliefSpecificationForCustomer102",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ProfileReliefSpecificationForCustomer102",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ProfileReliefSpecificationForCustomer102:
    """Special nested class for casting ProfileReliefSpecificationForCustomer102 to subclasses."""

    __parent__: "ProfileReliefSpecificationForCustomer102"

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
    def profile_relief_specification_for_customer_102(
        self: "CastSelf",
    ) -> "ProfileReliefSpecificationForCustomer102":
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
class ProfileReliefSpecificationForCustomer102(_1244.ProfileReliefWithDeviation):
    """ProfileReliefSpecificationForCustomer102

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PROFILE_RELIEF_SPECIFICATION_FOR_CUSTOMER_102

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def involute_profile_mu_m(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InvoluteProfileMuM")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def roll_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RollAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ProfileReliefSpecificationForCustomer102":
        """Cast to another type.

        Returns:
            _Cast_ProfileReliefSpecificationForCustomer102
        """
        return _Cast_ProfileReliefSpecificationForCustomer102(self)
