"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.analyses_and_results.load_case_groups._5948 import (
        AbstractDesignStateLoadCaseGroup,
    )
    from mastapy._private.system_model.analyses_and_results.load_case_groups._5949 import (
        AbstractLoadCaseGroup,
    )
    from mastapy._private.system_model.analyses_and_results.load_case_groups._5950 import (
        AbstractStaticLoadCaseGroup,
    )
    from mastapy._private.system_model.analyses_and_results.load_case_groups._5951 import (
        ClutchEngagementStatus,
    )
    from mastapy._private.system_model.analyses_and_results.load_case_groups._5952 import (
        ConceptSynchroGearEngagementStatus,
    )
    from mastapy._private.system_model.analyses_and_results.load_case_groups._5953 import (
        DesignState,
    )
    from mastapy._private.system_model.analyses_and_results.load_case_groups._5954 import (
        DutyCycle,
    )
    from mastapy._private.system_model.analyses_and_results.load_case_groups._5955 import (
        GenericClutchEngagementStatus,
    )
    from mastapy._private.system_model.analyses_and_results.load_case_groups._5956 import (
        LoadCaseGroupHistograms,
    )
    from mastapy._private.system_model.analyses_and_results.load_case_groups._5957 import (
        SubGroupInSingleDesignState,
    )
    from mastapy._private.system_model.analyses_and_results.load_case_groups._5958 import (
        SystemOptimisationGearSet,
    )
    from mastapy._private.system_model.analyses_and_results.load_case_groups._5959 import (
        SystemOptimiserGearSetOptimisation,
    )
    from mastapy._private.system_model.analyses_and_results.load_case_groups._5960 import (
        SystemOptimiserTargets,
    )
    from mastapy._private.system_model.analyses_and_results.load_case_groups._5961 import (
        TimeSeriesLoadCaseGroup,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.analyses_and_results.load_case_groups._5948": [
            "AbstractDesignStateLoadCaseGroup"
        ],
        "_private.system_model.analyses_and_results.load_case_groups._5949": [
            "AbstractLoadCaseGroup"
        ],
        "_private.system_model.analyses_and_results.load_case_groups._5950": [
            "AbstractStaticLoadCaseGroup"
        ],
        "_private.system_model.analyses_and_results.load_case_groups._5951": [
            "ClutchEngagementStatus"
        ],
        "_private.system_model.analyses_and_results.load_case_groups._5952": [
            "ConceptSynchroGearEngagementStatus"
        ],
        "_private.system_model.analyses_and_results.load_case_groups._5953": [
            "DesignState"
        ],
        "_private.system_model.analyses_and_results.load_case_groups._5954": [
            "DutyCycle"
        ],
        "_private.system_model.analyses_and_results.load_case_groups._5955": [
            "GenericClutchEngagementStatus"
        ],
        "_private.system_model.analyses_and_results.load_case_groups._5956": [
            "LoadCaseGroupHistograms"
        ],
        "_private.system_model.analyses_and_results.load_case_groups._5957": [
            "SubGroupInSingleDesignState"
        ],
        "_private.system_model.analyses_and_results.load_case_groups._5958": [
            "SystemOptimisationGearSet"
        ],
        "_private.system_model.analyses_and_results.load_case_groups._5959": [
            "SystemOptimiserGearSetOptimisation"
        ],
        "_private.system_model.analyses_and_results.load_case_groups._5960": [
            "SystemOptimiserTargets"
        ],
        "_private.system_model.analyses_and_results.load_case_groups._5961": [
            "TimeSeriesLoadCaseGroup"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractDesignStateLoadCaseGroup",
    "AbstractLoadCaseGroup",
    "AbstractStaticLoadCaseGroup",
    "ClutchEngagementStatus",
    "ConceptSynchroGearEngagementStatus",
    "DesignState",
    "DutyCycle",
    "GenericClutchEngagementStatus",
    "LoadCaseGroupHistograms",
    "SubGroupInSingleDesignState",
    "SystemOptimisationGearSet",
    "SystemOptimiserGearSetOptimisation",
    "SystemOptimiserTargets",
    "TimeSeriesLoadCaseGroup",
)
