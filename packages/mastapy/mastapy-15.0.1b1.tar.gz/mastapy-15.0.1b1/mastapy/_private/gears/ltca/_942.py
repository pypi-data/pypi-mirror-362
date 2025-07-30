"""GearFilletNodeStressResultsRow"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_GEAR_FILLET_NODE_STRESS_RESULTS_ROW = python_net_import(
    "SMT.MastaAPI.Gears.LTCA", "GearFilletNodeStressResultsRow"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.ltca import _933, _940

    Self = TypeVar("Self", bound="GearFilletNodeStressResultsRow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearFilletNodeStressResultsRow._Cast_GearFilletNodeStressResultsRow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearFilletNodeStressResultsRow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearFilletNodeStressResultsRow:
    """Special nested class for casting GearFilletNodeStressResultsRow to subclasses."""

    __parent__: "GearFilletNodeStressResultsRow"

    @property
    def cylindrical_gear_fillet_node_stress_results_row(
        self: "CastSelf",
    ) -> "_933.CylindricalGearFilletNodeStressResultsRow":
        from mastapy._private.gears.ltca import _933

        return self.__parent__._cast(_933.CylindricalGearFilletNodeStressResultsRow)

    @property
    def gear_fillet_node_stress_results_row(
        self: "CastSelf",
    ) -> "GearFilletNodeStressResultsRow":
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
class GearFilletNodeStressResultsRow(_0.APIBase):
    """GearFilletNodeStressResultsRow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_FILLET_NODE_STRESS_RESULTS_ROW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def fillet_row_index(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FilletRowIndex")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def node_results(self: "Self") -> "List[_940.GearFilletNodeStressResults]":
        """List[mastapy.gears.ltca.GearFilletNodeStressResults]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NodeResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_GearFilletNodeStressResultsRow":
        """Cast to another type.

        Returns:
            _Cast_GearFilletNodeStressResultsRow
        """
        return _Cast_GearFilletNodeStressResultsRow(self)
