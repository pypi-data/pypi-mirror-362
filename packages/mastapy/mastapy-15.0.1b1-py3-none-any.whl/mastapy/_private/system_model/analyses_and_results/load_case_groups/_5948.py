"""AbstractDesignStateLoadCaseGroup"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.load_case_groups import _5950

_ABSTRACT_DESIGN_STATE_LOAD_CASE_GROUP = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups",
    "AbstractDesignStateLoadCaseGroup",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.load_case_groups import (
        _5949,
        _5953,
        _5957,
    )

    Self = TypeVar("Self", bound="AbstractDesignStateLoadCaseGroup")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractDesignStateLoadCaseGroup._Cast_AbstractDesignStateLoadCaseGroup",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractDesignStateLoadCaseGroup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractDesignStateLoadCaseGroup:
    """Special nested class for casting AbstractDesignStateLoadCaseGroup to subclasses."""

    __parent__: "AbstractDesignStateLoadCaseGroup"

    @property
    def abstract_static_load_case_group(
        self: "CastSelf",
    ) -> "_5950.AbstractStaticLoadCaseGroup":
        return self.__parent__._cast(_5950.AbstractStaticLoadCaseGroup)

    @property
    def abstract_load_case_group(self: "CastSelf") -> "_5949.AbstractLoadCaseGroup":
        from mastapy._private.system_model.analyses_and_results.load_case_groups import (
            _5949,
        )

        return self.__parent__._cast(_5949.AbstractLoadCaseGroup)

    @property
    def design_state(self: "CastSelf") -> "_5953.DesignState":
        from mastapy._private.system_model.analyses_and_results.load_case_groups import (
            _5953,
        )

        return self.__parent__._cast(_5953.DesignState)

    @property
    def sub_group_in_single_design_state(
        self: "CastSelf",
    ) -> "_5957.SubGroupInSingleDesignState":
        from mastapy._private.system_model.analyses_and_results.load_case_groups import (
            _5957,
        )

        return self.__parent__._cast(_5957.SubGroupInSingleDesignState)

    @property
    def abstract_design_state_load_case_group(
        self: "CastSelf",
    ) -> "AbstractDesignStateLoadCaseGroup":
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
class AbstractDesignStateLoadCaseGroup(_5950.AbstractStaticLoadCaseGroup):
    """AbstractDesignStateLoadCaseGroup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_DESIGN_STATE_LOAD_CASE_GROUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def two_d_drawing_showing_power_flow(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TwoDDrawingShowingPowerFlow")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Ratio")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractDesignStateLoadCaseGroup":
        """Cast to another type.

        Returns:
            _Cast_AbstractDesignStateLoadCaseGroup
        """
        return _Cast_AbstractDesignStateLoadCaseGroup(self)
