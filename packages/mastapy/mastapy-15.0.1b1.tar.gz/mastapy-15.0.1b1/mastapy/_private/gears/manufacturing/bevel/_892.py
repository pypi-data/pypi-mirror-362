"""ConicalPinionMicroGeometryConfig"""

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
from mastapy._private.gears.manufacturing.bevel import _880

_CONICAL_PINION_MICRO_GEOMETRY_CONFIG = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel", "ConicalPinionMicroGeometryConfig"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1335, _1338, _1341
    from mastapy._private.gears.manufacturing.bevel import _881, _886

    Self = TypeVar("Self", bound="ConicalPinionMicroGeometryConfig")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalPinionMicroGeometryConfig._Cast_ConicalPinionMicroGeometryConfig",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalPinionMicroGeometryConfig",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalPinionMicroGeometryConfig:
    """Special nested class for casting ConicalPinionMicroGeometryConfig to subclasses."""

    __parent__: "ConicalPinionMicroGeometryConfig"

    @property
    def conical_gear_micro_geometry_config(
        self: "CastSelf",
    ) -> "_880.ConicalGearMicroGeometryConfig":
        return self.__parent__._cast(_880.ConicalGearMicroGeometryConfig)

    @property
    def conical_gear_micro_geometry_config_base(
        self: "CastSelf",
    ) -> "_881.ConicalGearMicroGeometryConfigBase":
        from mastapy._private.gears.manufacturing.bevel import _881

        return self.__parent__._cast(_881.ConicalGearMicroGeometryConfigBase)

    @property
    def gear_implementation_detail(
        self: "CastSelf",
    ) -> "_1341.GearImplementationDetail":
        from mastapy._private.gears.analysis import _1341

        return self.__parent__._cast(_1341.GearImplementationDetail)

    @property
    def gear_design_analysis(self: "CastSelf") -> "_1338.GearDesignAnalysis":
        from mastapy._private.gears.analysis import _1338

        return self.__parent__._cast(_1338.GearDesignAnalysis)

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1335.AbstractGearAnalysis":
        from mastapy._private.gears.analysis import _1335

        return self.__parent__._cast(_1335.AbstractGearAnalysis)

    @property
    def conical_pinion_micro_geometry_config(
        self: "CastSelf",
    ) -> "ConicalPinionMicroGeometryConfig":
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
class ConicalPinionMicroGeometryConfig(_880.ConicalGearMicroGeometryConfig):
    """ConicalPinionMicroGeometryConfig

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_PINION_MICRO_GEOMETRY_CONFIG

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def pinion_concave_ob_configuration(
        self: "Self",
    ) -> "_886.ConicalMeshFlankNURBSMicroGeometryConfig":
        """mastapy.gears.manufacturing.bevel.ConicalMeshFlankNURBSMicroGeometryConfig

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionConcaveOBConfiguration")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def pinion_convex_ib_configuration(
        self: "Self",
    ) -> "_886.ConicalMeshFlankNURBSMicroGeometryConfig":
        """mastapy.gears.manufacturing.bevel.ConicalMeshFlankNURBSMicroGeometryConfig

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionConvexIBConfiguration")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalPinionMicroGeometryConfig":
        """Cast to another type.

        Returns:
            _Cast_ConicalPinionMicroGeometryConfig
        """
        return _Cast_ConicalPinionMicroGeometryConfig(self)
