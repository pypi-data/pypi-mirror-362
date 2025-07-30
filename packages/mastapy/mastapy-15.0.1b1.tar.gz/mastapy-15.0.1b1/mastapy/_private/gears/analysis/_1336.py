"""AbstractGearMeshAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_ABSTRACT_GEAR_MESH_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.Analysis", "AbstractGearMeshAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.gears.analysis import _1335, _1342, _1343, _1344, _1345
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
    from mastapy._private.gears.rating import _443, _451, _456
    from mastapy._private.gears.rating.agma_gleason_conical import _656
    from mastapy._private.gears.rating.bevel import _645
    from mastapy._private.gears.rating.concept import _640, _641
    from mastapy._private.gears.rating.conical import _630, _635
    from mastapy._private.gears.rating.cylindrical import _549, _557
    from mastapy._private.gears.rating.face import _537, _538
    from mastapy._private.gears.rating.hypoid import _529
    from mastapy._private.gears.rating.klingelnberg_conical import _502
    from mastapy._private.gears.rating.klingelnberg_hypoid import _499
    from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _496
    from mastapy._private.gears.rating.spiral_bevel import _493
    from mastapy._private.gears.rating.straight_bevel import _486
    from mastapy._private.gears.rating.straight_bevel_diff import _489
    from mastapy._private.gears.rating.worm import _464, _468
    from mastapy._private.gears.rating.zerol_bevel import _460

    Self = TypeVar("Self", bound="AbstractGearMeshAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="AbstractGearMeshAnalysis._Cast_AbstractGearMeshAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractGearMeshAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractGearMeshAnalysis:
    """Special nested class for casting AbstractGearMeshAnalysis to subclasses."""

    __parent__: "AbstractGearMeshAnalysis"

    @property
    def abstract_gear_mesh_rating(self: "CastSelf") -> "_443.AbstractGearMeshRating":
        from mastapy._private.gears.rating import _443

        return self.__parent__._cast(_443.AbstractGearMeshRating)

    @property
    def gear_mesh_rating(self: "CastSelf") -> "_451.GearMeshRating":
        from mastapy._private.gears.rating import _451

        return self.__parent__._cast(_451.GearMeshRating)

    @property
    def mesh_duty_cycle_rating(self: "CastSelf") -> "_456.MeshDutyCycleRating":
        from mastapy._private.gears.rating import _456

        return self.__parent__._cast(_456.MeshDutyCycleRating)

    @property
    def zerol_bevel_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_460.ZerolBevelGearMeshRating":
        from mastapy._private.gears.rating.zerol_bevel import _460

        return self.__parent__._cast(_460.ZerolBevelGearMeshRating)

    @property
    def worm_gear_mesh_rating(self: "CastSelf") -> "_464.WormGearMeshRating":
        from mastapy._private.gears.rating.worm import _464

        return self.__parent__._cast(_464.WormGearMeshRating)

    @property
    def worm_mesh_duty_cycle_rating(self: "CastSelf") -> "_468.WormMeshDutyCycleRating":
        from mastapy._private.gears.rating.worm import _468

        return self.__parent__._cast(_468.WormMeshDutyCycleRating)

    @property
    def straight_bevel_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_486.StraightBevelGearMeshRating":
        from mastapy._private.gears.rating.straight_bevel import _486

        return self.__parent__._cast(_486.StraightBevelGearMeshRating)

    @property
    def straight_bevel_diff_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_489.StraightBevelDiffGearMeshRating":
        from mastapy._private.gears.rating.straight_bevel_diff import _489

        return self.__parent__._cast(_489.StraightBevelDiffGearMeshRating)

    @property
    def spiral_bevel_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_493.SpiralBevelGearMeshRating":
        from mastapy._private.gears.rating.spiral_bevel import _493

        return self.__parent__._cast(_493.SpiralBevelGearMeshRating)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_496.KlingelnbergCycloPalloidSpiralBevelGearMeshRating":
        from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _496

        return self.__parent__._cast(
            _496.KlingelnbergCycloPalloidSpiralBevelGearMeshRating
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_499.KlingelnbergCycloPalloidHypoidGearMeshRating":
        from mastapy._private.gears.rating.klingelnberg_hypoid import _499

        return self.__parent__._cast(_499.KlingelnbergCycloPalloidHypoidGearMeshRating)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_502.KlingelnbergCycloPalloidConicalGearMeshRating":
        from mastapy._private.gears.rating.klingelnberg_conical import _502

        return self.__parent__._cast(_502.KlingelnbergCycloPalloidConicalGearMeshRating)

    @property
    def hypoid_gear_mesh_rating(self: "CastSelf") -> "_529.HypoidGearMeshRating":
        from mastapy._private.gears.rating.hypoid import _529

        return self.__parent__._cast(_529.HypoidGearMeshRating)

    @property
    def face_gear_mesh_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_537.FaceGearMeshDutyCycleRating":
        from mastapy._private.gears.rating.face import _537

        return self.__parent__._cast(_537.FaceGearMeshDutyCycleRating)

    @property
    def face_gear_mesh_rating(self: "CastSelf") -> "_538.FaceGearMeshRating":
        from mastapy._private.gears.rating.face import _538

        return self.__parent__._cast(_538.FaceGearMeshRating)

    @property
    def cylindrical_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_549.CylindricalGearMeshRating":
        from mastapy._private.gears.rating.cylindrical import _549

        return self.__parent__._cast(_549.CylindricalGearMeshRating)

    @property
    def cylindrical_mesh_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_557.CylindricalMeshDutyCycleRating":
        from mastapy._private.gears.rating.cylindrical import _557

        return self.__parent__._cast(_557.CylindricalMeshDutyCycleRating)

    @property
    def conical_gear_mesh_rating(self: "CastSelf") -> "_630.ConicalGearMeshRating":
        from mastapy._private.gears.rating.conical import _630

        return self.__parent__._cast(_630.ConicalGearMeshRating)

    @property
    def conical_mesh_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_635.ConicalMeshDutyCycleRating":
        from mastapy._private.gears.rating.conical import _635

        return self.__parent__._cast(_635.ConicalMeshDutyCycleRating)

    @property
    def concept_gear_mesh_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_640.ConceptGearMeshDutyCycleRating":
        from mastapy._private.gears.rating.concept import _640

        return self.__parent__._cast(_640.ConceptGearMeshDutyCycleRating)

    @property
    def concept_gear_mesh_rating(self: "CastSelf") -> "_641.ConceptGearMeshRating":
        from mastapy._private.gears.rating.concept import _641

        return self.__parent__._cast(_641.ConceptGearMeshRating)

    @property
    def bevel_gear_mesh_rating(self: "CastSelf") -> "_645.BevelGearMeshRating":
        from mastapy._private.gears.rating.bevel import _645

        return self.__parent__._cast(_645.BevelGearMeshRating)

    @property
    def agma_gleason_conical_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_656.AGMAGleasonConicalGearMeshRating":
        from mastapy._private.gears.rating.agma_gleason_conical import _656

        return self.__parent__._cast(_656.AGMAGleasonConicalGearMeshRating)

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
    def gear_mesh_design_analysis(self: "CastSelf") -> "_1342.GearMeshDesignAnalysis":
        from mastapy._private.gears.analysis import _1342

        return self.__parent__._cast(_1342.GearMeshDesignAnalysis)

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
    def abstract_gear_mesh_analysis(self: "CastSelf") -> "AbstractGearMeshAnalysis":
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
class AbstractGearMeshAnalysis(_0.APIBase):
    """AbstractGearMeshAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_GEAR_MESH_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def mesh_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def gear_a(self: "Self") -> "_1335.AbstractGearAnalysis":
        """mastapy.gears.analysis.AbstractGearAnalysis

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
    def gear_b(self: "Self") -> "_1335.AbstractGearAnalysis":
        """mastapy.gears.analysis.AbstractGearAnalysis

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
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @exception_bridge
    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputDefaultReportTo", file_path)

    @exception_bridge
    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportTo", file_path)

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportAsTextTo", file_path)

    @exception_bridge
    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractGearMeshAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AbstractGearMeshAnalysis
        """
        return _Cast_AbstractGearMeshAnalysis(self)
