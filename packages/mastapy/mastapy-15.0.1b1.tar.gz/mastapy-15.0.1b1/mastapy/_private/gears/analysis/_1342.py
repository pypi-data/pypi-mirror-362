"""GearMeshDesignAnalysis"""

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
from mastapy._private.gears.analysis import _1336

_GEAR_MESH_DESIGN_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.Analysis", "GearMeshDesignAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1338, _1343, _1344, _1345, _1346
    from mastapy._private.gears.fe_model import _1318
    from mastapy._private.gears.fe_model.conical import _1325
    from mastapy._private.gears.fe_model.cylindrical import _1322
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import (
        _1211,
        _1212,
    )
    from mastapy._private.gears.gear_designs.face import _1096
    from mastapy._private.gears.gear_two_d_fe_analysis import _997, _998
    from mastapy._private.gears.load_case import _978
    from mastapy._private.gears.load_case.bevel import _995
    from mastapy._private.gears.load_case.concept import _993
    from mastapy._private.gears.load_case.conical import _990
    from mastapy._private.gears.load_case.cylindrical import _987
    from mastapy._private.gears.load_case.face import _984
    from mastapy._private.gears.load_case.worm import _981
    from mastapy._private.gears.ltca import _944
    from mastapy._private.gears.ltca.conical import _973
    from mastapy._private.gears.ltca.cylindrical import _960
    from mastapy._private.gears.manufacturing.bevel import _887, _888, _889, _890
    from mastapy._private.gears.manufacturing.cylindrical import _721, _722, _725

    Self = TypeVar("Self", bound="GearMeshDesignAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="GearMeshDesignAnalysis._Cast_GearMeshDesignAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshDesignAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMeshDesignAnalysis:
    """Special nested class for casting GearMeshDesignAnalysis to subclasses."""

    __parent__: "GearMeshDesignAnalysis"

    @property
    def abstract_gear_mesh_analysis(
        self: "CastSelf",
    ) -> "_1336.AbstractGearMeshAnalysis":
        return self.__parent__._cast(_1336.AbstractGearMeshAnalysis)

    @property
    def cylindrical_manufactured_gear_mesh_duty_cycle(
        self: "CastSelf",
    ) -> "_721.CylindricalManufacturedGearMeshDutyCycle":
        from mastapy._private.gears.manufacturing.cylindrical import _721

        return self.__parent__._cast(_721.CylindricalManufacturedGearMeshDutyCycle)

    @property
    def cylindrical_manufactured_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_722.CylindricalManufacturedGearMeshLoadCase":
        from mastapy._private.gears.manufacturing.cylindrical import _722

        return self.__parent__._cast(_722.CylindricalManufacturedGearMeshLoadCase)

    @property
    def cylindrical_mesh_manufacturing_config(
        self: "CastSelf",
    ) -> "_725.CylindricalMeshManufacturingConfig":
        from mastapy._private.gears.manufacturing.cylindrical import _725

        return self.__parent__._cast(_725.CylindricalMeshManufacturingConfig)

    @property
    def conical_mesh_manufacturing_analysis(
        self: "CastSelf",
    ) -> "_887.ConicalMeshManufacturingAnalysis":
        from mastapy._private.gears.manufacturing.bevel import _887

        return self.__parent__._cast(_887.ConicalMeshManufacturingAnalysis)

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
    def gear_mesh_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_944.GearMeshLoadDistributionAnalysis":
        from mastapy._private.gears.ltca import _944

        return self.__parent__._cast(_944.GearMeshLoadDistributionAnalysis)

    @property
    def cylindrical_gear_mesh_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_960.CylindricalGearMeshLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.cylindrical import _960

        return self.__parent__._cast(_960.CylindricalGearMeshLoadDistributionAnalysis)

    @property
    def conical_mesh_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_973.ConicalMeshLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.conical import _973

        return self.__parent__._cast(_973.ConicalMeshLoadDistributionAnalysis)

    @property
    def mesh_load_case(self: "CastSelf") -> "_978.MeshLoadCase":
        from mastapy._private.gears.load_case import _978

        return self.__parent__._cast(_978.MeshLoadCase)

    @property
    def worm_mesh_load_case(self: "CastSelf") -> "_981.WormMeshLoadCase":
        from mastapy._private.gears.load_case.worm import _981

        return self.__parent__._cast(_981.WormMeshLoadCase)

    @property
    def face_mesh_load_case(self: "CastSelf") -> "_984.FaceMeshLoadCase":
        from mastapy._private.gears.load_case.face import _984

        return self.__parent__._cast(_984.FaceMeshLoadCase)

    @property
    def cylindrical_mesh_load_case(self: "CastSelf") -> "_987.CylindricalMeshLoadCase":
        from mastapy._private.gears.load_case.cylindrical import _987

        return self.__parent__._cast(_987.CylindricalMeshLoadCase)

    @property
    def conical_mesh_load_case(self: "CastSelf") -> "_990.ConicalMeshLoadCase":
        from mastapy._private.gears.load_case.conical import _990

        return self.__parent__._cast(_990.ConicalMeshLoadCase)

    @property
    def concept_mesh_load_case(self: "CastSelf") -> "_993.ConceptMeshLoadCase":
        from mastapy._private.gears.load_case.concept import _993

        return self.__parent__._cast(_993.ConceptMeshLoadCase)

    @property
    def bevel_mesh_load_case(self: "CastSelf") -> "_995.BevelMeshLoadCase":
        from mastapy._private.gears.load_case.bevel import _995

        return self.__parent__._cast(_995.BevelMeshLoadCase)

    @property
    def cylindrical_gear_mesh_tiff_analysis(
        self: "CastSelf",
    ) -> "_997.CylindricalGearMeshTIFFAnalysis":
        from mastapy._private.gears.gear_two_d_fe_analysis import _997

        return self.__parent__._cast(_997.CylindricalGearMeshTIFFAnalysis)

    @property
    def cylindrical_gear_mesh_tiff_analysis_duty_cycle(
        self: "CastSelf",
    ) -> "_998.CylindricalGearMeshTIFFAnalysisDutyCycle":
        from mastapy._private.gears.gear_two_d_fe_analysis import _998

        return self.__parent__._cast(_998.CylindricalGearMeshTIFFAnalysisDutyCycle)

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
    def cylindrical_gear_mesh_micro_geometry_duty_cycle(
        self: "CastSelf",
    ) -> "_1212.CylindricalGearMeshMicroGeometryDutyCycle":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1212

        return self.__parent__._cast(_1212.CylindricalGearMeshMicroGeometryDutyCycle)

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
    def gear_mesh_implementation_analysis(
        self: "CastSelf",
    ) -> "_1343.GearMeshImplementationAnalysis":
        from mastapy._private.gears.analysis import _1343

        return self.__parent__._cast(_1343.GearMeshImplementationAnalysis)

    @property
    def gear_mesh_implementation_analysis_duty_cycle(
        self: "CastSelf",
    ) -> "_1344.GearMeshImplementationAnalysisDutyCycle":
        from mastapy._private.gears.analysis import _1344

        return self.__parent__._cast(_1344.GearMeshImplementationAnalysisDutyCycle)

    @property
    def gear_mesh_implementation_detail(
        self: "CastSelf",
    ) -> "_1345.GearMeshImplementationDetail":
        from mastapy._private.gears.analysis import _1345

        return self.__parent__._cast(_1345.GearMeshImplementationDetail)

    @property
    def gear_mesh_design_analysis(self: "CastSelf") -> "GearMeshDesignAnalysis":
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
class GearMeshDesignAnalysis(_1336.AbstractGearMeshAnalysis):
    """GearMeshDesignAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESH_DESIGN_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def gear_a(self: "Self") -> "_1338.GearDesignAnalysis":
        """mastapy.gears.analysis.GearDesignAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearA")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear_b(self: "Self") -> "_1338.GearDesignAnalysis":
        """mastapy.gears.analysis.GearDesignAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearB")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear_set(self: "Self") -> "_1346.GearSetDesignAnalysis":
        """mastapy.gears.analysis.GearSetDesignAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSet")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_GearMeshDesignAnalysis":
        """Cast to another type.

        Returns:
            _Cast_GearMeshDesignAnalysis
        """
        return _Cast_GearMeshDesignAnalysis(self)
