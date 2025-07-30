"""MeshSingleFlankRating"""

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
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_MESH_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating", "MeshSingleFlankRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.gears import _408
    from mastapy._private.gears.rating import _450, _455
    from mastapy._private.gears.rating.bevel.standards import _649, _651, _653
    from mastapy._private.gears.rating.conical import _637
    from mastapy._private.gears.rating.cylindrical import _558
    from mastapy._private.gears.rating.cylindrical.agma import _626
    from mastapy._private.gears.rating.cylindrical.din3990 import _624
    from mastapy._private.gears.rating.cylindrical.iso6336 import (
        _603,
        _605,
        _607,
        _609,
        _611,
    )
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import (
        _581,
        _583,
        _585,
    )
    from mastapy._private.gears.rating.hypoid.standards import _534
    from mastapy._private.gears.rating.iso_10300 import _513, _514, _515, _516, _517
    from mastapy._private.gears.rating.klingelnberg_conical.kn3030 import (
        _505,
        _509,
        _510,
    )

    Self = TypeVar("Self", bound="MeshSingleFlankRating")
    CastSelf = TypeVar(
        "CastSelf", bound="MeshSingleFlankRating._Cast_MeshSingleFlankRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MeshSingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MeshSingleFlankRating:
    """Special nested class for casting MeshSingleFlankRating to subclasses."""

    __parent__: "MeshSingleFlankRating"

    @property
    def klingelnberg_conical_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_505.KlingelnbergConicalMeshSingleFlankRating":
        from mastapy._private.gears.rating.klingelnberg_conical.kn3030 import _505

        return self.__parent__._cast(_505.KlingelnbergConicalMeshSingleFlankRating)

    @property
    def klingelnberg_cyclo_palloid_hypoid_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_509.KlingelnbergCycloPalloidHypoidMeshSingleFlankRating":
        from mastapy._private.gears.rating.klingelnberg_conical.kn3030 import _509

        return self.__parent__._cast(
            _509.KlingelnbergCycloPalloidHypoidMeshSingleFlankRating
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_510.KlingelnbergCycloPalloidSpiralBevelMeshSingleFlankRating":
        from mastapy._private.gears.rating.klingelnberg_conical.kn3030 import _510

        return self.__parent__._cast(
            _510.KlingelnbergCycloPalloidSpiralBevelMeshSingleFlankRating
        )

    @property
    def iso10300_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_513.ISO10300MeshSingleFlankRating":
        from mastapy._private.gears.rating.iso_10300 import _513

        return self.__parent__._cast(_513.ISO10300MeshSingleFlankRating)

    @property
    def iso10300_mesh_single_flank_rating_bevel_method_b2(
        self: "CastSelf",
    ) -> "_514.ISO10300MeshSingleFlankRatingBevelMethodB2":
        from mastapy._private.gears.rating.iso_10300 import _514

        return self.__parent__._cast(_514.ISO10300MeshSingleFlankRatingBevelMethodB2)

    @property
    def iso10300_mesh_single_flank_rating_hypoid_method_b2(
        self: "CastSelf",
    ) -> "_515.ISO10300MeshSingleFlankRatingHypoidMethodB2":
        from mastapy._private.gears.rating.iso_10300 import _515

        return self.__parent__._cast(_515.ISO10300MeshSingleFlankRatingHypoidMethodB2)

    @property
    def iso10300_mesh_single_flank_rating_method_b1(
        self: "CastSelf",
    ) -> "_516.ISO10300MeshSingleFlankRatingMethodB1":
        from mastapy._private.gears.rating.iso_10300 import _516

        return self.__parent__._cast(_516.ISO10300MeshSingleFlankRatingMethodB1)

    @property
    def iso10300_mesh_single_flank_rating_method_b2(
        self: "CastSelf",
    ) -> "_517.ISO10300MeshSingleFlankRatingMethodB2":
        from mastapy._private.gears.rating.iso_10300 import _517

        return self.__parent__._cast(_517.ISO10300MeshSingleFlankRatingMethodB2)

    @property
    def gleason_hypoid_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_534.GleasonHypoidMeshSingleFlankRating":
        from mastapy._private.gears.rating.hypoid.standards import _534

        return self.__parent__._cast(_534.GleasonHypoidMeshSingleFlankRating)

    @property
    def cylindrical_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_558.CylindricalMeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical import _558

        return self.__parent__._cast(_558.CylindricalMeshSingleFlankRating)

    @property
    def metal_plastic_or_plastic_metal_vdi2736_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_581.MetalPlasticOrPlasticMetalVDI2736MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _581

        return self.__parent__._cast(
            _581.MetalPlasticOrPlasticMetalVDI2736MeshSingleFlankRating
        )

    @property
    def plastic_gear_vdi2736_abstract_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_583.PlasticGearVDI2736AbstractMeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _583

        return self.__parent__._cast(
            _583.PlasticGearVDI2736AbstractMeshSingleFlankRating
        )

    @property
    def plastic_plastic_vdi2736_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_585.PlasticPlasticVDI2736MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _585

        return self.__parent__._cast(_585.PlasticPlasticVDI2736MeshSingleFlankRating)

    @property
    def iso63361996_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_603.ISO63361996MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _603

        return self.__parent__._cast(_603.ISO63361996MeshSingleFlankRating)

    @property
    def iso63362006_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_605.ISO63362006MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _605

        return self.__parent__._cast(_605.ISO63362006MeshSingleFlankRating)

    @property
    def iso63362019_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_607.ISO63362019MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _607

        return self.__parent__._cast(_607.ISO63362019MeshSingleFlankRating)

    @property
    def iso6336_abstract_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_609.ISO6336AbstractMeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _609

        return self.__parent__._cast(_609.ISO6336AbstractMeshSingleFlankRating)

    @property
    def iso6336_abstract_metal_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_611.ISO6336AbstractMetalMeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _611

        return self.__parent__._cast(_611.ISO6336AbstractMetalMeshSingleFlankRating)

    @property
    def din3990_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_624.DIN3990MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.din3990 import _624

        return self.__parent__._cast(_624.DIN3990MeshSingleFlankRating)

    @property
    def agma2101_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_626.AGMA2101MeshSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.agma import _626

        return self.__parent__._cast(_626.AGMA2101MeshSingleFlankRating)

    @property
    def conical_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_637.ConicalMeshSingleFlankRating":
        from mastapy._private.gears.rating.conical import _637

        return self.__parent__._cast(_637.ConicalMeshSingleFlankRating)

    @property
    def agma_spiral_bevel_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_649.AGMASpiralBevelMeshSingleFlankRating":
        from mastapy._private.gears.rating.bevel.standards import _649

        return self.__parent__._cast(_649.AGMASpiralBevelMeshSingleFlankRating)

    @property
    def gleason_spiral_bevel_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_651.GleasonSpiralBevelMeshSingleFlankRating":
        from mastapy._private.gears.rating.bevel.standards import _651

        return self.__parent__._cast(_651.GleasonSpiralBevelMeshSingleFlankRating)

    @property
    def spiral_bevel_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_653.SpiralBevelMeshSingleFlankRating":
        from mastapy._private.gears.rating.bevel.standards import _653

        return self.__parent__._cast(_653.SpiralBevelMeshSingleFlankRating)

    @property
    def mesh_single_flank_rating(self: "CastSelf") -> "MeshSingleFlankRating":
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
class MeshSingleFlankRating(_0.APIBase):
    """MeshSingleFlankRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MESH_SINGLE_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def coefficient_of_friction_calculation_method(
        self: "Self",
    ) -> "_408.CoefficientOfFrictionCalculationMethod":
        """mastapy.gears.CoefficientOfFrictionCalculationMethod"""
        temp = pythonnet_property_get(
            self.wrapped, "CoefficientOfFrictionCalculationMethod"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.CoefficientOfFrictionCalculationMethod"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears._408", "CoefficientOfFrictionCalculationMethod"
        )(value)

    @coefficient_of_friction_calculation_method.setter
    @exception_bridge
    @enforce_parameter_types
    def coefficient_of_friction_calculation_method(
        self: "Self", value: "_408.CoefficientOfFrictionCalculationMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.CoefficientOfFrictionCalculationMethod"
        )
        pythonnet_property_set(
            self.wrapped, "CoefficientOfFrictionCalculationMethod", value
        )

    @property
    @exception_bridge
    def efficiency_rating_method(self: "Self") -> "_450.GearMeshEfficiencyRatingMethod":
        """mastapy.gears.rating.GearMeshEfficiencyRatingMethod"""
        temp = pythonnet_property_get(self.wrapped, "EfficiencyRatingMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.Rating.GearMeshEfficiencyRatingMethod"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.rating._450", "GearMeshEfficiencyRatingMethod"
        )(value)

    @efficiency_rating_method.setter
    @exception_bridge
    @enforce_parameter_types
    def efficiency_rating_method(
        self: "Self", value: "_450.GearMeshEfficiencyRatingMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.Rating.GearMeshEfficiencyRatingMethod"
        )
        pythonnet_property_set(self.wrapped, "EfficiencyRatingMethod", value)

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
    def power(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Power")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def rating_standard_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RatingStandardName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def gear_single_flank_ratings(self: "Self") -> "List[_455.GearSingleFlankRating]":
        """List[mastapy.gears.rating.GearSingleFlankRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSingleFlankRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

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
    def cast_to(self: "Self") -> "_Cast_MeshSingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_MeshSingleFlankRating
        """
        return _Cast_MeshSingleFlankRating(self)
