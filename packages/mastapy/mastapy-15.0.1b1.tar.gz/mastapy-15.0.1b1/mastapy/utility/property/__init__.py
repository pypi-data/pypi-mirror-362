"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.property._2039 import DeletableCollectionMember
    from mastapy._private.utility.property._2040 import DutyCyclePropertySummary
    from mastapy._private.utility.property._2041 import DutyCyclePropertySummaryForce
    from mastapy._private.utility.property._2042 import (
        DutyCyclePropertySummaryPercentage,
    )
    from mastapy._private.utility.property._2043 import (
        DutyCyclePropertySummarySmallAngle,
    )
    from mastapy._private.utility.property._2044 import DutyCyclePropertySummaryStress
    from mastapy._private.utility.property._2045 import (
        DutyCyclePropertySummaryVeryShortLength,
    )
    from mastapy._private.utility.property._2046 import EnumWithBoolean
    from mastapy._private.utility.property._2047 import (
        NamedRangeWithOverridableMinAndMax,
    )
    from mastapy._private.utility.property._2048 import TypedObjectsWithOption
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.property._2039": ["DeletableCollectionMember"],
        "_private.utility.property._2040": ["DutyCyclePropertySummary"],
        "_private.utility.property._2041": ["DutyCyclePropertySummaryForce"],
        "_private.utility.property._2042": ["DutyCyclePropertySummaryPercentage"],
        "_private.utility.property._2043": ["DutyCyclePropertySummarySmallAngle"],
        "_private.utility.property._2044": ["DutyCyclePropertySummaryStress"],
        "_private.utility.property._2045": ["DutyCyclePropertySummaryVeryShortLength"],
        "_private.utility.property._2046": ["EnumWithBoolean"],
        "_private.utility.property._2047": ["NamedRangeWithOverridableMinAndMax"],
        "_private.utility.property._2048": ["TypedObjectsWithOption"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "DeletableCollectionMember",
    "DutyCyclePropertySummary",
    "DutyCyclePropertySummaryForce",
    "DutyCyclePropertySummaryPercentage",
    "DutyCyclePropertySummarySmallAngle",
    "DutyCyclePropertySummaryStress",
    "DutyCyclePropertySummaryVeryShortLength",
    "EnumWithBoolean",
    "NamedRangeWithOverridableMinAndMax",
    "TypedObjectsWithOption",
)
