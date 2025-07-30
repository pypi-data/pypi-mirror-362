"""ReliefWithDeviation"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_RELIEF_WITH_DEVIATION = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry", "ReliefWithDeviation"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import (
        _1227,
        _1229,
        _1230,
        _1231,
        _1241,
        _1243,
        _1244,
        _1245,
        _1248,
        _1249,
    )

    Self = TypeVar("Self", bound="ReliefWithDeviation")
    CastSelf = TypeVar(
        "CastSelf", bound="ReliefWithDeviation._Cast_ReliefWithDeviation"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ReliefWithDeviation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ReliefWithDeviation:
    """Special nested class for casting ReliefWithDeviation to subclasses."""

    __parent__: "ReliefWithDeviation"

    @property
    def lead_form_relief_with_deviation(
        self: "CastSelf",
    ) -> "_1227.LeadFormReliefWithDeviation":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1227

        return self.__parent__._cast(_1227.LeadFormReliefWithDeviation)

    @property
    def lead_relief_specification_for_customer_102(
        self: "CastSelf",
    ) -> "_1229.LeadReliefSpecificationForCustomer102":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1229

        return self.__parent__._cast(_1229.LeadReliefSpecificationForCustomer102)

    @property
    def lead_relief_with_deviation(self: "CastSelf") -> "_1230.LeadReliefWithDeviation":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1230

        return self.__parent__._cast(_1230.LeadReliefWithDeviation)

    @property
    def lead_slope_relief_with_deviation(
        self: "CastSelf",
    ) -> "_1231.LeadSlopeReliefWithDeviation":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1231

        return self.__parent__._cast(_1231.LeadSlopeReliefWithDeviation)

    @property
    def profile_form_relief_with_deviation(
        self: "CastSelf",
    ) -> "_1241.ProfileFormReliefWithDeviation":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1241

        return self.__parent__._cast(_1241.ProfileFormReliefWithDeviation)

    @property
    def profile_relief_specification_for_customer_102(
        self: "CastSelf",
    ) -> "_1243.ProfileReliefSpecificationForCustomer102":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1243

        return self.__parent__._cast(_1243.ProfileReliefSpecificationForCustomer102)

    @property
    def profile_relief_with_deviation(
        self: "CastSelf",
    ) -> "_1244.ProfileReliefWithDeviation":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1244

        return self.__parent__._cast(_1244.ProfileReliefWithDeviation)

    @property
    def profile_slope_relief_with_deviation(
        self: "CastSelf",
    ) -> "_1245.ProfileSlopeReliefWithDeviation":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1245

        return self.__parent__._cast(_1245.ProfileSlopeReliefWithDeviation)

    @property
    def total_lead_relief_with_deviation(
        self: "CastSelf",
    ) -> "_1248.TotalLeadReliefWithDeviation":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1248

        return self.__parent__._cast(_1248.TotalLeadReliefWithDeviation)

    @property
    def total_profile_relief_with_deviation(
        self: "CastSelf",
    ) -> "_1249.TotalProfileReliefWithDeviation":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1249

        return self.__parent__._cast(_1249.TotalProfileReliefWithDeviation)

    @property
    def relief_with_deviation(self: "CastSelf") -> "ReliefWithDeviation":
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
class ReliefWithDeviation(_0.APIBase):
    """ReliefWithDeviation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RELIEF_WITH_DEVIATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def lower_limit(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LowerLimit")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relief(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Relief")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def section(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Section")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def upper_limit(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UpperLimit")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ReliefWithDeviation":
        """Cast to another type.

        Returns:
            _Cast_ReliefWithDeviation
        """
        return _Cast_ReliefWithDeviation(self)
