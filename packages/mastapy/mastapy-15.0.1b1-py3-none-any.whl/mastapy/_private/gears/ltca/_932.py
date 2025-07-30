"""CylindricalGearFilletNodeStressResultsColumn"""

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
from mastapy._private.gears.ltca import _941

_CYLINDRICAL_GEAR_FILLET_NODE_STRESS_RESULTS_COLUMN = python_net_import(
    "SMT.MastaAPI.Gears.LTCA", "CylindricalGearFilletNodeStressResultsColumn"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CylindricalGearFilletNodeStressResultsColumn")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearFilletNodeStressResultsColumn._Cast_CylindricalGearFilletNodeStressResultsColumn",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearFilletNodeStressResultsColumn",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearFilletNodeStressResultsColumn:
    """Special nested class for casting CylindricalGearFilletNodeStressResultsColumn to subclasses."""

    __parent__: "CylindricalGearFilletNodeStressResultsColumn"

    @property
    def gear_fillet_node_stress_results_column(
        self: "CastSelf",
    ) -> "_941.GearFilletNodeStressResultsColumn":
        return self.__parent__._cast(_941.GearFilletNodeStressResultsColumn)

    @property
    def cylindrical_gear_fillet_node_stress_results_column(
        self: "CastSelf",
    ) -> "CylindricalGearFilletNodeStressResultsColumn":
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
class CylindricalGearFilletNodeStressResultsColumn(
    _941.GearFilletNodeStressResultsColumn
):
    """CylindricalGearFilletNodeStressResultsColumn

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_FILLET_NODE_STRESS_RESULTS_COLUMN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def face_width_position(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceWidthPosition")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearFilletNodeStressResultsColumn":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearFilletNodeStressResultsColumn
        """
        return _Cast_CylindricalGearFilletNodeStressResultsColumn(self)
