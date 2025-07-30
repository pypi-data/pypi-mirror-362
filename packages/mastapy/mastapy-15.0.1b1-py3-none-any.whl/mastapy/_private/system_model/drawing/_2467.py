"""ContourDrawStyle"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    overridable_enum_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import list_with_selected_item_and_image
from mastapy._private._internal.list_with_selected_item import (
    promote_to_list_with_selected_item,
)
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.geometry import _397
from mastapy._private.system_model.drawing import _2480

_CONTOUR_DRAW_STYLE = python_net_import(
    "SMT.MastaAPI.SystemModel.Drawing", "ContourDrawStyle"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6900,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6642,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _6054,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5744
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4929
    from mastapy._private.system_model.analyses_and_results.rotor_dynamics import _4287
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _4130,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3337,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _3069,
    )
    from mastapy._private.system_model.drawing import _2473
    from mastapy._private.utility.enums import _2019
    from mastapy._private.utility_gui import _2054

    Self = TypeVar("Self", bound="ContourDrawStyle")
    CastSelf = TypeVar("CastSelf", bound="ContourDrawStyle._Cast_ContourDrawStyle")


__docformat__ = "restructuredtext en"
__all__ = ("ContourDrawStyle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ContourDrawStyle:
    """Special nested class for casting ContourDrawStyle to subclasses."""

    __parent__: "ContourDrawStyle"

    @property
    def draw_style_base(self: "CastSelf") -> "_397.DrawStyleBase":
        return self.__parent__._cast(_397.DrawStyleBase)

    @property
    def system_deflection_draw_style(
        self: "CastSelf",
    ) -> "_3069.SystemDeflectionDrawStyle":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3069,
        )

        return self.__parent__._cast(_3069.SystemDeflectionDrawStyle)

    @property
    def steady_state_synchronous_response_draw_style(
        self: "CastSelf",
    ) -> "_3337.SteadyStateSynchronousResponseDrawStyle":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3337,
        )

        return self.__parent__._cast(_3337.SteadyStateSynchronousResponseDrawStyle)

    @property
    def stability_analysis_draw_style(
        self: "CastSelf",
    ) -> "_4130.StabilityAnalysisDrawStyle":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4130,
        )

        return self.__parent__._cast(_4130.StabilityAnalysisDrawStyle)

    @property
    def rotor_dynamics_draw_style(self: "CastSelf") -> "_4287.RotorDynamicsDrawStyle":
        from mastapy._private.system_model.analyses_and_results.rotor_dynamics import (
            _4287,
        )

        return self.__parent__._cast(_4287.RotorDynamicsDrawStyle)

    @property
    def modal_analysis_draw_style(self: "CastSelf") -> "_4929.ModalAnalysisDrawStyle":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4929,
        )

        return self.__parent__._cast(_4929.ModalAnalysisDrawStyle)

    @property
    def mbd_analysis_draw_style(self: "CastSelf") -> "_5744.MBDAnalysisDrawStyle":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5744,
        )

        return self.__parent__._cast(_5744.MBDAnalysisDrawStyle)

    @property
    def harmonic_analysis_draw_style(
        self: "CastSelf",
    ) -> "_6054.HarmonicAnalysisDrawStyle":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6054,
        )

        return self.__parent__._cast(_6054.HarmonicAnalysisDrawStyle)

    @property
    def dynamic_analysis_draw_style(
        self: "CastSelf",
    ) -> "_6642.DynamicAnalysisDrawStyle":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6642,
        )

        return self.__parent__._cast(_6642.DynamicAnalysisDrawStyle)

    @property
    def critical_speed_analysis_draw_style(
        self: "CastSelf",
    ) -> "_6900.CriticalSpeedAnalysisDrawStyle":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6900,
        )

        return self.__parent__._cast(_6900.CriticalSpeedAnalysisDrawStyle)

    @property
    def contour_draw_style(self: "CastSelf") -> "ContourDrawStyle":
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
class ContourDrawStyle(_397.DrawStyleBase):
    """ContourDrawStyle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONTOUR_DRAW_STYLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def contour(self: "Self") -> "_2019.ThreeDViewContourOption":
        """mastapy.utility.enums.ThreeDViewContourOption"""
        temp = pythonnet_property_get(self.wrapped, "Contour")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Utility.Enums.ThreeDViewContourOption"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.utility.enums._2019", "ThreeDViewContourOption"
        )(value)

    @contour.setter
    @exception_bridge
    @enforce_parameter_types
    def contour(self: "Self", value: "_2019.ThreeDViewContourOption") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Utility.Enums.ThreeDViewContourOption"
        )
        pythonnet_property_set(self.wrapped, "Contour", value)

    @property
    @exception_bridge
    def minimum_peak_value_displacement(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MinimumPeakValueDisplacement")

        if temp is None:
            return 0.0

        return temp

    @minimum_peak_value_displacement.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_peak_value_displacement(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumPeakValueDisplacement",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def minimum_peak_value_stress(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MinimumPeakValueStress")

        if temp is None:
            return 0.0

        return temp

    @minimum_peak_value_stress.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_peak_value_stress(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumPeakValueStress",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def show_local_maxima(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowLocalMaxima")

        if temp is None:
            return False

        return temp

    @show_local_maxima.setter
    @exception_bridge
    @enforce_parameter_types
    def show_local_maxima(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ShowLocalMaxima", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def stress_display(
        self: "Self",
    ) -> "list_with_selected_item_and_image.ListWithSelectedItemAndImage_StressResultOption":
        """ListWithSelectedItemAndImage[mastapy.system_model.drawing.StressResultOption]"""
        temp = pythonnet_property_get(self.wrapped, "StressDisplay")

        if temp is None:
            return None

        value = list_with_selected_item_and_image.ListWithSelectedItemAndImage_StressResultOption.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @stress_display.setter
    @exception_bridge
    @enforce_parameter_types
    def stress_display(self: "Self", value: "_2480.StressResultOption") -> None:
        generic_type = list_with_selected_item_and_image.ListWithSelectedItemAndImage_StressResultOption.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "StressDisplay", value)

    @property
    @exception_bridge
    def deflection_scaling(self: "Self") -> "_2054.ScalingDrawStyle":
        """mastapy.utility_gui.ScalingDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DeflectionScaling")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def model_view_options(self: "Self") -> "_2473.ModelViewOptionsDrawStyle":
        """mastapy.system_model.drawing.ModelViewOptionsDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModelViewOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ContourDrawStyle":
        """Cast to another type.

        Returns:
            _Cast_ContourDrawStyle
        """
        return _Cast_ContourDrawStyle(self)
