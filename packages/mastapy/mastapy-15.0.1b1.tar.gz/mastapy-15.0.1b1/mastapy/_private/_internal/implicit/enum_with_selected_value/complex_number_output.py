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
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _6056

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar(
        "Self",
        bound="EnumWithSelectedValue_HarmonicAnalysisFEExportOptions_ComplexNumberOutput",
    )


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_HarmonicAnalysisFEExportOptions_ComplexNumberOutput",)


class EnumWithSelectedValue_HarmonicAnalysisFEExportOptions_ComplexNumberOutput(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_HarmonicAnalysisFEExportOptions_ComplexNumberOutput

    A specific implementation of 'EnumWithSelectedValue' for 'HarmonicAnalysisFEExportOptions.ComplexNumberOutput' types.
    """

    __qualname__ = "HarmonicAnalysisFEExportOptions.ComplexNumberOutput"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_HarmonicAnalysisFEExportOptions_ComplexNumberOutput]",
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
        cls: "Type[EnumWithSelectedValue_HarmonicAnalysisFEExportOptions_ComplexNumberOutput]",
    ) -> "_6056.HarmonicAnalysisFEExportOptions.ComplexNumberOutput":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _6056.HarmonicAnalysisFEExportOptions.ComplexNumberOutput
        """
        return _6056.HarmonicAnalysisFEExportOptions.ComplexNumberOutput

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_HarmonicAnalysisFEExportOptions_ComplexNumberOutput]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _6056.HarmonicAnalysisFEExportOptions.ComplexNumberOutput.type_()

    @property
    @exception_bridge
    def selected_value(
        self: "Self",
    ) -> "_6056.HarmonicAnalysisFEExportOptions.ComplexNumberOutput":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.HarmonicAnalysisFEExportOptions.ComplexNumberOutput

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(
        self: "Self",
    ) -> "List[_6056.HarmonicAnalysisFEExportOptions.ComplexNumberOutput]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.HarmonicAnalysisFEExportOptions.ComplexNumberOutput]

        Note:
            This property is readonly.
        """
        return None
