"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.nodal_analysis.varying_input_components._99 import (
        AbstractVaryingInputComponent,
    )
    from mastapy._private.nodal_analysis.varying_input_components._100 import (
        AngleInputComponent,
    )
    from mastapy._private.nodal_analysis.varying_input_components._101 import (
        ForceInputComponent,
    )
    from mastapy._private.nodal_analysis.varying_input_components._102 import (
        MomentInputComponent,
    )
    from mastapy._private.nodal_analysis.varying_input_components._103 import (
        NonDimensionalInputComponent,
    )
    from mastapy._private.nodal_analysis.varying_input_components._104 import (
        SinglePointSelectionMethod,
    )
    from mastapy._private.nodal_analysis.varying_input_components._105 import (
        VelocityInputComponent,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.nodal_analysis.varying_input_components._99": [
            "AbstractVaryingInputComponent"
        ],
        "_private.nodal_analysis.varying_input_components._100": [
            "AngleInputComponent"
        ],
        "_private.nodal_analysis.varying_input_components._101": [
            "ForceInputComponent"
        ],
        "_private.nodal_analysis.varying_input_components._102": [
            "MomentInputComponent"
        ],
        "_private.nodal_analysis.varying_input_components._103": [
            "NonDimensionalInputComponent"
        ],
        "_private.nodal_analysis.varying_input_components._104": [
            "SinglePointSelectionMethod"
        ],
        "_private.nodal_analysis.varying_input_components._105": [
            "VelocityInputComponent"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractVaryingInputComponent",
    "AngleInputComponent",
    "ForceInputComponent",
    "MomentInputComponent",
    "NonDimensionalInputComponent",
    "SinglePointSelectionMethod",
    "VelocityInputComponent",
)
