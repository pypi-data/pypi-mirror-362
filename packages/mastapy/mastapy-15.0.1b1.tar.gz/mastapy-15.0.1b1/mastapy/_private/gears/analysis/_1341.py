"""GearImplementationDetail"""

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
from mastapy._private.gears.analysis import _1338

_GEAR_IMPLEMENTATION_DETAIL = python_net_import(
    "SMT.MastaAPI.Gears.Analysis", "GearImplementationDetail"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1335
    from mastapy._private.gears.fe_model import _1317
    from mastapy._private.gears.fe_model.conical import _1324
    from mastapy._private.gears.fe_model.cylindrical import _1321
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import (
        _1213,
        _1214,
        _1217,
    )
    from mastapy._private.gears.gear_designs.face import _1097
    from mastapy._private.gears.manufacturing.bevel import (
        _879,
        _880,
        _881,
        _891,
        _892,
        _897,
    )
    from mastapy._private.gears.manufacturing.cylindrical import _715
    from mastapy._private.utility.scripting import _1936

    Self = TypeVar("Self", bound="GearImplementationDetail")
    CastSelf = TypeVar(
        "CastSelf", bound="GearImplementationDetail._Cast_GearImplementationDetail"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearImplementationDetail",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearImplementationDetail:
    """Special nested class for casting GearImplementationDetail to subclasses."""

    __parent__: "GearImplementationDetail"

    @property
    def gear_design_analysis(self: "CastSelf") -> "_1338.GearDesignAnalysis":
        return self.__parent__._cast(_1338.GearDesignAnalysis)

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1335.AbstractGearAnalysis":
        from mastapy._private.gears.analysis import _1335

        return self.__parent__._cast(_1335.AbstractGearAnalysis)

    @property
    def cylindrical_gear_manufacturing_config(
        self: "CastSelf",
    ) -> "_715.CylindricalGearManufacturingConfig":
        from mastapy._private.gears.manufacturing.cylindrical import _715

        return self.__parent__._cast(_715.CylindricalGearManufacturingConfig)

    @property
    def conical_gear_manufacturing_config(
        self: "CastSelf",
    ) -> "_879.ConicalGearManufacturingConfig":
        from mastapy._private.gears.manufacturing.bevel import _879

        return self.__parent__._cast(_879.ConicalGearManufacturingConfig)

    @property
    def conical_gear_micro_geometry_config(
        self: "CastSelf",
    ) -> "_880.ConicalGearMicroGeometryConfig":
        from mastapy._private.gears.manufacturing.bevel import _880

        return self.__parent__._cast(_880.ConicalGearMicroGeometryConfig)

    @property
    def conical_gear_micro_geometry_config_base(
        self: "CastSelf",
    ) -> "_881.ConicalGearMicroGeometryConfigBase":
        from mastapy._private.gears.manufacturing.bevel import _881

        return self.__parent__._cast(_881.ConicalGearMicroGeometryConfigBase)

    @property
    def conical_pinion_manufacturing_config(
        self: "CastSelf",
    ) -> "_891.ConicalPinionManufacturingConfig":
        from mastapy._private.gears.manufacturing.bevel import _891

        return self.__parent__._cast(_891.ConicalPinionManufacturingConfig)

    @property
    def conical_pinion_micro_geometry_config(
        self: "CastSelf",
    ) -> "_892.ConicalPinionMicroGeometryConfig":
        from mastapy._private.gears.manufacturing.bevel import _892

        return self.__parent__._cast(_892.ConicalPinionMicroGeometryConfig)

    @property
    def conical_wheel_manufacturing_config(
        self: "CastSelf",
    ) -> "_897.ConicalWheelManufacturingConfig":
        from mastapy._private.gears.manufacturing.bevel import _897

        return self.__parent__._cast(_897.ConicalWheelManufacturingConfig)

    @property
    def face_gear_micro_geometry(self: "CastSelf") -> "_1097.FaceGearMicroGeometry":
        from mastapy._private.gears.gear_designs.face import _1097

        return self.__parent__._cast(_1097.FaceGearMicroGeometry)

    @property
    def cylindrical_gear_micro_geometry(
        self: "CastSelf",
    ) -> "_1213.CylindricalGearMicroGeometry":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1213

        return self.__parent__._cast(_1213.CylindricalGearMicroGeometry)

    @property
    def cylindrical_gear_micro_geometry_base(
        self: "CastSelf",
    ) -> "_1214.CylindricalGearMicroGeometryBase":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1214

        return self.__parent__._cast(_1214.CylindricalGearMicroGeometryBase)

    @property
    def cylindrical_gear_micro_geometry_per_tooth(
        self: "CastSelf",
    ) -> "_1217.CylindricalGearMicroGeometryPerTooth":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1217

        return self.__parent__._cast(_1217.CylindricalGearMicroGeometryPerTooth)

    @property
    def gear_fe_model(self: "CastSelf") -> "_1317.GearFEModel":
        from mastapy._private.gears.fe_model import _1317

        return self.__parent__._cast(_1317.GearFEModel)

    @property
    def cylindrical_gear_fe_model(self: "CastSelf") -> "_1321.CylindricalGearFEModel":
        from mastapy._private.gears.fe_model.cylindrical import _1321

        return self.__parent__._cast(_1321.CylindricalGearFEModel)

    @property
    def conical_gear_fe_model(self: "CastSelf") -> "_1324.ConicalGearFEModel":
        from mastapy._private.gears.fe_model.conical import _1324

        return self.__parent__._cast(_1324.ConicalGearFEModel)

    @property
    def gear_implementation_detail(self: "CastSelf") -> "GearImplementationDetail":
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
class GearImplementationDetail(_1338.GearDesignAnalysis):
    """GearImplementationDetail

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_IMPLEMENTATION_DETAIL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def user_specified_data(self: "Self") -> "_1936.UserSpecifiedData":
        """mastapy.utility.scripting.UserSpecifiedData

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UserSpecifiedData")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_GearImplementationDetail":
        """Cast to another type.

        Returns:
            _Cast_GearImplementationDetail
        """
        return _Cast_GearImplementationDetail(self)
