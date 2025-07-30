"""ShaftHubConnectionLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.static_loads import _7719

_ARRAY = python_net_import("System", "Array")
_SHAFT_HUB_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ShaftHubConnectionLoadCase",
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5779
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7706,
        _7795,
        _7799,
    )
    from mastapy._private.system_model.part_model.couplings import (
        _2835,
        _2840,
        _2841,
        _2842,
        _2843,
        _2845,
    )

    Self = TypeVar("Self", bound="ShaftHubConnectionLoadCase")
    CastSelf = TypeVar(
        "CastSelf", bound="ShaftHubConnectionLoadCase._Cast_ShaftHubConnectionLoadCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftHubConnectionLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftHubConnectionLoadCase:
    """Special nested class for casting ShaftHubConnectionLoadCase to subclasses."""

    __parent__: "ShaftHubConnectionLoadCase"

    @property
    def connector_load_case(self: "CastSelf") -> "_7719.ConnectorLoadCase":
        return self.__parent__._cast(_7719.ConnectorLoadCase)

    @property
    def mountable_component_load_case(
        self: "CastSelf",
    ) -> "_7795.MountableComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7795,
        )

        return self.__parent__._cast(_7795.MountableComponentLoadCase)

    @property
    def component_load_case(self: "CastSelf") -> "_7706.ComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7706,
        )

        return self.__parent__._cast(_7706.ComponentLoadCase)

    @property
    def part_load_case(self: "CastSelf") -> "_7799.PartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7799,
        )

        return self.__parent__._cast(_7799.PartLoadCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2898.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2898

        return self.__parent__._cast(_2898.PartAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2894.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2894

        return self.__parent__._cast(_2894.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2892.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2892

        return self.__parent__._cast(_2892.DesignEntityAnalysis)

    @property
    def shaft_hub_connection_load_case(
        self: "CastSelf",
    ) -> "ShaftHubConnectionLoadCase":
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
class ShaftHubConnectionLoadCase(_7719.ConnectorLoadCase):
    """ShaftHubConnectionLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_HUB_CONNECTION_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def additional_tilt_stiffness(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "AdditionalTiltStiffness")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @additional_tilt_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def additional_tilt_stiffness(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "AdditionalTiltStiffness", value)

    @property
    @exception_bridge
    def angular_backlash(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AngularBacklash")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def application_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ApplicationFactor")

        if temp is None:
            return 0.0

        return temp

    @application_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def application_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ApplicationFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def axial_preload(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "AxialPreload")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @axial_preload.setter
    @exception_bridge
    @enforce_parameter_types
    def axial_preload(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "AxialPreload", value)

    @property
    @exception_bridge
    def axial_stiffness(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "AxialStiffness")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @axial_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def axial_stiffness(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "AxialStiffness", value)

    @property
    @exception_bridge
    def is_torsionally_rigid(self: "Self") -> "overridable.Overridable_bool":
        """Overridable[bool]"""
        temp = pythonnet_property_get(self.wrapped, "IsTorsionallyRigid")

        if temp is None:
            return False

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_bool"
        )(temp)

    @is_torsionally_rigid.setter
    @exception_bridge
    @enforce_parameter_types
    def is_torsionally_rigid(
        self: "Self", value: "Union[bool, Tuple[bool, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else False, is_overridden
        )
        pythonnet_property_set(self.wrapped, "IsTorsionallyRigid", value)

    @property
    @exception_bridge
    def load_distribution_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "LoadDistributionFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @load_distribution_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def load_distribution_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "LoadDistributionFactor", value)

    @property
    @exception_bridge
    def load_distribution_factor_single_key(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LoadDistributionFactorSingleKey")

        if temp is None:
            return 0.0

        return temp

    @load_distribution_factor_single_key.setter
    @exception_bridge
    @enforce_parameter_types
    def load_distribution_factor_single_key(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LoadDistributionFactorSingleKey",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def normal_clearance(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "NormalClearance")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @normal_clearance.setter
    @exception_bridge
    @enforce_parameter_types
    def normal_clearance(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "NormalClearance", value)

    @property
    @exception_bridge
    def number_of_torque_peaks(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfTorquePeaks")

        if temp is None:
            return 0.0

        return temp

    @number_of_torque_peaks.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_torque_peaks(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfTorquePeaks",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def number_of_torque_reversals(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfTorqueReversals")

        if temp is None:
            return 0.0

        return temp

    @number_of_torque_reversals.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_torque_reversals(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfTorqueReversals",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def override_design_specified_stiffness_matrix(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "OverrideDesignSpecifiedStiffnessMatrix"
        )

        if temp is None:
            return False

        return temp

    @override_design_specified_stiffness_matrix.setter
    @exception_bridge
    @enforce_parameter_types
    def override_design_specified_stiffness_matrix(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OverrideDesignSpecifiedStiffnessMatrix",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def radial_clearance(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RadialClearance")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @radial_clearance.setter
    @exception_bridge
    @enforce_parameter_types
    def radial_clearance(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RadialClearance", value)

    @property
    @exception_bridge
    def radial_stiffness(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RadialStiffness")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @radial_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def radial_stiffness(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RadialStiffness", value)

    @property
    @exception_bridge
    def specified_application_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "SpecifiedApplicationFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @specified_application_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def specified_application_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "SpecifiedApplicationFactor", value)

    @property
    @exception_bridge
    def specified_backlash_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "SpecifiedBacklashFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @specified_backlash_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def specified_backlash_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "SpecifiedBacklashFactor", value)

    @property
    @exception_bridge
    def specified_load_distribution_factor(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "SpecifiedLoadDistributionFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @specified_load_distribution_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def specified_load_distribution_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "SpecifiedLoadDistributionFactor", value)

    @property
    @exception_bridge
    def specified_load_sharing_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "SpecifiedLoadSharingFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @specified_load_sharing_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def specified_load_sharing_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "SpecifiedLoadSharingFactor", value)

    @property
    @exception_bridge
    def tilt_clearance(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "TiltClearance")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @tilt_clearance.setter
    @exception_bridge
    @enforce_parameter_types
    def tilt_clearance(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "TiltClearance", value)

    @property
    @exception_bridge
    def tilt_stiffness(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "TiltStiffness")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @tilt_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def tilt_stiffness(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "TiltStiffness", value)

    @property
    @exception_bridge
    def torsional_stiffness(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "TorsionalStiffness")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @torsional_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def torsional_stiffness(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "TorsionalStiffness", value)

    @property
    @exception_bridge
    def torsional_twist_preload(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "TorsionalTwistPreload")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @torsional_twist_preload.setter
    @exception_bridge
    @enforce_parameter_types
    def torsional_twist_preload(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "TorsionalTwistPreload", value)

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2840.ShaftHubConnection":
        """mastapy.system_model.part_model.couplings.ShaftHubConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def damping_options(self: "Self") -> "_5779.SplineDampingOptions":
        """mastapy.system_model.analyses_and_results.mbd_analyses.SplineDampingOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DampingOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def external_half_manufacturing_error(
        self: "Self",
    ) -> "_2842.SplineHalfManufacturingError":
        """mastapy.system_model.part_model.couplings.SplineHalfManufacturingError

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExternalHalfManufacturingError")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def internal_half_manufacturing_error(
        self: "Self",
    ) -> "_2842.SplineHalfManufacturingError":
        """mastapy.system_model.part_model.couplings.SplineHalfManufacturingError

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InternalHalfManufacturingError")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def left_flank_lead_relief(self: "Self") -> "_2843.SplineLeadRelief":
        """mastapy.system_model.part_model.couplings.SplineLeadRelief

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeftFlankLeadRelief")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def major_fit_options(self: "Self") -> "_2841.SplineFitOptions":
        """mastapy.system_model.part_model.couplings.SplineFitOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MajorFitOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def minor_fit_options(self: "Self") -> "_2841.SplineFitOptions":
        """mastapy.system_model.part_model.couplings.SplineFitOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinorFitOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def right_flank_lead_relief(self: "Self") -> "_2843.SplineLeadRelief":
        """mastapy.system_model.part_model.couplings.SplineLeadRelief

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RightFlankLeadRelief")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def spline_pitch_error_options(self: "Self") -> "_2845.SplinePitchErrorOptions":
        """mastapy.system_model.part_model.couplings.SplinePitchErrorOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SplinePitchErrorOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def fit_options(self: "Self") -> "List[_2841.SplineFitOptions]":
        """List[mastapy.system_model.part_model.couplings.SplineFitOptions]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FitOptions")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def lead_reliefs(self: "Self") -> "List[_2843.SplineLeadRelief]":
        """List[mastapy.system_model.part_model.couplings.SplineLeadRelief]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeadReliefs")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def planetaries(self: "Self") -> "List[ShaftHubConnectionLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.ShaftHubConnectionLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Planetaries")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def spline_half_manufacturing_errors(
        self: "Self",
    ) -> "List[_2842.SplineHalfManufacturingError]":
        """List[mastapy.system_model.part_model.couplings.SplineHalfManufacturingError]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SplineHalfManufacturingErrors")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def tooth_locations_external_spline_half(
        self: "Self",
    ) -> "List[_2835.RigidConnectorToothLocation]":
        """List[mastapy.system_model.part_model.couplings.RigidConnectorToothLocation]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothLocationsExternalSplineHalf")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def specified_stiffness_for_shaft_hub_connection_in_local_coordinate_system(
        self: "Self",
    ) -> "List[List[float]]":
        """List[List[float]]"""
        temp = pythonnet_property_get(
            self.wrapped,
            "SpecifiedStiffnessForShaftHubConnectionInLocalCoordinateSystem",
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_list_float_2d(temp)

        if value is None:
            return None

        return value

    @specified_stiffness_for_shaft_hub_connection_in_local_coordinate_system.setter
    @exception_bridge
    @enforce_parameter_types
    def specified_stiffness_for_shaft_hub_connection_in_local_coordinate_system(
        self: "Self", value: "List[List[float]]"
    ) -> None:
        value = conversion.mp_to_pn_list_float_2d(value)
        pythonnet_property_set(
            self.wrapped,
            "SpecifiedStiffnessForShaftHubConnectionInLocalCoordinateSystem",
            value,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftHubConnectionLoadCase":
        """Cast to another type.

        Returns:
            _Cast_ShaftHubConnectionLoadCase
        """
        return _Cast_ShaftHubConnectionLoadCase(self)
