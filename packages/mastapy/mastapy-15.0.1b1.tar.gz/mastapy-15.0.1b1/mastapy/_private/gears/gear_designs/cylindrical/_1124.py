"""CylindricalGearDesignConstraints"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.utility.databases import _2028

_CYLINDRICAL_GEAR_DESIGN_CONSTRAINTS = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "CylindricalGearDesignConstraints"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1123

    Self = TypeVar("Self", bound="CylindricalGearDesignConstraints")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearDesignConstraints._Cast_CylindricalGearDesignConstraints",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearDesignConstraints",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearDesignConstraints:
    """Special nested class for casting CylindricalGearDesignConstraints to subclasses."""

    __parent__: "CylindricalGearDesignConstraints"

    @property
    def named_database_item(self: "CastSelf") -> "_2028.NamedDatabaseItem":
        return self.__parent__._cast(_2028.NamedDatabaseItem)

    @property
    def cylindrical_gear_design_constraints(
        self: "CastSelf",
    ) -> "CylindricalGearDesignConstraints":
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
class CylindricalGearDesignConstraints(_2028.NamedDatabaseItem):
    """CylindricalGearDesignConstraints

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_DESIGN_CONSTRAINTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def design_constraints(
        self: "Self",
    ) -> "List[_1123.CylindricalGearDesignConstraint]":
        """List[mastapy.gears.gear_designs.cylindrical.CylindricalGearDesignConstraint]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DesignConstraints")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearDesignConstraints":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearDesignConstraints
        """
        return _Cast_CylindricalGearDesignConstraints(self)
