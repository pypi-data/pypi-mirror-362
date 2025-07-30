"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.fe._2576 import AlignConnectedComponentOptions
    from mastapy._private.system_model.fe._2577 import AlignmentMethod
    from mastapy._private.system_model.fe._2578 import AlignmentMethodForRaceBearing
    from mastapy._private.system_model.fe._2579 import AlignmentUsingAxialNodePositions
    from mastapy._private.system_model.fe._2580 import AngleSource
    from mastapy._private.system_model.fe._2581 import BaseFEWithSelection
    from mastapy._private.system_model.fe._2582 import BatchOperations
    from mastapy._private.system_model.fe._2583 import BearingNodeAlignmentOption
    from mastapy._private.system_model.fe._2584 import BearingNodeOption
    from mastapy._private.system_model.fe._2585 import BearingRaceNodeLink
    from mastapy._private.system_model.fe._2586 import BearingRacePosition
    from mastapy._private.system_model.fe._2587 import ComponentOrientationOption
    from mastapy._private.system_model.fe._2588 import ContactPairWithSelection
    from mastapy._private.system_model.fe._2589 import CoordinateSystemWithSelection
    from mastapy._private.system_model.fe._2590 import CreateConnectedComponentOptions
    from mastapy._private.system_model.fe._2591 import (
        CreateMicrophoneNormalToSurfaceOptions,
    )
    from mastapy._private.system_model.fe._2592 import DegreeOfFreedomBoundaryCondition
    from mastapy._private.system_model.fe._2593 import (
        DegreeOfFreedomBoundaryConditionAngular,
    )
    from mastapy._private.system_model.fe._2594 import (
        DegreeOfFreedomBoundaryConditionLinear,
    )
    from mastapy._private.system_model.fe._2595 import ElectricMachineDataSet
    from mastapy._private.system_model.fe._2596 import ElectricMachineDynamicLoadData
    from mastapy._private.system_model.fe._2597 import ElementFaceGroupWithSelection
    from mastapy._private.system_model.fe._2598 import ElementPropertiesWithSelection
    from mastapy._private.system_model.fe._2599 import FEEntityGroupWithSelection
    from mastapy._private.system_model.fe._2600 import FEExportSettings
    from mastapy._private.system_model.fe._2601 import FEPartDRIVASurfaceSelection
    from mastapy._private.system_model.fe._2602 import FEPartWithBatchOptions
    from mastapy._private.system_model.fe._2603 import FEStiffnessGeometry
    from mastapy._private.system_model.fe._2604 import FEStiffnessTester
    from mastapy._private.system_model.fe._2605 import FESubstructure
    from mastapy._private.system_model.fe._2606 import FESubstructureExportOptions
    from mastapy._private.system_model.fe._2607 import FESubstructureNode
    from mastapy._private.system_model.fe._2608 import FESubstructureNodeModeShape
    from mastapy._private.system_model.fe._2609 import FESubstructureNodeModeShapes
    from mastapy._private.system_model.fe._2610 import FESubstructureType
    from mastapy._private.system_model.fe._2611 import FESubstructureWithBatchOptions
    from mastapy._private.system_model.fe._2612 import FESubstructureWithSelection
    from mastapy._private.system_model.fe._2613 import (
        FESubstructureWithSelectionComponents,
    )
    from mastapy._private.system_model.fe._2614 import (
        FESubstructureWithSelectionForHarmonicAnalysis,
    )
    from mastapy._private.system_model.fe._2615 import (
        FESubstructureWithSelectionForModalAnalysis,
    )
    from mastapy._private.system_model.fe._2616 import (
        FESubstructureWithSelectionForStaticAnalysis,
    )
    from mastapy._private.system_model.fe._2617 import GearMeshingOptions
    from mastapy._private.system_model.fe._2618 import (
        IndependentMASTACreatedCondensationNode,
    )
    from mastapy._private.system_model.fe._2619 import (
        IndependentMASTACreatedConstrainedNodes,
    )
    from mastapy._private.system_model.fe._2620 import (
        IndependentMASTACreatedConstrainedNodesWithSelectionComponents,
    )
    from mastapy._private.system_model.fe._2621 import (
        IndependentMASTACreatedRigidlyConnectedNodeGroup,
    )
    from mastapy._private.system_model.fe._2622 import (
        LinkComponentAxialPositionErrorReporter,
    )
    from mastapy._private.system_model.fe._2623 import LinkNodeSource
    from mastapy._private.system_model.fe._2624 import MaterialPropertiesWithSelection
    from mastapy._private.system_model.fe._2625 import (
        NodeBoundaryConditionStaticAnalysis,
    )
    from mastapy._private.system_model.fe._2626 import NodeGroupWithSelection
    from mastapy._private.system_model.fe._2627 import NodeSelectionDepthOption
    from mastapy._private.system_model.fe._2628 import (
        OptionsWhenExternalFEFileAlreadyExists,
    )
    from mastapy._private.system_model.fe._2629 import PerLinkExportOptions
    from mastapy._private.system_model.fe._2630 import PerNodeExportOptions
    from mastapy._private.system_model.fe._2631 import RaceBearingFE
    from mastapy._private.system_model.fe._2632 import RaceBearingFESystemDeflection
    from mastapy._private.system_model.fe._2633 import RaceBearingFEWithSelection
    from mastapy._private.system_model.fe._2634 import ReplacedShaftSelectionHelper
    from mastapy._private.system_model.fe._2635 import SystemDeflectionFEExportOptions
    from mastapy._private.system_model.fe._2636 import ThermalExpansionOption
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.fe._2576": ["AlignConnectedComponentOptions"],
        "_private.system_model.fe._2577": ["AlignmentMethod"],
        "_private.system_model.fe._2578": ["AlignmentMethodForRaceBearing"],
        "_private.system_model.fe._2579": ["AlignmentUsingAxialNodePositions"],
        "_private.system_model.fe._2580": ["AngleSource"],
        "_private.system_model.fe._2581": ["BaseFEWithSelection"],
        "_private.system_model.fe._2582": ["BatchOperations"],
        "_private.system_model.fe._2583": ["BearingNodeAlignmentOption"],
        "_private.system_model.fe._2584": ["BearingNodeOption"],
        "_private.system_model.fe._2585": ["BearingRaceNodeLink"],
        "_private.system_model.fe._2586": ["BearingRacePosition"],
        "_private.system_model.fe._2587": ["ComponentOrientationOption"],
        "_private.system_model.fe._2588": ["ContactPairWithSelection"],
        "_private.system_model.fe._2589": ["CoordinateSystemWithSelection"],
        "_private.system_model.fe._2590": ["CreateConnectedComponentOptions"],
        "_private.system_model.fe._2591": ["CreateMicrophoneNormalToSurfaceOptions"],
        "_private.system_model.fe._2592": ["DegreeOfFreedomBoundaryCondition"],
        "_private.system_model.fe._2593": ["DegreeOfFreedomBoundaryConditionAngular"],
        "_private.system_model.fe._2594": ["DegreeOfFreedomBoundaryConditionLinear"],
        "_private.system_model.fe._2595": ["ElectricMachineDataSet"],
        "_private.system_model.fe._2596": ["ElectricMachineDynamicLoadData"],
        "_private.system_model.fe._2597": ["ElementFaceGroupWithSelection"],
        "_private.system_model.fe._2598": ["ElementPropertiesWithSelection"],
        "_private.system_model.fe._2599": ["FEEntityGroupWithSelection"],
        "_private.system_model.fe._2600": ["FEExportSettings"],
        "_private.system_model.fe._2601": ["FEPartDRIVASurfaceSelection"],
        "_private.system_model.fe._2602": ["FEPartWithBatchOptions"],
        "_private.system_model.fe._2603": ["FEStiffnessGeometry"],
        "_private.system_model.fe._2604": ["FEStiffnessTester"],
        "_private.system_model.fe._2605": ["FESubstructure"],
        "_private.system_model.fe._2606": ["FESubstructureExportOptions"],
        "_private.system_model.fe._2607": ["FESubstructureNode"],
        "_private.system_model.fe._2608": ["FESubstructureNodeModeShape"],
        "_private.system_model.fe._2609": ["FESubstructureNodeModeShapes"],
        "_private.system_model.fe._2610": ["FESubstructureType"],
        "_private.system_model.fe._2611": ["FESubstructureWithBatchOptions"],
        "_private.system_model.fe._2612": ["FESubstructureWithSelection"],
        "_private.system_model.fe._2613": ["FESubstructureWithSelectionComponents"],
        "_private.system_model.fe._2614": [
            "FESubstructureWithSelectionForHarmonicAnalysis"
        ],
        "_private.system_model.fe._2615": [
            "FESubstructureWithSelectionForModalAnalysis"
        ],
        "_private.system_model.fe._2616": [
            "FESubstructureWithSelectionForStaticAnalysis"
        ],
        "_private.system_model.fe._2617": ["GearMeshingOptions"],
        "_private.system_model.fe._2618": ["IndependentMASTACreatedCondensationNode"],
        "_private.system_model.fe._2619": ["IndependentMASTACreatedConstrainedNodes"],
        "_private.system_model.fe._2620": [
            "IndependentMASTACreatedConstrainedNodesWithSelectionComponents"
        ],
        "_private.system_model.fe._2621": [
            "IndependentMASTACreatedRigidlyConnectedNodeGroup"
        ],
        "_private.system_model.fe._2622": ["LinkComponentAxialPositionErrorReporter"],
        "_private.system_model.fe._2623": ["LinkNodeSource"],
        "_private.system_model.fe._2624": ["MaterialPropertiesWithSelection"],
        "_private.system_model.fe._2625": ["NodeBoundaryConditionStaticAnalysis"],
        "_private.system_model.fe._2626": ["NodeGroupWithSelection"],
        "_private.system_model.fe._2627": ["NodeSelectionDepthOption"],
        "_private.system_model.fe._2628": ["OptionsWhenExternalFEFileAlreadyExists"],
        "_private.system_model.fe._2629": ["PerLinkExportOptions"],
        "_private.system_model.fe._2630": ["PerNodeExportOptions"],
        "_private.system_model.fe._2631": ["RaceBearingFE"],
        "_private.system_model.fe._2632": ["RaceBearingFESystemDeflection"],
        "_private.system_model.fe._2633": ["RaceBearingFEWithSelection"],
        "_private.system_model.fe._2634": ["ReplacedShaftSelectionHelper"],
        "_private.system_model.fe._2635": ["SystemDeflectionFEExportOptions"],
        "_private.system_model.fe._2636": ["ThermalExpansionOption"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AlignConnectedComponentOptions",
    "AlignmentMethod",
    "AlignmentMethodForRaceBearing",
    "AlignmentUsingAxialNodePositions",
    "AngleSource",
    "BaseFEWithSelection",
    "BatchOperations",
    "BearingNodeAlignmentOption",
    "BearingNodeOption",
    "BearingRaceNodeLink",
    "BearingRacePosition",
    "ComponentOrientationOption",
    "ContactPairWithSelection",
    "CoordinateSystemWithSelection",
    "CreateConnectedComponentOptions",
    "CreateMicrophoneNormalToSurfaceOptions",
    "DegreeOfFreedomBoundaryCondition",
    "DegreeOfFreedomBoundaryConditionAngular",
    "DegreeOfFreedomBoundaryConditionLinear",
    "ElectricMachineDataSet",
    "ElectricMachineDynamicLoadData",
    "ElementFaceGroupWithSelection",
    "ElementPropertiesWithSelection",
    "FEEntityGroupWithSelection",
    "FEExportSettings",
    "FEPartDRIVASurfaceSelection",
    "FEPartWithBatchOptions",
    "FEStiffnessGeometry",
    "FEStiffnessTester",
    "FESubstructure",
    "FESubstructureExportOptions",
    "FESubstructureNode",
    "FESubstructureNodeModeShape",
    "FESubstructureNodeModeShapes",
    "FESubstructureType",
    "FESubstructureWithBatchOptions",
    "FESubstructureWithSelection",
    "FESubstructureWithSelectionComponents",
    "FESubstructureWithSelectionForHarmonicAnalysis",
    "FESubstructureWithSelectionForModalAnalysis",
    "FESubstructureWithSelectionForStaticAnalysis",
    "GearMeshingOptions",
    "IndependentMASTACreatedCondensationNode",
    "IndependentMASTACreatedConstrainedNodes",
    "IndependentMASTACreatedConstrainedNodesWithSelectionComponents",
    "IndependentMASTACreatedRigidlyConnectedNodeGroup",
    "LinkComponentAxialPositionErrorReporter",
    "LinkNodeSource",
    "MaterialPropertiesWithSelection",
    "NodeBoundaryConditionStaticAnalysis",
    "NodeGroupWithSelection",
    "NodeSelectionDepthOption",
    "OptionsWhenExternalFEFileAlreadyExists",
    "PerLinkExportOptions",
    "PerNodeExportOptions",
    "RaceBearingFE",
    "RaceBearingFESystemDeflection",
    "RaceBearingFEWithSelection",
    "ReplacedShaftSelectionHelper",
    "SystemDeflectionFEExportOptions",
    "ThermalExpansionOption",
)
