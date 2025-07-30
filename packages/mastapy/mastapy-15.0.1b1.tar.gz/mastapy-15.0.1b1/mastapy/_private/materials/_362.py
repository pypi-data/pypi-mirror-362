"""MaterialsSettingsItem"""

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
from mastapy._private.materials import _363
from mastapy._private.utility.databases import _2028

_MATERIALS_SETTINGS_ITEM = python_net_import(
    "SMT.MastaAPI.Materials", "MaterialsSettingsItem"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.utility.property import _2046

    Self = TypeVar("Self", bound="MaterialsSettingsItem")
    CastSelf = TypeVar(
        "CastSelf", bound="MaterialsSettingsItem._Cast_MaterialsSettingsItem"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MaterialsSettingsItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MaterialsSettingsItem:
    """Special nested class for casting MaterialsSettingsItem to subclasses."""

    __parent__: "MaterialsSettingsItem"

    @property
    def named_database_item(self: "CastSelf") -> "_2028.NamedDatabaseItem":
        return self.__parent__._cast(_2028.NamedDatabaseItem)

    @property
    def materials_settings_item(self: "CastSelf") -> "MaterialsSettingsItem":
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
class MaterialsSettingsItem(_2028.NamedDatabaseItem):
    """MaterialsSettingsItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MATERIALS_SETTINGS_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def available_material_standards(
        self: "Self",
    ) -> "List[_2046.EnumWithBoolean[_363.MaterialStandards]]":
        """List[mastapy.utility.property.EnumWithBoolean[mastapy.materials.MaterialStandards]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AvailableMaterialStandards")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_MaterialsSettingsItem":
        """Cast to another type.

        Returns:
            _Cast_MaterialsSettingsItem
        """
        return _Cast_MaterialsSettingsItem(self)
