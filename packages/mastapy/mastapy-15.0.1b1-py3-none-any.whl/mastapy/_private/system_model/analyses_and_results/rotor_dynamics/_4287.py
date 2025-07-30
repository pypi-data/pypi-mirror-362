"""RotorDynamicsDrawStyle"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.drawing import _2467

_ROTOR_DYNAMICS_DRAW_STYLE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.RotorDynamics",
    "RotorDynamicsDrawStyle",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.geometry import _397
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6900,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _4130,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3337,
    )

    Self = TypeVar("Self", bound="RotorDynamicsDrawStyle")
    CastSelf = TypeVar(
        "CastSelf", bound="RotorDynamicsDrawStyle._Cast_RotorDynamicsDrawStyle"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RotorDynamicsDrawStyle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RotorDynamicsDrawStyle:
    """Special nested class for casting RotorDynamicsDrawStyle to subclasses."""

    __parent__: "RotorDynamicsDrawStyle"

    @property
    def contour_draw_style(self: "CastSelf") -> "_2467.ContourDrawStyle":
        return self.__parent__._cast(_2467.ContourDrawStyle)

    @property
    def draw_style_base(self: "CastSelf") -> "_397.DrawStyleBase":
        from mastapy._private.geometry import _397

        return self.__parent__._cast(_397.DrawStyleBase)

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
    def critical_speed_analysis_draw_style(
        self: "CastSelf",
    ) -> "_6900.CriticalSpeedAnalysisDrawStyle":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6900,
        )

        return self.__parent__._cast(_6900.CriticalSpeedAnalysisDrawStyle)

    @property
    def rotor_dynamics_draw_style(self: "CastSelf") -> "RotorDynamicsDrawStyle":
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
class RotorDynamicsDrawStyle(_2467.ContourDrawStyle):
    """RotorDynamicsDrawStyle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROTOR_DYNAMICS_DRAW_STYLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def show_whirl_orbits(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowWhirlOrbits")

        if temp is None:
            return False

        return temp

    @show_whirl_orbits.setter
    @exception_bridge
    @enforce_parameter_types
    def show_whirl_orbits(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ShowWhirlOrbits", bool(value) if value is not None else False
        )

    @property
    def cast_to(self: "Self") -> "_Cast_RotorDynamicsDrawStyle":
        """Cast to another type.

        Returns:
            _Cast_RotorDynamicsDrawStyle
        """
        return _Cast_RotorDynamicsDrawStyle(self)
