"""GearMeshImplementationDetail"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.analysis import _1342

_GEAR_MESH_IMPLEMENTATION_DETAIL = python_net_import(
    "SMT.MastaAPI.Gears.Analysis", "GearMeshImplementationDetail"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1336
    from mastapy._private.gears.fe_model import _1318
    from mastapy._private.gears.fe_model.conical import _1325
    from mastapy._private.gears.fe_model.cylindrical import _1322
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1211
    from mastapy._private.gears.gear_designs.face import _1096
    from mastapy._private.gears.manufacturing.bevel import _888, _889, _890
    from mastapy._private.gears.manufacturing.cylindrical import _725

    Self = TypeVar("Self", bound="GearMeshImplementationDetail")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearMeshImplementationDetail._Cast_GearMeshImplementationDetail",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshImplementationDetail",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMeshImplementationDetail:
    """Special nested class for casting GearMeshImplementationDetail to subclasses."""

    __parent__: "GearMeshImplementationDetail"

    @property
    def gear_mesh_design_analysis(self: "CastSelf") -> "_1342.GearMeshDesignAnalysis":
        return self.__parent__._cast(_1342.GearMeshDesignAnalysis)

    @property
    def abstract_gear_mesh_analysis(
        self: "CastSelf",
    ) -> "_1336.AbstractGearMeshAnalysis":
        from mastapy._private.gears.analysis import _1336

        return self.__parent__._cast(_1336.AbstractGearMeshAnalysis)

    @property
    def cylindrical_mesh_manufacturing_config(
        self: "CastSelf",
    ) -> "_725.CylindricalMeshManufacturingConfig":
        from mastapy._private.gears.manufacturing.cylindrical import _725

        return self.__parent__._cast(_725.CylindricalMeshManufacturingConfig)

    @property
    def conical_mesh_manufacturing_config(
        self: "CastSelf",
    ) -> "_888.ConicalMeshManufacturingConfig":
        from mastapy._private.gears.manufacturing.bevel import _888

        return self.__parent__._cast(_888.ConicalMeshManufacturingConfig)

    @property
    def conical_mesh_micro_geometry_config(
        self: "CastSelf",
    ) -> "_889.ConicalMeshMicroGeometryConfig":
        from mastapy._private.gears.manufacturing.bevel import _889

        return self.__parent__._cast(_889.ConicalMeshMicroGeometryConfig)

    @property
    def conical_mesh_micro_geometry_config_base(
        self: "CastSelf",
    ) -> "_890.ConicalMeshMicroGeometryConfigBase":
        from mastapy._private.gears.manufacturing.bevel import _890

        return self.__parent__._cast(_890.ConicalMeshMicroGeometryConfigBase)

    @property
    def face_gear_mesh_micro_geometry(
        self: "CastSelf",
    ) -> "_1096.FaceGearMeshMicroGeometry":
        from mastapy._private.gears.gear_designs.face import _1096

        return self.__parent__._cast(_1096.FaceGearMeshMicroGeometry)

    @property
    def cylindrical_gear_mesh_micro_geometry(
        self: "CastSelf",
    ) -> "_1211.CylindricalGearMeshMicroGeometry":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1211

        return self.__parent__._cast(_1211.CylindricalGearMeshMicroGeometry)

    @property
    def gear_mesh_fe_model(self: "CastSelf") -> "_1318.GearMeshFEModel":
        from mastapy._private.gears.fe_model import _1318

        return self.__parent__._cast(_1318.GearMeshFEModel)

    @property
    def cylindrical_gear_mesh_fe_model(
        self: "CastSelf",
    ) -> "_1322.CylindricalGearMeshFEModel":
        from mastapy._private.gears.fe_model.cylindrical import _1322

        return self.__parent__._cast(_1322.CylindricalGearMeshFEModel)

    @property
    def conical_mesh_fe_model(self: "CastSelf") -> "_1325.ConicalMeshFEModel":
        from mastapy._private.gears.fe_model.conical import _1325

        return self.__parent__._cast(_1325.ConicalMeshFEModel)

    @property
    def gear_mesh_implementation_detail(
        self: "CastSelf",
    ) -> "GearMeshImplementationDetail":
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
class GearMeshImplementationDetail(_1342.GearMeshDesignAnalysis):
    """GearMeshImplementationDetail

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESH_IMPLEMENTATION_DETAIL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_GearMeshImplementationDetail":
        """Cast to another type.

        Returns:
            _Cast_GearMeshImplementationDetail
        """
        return _Cast_GearMeshImplementationDetail(self)
