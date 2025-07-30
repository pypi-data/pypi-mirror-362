"""KIMoSBevelHypoidSingleLoadCaseResultsData"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_KI_MO_S_BEVEL_HYPOID_SINGLE_LOAD_CASE_RESULTS_DATA = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Conical",
    "KIMoSBevelHypoidSingleLoadCaseResultsData",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs.conical import _1287

    Self = TypeVar("Self", bound="KIMoSBevelHypoidSingleLoadCaseResultsData")
    CastSelf = TypeVar(
        "CastSelf",
        bound="KIMoSBevelHypoidSingleLoadCaseResultsData._Cast_KIMoSBevelHypoidSingleLoadCaseResultsData",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KIMoSBevelHypoidSingleLoadCaseResultsData",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KIMoSBevelHypoidSingleLoadCaseResultsData:
    """Special nested class for casting KIMoSBevelHypoidSingleLoadCaseResultsData to subclasses."""

    __parent__: "KIMoSBevelHypoidSingleLoadCaseResultsData"

    @property
    def ki_mo_s_bevel_hypoid_single_load_case_results_data(
        self: "CastSelf",
    ) -> "KIMoSBevelHypoidSingleLoadCaseResultsData":
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
class KIMoSBevelHypoidSingleLoadCaseResultsData(_0.APIBase):
    """KIMoSBevelHypoidSingleLoadCaseResultsData

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _KI_MO_S_BEVEL_HYPOID_SINGLE_LOAD_CASE_RESULTS_DATA

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def average_mesh_stiffness_per_unit_face_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AverageMeshStiffnessPerUnitFaceWidth"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_pressure_chart(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactPressureChart")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def contact_ratio_under_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactRatioUnderLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def efficiency(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Efficiency")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def flash_temperature_chart(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FlashTemperatureChart")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def friction_coefficient_chart(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrictionCoefficientChart")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def maximum_contact_pressure(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumContactPressure")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_flash_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumFlashTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_friction_coefficient(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumFrictionCoefficient")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_pinion_root_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumPinionRootStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_sliding_velocity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumSlidingVelocity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_wheel_root_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumWheelRootStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def peak_to_peak_te_linear_loaded(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PeakToPeakTELinearLoaded")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def peak_to_peak_te_linear_unloaded(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PeakToPeakTELinearUnloaded")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_root_stress_chart(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionRootStressChart")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def pressure_velocity_pv_chart(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PressureVelocityPVChart")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def sliding_velocity_chart(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SlidingVelocityChart")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def wheel_root_stress_chart(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelRootStressChart")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def single_rotation_angle_results(
        self: "Self",
    ) -> "List[_1287.KIMoSBevelHypoidSingleRotationAngleResult]":
        """List[mastapy.gears.gear_designs.conical.KIMoSBevelHypoidSingleRotationAngleResult]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SingleRotationAngleResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_KIMoSBevelHypoidSingleLoadCaseResultsData":
        """Cast to another type.

        Returns:
            _Cast_KIMoSBevelHypoidSingleLoadCaseResultsData
        """
        return _Cast_KIMoSBevelHypoidSingleLoadCaseResultsData(self)
