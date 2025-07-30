"""Module to simplify loading example files."""

from __future__ import annotations

from abc import ABC, ABCMeta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, TypeVar

    from mastapy.system_model import Design

    Self_ExamplesMeta = TypeVar("Self_ExamplesMeta", "ExamplesMeta")
    Self_ExampleName = TypeVar("Self_ExampleName", "ExampleName")

from mastapy._private._internal.utility import StrEnum


class ExamplesMeta(ABCMeta):
    """Meta class that disables attribute modification."""

    def __setattr__(self: "Self_ExamplesMeta", name: str, value: "Any") -> None:
        """Override of the setattr magic method."""
        if name.startswith("_"):
            super(ExamplesMeta, self).__setattr__(name, value)
        else:
            raise Exception("You cannot modify any of the example paths.") from None


class ExampleName(StrEnum):
    """Enum to simplify loading examples.

    >>> Design.load_example(ExampleName.SIMPLE_HOUSING)
    """

    SIMPLE_PULL_BELT_CVT_MODEL = "Automotive: CVT: Simple Pull-Belt CVT model"
    """Automotive: CVT: Simple Pull-Belt CVT model"""

    IMPROVED_PULL_BELT_CVT_MODEL = "Automotive: CVT: Improved Pull-Belt CVT model"
    """Automotive: CVT: Improved Pull-Belt CVT model"""

    SIMPLE_PUSH_BELT_CVT_MODEL = "Automotive: CVT: Simple Push-Belt CVT model"
    """Automotive: CVT: Simple Push-Belt CVT model"""

    IMPROVED_PUSH_BELT_CVT_MODEL = "Automotive: CVT: Improved Push-Belt CVT model"
    """Automotive: CVT: Improved Push-Belt CVT model"""

    CAR_TWO_LAYSHAFT_TRANSAXLE_GEARBOX_GEAR_MODEL = (
        "Automotive: Car Two Layshaft Transaxle Gearbox: Gear Model"
    )
    """Automotive: Car Two Layshaft Transaxle Gearbox: Gear Model"""

    CAR_TRANSAXLE_GEARBOX_GEAR_MODEL = "Automotive: Car Transaxle Gearbox: Gear Model"
    """Automotive: Car Transaxle Gearbox: Gear Model"""

    CONCEPT_MAIN_BEARINGS = (
        "Automotive: Car Two Layshaft Transaxle Gearbox: Concept Main Bearings"
    )
    """Automotive: Car Two Layshaft Transaxle Gearbox: Concept Main Bearings"""

    CAR_TWO_LAYSHAFT_TRANSAXLE_GEARBOX_CONCEPT_SYNCHRONISERS = (
        "Automotive: Car Two Layshaft Transaxle Gearbox: Concept Synchronisers"
    )
    """Automotive: Car Two Layshaft Transaxle Gearbox: Concept Synchronisers"""

    CAR_TRANSAXLE_GEARBOX_CONCEPT_SYNCHRONISERS = (
        "Automotive: Car Transaxle Gearbox: Concept Synchronisers"
    )
    """Automotive: Car Transaxle Gearbox: Concept Synchronisers"""

    CAR_TWO_LAYSHAFT_TRANSAXLE_GEARBOX_ROLLING_BEARINGS = (
        "Automotive: Car Two Layshaft Transaxle Gearbox: Rolling Bearings"
    )
    """Automotive: Car Two Layshaft Transaxle Gearbox: Rolling Bearings"""

    CAR_TRANSAXLE_GEARBOX_ROLLING_BEARINGS = (
        "Automotive: Car Transaxle Gearbox: Rolling Bearings"
    )
    """Automotive: Car Transaxle Gearbox: Rolling Bearings"""

    CAR_TWO_LAYSHAFT_TRANSAXLE_GEARBOX_SHAFT_DETAILS = (
        "Automotive: Car Two Layshaft Transaxle Gearbox: Shaft Details"
    )
    """Automotive: Car Two Layshaft Transaxle Gearbox: Shaft Details"""

    CAR_TRANSAXLE_GEARBOX_SHAFT_DETAILS = (
        "Automotive: Car Transaxle Gearbox: Shaft Details"
    )
    """Automotive: Car Transaxle Gearbox: Shaft Details"""

    CAR_AXLE_DRIVELINE = "Automotive: Car Axle & Driveline"
    """Automotive: Car Axle & Driveline"""

    CAR_AXLE = "Automotive: Car Axle"
    """Automotive: Car Axle"""

    GEAR_MODEL_CONCEPT_BEARINGS = (
        "Automotive: Car Transaxle Gearbox: Gear Model + Concept Bearings"
    )
    """Automotive: Car Transaxle Gearbox: Gear Model + Concept Bearings"""

    FULL_MODEL = "Automotive: Car Transaxle Gearbox: Full Model"
    """Automotive: Car Transaxle Gearbox: Full Model"""

    HELICAL_GEAR_SET = "Components: Gear Sets: Helical Gear Set"
    """Components: Gear Sets: Helical Gear Set"""

    TRUCK_AXLE = "Automotive: Truck Axle"
    """Automotive: Truck Axle"""

    AEROSPACE_ACCESSORY_GEARBOX_WITHOUT_FE_PARTS = (
        "Aerospace: Aerospace Accessory Gearbox without FE Parts"
    )
    """Aerospace: Aerospace Accessory Gearbox without FE Parts"""

    AEROSPACE_ACCESSORY_GEARBOX_WITH_FE_PARTS = (
        "Aerospace: Aerospace Accessory Gearbox with FE Parts"
    )
    """Aerospace: Aerospace Accessory Gearbox with FE Parts"""

    AIRCRAFT_NOSE_WHEEL = "Aerospace: Aircraft Nose Wheel"
    """Aerospace: Aircraft Nose Wheel"""

    HELICOPTER_TRANSMISSION = "Aerospace: Helicopter Transmission"
    """Aerospace: Helicopter Transmission"""

    AIRCRAFT_ENGINE = "Aerospace: Aircraft Engine"
    """Aerospace: Aircraft Engine"""

    WORM_GEAR_SET = "Components: Gear Sets: Worm Gear Set"
    """Components: Gear Sets: Worm Gear Set"""

    GEAR_SETS_SPIRAL_BEVEL_GEAR_SET = "Components: Gear Sets: Spiral Bevel Gear Set"
    """Components: Gear Sets: Spiral Bevel Gear Set"""

    BEVEL_LTCA_SPIRAL_BEVEL_GEAR_SET = "Analyses: Bevel LTCA: Spiral Bevel Gear Set"
    """Analyses: Bevel LTCA: Spiral Bevel Gear Set"""

    STRAIGHT_BEVEL_GEAR_SET = "Components: Gear Sets: Straight Bevel Gear Set"
    """Components: Gear Sets: Straight Bevel Gear Set"""

    KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET = (
        "Components: Gear Sets: Klingelnberg Cyclo-Palloid Spiral Bevel Gear Set"
    )
    """Components: Gear Sets: Klingelnberg Cyclo-Palloid Spiral Bevel Gear Set"""

    FACE_GEAR_SET = "Components: Gear Sets: Face Gear Set"
    """Components: Gear Sets: Face Gear Set"""

    KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET = (
        "Components: Gear Sets: Klingelnberg Cyclo-Palloid Hypoid Gear Set"
    )
    """Components: Gear Sets: Klingelnberg Cyclo-Palloid Hypoid Gear Set"""

    SIMPLE_DYNAMIC_ANGULAR_CONTACT_BALL_BEARING = (
        "Analyses: Rolling Bearings: Simple Dynamic Angular Contact Ball Bearing"
    )
    """Analyses: Rolling Bearings: Simple Dynamic Angular Contact Ball Bearing"""

    PLAIN_JOURNAL_BEARING = "Components: Fluid Film Bearings: Plain Journal Bearing"
    """Components: Fluid Film Bearings: Plain Journal Bearing"""

    TILTING_THRUST_PAD_BEARING = (
        "Components: Fluid Film Bearings: Tilting Thrust Pad Bearing"
    )
    """Components: Fluid Film Bearings: Tilting Thrust Pad Bearing"""

    TILTING_PAD_JOURNAL_BEARING = (
        "Components: Fluid Film Bearings: Tilting Pad Journal Bearing"
    )
    """Components: Fluid Film Bearings: Tilting Pad Journal Bearing"""

    TWO_Z_X_WW = "Components: Planetaries: 2Z-X WW"
    """Components: Planetaries: 2Z-X WW"""

    TWO_Z_X_NN_ONE_PLANET = "Components: Planetaries: 2Z-X NN 1 Planet"
    """Components: Planetaries: 2Z-X NN 1 Planet"""

    TWO_Z_X_NN = "Components: Planetaries: 2Z-X NN"
    """Components: Planetaries: 2Z-X NN"""

    TWO_Z_X_NW = "Components: Planetaries: 2Z-X NW"
    """Components: Planetaries: 2Z-X NW"""

    UNEQUAL_SPACING_IDLER = "Components: Planetaries: Unequal Spacing Idler"
    """Components: Planetaries: Unequal Spacing Idler"""

    CVT = "Components: CVTs: CVT"
    """Components: CVTs: CVT"""

    CVT_WITH_SIMPLE_FE_ANNULUS = "Components: CVTs: CVT - With Simple FE Annulus"
    """Components: CVTs: CVT - With Simple FE Annulus"""

    RANGE_CHANGER = "Components: Planetaries: Range Changer"
    """Components: Planetaries: Range Changer"""

    SIMPLE_PLANETARY_WITH_FE_CARRIER = (
        "Components: Planetaries: Simple Planetary with FE Carrier"
    )
    """Components: Planetaries: Simple Planetary with FE Carrier"""

    SIMPLE_CYCLOIDAL_DRIVE = "Components: Cycloidal Drives: Simple Cycloidal Drive"
    """Components: Cycloidal Drives: Simple Cycloidal Drive"""

    SIMPLE_HOUSING = "Components: Simple Housing"
    """Components: Simple Housing"""

    SIMPLE_HOUSING_FULL_MESH = "Components: Simple Housing Full Mesh"
    """Components: Simple Housing Full Mesh"""

    PARKING_LOCK_TRAINING_MODEL = "Components: Parking Lock Training Model"
    """Components: Parking Lock Training Model"""

    SIMPLE_HOUSING_FULL_MESH_FOR_ACOUSTICS = (
        "Analyses: Acoustics: Simple Housing Full Mesh for Acoustics"
    )
    """Analyses: Acoustics: Simple Housing Full Mesh for Acoustics"""

    HIGH_ASYMMETRY_RATIO_GEAR_EXAMPLE = (
        "Analyses: LTCA: High Asymmetry Ratio Gear Example"
    )
    """Analyses: LTCA: High Asymmetry Ratio Gear Example"""

    TRUCK_GEAR_PAIR_FE_MODEL_ZERO_ADJ_TEETH = (
        "Analyses: LTCA: Truck Gear Pair, FE Model, 0 Adj. Teeth"
    )
    """Analyses: LTCA: Truck Gear Pair, FE Model, 0 Adj. Teeth"""

    MARINE_GEAR_PAIR_FE_MODEL_ZERO_ADJ_TEETH = (
        "Analyses: LTCA: Marine Gear Pair, FE Model, 0 Adj. Teeth"
    )
    """Analyses: LTCA: Marine Gear Pair, FE Model, 0 Adj. Teeth"""

    ROTOR_DYNAMICS_TWO_SHAFTS = "Analyses: Rotor Dynamics: Rotor Dynamics Two Shafts"
    """Analyses: Rotor Dynamics: Rotor Dynamics Two Shafts"""

    ROTOR_DYNAMICS_TWO_SHAFTS_FULL_MODEL = (
        "Analyses: Rotor Dynamics: Rotor Dynamics Two Shafts - Full Model"
    )
    """Analyses: Rotor Dynamics: Rotor Dynamics Two Shafts - Full Model"""

    LAVEL_JEFFCOTT_ROTOR = "Analyses: Rotor Dynamics: Lavel Jeffcott Rotor"
    """Analyses: Rotor Dynamics: Lavel Jeffcott Rotor"""

    COMPLETE_CYLINDRICAL_GEAR_PAIR = (
        "Analyses: Cylindrical Gear Manufacturing: Complete Cylindrical Gear Pair"
    )
    """Analyses: Cylindrical Gear Manufacturing: Complete Cylindrical Gear Pair"""

    CYLINDRICAL_PLANETARY = (
        "Analyses: Cylindrical Gear Manufacturing: Cylindrical Planetary"
    )
    """Analyses: Cylindrical Gear Manufacturing: Cylindrical Planetary"""

    INTERNAL_GEAR_PAIR_FE_MODEL_ZERO_ADJ_TEETH = (
        "Analyses: LTCA: Internal Gear Pair, FE Model, 0 Adj. Teeth"
    )
    """Analyses: LTCA: Internal Gear Pair, FE Model, 0 Adj. Teeth"""

    MACK_ALDENER_SINGLE_STAGE = "Analyses: TIFF: MackAldener Single Stage"
    """Analyses: TIFF: MackAldener Single Stage"""

    MACK_ALDENER_IDLER = "Analyses: TIFF: MackAldener Idler"
    """Analyses: TIFF: MackAldener Idler"""

    FZG_TYPE_C_OPTIMISATION_EXAMPLE = (
        "Analyses: Macro Geometry Optimisation: FZG Type C - Optimisation Example"
    )
    """Analyses: Macro Geometry Optimisation: FZG Type C - Optimisation Example"""

    MULTI_MODE_HYBRID_TRANSMISSION = (
        "Automotive: Hybrid Transmission Examples: Multi Mode Hybrid Transmission"
    )
    """Automotive: Hybrid Transmission Examples: Multi Mode Hybrid Transmission"""

    MINIVAN_AXLE_NO_FE = "Automotive: Minivan Axle and Driveline: Minivan Axle no FE"
    """Automotive: Minivan Axle and Driveline: Minivan Axle no FE"""

    MINIVAN_AXLE_CASING_FE = (
        "Automotive: Minivan Axle and Driveline: Minivan Axle + Casing FE"
    )
    """Automotive: Minivan Axle and Driveline: Minivan Axle + Casing FE"""

    MINIVAN_AXLE_CASING_AND_DIFF_SHAFT_FE = "Automotive: Minivan Axle and Driveline: Minivan Axle + Casing and Diff Shaft FE"
    """Automotive: Minivan Axle and Driveline: Minivan Axle + Casing and Diff Shaft FE"""

    FULL_MODEL_DIFF_FE = "Automotive: Car Transaxle Gearbox: Full Model + Diff FE"
    """Automotive: Car Transaxle Gearbox: Full Model + Diff FE"""

    FULL_MODEL_DIFF_INTERNALS = (
        "Automotive: Car Transaxle Gearbox: Full Model + Diff Internals"
    )
    """Automotive: Car Transaxle Gearbox: Full Model + Diff Internals"""

    FULL_MODEL_DIFF_SHAFT_FE_DIFF_INTERNALS = (
        "Automotive: Car Transaxle Gearbox: Full Model + Diff Shaft FE + Diff Internals"
    )
    """Automotive: Car Transaxle Gearbox: Full Model + Diff Shaft FE + Diff Internals"""

    FULL_MODEL_DIFF_SHAFT_FE_DIFF_INTERNALS_PIN_FE = "Automotive: Car Transaxle Gearbox: Full Model + Diff Shaft FE + Diff Internals + Pin FE"
    """Automotive: Car Transaxle Gearbox: Full Model + Diff Shaft FE + Diff Internals + Pin FE"""

    AUTOMATIC_WITH_RAVIGNEAUX = (
        "Automotive: Automatic with Ravigneaux: Automatic with Ravigneaux"
    )
    """Automotive: Automatic with Ravigneaux: Automatic with Ravigneaux"""

    TRANSFER_CASE_BELT = "Automotive: Transfer Case - Belt"
    """Automotive: Transfer Case - Belt"""

    ELECTRIC_DRIVE_TRANSMISSION = (
        "Automotive: Electric Drive Transmission: Electric Drive Transmission"
    )
    """Automotive: Electric Drive Transmission: Electric Drive Transmission"""

    ELECTRIC_DRIVE_TRANSMISSION_WITH_ELECTRIC_MOTOR = "Automotive: Electric Drive Transmission: Electric Drive Transmission - With Electric Motor"
    """Automotive: Electric Drive Transmission: Electric Drive Transmission - With Electric Motor"""

    ELECTRIC_DRIVE_TRANSMISSION_DETAILED_MODEL = "Automotive: Electric Drive Transmission: Electric Drive Transmission - Detailed Model"
    """Automotive: Electric Drive Transmission: Electric Drive Transmission - Detailed Model"""

    ELECTRIC_DRIVE_TRANSMISSION_DETAILED_MODEL_NO_HOUSING_NO_DIFF_INTERNALS = "Automotive: Electric Drive Transmission: Electric Drive Transmission - Detailed Model - No Housing, No Diff Internals"
    """Automotive: Electric Drive Transmission: Electric Drive Transmission - Detailed Model - No Housing, No Diff Internals"""

    ELECTRIC_DRIVE_TRANSMISSION_SKEWED_ROTOR = "Automotive: Electric Drive Transmission: Electric Drive Transmission - Skewed Rotor"
    """Automotive: Electric Drive Transmission: Electric Drive Transmission - Skewed Rotor"""

    ELECTRIC_DRIVE_TRANSMISSION_AXIAL_FLUX_MOTOR = "Automotive: Electric Drive Transmission: Electric Drive Transmission - Axial Flux Motor"
    """Automotive: Electric Drive Transmission: Electric Drive Transmission - Axial Flux Motor"""

    TRANSFER_CASE_GEAR = "Automotive: Transfer Case - Gear"
    """Automotive: Transfer Case - Gear"""

    AUTOMATIC_WITH_RAVIGNEAUX_WITH_CARRIER_FE = "Automotive: Automatic with Ravigneaux: Automatic with Ravigneaux, with Carrier FE"
    """Automotive: Automatic with Ravigneaux: Automatic with Ravigneaux, with Carrier FE"""

    PLANETARY_RANGE_CHANGER = (
        "Automotive: Drive Train Simulation: Planetary Range Changer"
    )
    """Automotive: Drive Train Simulation: Planetary Range Changer"""

    TWO_SHAFTS_ONE_CLUTCH = "Automotive: Drive Train Simulation: Two Shafts One Clutch"
    """Automotive: Drive Train Simulation: Two Shafts One Clutch"""

    TORQUE_CONVERTER = "Automotive: Drive Train Simulation: Torque Converter"
    """Automotive: Drive Train Simulation: Torque Converter"""

    ENGINE_INERTIA_ADJUSTED_LOADS = (
        "Automotive: Drive Train Simulation: Engine - Inertia Adjusted Loads"
    )
    """Automotive: Drive Train Simulation: Engine - Inertia Adjusted Loads"""

    TWO_SPEED_DEMO = "Automotive: Drive Train Simulation: Two Speed Demo"
    """Automotive: Drive Train Simulation: Two Speed Demo"""

    FIVE_DOF_TORSIONAL_MODEL_NO_INPUTS = (
        "Automotive: Gear Rattle Training Manual: 5DOF Torsional Model (No Inputs)"
    )
    """Automotive: Gear Rattle Training Manual: 5DOF Torsional Model (No Inputs)"""

    FIVE_DOF_TORSIONAL_MODEL_COMPLETED_ONE_LASH = "Automotive: Gear Rattle Training Manual: 5DOF Torsional Model (Completed, 1 Lash)"
    """Automotive: Gear Rattle Training Manual: 5DOF Torsional Model (Completed, 1 Lash)"""

    FIVE_DOF_TORSIONAL_MODEL_COMPLETED_TWO_LASH = "Automotive: Gear Rattle Training Manual: 5DOF Torsional Model (Completed, 2 Lash)"
    """Automotive: Gear Rattle Training Manual: 5DOF Torsional Model (Completed, 2 Lash)"""

    SIMPLE_HOUSING_NO_INPUTS = (
        "Automotive: Gear Rattle Training Manual: Simple Housing (No Inputs)"
    )
    """Automotive: Gear Rattle Training Manual: Simple Housing (No Inputs)"""

    SIMPLE_HOUSING_COMPLETED = (
        "Automotive: Gear Rattle Training Manual: Simple Housing (Completed)"
    )
    """Automotive: Gear Rattle Training Manual: Simple Housing (Completed)"""

    SPLINE_RUMBLE = "Automotive: Spline Rumble Training Manual: Spline Rumble"
    """Automotive: Spline Rumble Training Manual: Spline Rumble"""

    WIND_TURBINE_FLEXIBLE_ANNULUS = "Wind Turbine: Wind Turbine - Flexible Annulus"
    """Wind Turbine: Wind Turbine - Flexible Annulus"""

    WIND_TURBINE = "Wind Turbine: Wind Turbine"
    """Wind Turbine: Wind Turbine"""

    WIND_TURBINE_FLEXIBLE_BEARING_OUTER_RACE = (
        "Wind Turbine: Wind Turbine - Flexible Bearing Outer Race"
    )
    """Wind Turbine: Wind Turbine - Flexible Bearing Outer Race"""

    WIND_TURBINE_GEARBOX = "Wind Turbine: Drive Train Simulation: Wind Turbine Gearbox"
    """Wind Turbine: Drive Train Simulation: Wind Turbine Gearbox"""

    WIND_TURBINE_FULL_DRIVETRAIN = (
        "Wind Turbine: Drive Train Simulation: Wind Turbine Full Drivetrain"
    )
    """Wind Turbine: Drive Train Simulation: Wind Turbine Full Drivetrain"""

    ONE_PLANETARY_TWO_PARALLEL_STAGES = (
        "Wind Turbine: Concept Designs: 1 Planetary, 2 Parallel Stages"
    )
    """Wind Turbine: Concept Designs: 1 Planetary, 2 Parallel Stages"""

    ONE_PLANETARY_TWO_PARALLEL_STAGES_WITH_TORQUE_LIMIT_STAGE = "Wind Turbine: Concept Designs: 1 Planetary, 2 Parallel Stages With Torque Limit Stage"
    """Wind Turbine: Concept Designs: 1 Planetary, 2 Parallel Stages With Torque Limit Stage"""

    ONE_PLANETARY_ONE_INTERNAL_STAGE = (
        "Wind Turbine: Concept Designs: 1 Planetary, 1 Internal Stage"
    )
    """Wind Turbine: Concept Designs: 1 Planetary, 1 Internal Stage"""

    TWO_PLANETARY_ONE_PARALLEL_STAGE = (
        "Wind Turbine: Concept Designs: 2 Planetary, 1 Parallel Stage"
    )
    """Wind Turbine: Concept Designs: 2 Planetary, 1 Parallel Stage"""

    THREE_PARALLEL_STAGES = "Wind Turbine: Concept Designs: Three Parallel Stages"
    """Wind Turbine: Concept Designs: Three Parallel Stages"""

    PRIMARY_STEP_UP_BEVEL_PLANETARY_WITH_MOTOR = (
        "Wind Turbine: Concept Designs: Primary Step-up, Bevel, Planetary With Motor"
    )
    """Wind Turbine: Concept Designs: Primary Step-up, Bevel, Planetary With Motor"""

    PLANETARY_DIFF_PLANETARY_STAR_PARALLEL_STAGES = (
        "Wind Turbine: Concept Designs: Planetary Diff, Planetary Star, Parallel Stages"
    )
    """Wind Turbine: Concept Designs: Planetary Diff, Planetary Star, Parallel Stages"""

    PLANETARY_PLANETARY_STAR_PLANETARY_DIFF_PARALLEL_STAGES = "Wind Turbine: Concept Designs: Planetary, Planetary Star, Planetary Diff, Parallel Stages"
    """Wind Turbine: Concept Designs: Planetary, Planetary Star, Planetary Diff, Parallel Stages"""

    ONE_PLANETARY_STAR_TWO_PLANETARY_DIFF_STAGES = (
        "Wind Turbine: Concept Designs: 1 Planetary Star, 2 Planetary Diff Stages"
    )
    """Wind Turbine: Concept Designs: 1 Planetary Star, 2 Planetary Diff Stages"""

    ONE_PLANETARY_TWO_PARALLEL_PLANETARY_DIFF_PLANETARY_STAR_TORQUE_CONVERTER_STAGES = "Wind Turbine: Concept Designs: 1 Planetary, 2 Parallel, Planetary Diff, Planetary Star, Torque Converter Stages"
    """Wind Turbine: Concept Designs: 1 Planetary, 2 Parallel, Planetary Diff, Planetary Star, Torque Converter Stages"""

    TWO_PLANETARY_PLANETARY_HYDROSTATIC_CVT = (
        "Wind Turbine: Concept Designs: 2 Planetary, Planetary Hydrostatic CVT"
    )
    """Wind Turbine: Concept Designs: 2 Planetary, Planetary Hydrostatic CVT"""

    PLANETARY_NO_SUN_PLANETARY_NO_ANNULUS_PARALLEL_STAGE = "Wind Turbine: Concept Designs: Planetary No Sun, Planetary No Annulus, Parallel Stage"
    """Wind Turbine: Concept Designs: Planetary No Sun, Planetary No Annulus, Parallel Stage"""

    TWO_STAGE_COMPOUND_PLANETARY_PARALLEL_STAGE = (
        "Wind Turbine: Concept Designs: 2 Stage Compound Planetary, Parallel Stage"
    )
    """Wind Turbine: Concept Designs: 2 Stage Compound Planetary, Parallel Stage"""

    STARTER_MODEL_CLUTCHED_SYSTEM = "Tutorials: Starter Model - Clutched System"
    """Tutorials: Starter Model - Clutched System"""

    OUTBOARD = "Marine: Outboard"
    """Marine: Outboard"""

    TIDAL_STREAM_GEARBOX = "Marine: Tidal Stream Gearbox"
    """Marine: Tidal Stream Gearbox"""

    RAIL_BOGIE = "Rail: Rail Bogie"
    """Rail: Rail Bogie"""

    WINCH_EXAMPLE = "Industrial: Winch Example"
    """Industrial: Winch Example"""

    RV_CYCLOIDAL_DRIVE_SIMPLE = "Robotics: RV Cycloidal Drive - Simple"
    """Robotics: RV Cycloidal Drive - Simple"""

    RV_CYCLOIDAL_DRIVE_DETAILED = "Robotics: RV Cycloidal Drive - Detailed"
    """Robotics: RV Cycloidal Drive - Detailed"""

    BELT_DRIVE = "Components: Belt Drive"
    """Components: Belt Drive"""

    AGMA_GEAR_SET_FOR_SCUFFING = "Components: Gear Sets: AGMA Gear Set For Scuffing"
    """Components: Gear Sets: AGMA Gear Set For Scuffing"""

    HYPOID_GEAR_SET = "Components: Gear Sets: Hypoid Gear Set"
    """Components: Gear Sets: Hypoid Gear Set"""

    ZEROL_BEVEL_GEAR_SET = "Components: Gear Sets: Zerol Bevel Gear Set"
    """Components: Gear Sets: Zerol Bevel Gear Set"""

    SIMPLE_PLANETARY = "Components: Planetaries: Simple Planetary"
    """Components: Planetaries: Simple Planetary"""

    HIGH_RATIO_COMPOUND = "Components: Planetaries: High Ratio Compound"
    """Components: Planetaries: High Ratio Compound"""

    BEVEL_DIFFERENTIAL_WITH_TWO_CARRIERS = (
        "Components: Planetaries: Bevel Differential with Two Carriers"
    )
    """Components: Planetaries: Bevel Differential with Two Carriers"""

    SCOOTER_GEARBOX = "Automotive: Scooter Gearbox"
    """Automotive: Scooter Gearbox"""

    def load(self: "Self_ExampleName") -> "Design":
        """Load the design."""
        from mastapy.system_model import Design

        return Design.load_example(self)


