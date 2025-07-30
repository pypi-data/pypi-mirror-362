"""GearDesignComponent"""

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

_GEAR_DESIGN_COMPONENT = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns", "GearDesignComponent"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.gears.gear_designs import _1051, _1053, _1054
    from mastapy._private.gears.gear_designs.agma_gleason_conical import (
        _1313,
        _1314,
        _1315,
        _1316,
    )
    from mastapy._private.gears.gear_designs.bevel import _1300, _1301, _1302, _1303
    from mastapy._private.gears.gear_designs.concept import _1296, _1297, _1298
    from mastapy._private.gears.gear_designs.conical import _1274, _1275, _1276, _1279
    from mastapy._private.gears.gear_designs.cylindrical import (
        _1122,
        _1128,
        _1138,
        _1151,
        _1152,
    )
    from mastapy._private.gears.gear_designs.face import (
        _1093,
        _1095,
        _1098,
        _1099,
        _1101,
    )
    from mastapy._private.gears.gear_designs.hypoid import _1089, _1090, _1091, _1092
    from mastapy._private.gears.gear_designs.klingelnberg_conical import (
        _1085,
        _1086,
        _1087,
        _1088,
    )
    from mastapy._private.gears.gear_designs.klingelnberg_hypoid import (
        _1081,
        _1082,
        _1083,
        _1084,
    )
    from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import (
        _1077,
        _1078,
        _1079,
        _1080,
    )
    from mastapy._private.gears.gear_designs.spiral_bevel import (
        _1073,
        _1074,
        _1075,
        _1076,
    )
    from mastapy._private.gears.gear_designs.straight_bevel import (
        _1065,
        _1066,
        _1067,
        _1068,
    )
    from mastapy._private.gears.gear_designs.straight_bevel_diff import (
        _1069,
        _1070,
        _1071,
        _1072,
    )
    from mastapy._private.gears.gear_designs.worm import (
        _1060,
        _1061,
        _1062,
        _1063,
        _1064,
    )
    from mastapy._private.gears.gear_designs.zerol_bevel import (
        _1056,
        _1057,
        _1058,
        _1059,
    )
    from mastapy._private.utility.scripting import _1936

    Self = TypeVar("Self", bound="GearDesignComponent")
    CastSelf = TypeVar(
        "CastSelf", bound="GearDesignComponent._Cast_GearDesignComponent"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearDesignComponent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearDesignComponent:
    """Special nested class for casting GearDesignComponent to subclasses."""

    __parent__: "GearDesignComponent"

    @property
    def gear_design(self: "CastSelf") -> "_1051.GearDesign":
        from mastapy._private.gears.gear_designs import _1051

        return self.__parent__._cast(_1051.GearDesign)

    @property
    def gear_mesh_design(self: "CastSelf") -> "_1053.GearMeshDesign":
        from mastapy._private.gears.gear_designs import _1053

        return self.__parent__._cast(_1053.GearMeshDesign)

    @property
    def gear_set_design(self: "CastSelf") -> "_1054.GearSetDesign":
        from mastapy._private.gears.gear_designs import _1054

        return self.__parent__._cast(_1054.GearSetDesign)

    @property
    def zerol_bevel_gear_design(self: "CastSelf") -> "_1056.ZerolBevelGearDesign":
        from mastapy._private.gears.gear_designs.zerol_bevel import _1056

        return self.__parent__._cast(_1056.ZerolBevelGearDesign)

    @property
    def zerol_bevel_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1057.ZerolBevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.zerol_bevel import _1057

        return self.__parent__._cast(_1057.ZerolBevelGearMeshDesign)

    @property
    def zerol_bevel_gear_set_design(
        self: "CastSelf",
    ) -> "_1058.ZerolBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.zerol_bevel import _1058

        return self.__parent__._cast(_1058.ZerolBevelGearSetDesign)

    @property
    def zerol_bevel_meshed_gear_design(
        self: "CastSelf",
    ) -> "_1059.ZerolBevelMeshedGearDesign":
        from mastapy._private.gears.gear_designs.zerol_bevel import _1059

        return self.__parent__._cast(_1059.ZerolBevelMeshedGearDesign)

    @property
    def worm_design(self: "CastSelf") -> "_1060.WormDesign":
        from mastapy._private.gears.gear_designs.worm import _1060

        return self.__parent__._cast(_1060.WormDesign)

    @property
    def worm_gear_design(self: "CastSelf") -> "_1061.WormGearDesign":
        from mastapy._private.gears.gear_designs.worm import _1061

        return self.__parent__._cast(_1061.WormGearDesign)

    @property
    def worm_gear_mesh_design(self: "CastSelf") -> "_1062.WormGearMeshDesign":
        from mastapy._private.gears.gear_designs.worm import _1062

        return self.__parent__._cast(_1062.WormGearMeshDesign)

    @property
    def worm_gear_set_design(self: "CastSelf") -> "_1063.WormGearSetDesign":
        from mastapy._private.gears.gear_designs.worm import _1063

        return self.__parent__._cast(_1063.WormGearSetDesign)

    @property
    def worm_wheel_design(self: "CastSelf") -> "_1064.WormWheelDesign":
        from mastapy._private.gears.gear_designs.worm import _1064

        return self.__parent__._cast(_1064.WormWheelDesign)

    @property
    def straight_bevel_gear_design(self: "CastSelf") -> "_1065.StraightBevelGearDesign":
        from mastapy._private.gears.gear_designs.straight_bevel import _1065

        return self.__parent__._cast(_1065.StraightBevelGearDesign)

    @property
    def straight_bevel_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1066.StraightBevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.straight_bevel import _1066

        return self.__parent__._cast(_1066.StraightBevelGearMeshDesign)

    @property
    def straight_bevel_gear_set_design(
        self: "CastSelf",
    ) -> "_1067.StraightBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.straight_bevel import _1067

        return self.__parent__._cast(_1067.StraightBevelGearSetDesign)

    @property
    def straight_bevel_meshed_gear_design(
        self: "CastSelf",
    ) -> "_1068.StraightBevelMeshedGearDesign":
        from mastapy._private.gears.gear_designs.straight_bevel import _1068

        return self.__parent__._cast(_1068.StraightBevelMeshedGearDesign)

    @property
    def straight_bevel_diff_gear_design(
        self: "CastSelf",
    ) -> "_1069.StraightBevelDiffGearDesign":
        from mastapy._private.gears.gear_designs.straight_bevel_diff import _1069

        return self.__parent__._cast(_1069.StraightBevelDiffGearDesign)

    @property
    def straight_bevel_diff_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1070.StraightBevelDiffGearMeshDesign":
        from mastapy._private.gears.gear_designs.straight_bevel_diff import _1070

        return self.__parent__._cast(_1070.StraightBevelDiffGearMeshDesign)

    @property
    def straight_bevel_diff_gear_set_design(
        self: "CastSelf",
    ) -> "_1071.StraightBevelDiffGearSetDesign":
        from mastapy._private.gears.gear_designs.straight_bevel_diff import _1071

        return self.__parent__._cast(_1071.StraightBevelDiffGearSetDesign)

    @property
    def straight_bevel_diff_meshed_gear_design(
        self: "CastSelf",
    ) -> "_1072.StraightBevelDiffMeshedGearDesign":
        from mastapy._private.gears.gear_designs.straight_bevel_diff import _1072

        return self.__parent__._cast(_1072.StraightBevelDiffMeshedGearDesign)

    @property
    def spiral_bevel_gear_design(self: "CastSelf") -> "_1073.SpiralBevelGearDesign":
        from mastapy._private.gears.gear_designs.spiral_bevel import _1073

        return self.__parent__._cast(_1073.SpiralBevelGearDesign)

    @property
    def spiral_bevel_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1074.SpiralBevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.spiral_bevel import _1074

        return self.__parent__._cast(_1074.SpiralBevelGearMeshDesign)

    @property
    def spiral_bevel_gear_set_design(
        self: "CastSelf",
    ) -> "_1075.SpiralBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.spiral_bevel import _1075

        return self.__parent__._cast(_1075.SpiralBevelGearSetDesign)

    @property
    def spiral_bevel_meshed_gear_design(
        self: "CastSelf",
    ) -> "_1076.SpiralBevelMeshedGearDesign":
        from mastapy._private.gears.gear_designs.spiral_bevel import _1076

        return self.__parent__._cast(_1076.SpiralBevelMeshedGearDesign)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_design(
        self: "CastSelf",
    ) -> "_1077.KlingelnbergCycloPalloidSpiralBevelGearDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1077

        return self.__parent__._cast(
            _1077.KlingelnbergCycloPalloidSpiralBevelGearDesign
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1078.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1078

        return self.__parent__._cast(
            _1078.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_design(
        self: "CastSelf",
    ) -> "_1079.KlingelnbergCycloPalloidSpiralBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1079

        return self.__parent__._cast(
            _1079.KlingelnbergCycloPalloidSpiralBevelGearSetDesign
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshed_gear_design(
        self: "CastSelf",
    ) -> "_1080.KlingelnbergCycloPalloidSpiralBevelMeshedGearDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1080

        return self.__parent__._cast(
            _1080.KlingelnbergCycloPalloidSpiralBevelMeshedGearDesign
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_design(
        self: "CastSelf",
    ) -> "_1081.KlingelnbergCycloPalloidHypoidGearDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1081

        return self.__parent__._cast(_1081.KlingelnbergCycloPalloidHypoidGearDesign)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1082.KlingelnbergCycloPalloidHypoidGearMeshDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1082

        return self.__parent__._cast(_1082.KlingelnbergCycloPalloidHypoidGearMeshDesign)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_design(
        self: "CastSelf",
    ) -> "_1083.KlingelnbergCycloPalloidHypoidGearSetDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1083

        return self.__parent__._cast(_1083.KlingelnbergCycloPalloidHypoidGearSetDesign)

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshed_gear_design(
        self: "CastSelf",
    ) -> "_1084.KlingelnbergCycloPalloidHypoidMeshedGearDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1084

        return self.__parent__._cast(
            _1084.KlingelnbergCycloPalloidHypoidMeshedGearDesign
        )

    @property
    def klingelnberg_conical_gear_design(
        self: "CastSelf",
    ) -> "_1085.KlingelnbergConicalGearDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_conical import _1085

        return self.__parent__._cast(_1085.KlingelnbergConicalGearDesign)

    @property
    def klingelnberg_conical_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1086.KlingelnbergConicalGearMeshDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_conical import _1086

        return self.__parent__._cast(_1086.KlingelnbergConicalGearMeshDesign)

    @property
    def klingelnberg_conical_gear_set_design(
        self: "CastSelf",
    ) -> "_1087.KlingelnbergConicalGearSetDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_conical import _1087

        return self.__parent__._cast(_1087.KlingelnbergConicalGearSetDesign)

    @property
    def klingelnberg_conical_meshed_gear_design(
        self: "CastSelf",
    ) -> "_1088.KlingelnbergConicalMeshedGearDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_conical import _1088

        return self.__parent__._cast(_1088.KlingelnbergConicalMeshedGearDesign)

    @property
    def hypoid_gear_design(self: "CastSelf") -> "_1089.HypoidGearDesign":
        from mastapy._private.gears.gear_designs.hypoid import _1089

        return self.__parent__._cast(_1089.HypoidGearDesign)

    @property
    def hypoid_gear_mesh_design(self: "CastSelf") -> "_1090.HypoidGearMeshDesign":
        from mastapy._private.gears.gear_designs.hypoid import _1090

        return self.__parent__._cast(_1090.HypoidGearMeshDesign)

    @property
    def hypoid_gear_set_design(self: "CastSelf") -> "_1091.HypoidGearSetDesign":
        from mastapy._private.gears.gear_designs.hypoid import _1091

        return self.__parent__._cast(_1091.HypoidGearSetDesign)

    @property
    def hypoid_meshed_gear_design(self: "CastSelf") -> "_1092.HypoidMeshedGearDesign":
        from mastapy._private.gears.gear_designs.hypoid import _1092

        return self.__parent__._cast(_1092.HypoidMeshedGearDesign)

    @property
    def face_gear_design(self: "CastSelf") -> "_1093.FaceGearDesign":
        from mastapy._private.gears.gear_designs.face import _1093

        return self.__parent__._cast(_1093.FaceGearDesign)

    @property
    def face_gear_mesh_design(self: "CastSelf") -> "_1095.FaceGearMeshDesign":
        from mastapy._private.gears.gear_designs.face import _1095

        return self.__parent__._cast(_1095.FaceGearMeshDesign)

    @property
    def face_gear_pinion_design(self: "CastSelf") -> "_1098.FaceGearPinionDesign":
        from mastapy._private.gears.gear_designs.face import _1098

        return self.__parent__._cast(_1098.FaceGearPinionDesign)

    @property
    def face_gear_set_design(self: "CastSelf") -> "_1099.FaceGearSetDesign":
        from mastapy._private.gears.gear_designs.face import _1099

        return self.__parent__._cast(_1099.FaceGearSetDesign)

    @property
    def face_gear_wheel_design(self: "CastSelf") -> "_1101.FaceGearWheelDesign":
        from mastapy._private.gears.gear_designs.face import _1101

        return self.__parent__._cast(_1101.FaceGearWheelDesign)

    @property
    def cylindrical_gear_design(self: "CastSelf") -> "_1122.CylindricalGearDesign":
        from mastapy._private.gears.gear_designs.cylindrical import _1122

        return self.__parent__._cast(_1122.CylindricalGearDesign)

    @property
    def cylindrical_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1128.CylindricalGearMeshDesign":
        from mastapy._private.gears.gear_designs.cylindrical import _1128

        return self.__parent__._cast(_1128.CylindricalGearMeshDesign)

    @property
    def cylindrical_gear_set_design(
        self: "CastSelf",
    ) -> "_1138.CylindricalGearSetDesign":
        from mastapy._private.gears.gear_designs.cylindrical import _1138

        return self.__parent__._cast(_1138.CylindricalGearSetDesign)

    @property
    def cylindrical_planetary_gear_set_design(
        self: "CastSelf",
    ) -> "_1151.CylindricalPlanetaryGearSetDesign":
        from mastapy._private.gears.gear_designs.cylindrical import _1151

        return self.__parent__._cast(_1151.CylindricalPlanetaryGearSetDesign)

    @property
    def cylindrical_planet_gear_design(
        self: "CastSelf",
    ) -> "_1152.CylindricalPlanetGearDesign":
        from mastapy._private.gears.gear_designs.cylindrical import _1152

        return self.__parent__._cast(_1152.CylindricalPlanetGearDesign)

    @property
    def conical_gear_design(self: "CastSelf") -> "_1274.ConicalGearDesign":
        from mastapy._private.gears.gear_designs.conical import _1274

        return self.__parent__._cast(_1274.ConicalGearDesign)

    @property
    def conical_gear_mesh_design(self: "CastSelf") -> "_1275.ConicalGearMeshDesign":
        from mastapy._private.gears.gear_designs.conical import _1275

        return self.__parent__._cast(_1275.ConicalGearMeshDesign)

    @property
    def conical_gear_set_design(self: "CastSelf") -> "_1276.ConicalGearSetDesign":
        from mastapy._private.gears.gear_designs.conical import _1276

        return self.__parent__._cast(_1276.ConicalGearSetDesign)

    @property
    def conical_meshed_gear_design(self: "CastSelf") -> "_1279.ConicalMeshedGearDesign":
        from mastapy._private.gears.gear_designs.conical import _1279

        return self.__parent__._cast(_1279.ConicalMeshedGearDesign)

    @property
    def concept_gear_design(self: "CastSelf") -> "_1296.ConceptGearDesign":
        from mastapy._private.gears.gear_designs.concept import _1296

        return self.__parent__._cast(_1296.ConceptGearDesign)

    @property
    def concept_gear_mesh_design(self: "CastSelf") -> "_1297.ConceptGearMeshDesign":
        from mastapy._private.gears.gear_designs.concept import _1297

        return self.__parent__._cast(_1297.ConceptGearMeshDesign)

    @property
    def concept_gear_set_design(self: "CastSelf") -> "_1298.ConceptGearSetDesign":
        from mastapy._private.gears.gear_designs.concept import _1298

        return self.__parent__._cast(_1298.ConceptGearSetDesign)

    @property
    def bevel_gear_design(self: "CastSelf") -> "_1300.BevelGearDesign":
        from mastapy._private.gears.gear_designs.bevel import _1300

        return self.__parent__._cast(_1300.BevelGearDesign)

    @property
    def bevel_gear_mesh_design(self: "CastSelf") -> "_1301.BevelGearMeshDesign":
        from mastapy._private.gears.gear_designs.bevel import _1301

        return self.__parent__._cast(_1301.BevelGearMeshDesign)

    @property
    def bevel_gear_set_design(self: "CastSelf") -> "_1302.BevelGearSetDesign":
        from mastapy._private.gears.gear_designs.bevel import _1302

        return self.__parent__._cast(_1302.BevelGearSetDesign)

    @property
    def bevel_meshed_gear_design(self: "CastSelf") -> "_1303.BevelMeshedGearDesign":
        from mastapy._private.gears.gear_designs.bevel import _1303

        return self.__parent__._cast(_1303.BevelMeshedGearDesign)

    @property
    def agma_gleason_conical_gear_design(
        self: "CastSelf",
    ) -> "_1313.AGMAGleasonConicalGearDesign":
        from mastapy._private.gears.gear_designs.agma_gleason_conical import _1313

        return self.__parent__._cast(_1313.AGMAGleasonConicalGearDesign)

    @property
    def agma_gleason_conical_gear_mesh_design(
        self: "CastSelf",
    ) -> "_1314.AGMAGleasonConicalGearMeshDesign":
        from mastapy._private.gears.gear_designs.agma_gleason_conical import _1314

        return self.__parent__._cast(_1314.AGMAGleasonConicalGearMeshDesign)

    @property
    def agma_gleason_conical_gear_set_design(
        self: "CastSelf",
    ) -> "_1315.AGMAGleasonConicalGearSetDesign":
        from mastapy._private.gears.gear_designs.agma_gleason_conical import _1315

        return self.__parent__._cast(_1315.AGMAGleasonConicalGearSetDesign)

    @property
    def agma_gleason_conical_meshed_gear_design(
        self: "CastSelf",
    ) -> "_1316.AGMAGleasonConicalMeshedGearDesign":
        from mastapy._private.gears.gear_designs.agma_gleason_conical import _1316

        return self.__parent__._cast(_1316.AGMAGleasonConicalMeshedGearDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "GearDesignComponent":
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
class GearDesignComponent(_0.APIBase):
    """GearDesignComponent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_DESIGN_COMPONENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @name.setter
    @exception_bridge
    @enforce_parameter_types
    def name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Name", str(value) if value is not None else ""
        )

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
    def dispose(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Dispose")

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

    def __enter__(self: "Self") -> None:
        return self

    def __exit__(
        self: "Self", exception_type: "Any", exception_value: "Any", traceback: "Any"
    ) -> None:
        self.dispose()

    @property
    def cast_to(self: "Self") -> "_Cast_GearDesignComponent":
        """Cast to another type.

        Returns:
            _Cast_GearDesignComponent
        """
        return _Cast_GearDesignComponent(self)
