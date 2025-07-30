"""ProfileModificationForCustomer102CAD"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1239

_PROFILE_MODIFICATION_FOR_CUSTOMER_102CAD = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry",
    "ProfileModificationForCustomer102CAD",
)

if TYPE_CHECKING:
    from typing import Any, List, Optional, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1243
    from mastapy._private.utility_gui.charts import _2070

    Self = TypeVar("Self", bound="ProfileModificationForCustomer102CAD")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ProfileModificationForCustomer102CAD._Cast_ProfileModificationForCustomer102CAD",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ProfileModificationForCustomer102CAD",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ProfileModificationForCustomer102CAD:
    """Special nested class for casting ProfileModificationForCustomer102CAD to subclasses."""

    __parent__: "ProfileModificationForCustomer102CAD"

    @property
    def modification_for_customer_102cad(
        self: "CastSelf",
    ) -> "_1239.ModificationForCustomer102CAD":
        return self.__parent__._cast(_1239.ModificationForCustomer102CAD)

    @property
    def profile_modification_for_customer_102cad(
        self: "CastSelf",
    ) -> "ProfileModificationForCustomer102CAD":
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
class ProfileModificationForCustomer102CAD(_1239.ModificationForCustomer102CAD):
    """ProfileModificationForCustomer102CAD

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PROFILE_MODIFICATION_FOR_CUSTOMER_102CAD

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def involute_range(self: "Self") -> "Optional[float]":
        """Optional[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InvoluteRange")

        if temp is None:
            return None

        return temp

    @property
    @exception_bridge
    def profile_tolerance_form_with_variation(
        self: "Self",
    ) -> "_2070.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProfileToleranceFormWithVariation")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def show_nominal_design(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowNominalDesign")

        if temp is None:
            return False

        return temp

    @show_nominal_design.setter
    @exception_bridge
    @enforce_parameter_types
    def show_nominal_design(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowNominalDesign",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def profile_relief_points_for_customer_102(
        self: "Self",
    ) -> "List[_1243.ProfileReliefSpecificationForCustomer102]":
        """List[mastapy.gears.gear_designs.cylindrical.micro_geometry.ProfileReliefSpecificationForCustomer102]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProfileReliefPointsForCustomer102")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ProfileModificationForCustomer102CAD":
        """Cast to another type.

        Returns:
            _Cast_ProfileModificationForCustomer102CAD
        """
        return _Cast_ProfileModificationForCustomer102CAD(self)
