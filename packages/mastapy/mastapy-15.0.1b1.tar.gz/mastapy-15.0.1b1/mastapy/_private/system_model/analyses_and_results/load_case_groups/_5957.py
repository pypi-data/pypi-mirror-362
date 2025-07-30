"""SubGroupInSingleDesignState"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.load_case_groups import _5948

_SUB_GROUP_IN_SINGLE_DESIGN_STATE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups",
    "SubGroupInSingleDesignState",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.load_case_groups import (
        _5949,
        _5950,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7674

    Self = TypeVar("Self", bound="SubGroupInSingleDesignState")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SubGroupInSingleDesignState._Cast_SubGroupInSingleDesignState",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SubGroupInSingleDesignState",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SubGroupInSingleDesignState:
    """Special nested class for casting SubGroupInSingleDesignState to subclasses."""

    __parent__: "SubGroupInSingleDesignState"

    @property
    def abstract_design_state_load_case_group(
        self: "CastSelf",
    ) -> "_5948.AbstractDesignStateLoadCaseGroup":
        return self.__parent__._cast(_5948.AbstractDesignStateLoadCaseGroup)

    @property
    def abstract_static_load_case_group(
        self: "CastSelf",
    ) -> "_5950.AbstractStaticLoadCaseGroup":
        from mastapy._private.system_model.analyses_and_results.load_case_groups import (
            _5950,
        )

        return self.__parent__._cast(_5950.AbstractStaticLoadCaseGroup)

    @property
    def abstract_load_case_group(self: "CastSelf") -> "_5949.AbstractLoadCaseGroup":
        from mastapy._private.system_model.analyses_and_results.load_case_groups import (
            _5949,
        )

        return self.__parent__._cast(_5949.AbstractLoadCaseGroup)

    @property
    def sub_group_in_single_design_state(
        self: "CastSelf",
    ) -> "SubGroupInSingleDesignState":
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
class SubGroupInSingleDesignState(_5948.AbstractDesignStateLoadCaseGroup):
    """SubGroupInSingleDesignState

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SUB_GROUP_IN_SINGLE_DESIGN_STATE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @exception_bridge
    @enforce_parameter_types
    def remove_static_load(self: "Self", static_load: "_7674.StaticLoadCase") -> None:
        """Method does not return.

        Args:
            static_load (mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase)
        """
        pythonnet_method_call(
            self.wrapped,
            "RemoveStaticLoad",
            static_load.wrapped if static_load else None,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_SubGroupInSingleDesignState":
        """Cast to another type.

        Returns:
            _Cast_SubGroupInSingleDesignState
        """
        return _Cast_SubGroupInSingleDesignState(self)
