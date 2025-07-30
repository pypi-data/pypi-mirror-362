"""NonLinearBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_designs import _2340

_NON_LINEAR_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns", "NonLinearBearing"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_designs import _2341
    from mastapy._private.bearings.bearing_designs.concept import _2408, _2409, _2410
    from mastapy._private.bearings.bearing_designs.fluid_film import (
        _2398,
        _2400,
        _2402,
        _2404,
        _2405,
        _2406,
    )
    from mastapy._private.bearings.bearing_designs.rolling import (
        _2345,
        _2346,
        _2347,
        _2348,
        _2349,
        _2350,
        _2352,
        _2358,
        _2359,
        _2360,
        _2364,
        _2369,
        _2370,
        _2371,
        _2372,
        _2375,
        _2377,
        _2380,
        _2381,
        _2382,
        _2383,
        _2384,
        _2385,
    )

    Self = TypeVar("Self", bound="NonLinearBearing")
    CastSelf = TypeVar("CastSelf", bound="NonLinearBearing._Cast_NonLinearBearing")


__docformat__ = "restructuredtext en"
__all__ = ("NonLinearBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NonLinearBearing:
    """Special nested class for casting NonLinearBearing to subclasses."""

    __parent__: "NonLinearBearing"

    @property
    def bearing_design(self: "CastSelf") -> "_2340.BearingDesign":
        return self.__parent__._cast(_2340.BearingDesign)

    @property
    def detailed_bearing(self: "CastSelf") -> "_2341.DetailedBearing":
        from mastapy._private.bearings.bearing_designs import _2341

        return self.__parent__._cast(_2341.DetailedBearing)

    @property
    def angular_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2345.AngularContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2345

        return self.__parent__._cast(_2345.AngularContactBallBearing)

    @property
    def angular_contact_thrust_ball_bearing(
        self: "CastSelf",
    ) -> "_2346.AngularContactThrustBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2346

        return self.__parent__._cast(_2346.AngularContactThrustBallBearing)

    @property
    def asymmetric_spherical_roller_bearing(
        self: "CastSelf",
    ) -> "_2347.AsymmetricSphericalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2347

        return self.__parent__._cast(_2347.AsymmetricSphericalRollerBearing)

    @property
    def axial_thrust_cylindrical_roller_bearing(
        self: "CastSelf",
    ) -> "_2348.AxialThrustCylindricalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2348

        return self.__parent__._cast(_2348.AxialThrustCylindricalRollerBearing)

    @property
    def axial_thrust_needle_roller_bearing(
        self: "CastSelf",
    ) -> "_2349.AxialThrustNeedleRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2349

        return self.__parent__._cast(_2349.AxialThrustNeedleRollerBearing)

    @property
    def ball_bearing(self: "CastSelf") -> "_2350.BallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2350

        return self.__parent__._cast(_2350.BallBearing)

    @property
    def barrel_roller_bearing(self: "CastSelf") -> "_2352.BarrelRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2352

        return self.__parent__._cast(_2352.BarrelRollerBearing)

    @property
    def crossed_roller_bearing(self: "CastSelf") -> "_2358.CrossedRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2358

        return self.__parent__._cast(_2358.CrossedRollerBearing)

    @property
    def cylindrical_roller_bearing(
        self: "CastSelf",
    ) -> "_2359.CylindricalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2359

        return self.__parent__._cast(_2359.CylindricalRollerBearing)

    @property
    def deep_groove_ball_bearing(self: "CastSelf") -> "_2360.DeepGrooveBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2360

        return self.__parent__._cast(_2360.DeepGrooveBallBearing)

    @property
    def four_point_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2364.FourPointContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2364

        return self.__parent__._cast(_2364.FourPointContactBallBearing)

    @property
    def multi_point_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2369.MultiPointContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2369

        return self.__parent__._cast(_2369.MultiPointContactBallBearing)

    @property
    def needle_roller_bearing(self: "CastSelf") -> "_2370.NeedleRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2370

        return self.__parent__._cast(_2370.NeedleRollerBearing)

    @property
    def non_barrel_roller_bearing(self: "CastSelf") -> "_2371.NonBarrelRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2371

        return self.__parent__._cast(_2371.NonBarrelRollerBearing)

    @property
    def roller_bearing(self: "CastSelf") -> "_2372.RollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2372

        return self.__parent__._cast(_2372.RollerBearing)

    @property
    def rolling_bearing(self: "CastSelf") -> "_2375.RollingBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2375

        return self.__parent__._cast(_2375.RollingBearing)

    @property
    def self_aligning_ball_bearing(self: "CastSelf") -> "_2377.SelfAligningBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2377

        return self.__parent__._cast(_2377.SelfAligningBallBearing)

    @property
    def spherical_roller_bearing(self: "CastSelf") -> "_2380.SphericalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2380

        return self.__parent__._cast(_2380.SphericalRollerBearing)

    @property
    def spherical_roller_thrust_bearing(
        self: "CastSelf",
    ) -> "_2381.SphericalRollerThrustBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2381

        return self.__parent__._cast(_2381.SphericalRollerThrustBearing)

    @property
    def taper_roller_bearing(self: "CastSelf") -> "_2382.TaperRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2382

        return self.__parent__._cast(_2382.TaperRollerBearing)

    @property
    def three_point_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2383.ThreePointContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2383

        return self.__parent__._cast(_2383.ThreePointContactBallBearing)

    @property
    def thrust_ball_bearing(self: "CastSelf") -> "_2384.ThrustBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2384

        return self.__parent__._cast(_2384.ThrustBallBearing)

    @property
    def toroidal_roller_bearing(self: "CastSelf") -> "_2385.ToroidalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2385

        return self.__parent__._cast(_2385.ToroidalRollerBearing)

    @property
    def pad_fluid_film_bearing(self: "CastSelf") -> "_2398.PadFluidFilmBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2398

        return self.__parent__._cast(_2398.PadFluidFilmBearing)

    @property
    def plain_grease_filled_journal_bearing(
        self: "CastSelf",
    ) -> "_2400.PlainGreaseFilledJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2400

        return self.__parent__._cast(_2400.PlainGreaseFilledJournalBearing)

    @property
    def plain_journal_bearing(self: "CastSelf") -> "_2402.PlainJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2402

        return self.__parent__._cast(_2402.PlainJournalBearing)

    @property
    def plain_oil_fed_journal_bearing(
        self: "CastSelf",
    ) -> "_2404.PlainOilFedJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2404

        return self.__parent__._cast(_2404.PlainOilFedJournalBearing)

    @property
    def tilting_pad_journal_bearing(
        self: "CastSelf",
    ) -> "_2405.TiltingPadJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2405

        return self.__parent__._cast(_2405.TiltingPadJournalBearing)

    @property
    def tilting_pad_thrust_bearing(self: "CastSelf") -> "_2406.TiltingPadThrustBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2406

        return self.__parent__._cast(_2406.TiltingPadThrustBearing)

    @property
    def concept_axial_clearance_bearing(
        self: "CastSelf",
    ) -> "_2408.ConceptAxialClearanceBearing":
        from mastapy._private.bearings.bearing_designs.concept import _2408

        return self.__parent__._cast(_2408.ConceptAxialClearanceBearing)

    @property
    def concept_clearance_bearing(self: "CastSelf") -> "_2409.ConceptClearanceBearing":
        from mastapy._private.bearings.bearing_designs.concept import _2409

        return self.__parent__._cast(_2409.ConceptClearanceBearing)

    @property
    def concept_radial_clearance_bearing(
        self: "CastSelf",
    ) -> "_2410.ConceptRadialClearanceBearing":
        from mastapy._private.bearings.bearing_designs.concept import _2410

        return self.__parent__._cast(_2410.ConceptRadialClearanceBearing)

    @property
    def non_linear_bearing(self: "CastSelf") -> "NonLinearBearing":
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
class NonLinearBearing(_2340.BearingDesign):
    """NonLinearBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NON_LINEAR_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_NonLinearBearing":
        """Cast to another type.

        Returns:
            _Cast_NonLinearBearing
        """
        return _Cast_NonLinearBearing(self)
