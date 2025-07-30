"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.connections_and_sockets._2486 import (
        AbstractShaftToMountableComponentConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2487 import (
        BearingInnerSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2488 import (
        BearingOuterSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2489 import (
        BeltConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2490 import (
        CoaxialConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2491 import (
        ComponentConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2492 import (
        ComponentMeasurer,
    )
    from mastapy._private.system_model.connections_and_sockets._2493 import Connection
    from mastapy._private.system_model.connections_and_sockets._2494 import (
        CVTBeltConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2495 import (
        CVTPulleySocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2496 import (
        CylindricalComponentConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2497 import (
        CylindricalSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2498 import (
        DatumMeasurement,
    )
    from mastapy._private.system_model.connections_and_sockets._2499 import (
        ElectricMachineStatorSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2500 import (
        InnerShaftSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2501 import (
        InnerShaftSocketBase,
    )
    from mastapy._private.system_model.connections_and_sockets._2502 import (
        InterMountableComponentConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2503 import (
        MountableComponentInnerSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2504 import (
        MountableComponentOuterSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2505 import (
        MountableComponentSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2506 import (
        OuterShaftSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2507 import (
        OuterShaftSocketBase,
    )
    from mastapy._private.system_model.connections_and_sockets._2508 import (
        PlanetaryConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2509 import (
        PlanetarySocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2510 import (
        PlanetarySocketBase,
    )
    from mastapy._private.system_model.connections_and_sockets._2511 import PulleySocket
    from mastapy._private.system_model.connections_and_sockets._2512 import (
        RealignmentResult,
    )
    from mastapy._private.system_model.connections_and_sockets._2513 import (
        RollingRingConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2514 import (
        RollingRingSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2515 import ShaftSocket
    from mastapy._private.system_model.connections_and_sockets._2516 import (
        ShaftToMountableComponentConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2517 import Socket
    from mastapy._private.system_model.connections_and_sockets._2518 import (
        SocketConnectionOptions,
    )
    from mastapy._private.system_model.connections_and_sockets._2519 import (
        SocketConnectionSelection,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.connections_and_sockets._2486": [
            "AbstractShaftToMountableComponentConnection"
        ],
        "_private.system_model.connections_and_sockets._2487": ["BearingInnerSocket"],
        "_private.system_model.connections_and_sockets._2488": ["BearingOuterSocket"],
        "_private.system_model.connections_and_sockets._2489": ["BeltConnection"],
        "_private.system_model.connections_and_sockets._2490": ["CoaxialConnection"],
        "_private.system_model.connections_and_sockets._2491": ["ComponentConnection"],
        "_private.system_model.connections_and_sockets._2492": ["ComponentMeasurer"],
        "_private.system_model.connections_and_sockets._2493": ["Connection"],
        "_private.system_model.connections_and_sockets._2494": ["CVTBeltConnection"],
        "_private.system_model.connections_and_sockets._2495": ["CVTPulleySocket"],
        "_private.system_model.connections_and_sockets._2496": [
            "CylindricalComponentConnection"
        ],
        "_private.system_model.connections_and_sockets._2497": ["CylindricalSocket"],
        "_private.system_model.connections_and_sockets._2498": ["DatumMeasurement"],
        "_private.system_model.connections_and_sockets._2499": [
            "ElectricMachineStatorSocket"
        ],
        "_private.system_model.connections_and_sockets._2500": ["InnerShaftSocket"],
        "_private.system_model.connections_and_sockets._2501": ["InnerShaftSocketBase"],
        "_private.system_model.connections_and_sockets._2502": [
            "InterMountableComponentConnection"
        ],
        "_private.system_model.connections_and_sockets._2503": [
            "MountableComponentInnerSocket"
        ],
        "_private.system_model.connections_and_sockets._2504": [
            "MountableComponentOuterSocket"
        ],
        "_private.system_model.connections_and_sockets._2505": [
            "MountableComponentSocket"
        ],
        "_private.system_model.connections_and_sockets._2506": ["OuterShaftSocket"],
        "_private.system_model.connections_and_sockets._2507": ["OuterShaftSocketBase"],
        "_private.system_model.connections_and_sockets._2508": ["PlanetaryConnection"],
        "_private.system_model.connections_and_sockets._2509": ["PlanetarySocket"],
        "_private.system_model.connections_and_sockets._2510": ["PlanetarySocketBase"],
        "_private.system_model.connections_and_sockets._2511": ["PulleySocket"],
        "_private.system_model.connections_and_sockets._2512": ["RealignmentResult"],
        "_private.system_model.connections_and_sockets._2513": [
            "RollingRingConnection"
        ],
        "_private.system_model.connections_and_sockets._2514": ["RollingRingSocket"],
        "_private.system_model.connections_and_sockets._2515": ["ShaftSocket"],
        "_private.system_model.connections_and_sockets._2516": [
            "ShaftToMountableComponentConnection"
        ],
        "_private.system_model.connections_and_sockets._2517": ["Socket"],
        "_private.system_model.connections_and_sockets._2518": [
            "SocketConnectionOptions"
        ],
        "_private.system_model.connections_and_sockets._2519": [
            "SocketConnectionSelection"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractShaftToMountableComponentConnection",
    "BearingInnerSocket",
    "BearingOuterSocket",
    "BeltConnection",
    "CoaxialConnection",
    "ComponentConnection",
    "ComponentMeasurer",
    "Connection",
    "CVTBeltConnection",
    "CVTPulleySocket",
    "CylindricalComponentConnection",
    "CylindricalSocket",
    "DatumMeasurement",
    "ElectricMachineStatorSocket",
    "InnerShaftSocket",
    "InnerShaftSocketBase",
    "InterMountableComponentConnection",
    "MountableComponentInnerSocket",
    "MountableComponentOuterSocket",
    "MountableComponentSocket",
    "OuterShaftSocket",
    "OuterShaftSocketBase",
    "PlanetaryConnection",
    "PlanetarySocket",
    "PlanetarySocketBase",
    "PulleySocket",
    "RealignmentResult",
    "RollingRingConnection",
    "RollingRingSocket",
    "ShaftSocket",
    "ShaftToMountableComponentConnection",
    "Socket",
    "SocketConnectionOptions",
    "SocketConnectionSelection",
)
