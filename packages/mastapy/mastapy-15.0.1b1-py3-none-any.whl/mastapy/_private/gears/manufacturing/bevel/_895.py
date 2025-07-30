"""ConicalSetMicroGeometryConfig"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private.gears.manufacturing.bevel import _896

_CONICAL_SET_MICRO_GEOMETRY_CONFIG = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel", "ConicalSetMicroGeometryConfig"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1337, _1346, _1351
    from mastapy._private.gears.manufacturing.bevel import _880, _889

    Self = TypeVar("Self", bound="ConicalSetMicroGeometryConfig")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalSetMicroGeometryConfig._Cast_ConicalSetMicroGeometryConfig",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalSetMicroGeometryConfig",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalSetMicroGeometryConfig:
    """Special nested class for casting ConicalSetMicroGeometryConfig to subclasses."""

    __parent__: "ConicalSetMicroGeometryConfig"

    @property
    def conical_set_micro_geometry_config_base(
        self: "CastSelf",
    ) -> "_896.ConicalSetMicroGeometryConfigBase":
        return self.__parent__._cast(_896.ConicalSetMicroGeometryConfigBase)

    @property
    def gear_set_implementation_detail(
        self: "CastSelf",
    ) -> "_1351.GearSetImplementationDetail":
        from mastapy._private.gears.analysis import _1351

        return self.__parent__._cast(_1351.GearSetImplementationDetail)

    @property
    def gear_set_design_analysis(self: "CastSelf") -> "_1346.GearSetDesignAnalysis":
        from mastapy._private.gears.analysis import _1346

        return self.__parent__._cast(_1346.GearSetDesignAnalysis)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1337.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1337

        return self.__parent__._cast(_1337.AbstractGearSetAnalysis)

    @property
    def conical_set_micro_geometry_config(
        self: "CastSelf",
    ) -> "ConicalSetMicroGeometryConfig":
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
class ConicalSetMicroGeometryConfig(_896.ConicalSetMicroGeometryConfigBase):
    """ConicalSetMicroGeometryConfig

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_SET_MICRO_GEOMETRY_CONFIG

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def gear_micro_geometry_configuration(
        self: "Self",
    ) -> "List[_880.ConicalGearMicroGeometryConfig]":
        """List[mastapy.gears.manufacturing.bevel.ConicalGearMicroGeometryConfig]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearMicroGeometryConfiguration")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def meshes(self: "Self") -> "List[_889.ConicalMeshMicroGeometryConfig]":
        """List[mastapy.gears.manufacturing.bevel.ConicalMeshMicroGeometryConfig]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Meshes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    def duplicate(self: "Self") -> "ConicalSetMicroGeometryConfig":
        """mastapy.gears.manufacturing.bevel.ConicalSetMicroGeometryConfig"""
        method_result = pythonnet_method_call(self.wrapped, "Duplicate")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalSetMicroGeometryConfig":
        """Cast to another type.

        Returns:
            _Cast_ConicalSetMicroGeometryConfig
        """
        return _Cast_ConicalSetMicroGeometryConfig(self)
