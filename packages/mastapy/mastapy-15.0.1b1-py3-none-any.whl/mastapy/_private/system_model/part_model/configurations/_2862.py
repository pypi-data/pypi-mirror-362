"""BearingDetailSelection"""

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
from mastapy._private.bearings.bearing_designs import _2340
from mastapy._private.system_model.part_model import _2664
from mastapy._private.system_model.part_model.configurations import _2865

_BEARING_DETAIL_SELECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Configurations", "BearingDetailSelection"
)

if TYPE_CHECKING:
    from typing import Any, List, Optional, Type, TypeVar

    from mastapy._private.bearings.bearing_results import _2166
    from mastapy._private.system_model.part_model import _2666

    Self = TypeVar("Self", bound="BearingDetailSelection")
    CastSelf = TypeVar(
        "CastSelf", bound="BearingDetailSelection._Cast_BearingDetailSelection"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BearingDetailSelection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BearingDetailSelection:
    """Special nested class for casting BearingDetailSelection to subclasses."""

    __parent__: "BearingDetailSelection"

    @property
    def part_detail_selection(self: "CastSelf") -> "_2865.PartDetailSelection":
        return self.__parent__._cast(_2865.PartDetailSelection)

    @property
    def bearing_detail_selection(self: "CastSelf") -> "BearingDetailSelection":
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
class BearingDetailSelection(
    _2865.PartDetailSelection[_2664.Bearing, _2340.BearingDesign]
):
    """BearingDetailSelection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEARING_DETAIL_SELECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def inner_offset(self: "Self") -> "Optional[float]":
        """Optional[float]"""
        temp = pythonnet_property_get(self.wrapped, "InnerOffset")

        if temp is None:
            return None

        return temp

    @inner_offset.setter
    @exception_bridge
    @enforce_parameter_types
    def inner_offset(self: "Self", value: "Optional[float]") -> None:
        pythonnet_property_set(self.wrapped, "InnerOffset", value)

    @property
    @exception_bridge
    def orientation(self: "Self") -> "_2166.Orientations":
        """mastapy.bearings.bearing_results.Orientations"""
        temp = pythonnet_property_get(self.wrapped, "Orientation")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.BearingResults.Orientations"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings.bearing_results._2166", "Orientations"
        )(value)

    @orientation.setter
    @exception_bridge
    @enforce_parameter_types
    def orientation(self: "Self", value: "_2166.Orientations") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Bearings.BearingResults.Orientations"
        )
        pythonnet_property_set(self.wrapped, "Orientation", value)

    @property
    @exception_bridge
    def outer_offset(self: "Self") -> "Optional[float]":
        """Optional[float]"""
        temp = pythonnet_property_get(self.wrapped, "OuterOffset")

        if temp is None:
            return None

        return temp

    @outer_offset.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_offset(self: "Self", value: "Optional[float]") -> None:
        pythonnet_property_set(self.wrapped, "OuterOffset", value)

    @property
    @exception_bridge
    def mounting(self: "Self") -> "List[_2666.BearingRaceMountingOptions]":
        """List[mastapy.system_model.part_model.BearingRaceMountingOptions]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Mounting")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_BearingDetailSelection":
        """Cast to another type.

        Returns:
            _Cast_BearingDetailSelection
        """
        return _Cast_BearingDetailSelection(self)
