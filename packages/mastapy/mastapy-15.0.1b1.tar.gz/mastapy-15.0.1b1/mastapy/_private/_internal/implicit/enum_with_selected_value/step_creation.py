"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _6114

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar(
        "Self",
        bound="EnumWithSelectedValue_StiffnessOptionsForHarmonicAnalysis_StepCreation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_StiffnessOptionsForHarmonicAnalysis_StepCreation",)


class EnumWithSelectedValue_StiffnessOptionsForHarmonicAnalysis_StepCreation(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_StiffnessOptionsForHarmonicAnalysis_StepCreation

    A specific implementation of 'EnumWithSelectedValue' for 'StiffnessOptionsForHarmonicAnalysis.StepCreation' types.
    """

    __qualname__ = "StiffnessOptionsForHarmonicAnalysis.StepCreation"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_StiffnessOptionsForHarmonicAnalysis_StepCreation]",
    ) -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_StiffnessOptionsForHarmonicAnalysis_StepCreation]",
    ) -> "_6114.StiffnessOptionsForHarmonicAnalysis.StepCreation":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _6114.StiffnessOptionsForHarmonicAnalysis.StepCreation
        """
        return _6114.StiffnessOptionsForHarmonicAnalysis.StepCreation

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_StiffnessOptionsForHarmonicAnalysis_StepCreation]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _6114.StiffnessOptionsForHarmonicAnalysis.StepCreation.type_()

    @property
    @exception_bridge
    def selected_value(
        self: "Self",
    ) -> "_6114.StiffnessOptionsForHarmonicAnalysis.StepCreation":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.StiffnessOptionsForHarmonicAnalysis.StepCreation

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(
        self: "Self",
    ) -> "List[_6114.StiffnessOptionsForHarmonicAnalysis.StepCreation]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.StiffnessOptionsForHarmonicAnalysis.StepCreation]

        Note:
            This property is readonly.
        """
        return None
