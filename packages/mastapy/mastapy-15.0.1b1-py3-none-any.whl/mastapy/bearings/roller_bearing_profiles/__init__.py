"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.bearings.roller_bearing_profiles._2130 import ProfileDataToUse
    from mastapy._private.bearings.roller_bearing_profiles._2131 import ProfileSet
    from mastapy._private.bearings.roller_bearing_profiles._2132 import ProfileToFit
    from mastapy._private.bearings.roller_bearing_profiles._2133 import (
        RollerBearingConicalProfile,
    )
    from mastapy._private.bearings.roller_bearing_profiles._2134 import (
        RollerBearingCrownedProfile,
    )
    from mastapy._private.bearings.roller_bearing_profiles._2135 import (
        RollerBearingDinLundbergProfile,
    )
    from mastapy._private.bearings.roller_bearing_profiles._2136 import (
        RollerBearingFlatProfile,
    )
    from mastapy._private.bearings.roller_bearing_profiles._2137 import (
        RollerBearingFujiwaraKawaseProfile,
    )
    from mastapy._private.bearings.roller_bearing_profiles._2138 import (
        RollerBearingJohnsGoharProfile,
    )
    from mastapy._private.bearings.roller_bearing_profiles._2139 import (
        RollerBearingLoadDependentProfile,
    )
    from mastapy._private.bearings.roller_bearing_profiles._2140 import (
        RollerBearingLundbergProfile,
    )
    from mastapy._private.bearings.roller_bearing_profiles._2141 import (
        RollerBearingProfile,
    )
    from mastapy._private.bearings.roller_bearing_profiles._2142 import (
        RollerBearingTangentialCrownedProfile,
    )
    from mastapy._private.bearings.roller_bearing_profiles._2143 import (
        RollerBearingUserSpecifiedProfile,
    )
    from mastapy._private.bearings.roller_bearing_profiles._2144 import (
        RollerRaceProfilePoint,
    )
    from mastapy._private.bearings.roller_bearing_profiles._2145 import (
        UserSpecifiedProfilePoint,
    )
    from mastapy._private.bearings.roller_bearing_profiles._2146 import (
        UserSpecifiedRollerRaceProfilePoint,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.bearings.roller_bearing_profiles._2130": ["ProfileDataToUse"],
        "_private.bearings.roller_bearing_profiles._2131": ["ProfileSet"],
        "_private.bearings.roller_bearing_profiles._2132": ["ProfileToFit"],
        "_private.bearings.roller_bearing_profiles._2133": [
            "RollerBearingConicalProfile"
        ],
        "_private.bearings.roller_bearing_profiles._2134": [
            "RollerBearingCrownedProfile"
        ],
        "_private.bearings.roller_bearing_profiles._2135": [
            "RollerBearingDinLundbergProfile"
        ],
        "_private.bearings.roller_bearing_profiles._2136": ["RollerBearingFlatProfile"],
        "_private.bearings.roller_bearing_profiles._2137": [
            "RollerBearingFujiwaraKawaseProfile"
        ],
        "_private.bearings.roller_bearing_profiles._2138": [
            "RollerBearingJohnsGoharProfile"
        ],
        "_private.bearings.roller_bearing_profiles._2139": [
            "RollerBearingLoadDependentProfile"
        ],
        "_private.bearings.roller_bearing_profiles._2140": [
            "RollerBearingLundbergProfile"
        ],
        "_private.bearings.roller_bearing_profiles._2141": ["RollerBearingProfile"],
        "_private.bearings.roller_bearing_profiles._2142": [
            "RollerBearingTangentialCrownedProfile"
        ],
        "_private.bearings.roller_bearing_profiles._2143": [
            "RollerBearingUserSpecifiedProfile"
        ],
        "_private.bearings.roller_bearing_profiles._2144": ["RollerRaceProfilePoint"],
        "_private.bearings.roller_bearing_profiles._2145": [
            "UserSpecifiedProfilePoint"
        ],
        "_private.bearings.roller_bearing_profiles._2146": [
            "UserSpecifiedRollerRaceProfilePoint"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ProfileDataToUse",
    "ProfileSet",
    "ProfileToFit",
    "RollerBearingConicalProfile",
    "RollerBearingCrownedProfile",
    "RollerBearingDinLundbergProfile",
    "RollerBearingFlatProfile",
    "RollerBearingFujiwaraKawaseProfile",
    "RollerBearingJohnsGoharProfile",
    "RollerBearingLoadDependentProfile",
    "RollerBearingLundbergProfile",
    "RollerBearingProfile",
    "RollerBearingTangentialCrownedProfile",
    "RollerBearingUserSpecifiedProfile",
    "RollerRaceProfilePoint",
    "UserSpecifiedProfilePoint",
    "UserSpecifiedRollerRaceProfilePoint",
)
