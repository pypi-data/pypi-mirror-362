"""LoadedRollerBearingRow"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.bearings.bearing_results.rolling import _2242

_LOADED_ROLLER_BEARING_ROW = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "LoadedRollerBearingRow"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling import (
        _2177,
        _2198,
        _2203,
        _2206,
        _2214,
        _2218,
        _2230,
        _2233,
        _2237,
        _2249,
        _2252,
        _2257,
        _2266,
    )

    Self = TypeVar("Self", bound="LoadedRollerBearingRow")
    CastSelf = TypeVar(
        "CastSelf", bound="LoadedRollerBearingRow._Cast_LoadedRollerBearingRow"
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedRollerBearingRow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedRollerBearingRow:
    """Special nested class for casting LoadedRollerBearingRow to subclasses."""

    __parent__: "LoadedRollerBearingRow"

    @property
    def loaded_rolling_bearing_row(self: "CastSelf") -> "_2242.LoadedRollingBearingRow":
        return self.__parent__._cast(_2242.LoadedRollingBearingRow)

    @property
    def loaded_asymmetric_spherical_roller_bearing_row(
        self: "CastSelf",
    ) -> "_2198.LoadedAsymmetricSphericalRollerBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2198

        return self.__parent__._cast(_2198.LoadedAsymmetricSphericalRollerBearingRow)

    @property
    def loaded_axial_thrust_cylindrical_roller_bearing_row(
        self: "CastSelf",
    ) -> "_2203.LoadedAxialThrustCylindricalRollerBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2203

        return self.__parent__._cast(_2203.LoadedAxialThrustCylindricalRollerBearingRow)

    @property
    def loaded_axial_thrust_needle_roller_bearing_row(
        self: "CastSelf",
    ) -> "_2206.LoadedAxialThrustNeedleRollerBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2206

        return self.__parent__._cast(_2206.LoadedAxialThrustNeedleRollerBearingRow)

    @property
    def loaded_crossed_roller_bearing_row(
        self: "CastSelf",
    ) -> "_2214.LoadedCrossedRollerBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2214

        return self.__parent__._cast(_2214.LoadedCrossedRollerBearingRow)

    @property
    def loaded_cylindrical_roller_bearing_row(
        self: "CastSelf",
    ) -> "_2218.LoadedCylindricalRollerBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2218

        return self.__parent__._cast(_2218.LoadedCylindricalRollerBearingRow)

    @property
    def loaded_needle_roller_bearing_row(
        self: "CastSelf",
    ) -> "_2230.LoadedNeedleRollerBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2230

        return self.__parent__._cast(_2230.LoadedNeedleRollerBearingRow)

    @property
    def loaded_non_barrel_roller_bearing_row(
        self: "CastSelf",
    ) -> "_2233.LoadedNonBarrelRollerBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2233

        return self.__parent__._cast(_2233.LoadedNonBarrelRollerBearingRow)

    @property
    def loaded_spherical_roller_radial_bearing_row(
        self: "CastSelf",
    ) -> "_2249.LoadedSphericalRollerRadialBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2249

        return self.__parent__._cast(_2249.LoadedSphericalRollerRadialBearingRow)

    @property
    def loaded_spherical_roller_thrust_bearing_row(
        self: "CastSelf",
    ) -> "_2252.LoadedSphericalRollerThrustBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2252

        return self.__parent__._cast(_2252.LoadedSphericalRollerThrustBearingRow)

    @property
    def loaded_taper_roller_bearing_row(
        self: "CastSelf",
    ) -> "_2257.LoadedTaperRollerBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2257

        return self.__parent__._cast(_2257.LoadedTaperRollerBearingRow)

    @property
    def loaded_toroidal_roller_bearing_row(
        self: "CastSelf",
    ) -> "_2266.LoadedToroidalRollerBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2266

        return self.__parent__._cast(_2266.LoadedToroidalRollerBearingRow)

    @property
    def loaded_roller_bearing_row(self: "CastSelf") -> "LoadedRollerBearingRow":
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
class LoadedRollerBearingRow(_2242.LoadedRollingBearingRow):
    """LoadedRollerBearingRow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_ROLLER_BEARING_ROW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def depth_of_maximum_shear_stress_chart_inner(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DepthOfMaximumShearStressChartInner"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def depth_of_maximum_shear_stress_chart_outer(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DepthOfMaximumShearStressChartOuter"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def hertzian_contact_width_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HertzianContactWidthInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hertzian_contact_width_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HertzianContactWidthOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def inner_race_profile_warning(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerRaceProfileWarning")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def maximum_normal_edge_stress_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumNormalEdgeStressInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_normal_edge_stress_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumNormalEdgeStressOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_shear_stress_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumShearStressInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_shear_stress_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumShearStressOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def outer_race_profile_warning(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterRaceProfileWarning")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def roller_profile_warning(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RollerProfileWarning")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def shear_stress_chart_inner(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShearStressChartInner")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def shear_stress_chart_outer(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShearStressChartOuter")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def loaded_bearing(self: "Self") -> "_2237.LoadedRollerBearingResults":
        """mastapy.bearings.bearing_results.rolling.LoadedRollerBearingResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadedBearing")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def lamina_dynamic_equivalent_loads(
        self: "Self",
    ) -> "List[_2177.ForceAtLaminaGroupReportable]":
        """List[mastapy.bearings.bearing_results.rolling.ForceAtLaminaGroupReportable]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LaminaDynamicEquivalentLoads")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedRollerBearingRow":
        """Cast to another type.

        Returns:
            _Cast_LoadedRollerBearingRow
        """
        return _Cast_LoadedRollerBearingRow(self)
