"""DesignConstraintsCollection"""

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
from mastapy._private.gears.gear_designs import _1048
from mastapy._private.utility.databases import _2028

_DESIGN_CONSTRAINTS_COLLECTION = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns", "DesignConstraintsCollection"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.utility.property import _2039

    Self = TypeVar("Self", bound="DesignConstraintsCollection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="DesignConstraintsCollection._Cast_DesignConstraintsCollection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("DesignConstraintsCollection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DesignConstraintsCollection:
    """Special nested class for casting DesignConstraintsCollection to subclasses."""

    __parent__: "DesignConstraintsCollection"

    @property
    def named_database_item(self: "CastSelf") -> "_2028.NamedDatabaseItem":
        return self.__parent__._cast(_2028.NamedDatabaseItem)

    @property
    def design_constraints_collection(
        self: "CastSelf",
    ) -> "DesignConstraintsCollection":
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
class DesignConstraintsCollection(_2028.NamedDatabaseItem):
    """DesignConstraintsCollection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DESIGN_CONSTRAINTS_COLLECTION

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
    ) -> "List[_2039.DeletableCollectionMember[_1048.DesignConstraint]]":
        """List[mastapy.utility.property.DeletableCollectionMember[mastapy.gears.gear_designs.DesignConstraint]]

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
    def cast_to(self: "Self") -> "_Cast_DesignConstraintsCollection":
        """Cast to another type.

        Returns:
            _Cast_DesignConstraintsCollection
        """
        return _Cast_DesignConstraintsCollection(self)
