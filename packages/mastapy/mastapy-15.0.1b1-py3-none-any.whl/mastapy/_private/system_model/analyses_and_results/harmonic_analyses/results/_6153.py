"""ExcitationSourceSelectionGroup"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.harmonic_analyses.results import (
    _6152,
)

_EXCITATION_SOURCE_SELECTION_GROUP = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Results",
    "ExcitationSourceSelectionGroup",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.math_utility import _1713

    Self = TypeVar("Self", bound="ExcitationSourceSelectionGroup")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ExcitationSourceSelectionGroup._Cast_ExcitationSourceSelectionGroup",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ExcitationSourceSelectionGroup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ExcitationSourceSelectionGroup:
    """Special nested class for casting ExcitationSourceSelectionGroup to subclasses."""

    __parent__: "ExcitationSourceSelectionGroup"

    @property
    def excitation_source_selection_base(
        self: "CastSelf",
    ) -> "_6152.ExcitationSourceSelectionBase":
        return self.__parent__._cast(_6152.ExcitationSourceSelectionBase)

    @property
    def excitation_source_selection_group(
        self: "CastSelf",
    ) -> "ExcitationSourceSelectionGroup":
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
class ExcitationSourceSelectionGroup(_6152.ExcitationSourceSelectionBase):
    """ExcitationSourceSelectionGroup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _EXCITATION_SOURCE_SELECTION_GROUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def sub_items(self: "Self") -> "List[_6152.ExcitationSourceSelectionBase]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.results.ExcitationSourceSelectionBase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SubItems")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def selection_as_xml_string(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "SelectionAsXmlString")

        if temp is None:
            return ""

        return temp

    @selection_as_xml_string.setter
    @exception_bridge
    @enforce_parameter_types
    def selection_as_xml_string(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SelectionAsXmlString",
            str(value) if value is not None else "",
        )

    @exception_bridge
    @enforce_parameter_types
    def include_only_harmonics_with_order(
        self: "Self", order: "_1713.RoundedOrder"
    ) -> None:
        """Method does not return.

        Args:
            order (mastapy.math_utility.RoundedOrder)
        """
        pythonnet_method_call(
            self.wrapped,
            "IncludeOnlyHarmonicsWithOrder",
            order.wrapped if order else None,
        )

    @exception_bridge
    @enforce_parameter_types
    def set_all_harmonics_of_selected_excitation_sources(
        self: "Self", included: "bool"
    ) -> None:
        """Method does not return.

        Args:
            included (bool)
        """
        included = bool(included)
        pythonnet_method_call(
            self.wrapped,
            "SetAllHarmonicsOfSelectedExcitationSources",
            included if included else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ExcitationSourceSelectionGroup":
        """Cast to another type.

        Returns:
            _Cast_ExcitationSourceSelectionGroup
        """
        return _Cast_ExcitationSourceSelectionGroup(self)
