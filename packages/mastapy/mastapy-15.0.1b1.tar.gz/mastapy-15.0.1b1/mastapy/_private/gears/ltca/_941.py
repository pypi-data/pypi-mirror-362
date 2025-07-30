"""GearFilletNodeStressResultsColumn"""

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

_GEAR_FILLET_NODE_STRESS_RESULTS_COLUMN = python_net_import(
    "SMT.MastaAPI.Gears.LTCA", "GearFilletNodeStressResultsColumn"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.ltca import _932, _940

    Self = TypeVar("Self", bound="GearFilletNodeStressResultsColumn")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearFilletNodeStressResultsColumn._Cast_GearFilletNodeStressResultsColumn",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearFilletNodeStressResultsColumn",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearFilletNodeStressResultsColumn:
    """Special nested class for casting GearFilletNodeStressResultsColumn to subclasses."""

    __parent__: "GearFilletNodeStressResultsColumn"

    @property
    def cylindrical_gear_fillet_node_stress_results_column(
        self: "CastSelf",
    ) -> "_932.CylindricalGearFilletNodeStressResultsColumn":
        from mastapy._private.gears.ltca import _932

        return self.__parent__._cast(_932.CylindricalGearFilletNodeStressResultsColumn)

    @property
    def gear_fillet_node_stress_results_column(
        self: "CastSelf",
    ) -> "GearFilletNodeStressResultsColumn":
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
class GearFilletNodeStressResultsColumn(_0.APIBase):
    """GearFilletNodeStressResultsColumn

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_FILLET_NODE_STRESS_RESULTS_COLUMN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def fillet_column_index(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FilletColumnIndex")

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
    def cast_to(self: "Self") -> "_Cast_GearFilletNodeStressResultsColumn":
        """Cast to another type.

        Returns:
            _Cast_GearFilletNodeStressResultsColumn
        """
        return _Cast_GearFilletNodeStressResultsColumn(self)
