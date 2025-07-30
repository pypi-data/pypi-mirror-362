"""ConicalMeshManufacturingConfig"""

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
from mastapy._private.gears.manufacturing.bevel import _890

_CONICAL_MESH_MANUFACTURING_CONFIG = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel", "ConicalMeshManufacturingConfig"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1336, _1342, _1345
    from mastapy._private.gears.manufacturing.bevel import _891, _897

    Self = TypeVar("Self", bound="ConicalMeshManufacturingConfig")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalMeshManufacturingConfig._Cast_ConicalMeshManufacturingConfig",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalMeshManufacturingConfig",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalMeshManufacturingConfig:
    """Special nested class for casting ConicalMeshManufacturingConfig to subclasses."""

    __parent__: "ConicalMeshManufacturingConfig"

    @property
    def conical_mesh_micro_geometry_config_base(
        self: "CastSelf",
    ) -> "_890.ConicalMeshMicroGeometryConfigBase":
        return self.__parent__._cast(_890.ConicalMeshMicroGeometryConfigBase)

    @property
    def gear_mesh_implementation_detail(
        self: "CastSelf",
    ) -> "_1345.GearMeshImplementationDetail":
        from mastapy._private.gears.analysis import _1345

        return self.__parent__._cast(_1345.GearMeshImplementationDetail)

    @property
    def gear_mesh_design_analysis(self: "CastSelf") -> "_1342.GearMeshDesignAnalysis":
        from mastapy._private.gears.analysis import _1342

        return self.__parent__._cast(_1342.GearMeshDesignAnalysis)

    @property
    def abstract_gear_mesh_analysis(
        self: "CastSelf",
    ) -> "_1336.AbstractGearMeshAnalysis":
        from mastapy._private.gears.analysis import _1336

        return self.__parent__._cast(_1336.AbstractGearMeshAnalysis)

    @property
    def conical_mesh_manufacturing_config(
        self: "CastSelf",
    ) -> "ConicalMeshManufacturingConfig":
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
class ConicalMeshManufacturingConfig(_890.ConicalMeshMicroGeometryConfigBase):
    """ConicalMeshManufacturingConfig

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_MESH_MANUFACTURING_CONFIG

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def pinion_config(self: "Self") -> "_891.ConicalPinionManufacturingConfig":
        """mastapy.gears.manufacturing.bevel.ConicalPinionManufacturingConfig

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionConfig")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def wheel_config(self: "Self") -> "_897.ConicalWheelManufacturingConfig":
        """mastapy.gears.manufacturing.bevel.ConicalWheelManufacturingConfig

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelConfig")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalMeshManufacturingConfig":
        """Cast to another type.

        Returns:
            _Cast_ConicalMeshManufacturingConfig
        """
        return _Cast_ConicalMeshManufacturingConfig(self)
