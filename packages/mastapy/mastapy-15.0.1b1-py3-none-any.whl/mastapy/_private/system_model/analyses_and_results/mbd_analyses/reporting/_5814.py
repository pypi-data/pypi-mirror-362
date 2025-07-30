"""DynamicTorqueVector3DResult"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_DYNAMIC_TORQUE_VECTOR_3D_RESULT = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Reporting",
    "DynamicTorqueVector3DResult",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.mbd_analyses.reporting import (
        _5813,
    )

    Self = TypeVar("Self", bound="DynamicTorqueVector3DResult")
    CastSelf = TypeVar(
        "CastSelf",
        bound="DynamicTorqueVector3DResult._Cast_DynamicTorqueVector3DResult",
    )


__docformat__ = "restructuredtext en"
__all__ = ("DynamicTorqueVector3DResult",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DynamicTorqueVector3DResult:
    """Special nested class for casting DynamicTorqueVector3DResult to subclasses."""

    __parent__: "DynamicTorqueVector3DResult"

    @property
    def dynamic_torque_vector_3d_result(
        self: "CastSelf",
    ) -> "DynamicTorqueVector3DResult":
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
class DynamicTorqueVector3DResult(_0.APIBase):
    """DynamicTorqueVector3DResult

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DYNAMIC_TORQUE_VECTOR_3D_RESULT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def magnitude(self: "Self") -> "_5813.DynamicTorqueResultAtTime":
        """mastapy.system_model.analyses_and_results.mbd_analyses.reporting.DynamicTorqueResultAtTime

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Magnitude")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def radial_magnitude(self: "Self") -> "_5813.DynamicTorqueResultAtTime":
        """mastapy.system_model.analyses_and_results.mbd_analyses.reporting.DynamicTorqueResultAtTime

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RadialMagnitude")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def x(self: "Self") -> "_5813.DynamicTorqueResultAtTime":
        """mastapy.system_model.analyses_and_results.mbd_analyses.reporting.DynamicTorqueResultAtTime

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "X")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def y(self: "Self") -> "_5813.DynamicTorqueResultAtTime":
        """mastapy.system_model.analyses_and_results.mbd_analyses.reporting.DynamicTorqueResultAtTime

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Y")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def z(self: "Self") -> "_5813.DynamicTorqueResultAtTime":
        """mastapy.system_model.analyses_and_results.mbd_analyses.reporting.DynamicTorqueResultAtTime

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Z")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_DynamicTorqueVector3DResult":
        """Cast to another type.

        Returns:
            _Cast_DynamicTorqueVector3DResult
        """
        return _Cast_DynamicTorqueVector3DResult(self)
