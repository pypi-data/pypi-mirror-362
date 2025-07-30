"""GearRootFilletStressResults"""

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

_GEAR_ROOT_FILLET_STRESS_RESULTS = python_net_import(
    "SMT.MastaAPI.Gears.LTCA", "GearRootFilletStressResults"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.ltca import _929, _934, _941, _942

    Self = TypeVar("Self", bound="GearRootFilletStressResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearRootFilletStressResults._Cast_GearRootFilletStressResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearRootFilletStressResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearRootFilletStressResults:
    """Special nested class for casting GearRootFilletStressResults to subclasses."""

    __parent__: "GearRootFilletStressResults"

    @property
    def conical_gear_root_fillet_stress_results(
        self: "CastSelf",
    ) -> "_929.ConicalGearRootFilletStressResults":
        from mastapy._private.gears.ltca import _929

        return self.__parent__._cast(_929.ConicalGearRootFilletStressResults)

    @property
    def cylindrical_gear_root_fillet_stress_results(
        self: "CastSelf",
    ) -> "_934.CylindricalGearRootFilletStressResults":
        from mastapy._private.gears.ltca import _934

        return self.__parent__._cast(_934.CylindricalGearRootFilletStressResults)

    @property
    def gear_root_fillet_stress_results(
        self: "CastSelf",
    ) -> "GearRootFilletStressResults":
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
class GearRootFilletStressResults(_0.APIBase):
    """GearRootFilletStressResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_ROOT_FILLET_STRESS_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def contact_line_index(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactLineIndex")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def columns(self: "Self") -> "List[_941.GearFilletNodeStressResultsColumn]":
        """List[mastapy.gears.ltca.GearFilletNodeStressResultsColumn]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Columns")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def rows(self: "Self") -> "List[_942.GearFilletNodeStressResultsRow]":
        """List[mastapy.gears.ltca.GearFilletNodeStressResultsRow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Rows")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_GearRootFilletStressResults":
        """Cast to another type.

        Returns:
            _Cast_GearRootFilletStressResults
        """
        return _Cast_GearRootFilletStressResults(self)
