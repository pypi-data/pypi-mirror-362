"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.klingelnberg_conical.kn3030._505 import (
        KlingelnbergConicalMeshSingleFlankRating,
    )
    from mastapy._private.gears.rating.klingelnberg_conical.kn3030._506 import (
        KlingelnbergConicalRateableMesh,
    )
    from mastapy._private.gears.rating.klingelnberg_conical.kn3030._507 import (
        KlingelnbergCycloPalloidConicalGearSingleFlankRating,
    )
    from mastapy._private.gears.rating.klingelnberg_conical.kn3030._508 import (
        KlingelnbergCycloPalloidHypoidGearSingleFlankRating,
    )
    from mastapy._private.gears.rating.klingelnberg_conical.kn3030._509 import (
        KlingelnbergCycloPalloidHypoidMeshSingleFlankRating,
    )
    from mastapy._private.gears.rating.klingelnberg_conical.kn3030._510 import (
        KlingelnbergCycloPalloidSpiralBevelMeshSingleFlankRating,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.klingelnberg_conical.kn3030._505": [
            "KlingelnbergConicalMeshSingleFlankRating"
        ],
        "_private.gears.rating.klingelnberg_conical.kn3030._506": [
            "KlingelnbergConicalRateableMesh"
        ],
        "_private.gears.rating.klingelnberg_conical.kn3030._507": [
            "KlingelnbergCycloPalloidConicalGearSingleFlankRating"
        ],
        "_private.gears.rating.klingelnberg_conical.kn3030._508": [
            "KlingelnbergCycloPalloidHypoidGearSingleFlankRating"
        ],
        "_private.gears.rating.klingelnberg_conical.kn3030._509": [
            "KlingelnbergCycloPalloidHypoidMeshSingleFlankRating"
        ],
        "_private.gears.rating.klingelnberg_conical.kn3030._510": [
            "KlingelnbergCycloPalloidSpiralBevelMeshSingleFlankRating"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "KlingelnbergConicalMeshSingleFlankRating",
    "KlingelnbergConicalRateableMesh",
    "KlingelnbergCycloPalloidConicalGearSingleFlankRating",
    "KlingelnbergCycloPalloidHypoidGearSingleFlankRating",
    "KlingelnbergCycloPalloidHypoidMeshSingleFlankRating",
    "KlingelnbergCycloPalloidSpiralBevelMeshSingleFlankRating",
)
