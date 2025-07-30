"""BearingDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_BEARING_DESIGN = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns", "BearingDesign"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.bearings import _2080
    from mastapy._private.bearings.bearing_designs import _2341, _2342, _2343, _2344
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
    from mastapy._private.math_utility import _1702

    Self = TypeVar("Self", bound="BearingDesign")
    CastSelf = TypeVar("CastSelf", bound="BearingDesign._Cast_BearingDesign")


__docformat__ = "restructuredtext en"
__all__ = ("BearingDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BearingDesign:
    """Special nested class for casting BearingDesign to subclasses."""

    __parent__: "BearingDesign"

    @property
    def detailed_bearing(self: "CastSelf") -> "_2341.DetailedBearing":
        from mastapy._private.bearings.bearing_designs import _2341

        return self.__parent__._cast(_2341.DetailedBearing)

    @property
    def dummy_rolling_bearing(self: "CastSelf") -> "_2342.DummyRollingBearing":
        from mastapy._private.bearings.bearing_designs import _2342

        return self.__parent__._cast(_2342.DummyRollingBearing)

    @property
    def linear_bearing(self: "CastSelf") -> "_2343.LinearBearing":
        from mastapy._private.bearings.bearing_designs import _2343

        return self.__parent__._cast(_2343.LinearBearing)

    @property
    def non_linear_bearing(self: "CastSelf") -> "_2344.NonLinearBearing":
        from mastapy._private.bearings.bearing_designs import _2344

        return self.__parent__._cast(_2344.NonLinearBearing)

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
    def bearing_design(self: "CastSelf") -> "BearingDesign":
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
class BearingDesign(_0.APIBase):
    """BearingDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEARING_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def bore(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Bore")

        if temp is None:
            return 0.0

        return temp

    @bore.setter
    @exception_bridge
    @enforce_parameter_types
    def bore(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Bore", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def mass(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Mass")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @mass.setter
    @exception_bridge
    @enforce_parameter_types
    def mass(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Mass", value)

    @property
    @exception_bridge
    def model(self: "Self") -> "_2080.BearingModel":
        """mastapy.bearings.BearingModel

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Model")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Bearings.BearingModel")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings._2080", "BearingModel"
        )(value)

    @property
    @exception_bridge
    def outer_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterDiameter")

        if temp is None:
            return 0.0

        return temp

    @outer_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "OuterDiameter", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def type_(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Type")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Width")

        if temp is None:
            return 0.0

        return temp

    @width.setter
    @exception_bridge
    @enforce_parameter_types
    def width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Width", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def mass_properties_of_elements_from_geometry(
        self: "Self",
    ) -> "_1702.MassProperties":
        """mastapy.math_utility.MassProperties

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MassPropertiesOfElementsFromGeometry"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def mass_properties_of_inner_ring_from_geometry(
        self: "Self",
    ) -> "_1702.MassProperties":
        """mastapy.math_utility.MassProperties

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MassPropertiesOfInnerRingFromGeometry"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def mass_properties_of_outer_ring_from_geometry(
        self: "Self",
    ) -> "_1702.MassProperties":
        """mastapy.math_utility.MassProperties

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MassPropertiesOfOuterRingFromGeometry"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def total_mass_properties(self: "Self") -> "_1702.MassProperties":
        """mastapy.math_utility.MassProperties

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalMassProperties")

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
    def cast_to(self: "Self") -> "_Cast_BearingDesign":
        """Cast to another type.

        Returns:
            _Cast_BearingDesign
        """
        return _Cast_BearingDesign(self)
