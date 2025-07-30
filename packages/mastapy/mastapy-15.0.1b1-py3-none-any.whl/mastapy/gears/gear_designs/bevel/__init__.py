"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs.bevel._1299 import (
        AGMAGleasonConicalGearGeometryMethods,
    )
    from mastapy._private.gears.gear_designs.bevel._1300 import BevelGearDesign
    from mastapy._private.gears.gear_designs.bevel._1301 import BevelGearMeshDesign
    from mastapy._private.gears.gear_designs.bevel._1302 import BevelGearSetDesign
    from mastapy._private.gears.gear_designs.bevel._1303 import BevelMeshedGearDesign
    from mastapy._private.gears.gear_designs.bevel._1304 import (
        DrivenMachineCharacteristicGleason,
    )
    from mastapy._private.gears.gear_designs.bevel._1305 import EdgeRadiusType
    from mastapy._private.gears.gear_designs.bevel._1306 import FinishingMethods
    from mastapy._private.gears.gear_designs.bevel._1307 import (
        MachineCharacteristicAGMAKlingelnberg,
    )
    from mastapy._private.gears.gear_designs.bevel._1308 import (
        PrimeMoverCharacteristicGleason,
    )
    from mastapy._private.gears.gear_designs.bevel._1309 import (
        ToothProportionsInputMethod,
    )
    from mastapy._private.gears.gear_designs.bevel._1310 import (
        ToothThicknessSpecificationMethod,
    )
    from mastapy._private.gears.gear_designs.bevel._1311 import (
        WheelFinishCutterPointWidthRestrictionMethod,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs.bevel._1299": [
            "AGMAGleasonConicalGearGeometryMethods"
        ],
        "_private.gears.gear_designs.bevel._1300": ["BevelGearDesign"],
        "_private.gears.gear_designs.bevel._1301": ["BevelGearMeshDesign"],
        "_private.gears.gear_designs.bevel._1302": ["BevelGearSetDesign"],
        "_private.gears.gear_designs.bevel._1303": ["BevelMeshedGearDesign"],
        "_private.gears.gear_designs.bevel._1304": [
            "DrivenMachineCharacteristicGleason"
        ],
        "_private.gears.gear_designs.bevel._1305": ["EdgeRadiusType"],
        "_private.gears.gear_designs.bevel._1306": ["FinishingMethods"],
        "_private.gears.gear_designs.bevel._1307": [
            "MachineCharacteristicAGMAKlingelnberg"
        ],
        "_private.gears.gear_designs.bevel._1308": ["PrimeMoverCharacteristicGleason"],
        "_private.gears.gear_designs.bevel._1309": ["ToothProportionsInputMethod"],
        "_private.gears.gear_designs.bevel._1310": [
            "ToothThicknessSpecificationMethod"
        ],
        "_private.gears.gear_designs.bevel._1311": [
            "WheelFinishCutterPointWidthRestrictionMethod"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AGMAGleasonConicalGearGeometryMethods",
    "BevelGearDesign",
    "BevelGearMeshDesign",
    "BevelGearSetDesign",
    "BevelMeshedGearDesign",
    "DrivenMachineCharacteristicGleason",
    "EdgeRadiusType",
    "FinishingMethods",
    "MachineCharacteristicAGMAKlingelnberg",
    "PrimeMoverCharacteristicGleason",
    "ToothProportionsInputMethod",
    "ToothThicknessSpecificationMethod",
    "WheelFinishCutterPointWidthRestrictionMethod",
)
