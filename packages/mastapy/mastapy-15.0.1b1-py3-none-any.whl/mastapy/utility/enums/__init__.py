"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.enums._2016 import BearingForceArrowOption
    from mastapy._private.utility.enums._2017 import PropertySpecificationMethod
    from mastapy._private.utility.enums._2018 import TableAndChartOptions
    from mastapy._private.utility.enums._2019 import ThreeDViewContourOption
    from mastapy._private.utility.enums._2020 import (
        ThreeDViewContourOptionFirstSelection,
    )
    from mastapy._private.utility.enums._2021 import (
        ThreeDViewContourOptionSecondSelection,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.enums._2016": ["BearingForceArrowOption"],
        "_private.utility.enums._2017": ["PropertySpecificationMethod"],
        "_private.utility.enums._2018": ["TableAndChartOptions"],
        "_private.utility.enums._2019": ["ThreeDViewContourOption"],
        "_private.utility.enums._2020": ["ThreeDViewContourOptionFirstSelection"],
        "_private.utility.enums._2021": ["ThreeDViewContourOptionSecondSelection"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BearingForceArrowOption",
    "PropertySpecificationMethod",
    "TableAndChartOptions",
    "ThreeDViewContourOption",
    "ThreeDViewContourOptionFirstSelection",
    "ThreeDViewContourOptionSecondSelection",
)
