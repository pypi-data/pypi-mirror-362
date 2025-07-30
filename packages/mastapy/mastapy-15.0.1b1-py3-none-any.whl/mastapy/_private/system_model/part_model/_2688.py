"""LoadSharingSettings"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
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

_LOAD_SHARING_SETTINGS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "LoadSharingSettings"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.part_model import _2662, _2687

    Self = TypeVar("Self", bound="LoadSharingSettings")
    CastSelf = TypeVar(
        "CastSelf", bound="LoadSharingSettings._Cast_LoadSharingSettings"
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadSharingSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadSharingSettings:
    """Special nested class for casting LoadSharingSettings to subclasses."""

    __parent__: "LoadSharingSettings"

    @property
    def load_sharing_settings(self: "CastSelf") -> "LoadSharingSettings":
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
class LoadSharingSettings(_0.APIBase):
    """LoadSharingSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOAD_SHARING_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def planetary_load_sharing(self: "Self") -> "_2687.LoadSharingModes":
        """mastapy.system_model.part_model.LoadSharingModes"""
        temp = pythonnet_property_get(self.wrapped, "PlanetaryLoadSharing")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.SystemModel.PartModel.LoadSharingModes"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.part_model._2687", "LoadSharingModes"
        )(value)

    @planetary_load_sharing.setter
    @exception_bridge
    @enforce_parameter_types
    def planetary_load_sharing(self: "Self", value: "_2687.LoadSharingModes") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.SystemModel.PartModel.LoadSharingModes"
        )
        pythonnet_property_set(self.wrapped, "PlanetaryLoadSharing", value)

    @property
    @exception_bridge
    def planetary_load_sharing_agma_application_level(
        self: "Self",
    ) -> "_2662.AGMALoadSharingTableApplicationLevel":
        """mastapy.system_model.part_model.AGMALoadSharingTableApplicationLevel"""
        temp = pythonnet_property_get(
            self.wrapped, "PlanetaryLoadSharingAGMAApplicationLevel"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.PartModel.AGMALoadSharingTableApplicationLevel",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.part_model._2662",
            "AGMALoadSharingTableApplicationLevel",
        )(value)

    @planetary_load_sharing_agma_application_level.setter
    @exception_bridge
    @enforce_parameter_types
    def planetary_load_sharing_agma_application_level(
        self: "Self", value: "_2662.AGMALoadSharingTableApplicationLevel"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.PartModel.AGMALoadSharingTableApplicationLevel",
        )
        pythonnet_property_set(
            self.wrapped, "PlanetaryLoadSharingAGMAApplicationLevel", value
        )

    @property
    def cast_to(self: "Self") -> "_Cast_LoadSharingSettings":
        """Cast to another type.

        Returns:
            _Cast_LoadSharingSettings
        """
        return _Cast_LoadSharingSettings(self)
