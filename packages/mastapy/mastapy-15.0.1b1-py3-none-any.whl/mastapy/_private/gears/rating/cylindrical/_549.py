"""CylindricalGearMeshRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating import _451

_CYLINDRICAL_GEAR_MESH_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical", "CylindricalGearMeshRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears import _412, _431
    from mastapy._private.gears.analysis import _1336
    from mastapy._private.gears.gear_designs.cylindrical import _1128
    from mastapy._private.gears.load_case.cylindrical import _987
    from mastapy._private.gears.rating import _443
    from mastapy._private.gears.rating.cylindrical import _551, _555, _558
    from mastapy._private.gears.rating.cylindrical.agma import _626
    from mastapy._private.gears.rating.cylindrical.iso6336 import _611
    from mastapy._private.gears.rating.cylindrical.vdi import _580
    from mastapy._private.utility_gui.charts import _2070

    Self = TypeVar("Self", bound="CylindricalGearMeshRating")
    CastSelf = TypeVar(
        "CastSelf", bound="CylindricalGearMeshRating._Cast_CylindricalGearMeshRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearMeshRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearMeshRating:
    """Special nested class for casting CylindricalGearMeshRating to subclasses."""

    __parent__: "CylindricalGearMeshRating"

    @property
    def gear_mesh_rating(self: "CastSelf") -> "_451.GearMeshRating":
        return self.__parent__._cast(_451.GearMeshRating)

    @property
    def abstract_gear_mesh_rating(self: "CastSelf") -> "_443.AbstractGearMeshRating":
        from mastapy._private.gears.rating import _443

        return self.__parent__._cast(_443.AbstractGearMeshRating)

    @property
    def abstract_gear_mesh_analysis(
        self: "CastSelf",
    ) -> "_1336.AbstractGearMeshAnalysis":
        from mastapy._private.gears.analysis import _1336

        return self.__parent__._cast(_1336.AbstractGearMeshAnalysis)

    @property
    def cylindrical_gear_mesh_rating(self: "CastSelf") -> "CylindricalGearMeshRating":
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
class CylindricalGearMeshRating(_451.GearMeshRating):
    """CylindricalGearMeshRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_MESH_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def active_flank(self: "Self") -> "_412.CylindricalFlanks":
        """mastapy.gears.CylindricalFlanks

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveFlank")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Gears.CylindricalFlanks")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears._412", "CylindricalFlanks"
        )(value)

    @property
    @exception_bridge
    def iso14179_part_2_tooth_loss_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISO14179Part2ToothLossFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_intensity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadIntensity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_sharing_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadSharingFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_sharing_factor_source(
        self: "Self",
    ) -> "_431.PlanetaryRatingLoadSharingOption":
        """mastapy.gears.PlanetaryRatingLoadSharingOption

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadSharingFactorSource")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.PlanetaryRatingLoadSharingOption"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears._431", "PlanetaryRatingLoadSharingOption"
        )(value)

    @property
    @exception_bridge
    def mechanical_advantage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MechanicalAdvantage")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mesh_coefficient_of_friction(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshCoefficientOfFriction")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mesh_coefficient_of_friction_benedict_and_kelley(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MeshCoefficientOfFrictionBenedictAndKelley"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mesh_coefficient_of_friction_drozdov_and_gavrikov(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MeshCoefficientOfFrictionDrozdovAndGavrikov"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mesh_coefficient_of_friction_isotc60(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshCoefficientOfFrictionISOTC60")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mesh_coefficient_of_friction_isotr1417912001(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MeshCoefficientOfFrictionISOTR1417912001"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mesh_coefficient_of_friction_isotr1417912001_with_surface_roughness_parameter(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "MeshCoefficientOfFrictionISOTR1417912001WithSurfaceRoughnessParameter",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mesh_coefficient_of_friction_isotr1417922001_martins_et_al(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MeshCoefficientOfFrictionISOTR1417922001MartinsEtAl"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mesh_coefficient_of_friction_isotr1417922001(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MeshCoefficientOfFrictionISOTR1417922001"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mesh_coefficient_of_friction_misharin(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshCoefficientOfFrictionMisharin")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mesh_coefficient_of_friction_o_donoghue_and_cameron(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MeshCoefficientOfFrictionODonoghueAndCameron"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mesh_coefficient_of_friction_at_diameter_benedict_and_kelley(
        self: "Self",
    ) -> "_2070.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MeshCoefficientOfFrictionAtDiameterBenedictAndKelley"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def no_load_power_loss(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NoLoadPowerLoss")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sliding_ratio_at_end_of_recess(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SlidingRatioAtEndOfRecess")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sliding_ratio_at_start_of_approach(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SlidingRatioAtStartOfApproach")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def agma_cylindrical_mesh_single_flank_rating(
        self: "Self",
    ) -> "_626.AGMA2101MeshSingleFlankRating":
        """mastapy.gears.rating.cylindrical.agma.AGMA2101MeshSingleFlankRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AGMACylindricalMeshSingleFlankRating"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_gear_mesh(self: "Self") -> "_1128.CylindricalGearMeshDesign":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearMeshDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearMesh")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_mesh_single_flank_rating(
        self: "Self",
    ) -> "_558.CylindricalMeshSingleFlankRating":
        """mastapy.gears.rating.cylindrical.CylindricalMeshSingleFlankRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalMeshSingleFlankRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear_set_rating(self: "Self") -> "_555.CylindricalGearSetRating":
        """mastapy.gears.rating.cylindrical.CylindricalGearSetRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSetRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def isodin_cylindrical_mesh_single_flank_rating(
        self: "Self",
    ) -> "_611.ISO6336AbstractMetalMeshSingleFlankRating":
        """mastapy.gears.rating.cylindrical.iso6336.ISO6336AbstractMetalMeshSingleFlankRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ISODINCylindricalMeshSingleFlankRating"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def mesh_load_case(self: "Self") -> "_987.CylindricalMeshLoadCase":
        """mastapy.gears.load_case.cylindrical.CylindricalMeshLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def mesh_single_flank_rating(
        self: "Self",
    ) -> "_558.CylindricalMeshSingleFlankRating":
        """mastapy.gears.rating.cylindrical.CylindricalMeshSingleFlankRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshSingleFlankRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def vdi_cylindrical_gear_single_flank_rating(
        self: "Self",
    ) -> "_580.VDI2737InternalGearSingleFlankRating":
        """mastapy.gears.rating.cylindrical.vdi.VDI2737InternalGearSingleFlankRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "VDICylindricalGearSingleFlankRating"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_gear_ratings(self: "Self") -> "List[_551.CylindricalGearRating]":
        """List[mastapy.gears.rating.cylindrical.CylindricalGearRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearMeshRating":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearMeshRating
        """
        return _Cast_CylindricalGearMeshRating(self)