class Examples(ABC, metaclass=ExamplesMeta):
    """Root of the Examples hierarchy.

    This is designed to simplify loading examples. The easiest way to
    use this class is by calling the load method on the enum itself.

    Alternatively, you can pass the enum directly into Design.load_example().

    Loading design examples with a string is still supported.

    Examples:
        >>> design = Examples.Automotive.SCOOTER_GEARBOX.load()
        >>> design = Design.load_example(Examples.Automotive.SCOOTER_GEARBOX)
    """

    class Automotive(ABC, metaclass=ExamplesMeta):
        """Automotive examples."""

        class CVT(ABC, metaclass=ExamplesMeta):
            """CVT examples."""

            SIMPLE_PULL_BELT_CVT_MODEL = ExampleName.SIMPLE_PULL_BELT_CVT_MODEL
            """Automotive: CVT: Simple Pull-Belt CVT model"""

            IMPROVED_PULL_BELT_CVT_MODEL = ExampleName.IMPROVED_PULL_BELT_CVT_MODEL
            """Automotive: CVT: Improved Pull-Belt CVT model"""

            SIMPLE_PUSH_BELT_CVT_MODEL = ExampleName.SIMPLE_PUSH_BELT_CVT_MODEL
            """Automotive: CVT: Simple Push-Belt CVT model"""

            IMPROVED_PUSH_BELT_CVT_MODEL = ExampleName.IMPROVED_PUSH_BELT_CVT_MODEL
            """Automotive: CVT: Improved Push-Belt CVT model"""

        class CarTwoLayshaftTransaxleGearbox(ABC, metaclass=ExamplesMeta):
            """Car Two Layshaft Transaxle Gearbox examples."""

            GEAR_MODEL = ExampleName.CAR_TWO_LAYSHAFT_TRANSAXLE_GEARBOX_GEAR_MODEL
            """Automotive: Car Two Layshaft Transaxle Gearbox: Gear Model"""

            CONCEPT_MAIN_BEARINGS = ExampleName.CONCEPT_MAIN_BEARINGS
            """Automotive: Car Two Layshaft Transaxle Gearbox: Concept Main Bearings"""

            CONCEPT_SYNCHRONISERS = (
                ExampleName.CAR_TWO_LAYSHAFT_TRANSAXLE_GEARBOX_CONCEPT_SYNCHRONISERS
            )
            """Automotive: Car Two Layshaft Transaxle Gearbox: Concept Synchronisers"""

            ROLLING_BEARINGS = (
                ExampleName.CAR_TWO_LAYSHAFT_TRANSAXLE_GEARBOX_ROLLING_BEARINGS
            )
            """Automotive: Car Two Layshaft Transaxle Gearbox: Rolling Bearings"""

            SHAFT_DETAILS = ExampleName.CAR_TWO_LAYSHAFT_TRANSAXLE_GEARBOX_SHAFT_DETAILS
            """Automotive: Car Two Layshaft Transaxle Gearbox: Shaft Details"""

        class CarTransaxleGearbox(ABC, metaclass=ExamplesMeta):
            """Car Transaxle Gearbox examples."""

            GEAR_MODEL = ExampleName.CAR_TRANSAXLE_GEARBOX_GEAR_MODEL
            """Automotive: Car Transaxle Gearbox: Gear Model"""

            CONCEPT_SYNCHRONISERS = (
                ExampleName.CAR_TRANSAXLE_GEARBOX_CONCEPT_SYNCHRONISERS
            )
            """Automotive: Car Transaxle Gearbox: Concept Synchronisers"""

            ROLLING_BEARINGS = ExampleName.CAR_TRANSAXLE_GEARBOX_ROLLING_BEARINGS
            """Automotive: Car Transaxle Gearbox: Rolling Bearings"""

            SHAFT_DETAILS = ExampleName.CAR_TRANSAXLE_GEARBOX_SHAFT_DETAILS
            """Automotive: Car Transaxle Gearbox: Shaft Details"""

            GEAR_MODEL_CONCEPT_BEARINGS = ExampleName.GEAR_MODEL_CONCEPT_BEARINGS
            """Automotive: Car Transaxle Gearbox: Gear Model + Concept Bearings"""

            FULL_MODEL = ExampleName.FULL_MODEL
            """Automotive: Car Transaxle Gearbox: Full Model"""

            FULL_MODEL_DIFF_FE = ExampleName.FULL_MODEL_DIFF_FE
            """Automotive: Car Transaxle Gearbox: Full Model + Diff FE"""

            FULL_MODEL_DIFF_INTERNALS = ExampleName.FULL_MODEL_DIFF_INTERNALS
            """Automotive: Car Transaxle Gearbox: Full Model + Diff Internals"""

            FULL_MODEL_DIFF_SHAFT_FE_DIFF_INTERNALS = (
                ExampleName.FULL_MODEL_DIFF_SHAFT_FE_DIFF_INTERNALS
            )
            """Automotive: Car Transaxle Gearbox: Full Model + Diff Shaft FE + Diff Internals"""

            FULL_MODEL_DIFF_SHAFT_FE_DIFF_INTERNALS_PIN_FE = (
                ExampleName.FULL_MODEL_DIFF_SHAFT_FE_DIFF_INTERNALS_PIN_FE
            )
            """Automotive: Car Transaxle Gearbox: Full Model + Diff Shaft FE + Diff Internals + Pin FE"""

        CAR_AXLE_DRIVELINE = ExampleName.CAR_AXLE_DRIVELINE
        """Automotive: Car Axle & Driveline"""

        CAR_AXLE = ExampleName.CAR_AXLE
        """Automotive: Car Axle"""

        TRUCK_AXLE = ExampleName.TRUCK_AXLE
        """Automotive: Truck Axle"""

        class HybridTransmissionExamples(ABC, metaclass=ExamplesMeta):
            """Hybrid Transmission Examples examples."""

            MULTI_MODE_HYBRID_TRANSMISSION = ExampleName.MULTI_MODE_HYBRID_TRANSMISSION
            """Automotive: Hybrid Transmission Examples: Multi Mode Hybrid Transmission"""

        class MinivanAxleAndDriveline(ABC, metaclass=ExamplesMeta):
            """Minivan Axle and Driveline examples."""

            MINIVAN_AXLE_NO_FE = ExampleName.MINIVAN_AXLE_NO_FE
            """Automotive: Minivan Axle and Driveline: Minivan Axle no FE"""

            MINIVAN_AXLE_CASING_FE = ExampleName.MINIVAN_AXLE_CASING_FE
            """Automotive: Minivan Axle and Driveline: Minivan Axle + Casing FE"""

            MINIVAN_AXLE_CASING_AND_DIFF_SHAFT_FE = (
                ExampleName.MINIVAN_AXLE_CASING_AND_DIFF_SHAFT_FE
            )
            """Automotive: Minivan Axle and Driveline: Minivan Axle + Casing and Diff Shaft FE"""

        class AutomaticWithRavigneaux(ABC, metaclass=ExamplesMeta):
            """Automatic with Ravigneaux examples."""

            AUTOMATIC_WITH_RAVIGNEAUX = ExampleName.AUTOMATIC_WITH_RAVIGNEAUX
            """Automotive: Automatic with Ravigneaux: Automatic with Ravigneaux"""

            AUTOMATIC_WITH_RAVIGNEAUX_WITH_CARRIER_FE = (
                ExampleName.AUTOMATIC_WITH_RAVIGNEAUX_WITH_CARRIER_FE
            )
            """Automotive: Automatic with Ravigneaux: Automatic with Ravigneaux, with Carrier FE"""

        TRANSFER_CASE_BELT = ExampleName.TRANSFER_CASE_BELT
        """Automotive: Transfer Case - Belt"""

        class ElectricDriveTransmission(ABC, metaclass=ExamplesMeta):
            """Electric Drive Transmission examples."""

            ELECTRIC_DRIVE_TRANSMISSION = ExampleName.ELECTRIC_DRIVE_TRANSMISSION
            """Automotive: Electric Drive Transmission: Electric Drive Transmission"""

            ELECTRIC_DRIVE_TRANSMISSION_WITH_ELECTRIC_MOTOR = (
                ExampleName.ELECTRIC_DRIVE_TRANSMISSION_WITH_ELECTRIC_MOTOR
            )
            """Automotive: Electric Drive Transmission: Electric Drive Transmission - With Electric Motor"""

            ELECTRIC_DRIVE_TRANSMISSION_DETAILED_MODEL = (
                ExampleName.ELECTRIC_DRIVE_TRANSMISSION_DETAILED_MODEL
            )
            """Automotive: Electric Drive Transmission: Electric Drive Transmission - Detailed Model"""

            ELECTRIC_DRIVE_TRANSMISSION_DETAILED_MODEL_NO_HOUSING_NO_DIFF_INTERNALS = ExampleName.ELECTRIC_DRIVE_TRANSMISSION_DETAILED_MODEL_NO_HOUSING_NO_DIFF_INTERNALS
            """Automotive: Electric Drive Transmission: Electric Drive Transmission - Detailed Model - No Housing, No Diff Internals"""

            ELECTRIC_DRIVE_TRANSMISSION_SKEWED_ROTOR = (
                ExampleName.ELECTRIC_DRIVE_TRANSMISSION_SKEWED_ROTOR
            )
            """Automotive: Electric Drive Transmission: Electric Drive Transmission - Skewed Rotor"""

            ELECTRIC_DRIVE_TRANSMISSION_AXIAL_FLUX_MOTOR = (
                ExampleName.ELECTRIC_DRIVE_TRANSMISSION_AXIAL_FLUX_MOTOR
            )
            """Automotive: Electric Drive Transmission: Electric Drive Transmission - Axial Flux Motor"""

        TRANSFER_CASE_GEAR = ExampleName.TRANSFER_CASE_GEAR
        """Automotive: Transfer Case - Gear"""

        class DriveTrainSimulation(ABC, metaclass=ExamplesMeta):
            """Drive Train Simulation examples."""

            PLANETARY_RANGE_CHANGER = ExampleName.PLANETARY_RANGE_CHANGER
            """Automotive: Drive Train Simulation: Planetary Range Changer"""

            TWO_SHAFTS_ONE_CLUTCH = ExampleName.TWO_SHAFTS_ONE_CLUTCH
            """Automotive: Drive Train Simulation: Two Shafts One Clutch"""

            TORQUE_CONVERTER = ExampleName.TORQUE_CONVERTER
            """Automotive: Drive Train Simulation: Torque Converter"""

            ENGINE_INERTIA_ADJUSTED_LOADS = ExampleName.ENGINE_INERTIA_ADJUSTED_LOADS
            """Automotive: Drive Train Simulation: Engine - Inertia Adjusted Loads"""

            TWO_SPEED_DEMO = ExampleName.TWO_SPEED_DEMO
            """Automotive: Drive Train Simulation: Two Speed Demo"""

        class GearRattleTrainingManual(ABC, metaclass=ExamplesMeta):
            """Gear Rattle Training Manual examples."""

            FIVE_DOF_TORSIONAL_MODEL_NO_INPUTS = (
                ExampleName.FIVE_DOF_TORSIONAL_MODEL_NO_INPUTS
            )
            """Automotive: Gear Rattle Training Manual: 5DOF Torsional Model (No Inputs)"""

            FIVE_DOF_TORSIONAL_MODEL_COMPLETED_ONE_LASH = (
                ExampleName.FIVE_DOF_TORSIONAL_MODEL_COMPLETED_ONE_LASH
            )
            """Automotive: Gear Rattle Training Manual: 5DOF Torsional Model (Completed, 1 Lash)"""

            FIVE_DOF_TORSIONAL_MODEL_COMPLETED_TWO_LASH = (
                ExampleName.FIVE_DOF_TORSIONAL_MODEL_COMPLETED_TWO_LASH
            )
            """Automotive: Gear Rattle Training Manual: 5DOF Torsional Model (Completed, 2 Lash)"""

            SIMPLE_HOUSING_NO_INPUTS = ExampleName.SIMPLE_HOUSING_NO_INPUTS
            """Automotive: Gear Rattle Training Manual: Simple Housing (No Inputs)"""

            SIMPLE_HOUSING_COMPLETED = ExampleName.SIMPLE_HOUSING_COMPLETED
            """Automotive: Gear Rattle Training Manual: Simple Housing (Completed)"""

        class SplineRumbleTrainingManual(ABC, metaclass=ExamplesMeta):
            """Spline Rumble Training Manual examples."""

            SPLINE_RUMBLE = ExampleName.SPLINE_RUMBLE
            """Automotive: Spline Rumble Training Manual: Spline Rumble"""

        SCOOTER_GEARBOX = ExampleName.SCOOTER_GEARBOX
        """Automotive: Scooter Gearbox"""

    class Components(ABC, metaclass=ExamplesMeta):
        """Components examples."""

        class GearSets(ABC, metaclass=ExamplesMeta):
            """Gear Sets examples."""

            HELICAL_GEAR_SET = ExampleName.HELICAL_GEAR_SET
            """Components: Gear Sets: Helical Gear Set"""

            WORM_GEAR_SET = ExampleName.WORM_GEAR_SET
            """Components: Gear Sets: Worm Gear Set"""

            SPIRAL_BEVEL_GEAR_SET = ExampleName.GEAR_SETS_SPIRAL_BEVEL_GEAR_SET
            """Components: Gear Sets: Spiral Bevel Gear Set"""

            STRAIGHT_BEVEL_GEAR_SET = ExampleName.STRAIGHT_BEVEL_GEAR_SET
            """Components: Gear Sets: Straight Bevel Gear Set"""

            KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET = (
                ExampleName.KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET
            )
            """Components: Gear Sets: Klingelnberg Cyclo-Palloid Spiral Bevel Gear Set"""

            FACE_GEAR_SET = ExampleName.FACE_GEAR_SET
            """Components: Gear Sets: Face Gear Set"""

            KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET = (
                ExampleName.KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET
            )
            """Components: Gear Sets: Klingelnberg Cyclo-Palloid Hypoid Gear Set"""

            AGMA_GEAR_SET_FOR_SCUFFING = ExampleName.AGMA_GEAR_SET_FOR_SCUFFING
            """Components: Gear Sets: AGMA Gear Set For Scuffing"""

            HYPOID_GEAR_SET = ExampleName.HYPOID_GEAR_SET
            """Components: Gear Sets: Hypoid Gear Set"""

            ZEROL_BEVEL_GEAR_SET = ExampleName.ZEROL_BEVEL_GEAR_SET
            """Components: Gear Sets: Zerol Bevel Gear Set"""

        class FluidFilmBearings(ABC, metaclass=ExamplesMeta):
            """Fluid Film Bearings examples."""

            PLAIN_JOURNAL_BEARING = ExampleName.PLAIN_JOURNAL_BEARING
            """Components: Fluid Film Bearings: Plain Journal Bearing"""

            TILTING_THRUST_PAD_BEARING = ExampleName.TILTING_THRUST_PAD_BEARING
            """Components: Fluid Film Bearings: Tilting Thrust Pad Bearing"""

            TILTING_PAD_JOURNAL_BEARING = ExampleName.TILTING_PAD_JOURNAL_BEARING
            """Components: Fluid Film Bearings: Tilting Pad Journal Bearing"""

        class Planetaries(ABC, metaclass=ExamplesMeta):
            """Planetaries examples."""

            TWO_Z_X_WW = ExampleName.TWO_Z_X_WW
            """Components: Planetaries: 2Z-X WW"""

            TWO_Z_X_NN_ONE_PLANET = ExampleName.TWO_Z_X_NN_ONE_PLANET
            """Components: Planetaries: 2Z-X NN 1 Planet"""

            TWO_Z_X_NN = ExampleName.TWO_Z_X_NN
            """Components: Planetaries: 2Z-X NN"""

            TWO_Z_X_NW = ExampleName.TWO_Z_X_NW
            """Components: Planetaries: 2Z-X NW"""

            UNEQUAL_SPACING_IDLER = ExampleName.UNEQUAL_SPACING_IDLER
            """Components: Planetaries: Unequal Spacing Idler"""

            RANGE_CHANGER = ExampleName.RANGE_CHANGER
            """Components: Planetaries: Range Changer"""

            SIMPLE_PLANETARY_WITH_FE_CARRIER = (
                ExampleName.SIMPLE_PLANETARY_WITH_FE_CARRIER
            )
            """Components: Planetaries: Simple Planetary with FE Carrier"""

            SIMPLE_PLANETARY = ExampleName.SIMPLE_PLANETARY
            """Components: Planetaries: Simple Planetary"""

            HIGH_RATIO_COMPOUND = ExampleName.HIGH_RATIO_COMPOUND
            """Components: Planetaries: High Ratio Compound"""

            BEVEL_DIFFERENTIAL_WITH_TWO_CARRIERS = (
                ExampleName.BEVEL_DIFFERENTIAL_WITH_TWO_CARRIERS
            )
            """Components: Planetaries: Bevel Differential with Two Carriers"""

        class CVTs(ABC, metaclass=ExamplesMeta):
            """CVTs examples."""

            CVT = ExampleName.CVT
            """Components: CVTs: CVT"""

            CVT_WITH_SIMPLE_FE_ANNULUS = ExampleName.CVT_WITH_SIMPLE_FE_ANNULUS
            """Components: CVTs: CVT - With Simple FE Annulus"""

        class CycloidalDrives(ABC, metaclass=ExamplesMeta):
            """Cycloidal Drives examples."""

            SIMPLE_CYCLOIDAL_DRIVE = ExampleName.SIMPLE_CYCLOIDAL_DRIVE
            """Components: Cycloidal Drives: Simple Cycloidal Drive"""

        SIMPLE_HOUSING = ExampleName.SIMPLE_HOUSING
        """Components: Simple Housing"""

        SIMPLE_HOUSING_FULL_MESH = ExampleName.SIMPLE_HOUSING_FULL_MESH
        """Components: Simple Housing Full Mesh"""

        PARKING_LOCK_TRAINING_MODEL = ExampleName.PARKING_LOCK_TRAINING_MODEL
        """Components: Parking Lock Training Model"""

        BELT_DRIVE = ExampleName.BELT_DRIVE
        """Components: Belt Drive"""

    class Aerospace(ABC, metaclass=ExamplesMeta):
        """Aerospace examples."""

        AEROSPACE_ACCESSORY_GEARBOX_WITHOUT_FE_PARTS = (
            ExampleName.AEROSPACE_ACCESSORY_GEARBOX_WITHOUT_FE_PARTS
        )
        """Aerospace: Aerospace Accessory Gearbox without FE Parts"""

        AEROSPACE_ACCESSORY_GEARBOX_WITH_FE_PARTS = (
            ExampleName.AEROSPACE_ACCESSORY_GEARBOX_WITH_FE_PARTS
        )
        """Aerospace: Aerospace Accessory Gearbox with FE Parts"""

        AIRCRAFT_NOSE_WHEEL = ExampleName.AIRCRAFT_NOSE_WHEEL
        """Aerospace: Aircraft Nose Wheel"""

        HELICOPTER_TRANSMISSION = ExampleName.HELICOPTER_TRANSMISSION
        """Aerospace: Helicopter Transmission"""

        AIRCRAFT_ENGINE = ExampleName.AIRCRAFT_ENGINE
        """Aerospace: Aircraft Engine"""

    class Analyses(ABC, metaclass=ExamplesMeta):
        """Analyses examples."""

        class BevelLTCA(ABC, metaclass=ExamplesMeta):
            """Bevel LTCA examples."""

            SPIRAL_BEVEL_GEAR_SET = ExampleName.BEVEL_LTCA_SPIRAL_BEVEL_GEAR_SET
            """Analyses: Bevel LTCA: Spiral Bevel Gear Set"""

        class RollingBearings(ABC, metaclass=ExamplesMeta):
            """Rolling Bearings examples."""

            SIMPLE_DYNAMIC_ANGULAR_CONTACT_BALL_BEARING = (
                ExampleName.SIMPLE_DYNAMIC_ANGULAR_CONTACT_BALL_BEARING
            )
            """Analyses: Rolling Bearings: Simple Dynamic Angular Contact Ball Bearing"""

        class Acoustics(ABC, metaclass=ExamplesMeta):
            """Acoustics examples."""

            SIMPLE_HOUSING_FULL_MESH_FOR_ACOUSTICS = (
                ExampleName.SIMPLE_HOUSING_FULL_MESH_FOR_ACOUSTICS
            )
            """Analyses: Acoustics: Simple Housing Full Mesh for Acoustics"""

        class LTCA(ABC, metaclass=ExamplesMeta):
            """LTCA examples."""

            HIGH_ASYMMETRY_RATIO_GEAR_EXAMPLE = (
                ExampleName.HIGH_ASYMMETRY_RATIO_GEAR_EXAMPLE
            )
            """Analyses: LTCA: High Asymmetry Ratio Gear Example"""

            TRUCK_GEAR_PAIR_FE_MODEL_ZERO_ADJ_TEETH = (
                ExampleName.TRUCK_GEAR_PAIR_FE_MODEL_ZERO_ADJ_TEETH
            )
            """Analyses: LTCA: Truck Gear Pair, FE Model, 0 Adj. Teeth"""

            MARINE_GEAR_PAIR_FE_MODEL_ZERO_ADJ_TEETH = (
                ExampleName.MARINE_GEAR_PAIR_FE_MODEL_ZERO_ADJ_TEETH
            )
            """Analyses: LTCA: Marine Gear Pair, FE Model, 0 Adj. Teeth"""

            INTERNAL_GEAR_PAIR_FE_MODEL_ZERO_ADJ_TEETH = (
                ExampleName.INTERNAL_GEAR_PAIR_FE_MODEL_ZERO_ADJ_TEETH
            )
            """Analyses: LTCA: Internal Gear Pair, FE Model, 0 Adj. Teeth"""

        class RotorDynamics(ABC, metaclass=ExamplesMeta):
            """Rotor Dynamics examples."""

            ROTOR_DYNAMICS_TWO_SHAFTS = ExampleName.ROTOR_DYNAMICS_TWO_SHAFTS
            """Analyses: Rotor Dynamics: Rotor Dynamics Two Shafts"""

            ROTOR_DYNAMICS_TWO_SHAFTS_FULL_MODEL = (
                ExampleName.ROTOR_DYNAMICS_TWO_SHAFTS_FULL_MODEL
            )
            """Analyses: Rotor Dynamics: Rotor Dynamics Two Shafts - Full Model"""

            LAVEL_JEFFCOTT_ROTOR = ExampleName.LAVEL_JEFFCOTT_ROTOR
            """Analyses: Rotor Dynamics: Lavel Jeffcott Rotor"""

        class CylindricalGearManufacturing(ABC, metaclass=ExamplesMeta):
            """Cylindrical Gear Manufacturing examples."""

            COMPLETE_CYLINDRICAL_GEAR_PAIR = ExampleName.COMPLETE_CYLINDRICAL_GEAR_PAIR
            """Analyses: Cylindrical Gear Manufacturing: Complete Cylindrical Gear Pair"""

            CYLINDRICAL_PLANETARY = ExampleName.CYLINDRICAL_PLANETARY
            """Analyses: Cylindrical Gear Manufacturing: Cylindrical Planetary"""

        class TIFF(ABC, metaclass=ExamplesMeta):
            """TIFF examples."""

            MACK_ALDENER_SINGLE_STAGE = ExampleName.MACK_ALDENER_SINGLE_STAGE
            """Analyses: TIFF: MackAldener Single Stage"""

            MACK_ALDENER_IDLER = ExampleName.MACK_ALDENER_IDLER
            """Analyses: TIFF: MackAldener Idler"""

        class MacroGeometryOptimisation(ABC, metaclass=ExamplesMeta):
            """Macro Geometry Optimisation examples."""

            FZG_TYPE_C_OPTIMISATION_EXAMPLE = (
                ExampleName.FZG_TYPE_C_OPTIMISATION_EXAMPLE
            )
            """Analyses: Macro Geometry Optimisation: FZG Type C - Optimisation Example"""

    class WindTurbine(ABC, metaclass=ExamplesMeta):
        """Wind Turbine examples."""

        WIND_TURBINE_FLEXIBLE_ANNULUS = ExampleName.WIND_TURBINE_FLEXIBLE_ANNULUS
        """Wind Turbine: Wind Turbine - Flexible Annulus"""

        WIND_TURBINE = ExampleName.WIND_TURBINE
        """Wind Turbine: Wind Turbine"""

        WIND_TURBINE_FLEXIBLE_BEARING_OUTER_RACE = (
            ExampleName.WIND_TURBINE_FLEXIBLE_BEARING_OUTER_RACE
        )
        """Wind Turbine: Wind Turbine - Flexible Bearing Outer Race"""

        class DriveTrainSimulation(ABC, metaclass=ExamplesMeta):
            """Drive Train Simulation examples."""

            WIND_TURBINE_GEARBOX = ExampleName.WIND_TURBINE_GEARBOX
            """Wind Turbine: Drive Train Simulation: Wind Turbine Gearbox"""

            WIND_TURBINE_FULL_DRIVETRAIN = ExampleName.WIND_TURBINE_FULL_DRIVETRAIN
            """Wind Turbine: Drive Train Simulation: Wind Turbine Full Drivetrain"""

        class ConceptDesigns(ABC, metaclass=ExamplesMeta):
            """Concept Designs examples."""

            ONE_PLANETARY_TWO_PARALLEL_STAGES = (
                ExampleName.ONE_PLANETARY_TWO_PARALLEL_STAGES
            )
            """Wind Turbine: Concept Designs: 1 Planetary, 2 Parallel Stages"""

            ONE_PLANETARY_TWO_PARALLEL_STAGES_WITH_TORQUE_LIMIT_STAGE = (
                ExampleName.ONE_PLANETARY_TWO_PARALLEL_STAGES_WITH_TORQUE_LIMIT_STAGE
            )
            """Wind Turbine: Concept Designs: 1 Planetary, 2 Parallel Stages With Torque Limit Stage"""

            ONE_PLANETARY_ONE_INTERNAL_STAGE = (
                ExampleName.ONE_PLANETARY_ONE_INTERNAL_STAGE
            )
            """Wind Turbine: Concept Designs: 1 Planetary, 1 Internal Stage"""

            TWO_PLANETARY_ONE_PARALLEL_STAGE = (
                ExampleName.TWO_PLANETARY_ONE_PARALLEL_STAGE
            )
            """Wind Turbine: Concept Designs: 2 Planetary, 1 Parallel Stage"""

            THREE_PARALLEL_STAGES = ExampleName.THREE_PARALLEL_STAGES
            """Wind Turbine: Concept Designs: Three Parallel Stages"""

            PRIMARY_STEP_UP_BEVEL_PLANETARY_WITH_MOTOR = (
                ExampleName.PRIMARY_STEP_UP_BEVEL_PLANETARY_WITH_MOTOR
            )
            """Wind Turbine: Concept Designs: Primary Step-up, Bevel, Planetary With Motor"""

            PLANETARY_DIFF_PLANETARY_STAR_PARALLEL_STAGES = (
                ExampleName.PLANETARY_DIFF_PLANETARY_STAR_PARALLEL_STAGES
            )
            """Wind Turbine: Concept Designs: Planetary Diff, Planetary Star, Parallel Stages"""

            PLANETARY_PLANETARY_STAR_PLANETARY_DIFF_PARALLEL_STAGES = (
                ExampleName.PLANETARY_PLANETARY_STAR_PLANETARY_DIFF_PARALLEL_STAGES
            )
            """Wind Turbine: Concept Designs: Planetary, Planetary Star, Planetary Diff, Parallel Stages"""

            ONE_PLANETARY_STAR_TWO_PLANETARY_DIFF_STAGES = (
                ExampleName.ONE_PLANETARY_STAR_TWO_PLANETARY_DIFF_STAGES
            )
            """Wind Turbine: Concept Designs: 1 Planetary Star, 2 Planetary Diff Stages"""

            ONE_PLANETARY_TWO_PARALLEL_PLANETARY_DIFF_PLANETARY_STAR_TORQUE_CONVERTER_STAGES = ExampleName.ONE_PLANETARY_TWO_PARALLEL_PLANETARY_DIFF_PLANETARY_STAR_TORQUE_CONVERTER_STAGES
            """Wind Turbine: Concept Designs: 1 Planetary, 2 Parallel, Planetary Diff, Planetary Star, Torque Converter Stages"""

            TWO_PLANETARY_PLANETARY_HYDROSTATIC_CVT = (
                ExampleName.TWO_PLANETARY_PLANETARY_HYDROSTATIC_CVT
            )
            """Wind Turbine: Concept Designs: 2 Planetary, Planetary Hydrostatic CVT"""

            PLANETARY_NO_SUN_PLANETARY_NO_ANNULUS_PARALLEL_STAGE = (
                ExampleName.PLANETARY_NO_SUN_PLANETARY_NO_ANNULUS_PARALLEL_STAGE
            )
            """Wind Turbine: Concept Designs: Planetary No Sun, Planetary No Annulus, Parallel Stage"""

            TWO_STAGE_COMPOUND_PLANETARY_PARALLEL_STAGE = (
                ExampleName.TWO_STAGE_COMPOUND_PLANETARY_PARALLEL_STAGE
            )
            """Wind Turbine: Concept Designs: 2 Stage Compound Planetary, Parallel Stage"""

    class Tutorials(ABC, metaclass=ExamplesMeta):
        """Tutorials examples."""

        STARTER_MODEL_CLUTCHED_SYSTEM = ExampleName.STARTER_MODEL_CLUTCHED_SYSTEM
        """Tutorials: Starter Model - Clutched System"""

    class Marine(ABC, metaclass=ExamplesMeta):
        """Marine examples."""

        OUTBOARD = ExampleName.OUTBOARD
        """Marine: Outboard"""

        TIDAL_STREAM_GEARBOX = ExampleName.TIDAL_STREAM_GEARBOX
        """Marine: Tidal Stream Gearbox"""

    class Rail(ABC, metaclass=ExamplesMeta):
        """Rail examples."""

        RAIL_BOGIE = ExampleName.RAIL_BOGIE
        """Rail: Rail Bogie"""

    class Industrial(ABC, metaclass=ExamplesMeta):
        """Industrial examples."""

        WINCH_EXAMPLE = ExampleName.WINCH_EXAMPLE
        """Industrial: Winch Example"""

    class Robotics(ABC, metaclass=ExamplesMeta):
        """Robotics examples."""

        RV_CYCLOIDAL_DRIVE_SIMPLE = ExampleName.RV_CYCLOIDAL_DRIVE_SIMPLE
        """Robotics: RV Cycloidal Drive - Simple"""

        RV_CYCLOIDAL_DRIVE_DETAILED = ExampleName.RV_CYCLOIDAL_DRIVE_DETAILED
        """Robotics: RV Cycloidal Drive - Detailed"""
