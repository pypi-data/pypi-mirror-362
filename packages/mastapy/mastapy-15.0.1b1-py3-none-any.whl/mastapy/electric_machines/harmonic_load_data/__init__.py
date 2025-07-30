"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.electric_machines.harmonic_load_data._1562 import (
        ElectricMachineHarmonicLoadDataBase,
    )
    from mastapy._private.electric_machines.harmonic_load_data._1563 import (
        ForceDisplayOption,
    )
    from mastapy._private.electric_machines.harmonic_load_data._1564 import (
        HarmonicLoadDataBase,
    )
    from mastapy._private.electric_machines.harmonic_load_data._1565 import (
        HarmonicLoadDataControlExcitationOptionBase,
    )
    from mastapy._private.electric_machines.harmonic_load_data._1566 import (
        HarmonicLoadDataType,
    )
    from mastapy._private.electric_machines.harmonic_load_data._1567 import (
        SimpleElectricMachineTooth,
    )
    from mastapy._private.electric_machines.harmonic_load_data._1568 import (
        SpeedDependentHarmonicLoadData,
    )
    from mastapy._private.electric_machines.harmonic_load_data._1569 import (
        StatorToothInterpolator,
    )
    from mastapy._private.electric_machines.harmonic_load_data._1570 import (
        StatorToothLoadInterpolator,
    )
    from mastapy._private.electric_machines.harmonic_load_data._1571 import (
        StatorToothMomentInterpolator,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.electric_machines.harmonic_load_data._1562": [
            "ElectricMachineHarmonicLoadDataBase"
        ],
        "_private.electric_machines.harmonic_load_data._1563": ["ForceDisplayOption"],
        "_private.electric_machines.harmonic_load_data._1564": ["HarmonicLoadDataBase"],
        "_private.electric_machines.harmonic_load_data._1565": [
            "HarmonicLoadDataControlExcitationOptionBase"
        ],
        "_private.electric_machines.harmonic_load_data._1566": ["HarmonicLoadDataType"],
        "_private.electric_machines.harmonic_load_data._1567": [
            "SimpleElectricMachineTooth"
        ],
        "_private.electric_machines.harmonic_load_data._1568": [
            "SpeedDependentHarmonicLoadData"
        ],
        "_private.electric_machines.harmonic_load_data._1569": [
            "StatorToothInterpolator"
        ],
        "_private.electric_machines.harmonic_load_data._1570": [
            "StatorToothLoadInterpolator"
        ],
        "_private.electric_machines.harmonic_load_data._1571": [
            "StatorToothMomentInterpolator"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ElectricMachineHarmonicLoadDataBase",
    "ForceDisplayOption",
    "HarmonicLoadDataBase",
    "HarmonicLoadDataControlExcitationOptionBase",
    "HarmonicLoadDataType",
    "SimpleElectricMachineTooth",
    "SpeedDependentHarmonicLoadData",
    "StatorToothInterpolator",
    "StatorToothLoadInterpolator",
    "StatorToothMomentInterpolator",
)
