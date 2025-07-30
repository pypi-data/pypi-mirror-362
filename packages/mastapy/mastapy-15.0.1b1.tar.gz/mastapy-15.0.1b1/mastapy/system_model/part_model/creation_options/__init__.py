"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.creation_options._2809 import (
        BeltCreationOptions,
    )
    from mastapy._private.system_model.part_model.creation_options._2810 import (
        CycloidalAssemblyCreationOptions,
    )
    from mastapy._private.system_model.part_model.creation_options._2811 import (
        CylindricalGearLinearTrainCreationOptions,
    )
    from mastapy._private.system_model.part_model.creation_options._2812 import (
        MicrophoneArrayCreationOptions,
    )
    from mastapy._private.system_model.part_model.creation_options._2813 import (
        PlanetCarrierCreationOptions,
    )
    from mastapy._private.system_model.part_model.creation_options._2814 import (
        ShaftCreationOptions,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.creation_options._2809": [
            "BeltCreationOptions"
        ],
        "_private.system_model.part_model.creation_options._2810": [
            "CycloidalAssemblyCreationOptions"
        ],
        "_private.system_model.part_model.creation_options._2811": [
            "CylindricalGearLinearTrainCreationOptions"
        ],
        "_private.system_model.part_model.creation_options._2812": [
            "MicrophoneArrayCreationOptions"
        ],
        "_private.system_model.part_model.creation_options._2813": [
            "PlanetCarrierCreationOptions"
        ],
        "_private.system_model.part_model.creation_options._2814": [
            "ShaftCreationOptions"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BeltCreationOptions",
    "CycloidalAssemblyCreationOptions",
    "CylindricalGearLinearTrainCreationOptions",
    "MicrophoneArrayCreationOptions",
    "PlanetCarrierCreationOptions",
    "ShaftCreationOptions",
)
