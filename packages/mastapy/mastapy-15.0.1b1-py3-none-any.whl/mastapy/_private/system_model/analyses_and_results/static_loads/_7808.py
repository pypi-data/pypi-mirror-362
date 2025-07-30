"""PointLoadHarmonicLoadData"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import list_with_selected_item
from mastapy._private._internal.list_with_selected_item import (
    promote_to_list_with_selected_item,
)
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.electric_machines.harmonic_load_data import _1568

_POINT_LOAD_HARMONIC_LOAD_DATA = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "PointLoadHarmonicLoadData",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.electric_machines.harmonic_load_data import _1564
    from mastapy._private.math_utility import _1688, _1697

    Self = TypeVar("Self", bound="PointLoadHarmonicLoadData")
    CastSelf = TypeVar(
        "CastSelf", bound="PointLoadHarmonicLoadData._Cast_PointLoadHarmonicLoadData"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PointLoadHarmonicLoadData",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PointLoadHarmonicLoadData:
    """Special nested class for casting PointLoadHarmonicLoadData to subclasses."""

    __parent__: "PointLoadHarmonicLoadData"

    @property
    def speed_dependent_harmonic_load_data(
        self: "CastSelf",
    ) -> "_1568.SpeedDependentHarmonicLoadData":
        return self.__parent__._cast(_1568.SpeedDependentHarmonicLoadData)

    @property
    def harmonic_load_data_base(self: "CastSelf") -> "_1564.HarmonicLoadDataBase":
        from mastapy._private.electric_machines.harmonic_load_data import _1564

        return self.__parent__._cast(_1564.HarmonicLoadDataBase)

    @property
    def point_load_harmonic_load_data(self: "CastSelf") -> "PointLoadHarmonicLoadData":
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
class PointLoadHarmonicLoadData(_1568.SpeedDependentHarmonicLoadData):
    """PointLoadHarmonicLoadData

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _POINT_LOAD_HARMONIC_LOAD_DATA

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def degree_of_freedom(self: "Self") -> "_1688.DegreeOfFreedom":
        """mastapy.math_utility.DegreeOfFreedom"""
        temp = pythonnet_property_get(self.wrapped, "DegreeOfFreedom")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.MathUtility.DegreeOfFreedom"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.math_utility._1688", "DegreeOfFreedom"
        )(value)

    @degree_of_freedom.setter
    @exception_bridge
    @enforce_parameter_types
    def degree_of_freedom(self: "Self", value: "_1688.DegreeOfFreedom") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.MathUtility.DegreeOfFreedom"
        )
        pythonnet_property_set(self.wrapped, "DegreeOfFreedom", value)

    @property
    @exception_bridge
    def reference_shaft(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "ReferenceShaft")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @reference_shaft.setter
    @exception_bridge
    @enforce_parameter_types
    def reference_shaft(self: "Self", value: "str") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "ReferenceShaft", value)

    @property
    @exception_bridge
    def excitations(self: "Self") -> "List[_1697.FourierSeries]":
        """List[mastapy.math_utility.FourierSeries]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Excitations")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_PointLoadHarmonicLoadData":
        """Cast to another type.

        Returns:
            _Cast_PointLoadHarmonicLoadData
        """
        return _Cast_PointLoadHarmonicLoadData(self)
