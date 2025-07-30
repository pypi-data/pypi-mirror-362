"""ISO6336AbstractGearSingleFlankRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.cylindrical import _556

_ISO6336_ABSTRACT_GEAR_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336",
    "ISO6336AbstractGearSingleFlankRating",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _455
    from mastapy._private.gears.rating.cylindrical.din3990 import _623
    from mastapy._private.gears.rating.cylindrical.iso6336 import _602, _604, _606, _610
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import (
        _582,
        _587,
        _588,
    )

    Self = TypeVar("Self", bound="ISO6336AbstractGearSingleFlankRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ISO6336AbstractGearSingleFlankRating._Cast_ISO6336AbstractGearSingleFlankRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISO6336AbstractGearSingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISO6336AbstractGearSingleFlankRating:
    """Special nested class for casting ISO6336AbstractGearSingleFlankRating to subclasses."""

    __parent__: "ISO6336AbstractGearSingleFlankRating"

    @property
    def cylindrical_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_556.CylindricalGearSingleFlankRating":
        return self.__parent__._cast(_556.CylindricalGearSingleFlankRating)

    @property
    def gear_single_flank_rating(self: "CastSelf") -> "_455.GearSingleFlankRating":
        from mastapy._private.gears.rating import _455

        return self.__parent__._cast(_455.GearSingleFlankRating)

    @property
    def plastic_gear_vdi2736_abstract_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_582.PlasticGearVDI2736AbstractGearSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _582

        return self.__parent__._cast(
            _582.PlasticGearVDI2736AbstractGearSingleFlankRating
        )

    @property
    def plastic_vdi2736_gear_single_flank_rating_in_a_metal_plastic_or_a_plastic_metal_mesh(
        self: "CastSelf",
    ) -> "_587.PlasticVDI2736GearSingleFlankRatingInAMetalPlasticOrAPlasticMetalMesh":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _587

        return self.__parent__._cast(
            _587.PlasticVDI2736GearSingleFlankRatingInAMetalPlasticOrAPlasticMetalMesh
        )

    @property
    def plastic_vdi2736_gear_single_flank_rating_in_a_plastic_plastic_mesh(
        self: "CastSelf",
    ) -> "_588.PlasticVDI2736GearSingleFlankRatingInAPlasticPlasticMesh":
        from mastapy._private.gears.rating.cylindrical.plastic_vdi2736 import _588

        return self.__parent__._cast(
            _588.PlasticVDI2736GearSingleFlankRatingInAPlasticPlasticMesh
        )

    @property
    def iso63361996_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_602.ISO63361996GearSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _602

        return self.__parent__._cast(_602.ISO63361996GearSingleFlankRating)

    @property
    def iso63362006_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_604.ISO63362006GearSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _604

        return self.__parent__._cast(_604.ISO63362006GearSingleFlankRating)

    @property
    def iso63362019_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_606.ISO63362019GearSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _606

        return self.__parent__._cast(_606.ISO63362019GearSingleFlankRating)

    @property
    def iso6336_abstract_metal_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_610.ISO6336AbstractMetalGearSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _610

        return self.__parent__._cast(_610.ISO6336AbstractMetalGearSingleFlankRating)

    @property
    def din3990_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_623.DIN3990GearSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.din3990 import _623

        return self.__parent__._cast(_623.DIN3990GearSingleFlankRating)

    @property
    def iso6336_abstract_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "ISO6336AbstractGearSingleFlankRating":
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
class ISO6336AbstractGearSingleFlankRating(_556.CylindricalGearSingleFlankRating):
    """ISO6336AbstractGearSingleFlankRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISO6336_ABSTRACT_GEAR_SINGLE_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def e(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "E")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def face_width_for_root_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceWidthForRootStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def form_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FormFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def g(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "G")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def h(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "H")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def intermediate_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IntermediateAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def nominal_tooth_root_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalToothRootStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def notch_parameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NotchParameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def roughness_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RoughnessFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stress_correction_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StressCorrectionFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stress_correction_factor_bending_for_test_gears(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StressCorrectionFactorBendingForTestGears"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ISO6336AbstractGearSingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_ISO6336AbstractGearSingleFlankRating
        """
        return _Cast_ISO6336AbstractGearSingleFlankRating(self)
