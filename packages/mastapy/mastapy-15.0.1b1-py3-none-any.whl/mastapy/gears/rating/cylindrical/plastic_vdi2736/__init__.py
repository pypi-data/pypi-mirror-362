"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736._581 import (
        MetalPlasticOrPlasticMetalVDI2736MeshSingleFlankRating,
    )
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736._582 import (
        PlasticGearVDI2736AbstractGearSingleFlankRating,
    )
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736._583 import (
        PlasticGearVDI2736AbstractMeshSingleFlankRating,
    )
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736._584 import (
        PlasticGearVDI2736AbstractRateableMesh,
    )
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736._585 import (
        PlasticPlasticVDI2736MeshSingleFlankRating,
    )
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736._586 import (
        PlasticSNCurveForTheSpecifiedOperatingConditions,
    )
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736._587 import (
        PlasticVDI2736GearSingleFlankRatingInAMetalPlasticOrAPlasticMetalMesh,
    )
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736._588 import (
        PlasticVDI2736GearSingleFlankRatingInAPlasticPlasticMesh,
    )
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736._589 import (
        VDI2736MetalPlasticRateableMesh,
    )
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736._590 import (
        VDI2736PlasticMetalRateableMesh,
    )
    from mastapy._private.gears.rating.cylindrical.plastic_vdi2736._591 import (
        VDI2736PlasticPlasticRateableMesh,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.cylindrical.plastic_vdi2736._581": [
            "MetalPlasticOrPlasticMetalVDI2736MeshSingleFlankRating"
        ],
        "_private.gears.rating.cylindrical.plastic_vdi2736._582": [
            "PlasticGearVDI2736AbstractGearSingleFlankRating"
        ],
        "_private.gears.rating.cylindrical.plastic_vdi2736._583": [
            "PlasticGearVDI2736AbstractMeshSingleFlankRating"
        ],
        "_private.gears.rating.cylindrical.plastic_vdi2736._584": [
            "PlasticGearVDI2736AbstractRateableMesh"
        ],
        "_private.gears.rating.cylindrical.plastic_vdi2736._585": [
            "PlasticPlasticVDI2736MeshSingleFlankRating"
        ],
        "_private.gears.rating.cylindrical.plastic_vdi2736._586": [
            "PlasticSNCurveForTheSpecifiedOperatingConditions"
        ],
        "_private.gears.rating.cylindrical.plastic_vdi2736._587": [
            "PlasticVDI2736GearSingleFlankRatingInAMetalPlasticOrAPlasticMetalMesh"
        ],
        "_private.gears.rating.cylindrical.plastic_vdi2736._588": [
            "PlasticVDI2736GearSingleFlankRatingInAPlasticPlasticMesh"
        ],
        "_private.gears.rating.cylindrical.plastic_vdi2736._589": [
            "VDI2736MetalPlasticRateableMesh"
        ],
        "_private.gears.rating.cylindrical.plastic_vdi2736._590": [
            "VDI2736PlasticMetalRateableMesh"
        ],
        "_private.gears.rating.cylindrical.plastic_vdi2736._591": [
            "VDI2736PlasticPlasticRateableMesh"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "MetalPlasticOrPlasticMetalVDI2736MeshSingleFlankRating",
    "PlasticGearVDI2736AbstractGearSingleFlankRating",
    "PlasticGearVDI2736AbstractMeshSingleFlankRating",
    "PlasticGearVDI2736AbstractRateableMesh",
    "PlasticPlasticVDI2736MeshSingleFlankRating",
    "PlasticSNCurveForTheSpecifiedOperatingConditions",
    "PlasticVDI2736GearSingleFlankRatingInAMetalPlasticOrAPlasticMetalMesh",
    "PlasticVDI2736GearSingleFlankRatingInAPlasticPlasticMesh",
    "VDI2736MetalPlasticRateableMesh",
    "VDI2736PlasticMetalRateableMesh",
    "VDI2736PlasticPlasticRateableMesh",
)
