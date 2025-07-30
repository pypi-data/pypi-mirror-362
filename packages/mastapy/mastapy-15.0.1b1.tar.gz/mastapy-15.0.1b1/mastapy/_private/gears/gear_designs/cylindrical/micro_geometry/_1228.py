"""LeadModificationForCustomer102CAD"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1239

_LEAD_MODIFICATION_FOR_CUSTOMER_102CAD = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry",
    "LeadModificationForCustomer102CAD",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1229
    from mastapy._private.utility_gui.charts import _2070

    Self = TypeVar("Self", bound="LeadModificationForCustomer102CAD")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LeadModificationForCustomer102CAD._Cast_LeadModificationForCustomer102CAD",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LeadModificationForCustomer102CAD",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LeadModificationForCustomer102CAD:
    """Special nested class for casting LeadModificationForCustomer102CAD to subclasses."""

    __parent__: "LeadModificationForCustomer102CAD"

    @property
    def modification_for_customer_102cad(
        self: "CastSelf",
    ) -> "_1239.ModificationForCustomer102CAD":
        return self.__parent__._cast(_1239.ModificationForCustomer102CAD)

    @property
    def lead_modification_for_customer_102cad(
        self: "CastSelf",
    ) -> "LeadModificationForCustomer102CAD":
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
class LeadModificationForCustomer102CAD(_1239.ModificationForCustomer102CAD):
    """LeadModificationForCustomer102CAD

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LEAD_MODIFICATION_FOR_CUSTOMER_102CAD

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def crowning(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Crowning")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lead_evaluation_length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeadEvaluationLength")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lead_with_variation(self: "Self") -> "_2070.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeadWithVariation")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def lead_relief_points_for_customer_102(
        self: "Self",
    ) -> "List[_1229.LeadReliefSpecificationForCustomer102]":
        """List[mastapy.gears.gear_designs.cylindrical.micro_geometry.LeadReliefSpecificationForCustomer102]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeadReliefPointsForCustomer102")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_LeadModificationForCustomer102CAD":
        """Cast to another type.

        Returns:
            _Cast_LeadModificationForCustomer102CAD
        """
        return _Cast_LeadModificationForCustomer102CAD(self)
