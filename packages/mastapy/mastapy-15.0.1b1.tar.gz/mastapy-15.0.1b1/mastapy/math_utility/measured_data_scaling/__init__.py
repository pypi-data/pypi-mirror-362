"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.math_utility.measured_data_scaling._1753 import (
        DataScalingOptions,
    )
    from mastapy._private.math_utility.measured_data_scaling._1754 import (
        DataScalingReferenceValues,
    )
    from mastapy._private.math_utility.measured_data_scaling._1755 import (
        DataScalingReferenceValuesBase,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.math_utility.measured_data_scaling._1753": ["DataScalingOptions"],
        "_private.math_utility.measured_data_scaling._1754": [
            "DataScalingReferenceValues"
        ],
        "_private.math_utility.measured_data_scaling._1755": [
            "DataScalingReferenceValuesBase"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "DataScalingOptions",
    "DataScalingReferenceValues",
    "DataScalingReferenceValuesBase",
)
