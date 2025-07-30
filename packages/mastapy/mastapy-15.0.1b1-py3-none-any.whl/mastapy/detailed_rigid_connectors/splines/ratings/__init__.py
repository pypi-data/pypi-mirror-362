"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.detailed_rigid_connectors.splines.ratings._1608 import (
        AGMA6123SplineHalfRating,
    )
    from mastapy._private.detailed_rigid_connectors.splines.ratings._1609 import (
        AGMA6123SplineJointRating,
    )
    from mastapy._private.detailed_rigid_connectors.splines.ratings._1610 import (
        DIN5466SplineHalfRating,
    )
    from mastapy._private.detailed_rigid_connectors.splines.ratings._1611 import (
        DIN5466SplineRating,
    )
    from mastapy._private.detailed_rigid_connectors.splines.ratings._1612 import (
        GBT17855SplineHalfRating,
    )
    from mastapy._private.detailed_rigid_connectors.splines.ratings._1613 import (
        GBT17855SplineJointRating,
    )
    from mastapy._private.detailed_rigid_connectors.splines.ratings._1614 import (
        SAESplineHalfRating,
    )
    from mastapy._private.detailed_rigid_connectors.splines.ratings._1615 import (
        SAESplineJointRating,
    )
    from mastapy._private.detailed_rigid_connectors.splines.ratings._1616 import (
        SplineHalfRating,
    )
    from mastapy._private.detailed_rigid_connectors.splines.ratings._1617 import (
        SplineJointRating,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.detailed_rigid_connectors.splines.ratings._1608": [
            "AGMA6123SplineHalfRating"
        ],
        "_private.detailed_rigid_connectors.splines.ratings._1609": [
            "AGMA6123SplineJointRating"
        ],
        "_private.detailed_rigid_connectors.splines.ratings._1610": [
            "DIN5466SplineHalfRating"
        ],
        "_private.detailed_rigid_connectors.splines.ratings._1611": [
            "DIN5466SplineRating"
        ],
        "_private.detailed_rigid_connectors.splines.ratings._1612": [
            "GBT17855SplineHalfRating"
        ],
        "_private.detailed_rigid_connectors.splines.ratings._1613": [
            "GBT17855SplineJointRating"
        ],
        "_private.detailed_rigid_connectors.splines.ratings._1614": [
            "SAESplineHalfRating"
        ],
        "_private.detailed_rigid_connectors.splines.ratings._1615": [
            "SAESplineJointRating"
        ],
        "_private.detailed_rigid_connectors.splines.ratings._1616": [
            "SplineHalfRating"
        ],
        "_private.detailed_rigid_connectors.splines.ratings._1617": [
            "SplineJointRating"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AGMA6123SplineHalfRating",
    "AGMA6123SplineJointRating",
    "DIN5466SplineHalfRating",
    "DIN5466SplineRating",
    "GBT17855SplineHalfRating",
    "GBT17855SplineJointRating",
    "SAESplineHalfRating",
    "SAESplineJointRating",
    "SplineHalfRating",
    "SplineJointRating",
)
