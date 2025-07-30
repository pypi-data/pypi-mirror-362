"""ConicalMeshFlankManufacturingConfig"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.manufacturing.bevel import _885

_CONICAL_MESH_FLANK_MANUFACTURING_CONFIG = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel", "ConicalMeshFlankManufacturingConfig"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.bevel.basic_machine_settings import (
        _926,
        _927,
    )
    from mastapy._private.gears.manufacturing.bevel.control_parameters import _920

    Self = TypeVar("Self", bound="ConicalMeshFlankManufacturingConfig")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalMeshFlankManufacturingConfig._Cast_ConicalMeshFlankManufacturingConfig",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalMeshFlankManufacturingConfig",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalMeshFlankManufacturingConfig:
    """Special nested class for casting ConicalMeshFlankManufacturingConfig to subclasses."""

    __parent__: "ConicalMeshFlankManufacturingConfig"

    @property
    def conical_mesh_flank_micro_geometry_config(
        self: "CastSelf",
    ) -> "_885.ConicalMeshFlankMicroGeometryConfig":
        return self.__parent__._cast(_885.ConicalMeshFlankMicroGeometryConfig)

    @property
    def conical_mesh_flank_manufacturing_config(
        self: "CastSelf",
    ) -> "ConicalMeshFlankManufacturingConfig":
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
class ConicalMeshFlankManufacturingConfig(_885.ConicalMeshFlankMicroGeometryConfig):
    """ConicalMeshFlankManufacturingConfig

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_MESH_FLANK_MANUFACTURING_CONFIG

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def control_parameters(
        self: "Self",
    ) -> "_920.ConicalGearManufacturingControlParameters":
        """mastapy.gears.manufacturing.bevel.control_parameters.ConicalGearManufacturingControlParameters

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ControlParameters")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def specified_cradle_style_machine_settings(
        self: "Self",
    ) -> "_927.CradleStyleConicalMachineSettingsGenerated":
        """mastapy.gears.manufacturing.bevel.basic_machine_settings.CradleStyleConicalMachineSettingsGenerated

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SpecifiedCradleStyleMachineSettings"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def specified_phoenix_style_machine_settings(
        self: "Self",
    ) -> "_926.BasicConicalGearMachineSettingsGenerated":
        """mastapy.gears.manufacturing.bevel.basic_machine_settings.BasicConicalGearMachineSettingsGenerated

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SpecifiedPhoenixStyleMachineSettings"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalMeshFlankManufacturingConfig":
        """Cast to another type.

        Returns:
            _Cast_ConicalMeshFlankManufacturingConfig
        """
        return _Cast_ConicalMeshFlankManufacturingConfig(self)
