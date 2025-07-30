"""ShaftPerModeResult"""

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
from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
    _4991,
)

_SHAFT_PER_MODE_RESULT = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Reporting",
    "ShaftPerModeResult",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ShaftPerModeResult")
    CastSelf = TypeVar("CastSelf", bound="ShaftPerModeResult._Cast_ShaftPerModeResult")


__docformat__ = "restructuredtext en"
__all__ = ("ShaftPerModeResult",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftPerModeResult:
    """Special nested class for casting ShaftPerModeResult to subclasses."""

    __parent__: "ShaftPerModeResult"

    @property
    def component_per_mode_result(self: "CastSelf") -> "_4991.ComponentPerModeResult":
        return self.__parent__._cast(_4991.ComponentPerModeResult)

    @property
    def shaft_per_mode_result(self: "CastSelf") -> "ShaftPerModeResult":
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
class ShaftPerModeResult(_4991.ComponentPerModeResult):
    """ShaftPerModeResult

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_PER_MODE_RESULT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def torsional_mode_shape(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorsionalModeShape")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftPerModeResult":
        """Cast to another type.

        Returns:
            _Cast_ShaftPerModeResult
        """
        return _Cast_ShaftPerModeResult(self)
