"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.nodal_analysis.geometry_modeller_link._229 import (
        BaseGeometryModellerDimension,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._230 import (
        GearTipRadiusClashTest,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._231 import (
        GeometryModellerAngleDimension,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._232 import (
        GeometryModellerCountDimension,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._233 import (
        GeometryModellerDesignInformation,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._234 import (
        GeometryModellerDimension,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._235 import (
        GeometryModellerDimensions,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._236 import (
        GeometryModellerDimensionType,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._237 import (
        GeometryModellerLengthDimension,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._238 import (
        GeometryModellerSettings,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._239 import (
        GeometryModellerUnitlessDimension,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._240 import (
        GeometryTypeForComponentImport,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._241 import MeshRequest
    from mastapy._private.nodal_analysis.geometry_modeller_link._242 import (
        MeshRequestResult,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._243 import (
        ProfileFromImport,
    )
    from mastapy._private.nodal_analysis.geometry_modeller_link._244 import (
        RepositionComponentDetails,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.nodal_analysis.geometry_modeller_link._229": [
            "BaseGeometryModellerDimension"
        ],
        "_private.nodal_analysis.geometry_modeller_link._230": [
            "GearTipRadiusClashTest"
        ],
        "_private.nodal_analysis.geometry_modeller_link._231": [
            "GeometryModellerAngleDimension"
        ],
        "_private.nodal_analysis.geometry_modeller_link._232": [
            "GeometryModellerCountDimension"
        ],
        "_private.nodal_analysis.geometry_modeller_link._233": [
            "GeometryModellerDesignInformation"
        ],
        "_private.nodal_analysis.geometry_modeller_link._234": [
            "GeometryModellerDimension"
        ],
        "_private.nodal_analysis.geometry_modeller_link._235": [
            "GeometryModellerDimensions"
        ],
        "_private.nodal_analysis.geometry_modeller_link._236": [
            "GeometryModellerDimensionType"
        ],
        "_private.nodal_analysis.geometry_modeller_link._237": [
            "GeometryModellerLengthDimension"
        ],
        "_private.nodal_analysis.geometry_modeller_link._238": [
            "GeometryModellerSettings"
        ],
        "_private.nodal_analysis.geometry_modeller_link._239": [
            "GeometryModellerUnitlessDimension"
        ],
        "_private.nodal_analysis.geometry_modeller_link._240": [
            "GeometryTypeForComponentImport"
        ],
        "_private.nodal_analysis.geometry_modeller_link._241": ["MeshRequest"],
        "_private.nodal_analysis.geometry_modeller_link._242": ["MeshRequestResult"],
        "_private.nodal_analysis.geometry_modeller_link._243": ["ProfileFromImport"],
        "_private.nodal_analysis.geometry_modeller_link._244": [
            "RepositionComponentDetails"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BaseGeometryModellerDimension",
    "GearTipRadiusClashTest",
    "GeometryModellerAngleDimension",
    "GeometryModellerCountDimension",
    "GeometryModellerDesignInformation",
    "GeometryModellerDimension",
    "GeometryModellerDimensions",
    "GeometryModellerDimensionType",
    "GeometryModellerLengthDimension",
    "GeometryModellerSettings",
    "GeometryModellerUnitlessDimension",
    "GeometryTypeForComponentImport",
    "MeshRequest",
    "MeshRequestResult",
    "ProfileFromImport",
    "RepositionComponentDetails",
)
