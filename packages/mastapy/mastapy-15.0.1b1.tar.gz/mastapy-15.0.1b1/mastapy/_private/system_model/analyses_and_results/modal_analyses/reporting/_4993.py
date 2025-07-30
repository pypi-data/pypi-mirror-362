"""ModalCMSResultsForModeAndFE"""

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

_MODAL_CMS_RESULTS_FOR_MODE_AND_FE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Reporting",
    "ModalCMSResultsForModeAndFE",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis.component_mode_synthesis import _318

    Self = TypeVar("Self", bound="ModalCMSResultsForModeAndFE")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ModalCMSResultsForModeAndFE._Cast_ModalCMSResultsForModeAndFE",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ModalCMSResultsForModeAndFE",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ModalCMSResultsForModeAndFE:
    """Special nested class for casting ModalCMSResultsForModeAndFE to subclasses."""

    __parent__: "ModalCMSResultsForModeAndFE"

    @property
    def modal_cms_results_for_mode_and_fe(
        self: "CastSelf",
    ) -> "ModalCMSResultsForModeAndFE":
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
class ModalCMSResultsForModeAndFE(_0.APIBase):
    """ModalCMSResultsForModeAndFE

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MODAL_CMS_RESULTS_FOR_MODE_AND_FE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def fe_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FEName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def modal_full_fe_results(self: "Self") -> "_318.ModalCMSResults":
        """mastapy.nodal_analysis.component_mode_synthesis.ModalCMSResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModalFullFEResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ModalCMSResultsForModeAndFE":
        """Cast to another type.

        Returns:
            _Cast_ModalCMSResultsForModeAndFE
        """
        return _Cast_ModalCMSResultsForModeAndFE(self)
