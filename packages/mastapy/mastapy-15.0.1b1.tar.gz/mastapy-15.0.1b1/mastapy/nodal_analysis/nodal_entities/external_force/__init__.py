"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.nodal_analysis.nodal_entities.external_force._171 import (
        ExternalForceEntity,
    )
    from mastapy._private.nodal_analysis.nodal_entities.external_force._172 import (
        ExternalForceLineContactEntity,
    )
    from mastapy._private.nodal_analysis.nodal_entities.external_force._173 import (
        ExternalForceSinglePointEntity,
    )
    from mastapy._private.nodal_analysis.nodal_entities.external_force._174 import (
        GearMeshBothFlankContacts,
    )
    from mastapy._private.nodal_analysis.nodal_entities.external_force._175 import (
        GearMeshDirectSingleFlankContact,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.nodal_analysis.nodal_entities.external_force._171": [
            "ExternalForceEntity"
        ],
        "_private.nodal_analysis.nodal_entities.external_force._172": [
            "ExternalForceLineContactEntity"
        ],
        "_private.nodal_analysis.nodal_entities.external_force._173": [
            "ExternalForceSinglePointEntity"
        ],
        "_private.nodal_analysis.nodal_entities.external_force._174": [
            "GearMeshBothFlankContacts"
        ],
        "_private.nodal_analysis.nodal_entities.external_force._175": [
            "GearMeshDirectSingleFlankContact"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ExternalForceEntity",
    "ExternalForceLineContactEntity",
    "ExternalForceSinglePointEntity",
    "GearMeshBothFlankContacts",
    "GearMeshDirectSingleFlankContact",
)
