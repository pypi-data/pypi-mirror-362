"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.connections_and_sockets.couplings._2563 import (
        ClutchConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2564 import (
        ClutchSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2565 import (
        ConceptCouplingConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2566 import (
        ConceptCouplingSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2567 import (
        CouplingConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2568 import (
        CouplingSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2569 import (
        PartToPartShearCouplingConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2570 import (
        PartToPartShearCouplingSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2571 import (
        SpringDamperConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2572 import (
        SpringDamperSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2573 import (
        TorqueConverterConnection,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2574 import (
        TorqueConverterPumpSocket,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings._2575 import (
        TorqueConverterTurbineSocket,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.connections_and_sockets.couplings._2563": [
            "ClutchConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2564": [
            "ClutchSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2565": [
            "ConceptCouplingConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2566": [
            "ConceptCouplingSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2567": [
            "CouplingConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2568": [
            "CouplingSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2569": [
            "PartToPartShearCouplingConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2570": [
            "PartToPartShearCouplingSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2571": [
            "SpringDamperConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2572": [
            "SpringDamperSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2573": [
            "TorqueConverterConnection"
        ],
        "_private.system_model.connections_and_sockets.couplings._2574": [
            "TorqueConverterPumpSocket"
        ],
        "_private.system_model.connections_and_sockets.couplings._2575": [
            "TorqueConverterTurbineSocket"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ClutchConnection",
    "ClutchSocket",
    "ConceptCouplingConnection",
    "ConceptCouplingSocket",
    "CouplingConnection",
    "CouplingSocket",
    "PartToPartShearCouplingConnection",
    "PartToPartShearCouplingSocket",
    "SpringDamperConnection",
    "SpringDamperSocket",
    "TorqueConverterConnection",
    "TorqueConverterPumpSocket",
    "TorqueConverterTurbineSocket",
)
