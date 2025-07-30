from typing import List

from pydantic import Field

from rompy.core.types import RompyBaseModel


class SED_CORE(RompyBaseModel):
    Sd50: List[float] = Field(
        [0.12, 0.18, 0.39, 0.60, 1.2],
        description="D50 MEDIAN SEDIMENT GRAIN DIAMETER (mm) for Ntracers",
    )
    Erate: List[float] = Field(
        [1.6e-3, 1.6e-3, 1.6e-3, 1.6e-3, 1.6e-3],
        description="SURFACE EROSION RATE, E0 (kg/m/m/s) or (s/m) if ierosion=1 for Ntracers",
    )


class SED_OPT(RompyBaseModel):
    iSedtype: List[int] = Field(
        [1, 1, 1, 1, 1],
        description="SEDIMENT TYPE (0=MUD, 1=SAND, 2=GRAVEL) for Ntracers",
    )
    Srho: List[float] = Field(
        [2650.0, 2650.0, 2650.0, 2650.0, 2650.0],
        description="SEDIMENT GRAIN DENSITY (kg/m3) for Ntracers",
    )
    comp_ws: int = Field(
        0,
        description="COMPUTATION OF SEDIMENT SETTLING VELOCITY (0=Disabled, 1=Enabled)",
    )
    comp_tauce: int = Field(
        0,
        description="COMPUTATION OF SEDIMENT CRITICAL SHEAR STRESS (0=Disabled, 1=Enabled)",
    )
    Wsed: List[float] = Field(
        [1.06, 3.92, 5.43, 10.19, 28.65],
        description="PARTICLES SETTLING VELOCITY (mm/s) for Ntracers",
    )
    tau_ce: List[float] = Field(
        [0.15, 0.17, 0.23, 0.3, 0.6],
        description="CRITICAL SHEAR STRESS FOR EROSION (Pa) for Ntracers",
    )
    sed_debug: int = Field(
        0,
        description="DEBUG (0=silent, 1=output variables to nonfatal_* files)",
    )
    ised_dump: int = Field(
        0,
        description="Dumping/dredging option (0=No, 1=Requires input sed_dump.in)",
    )
    bedload: int = Field(
        1,
        description="BEDLOAD (0=Disabled, 1=van rijn, 2=Meyer-Peter and Mueller, 3=Soulsby and Damgaard, 4=Wu and Lin)",
    )
    bedload_filter: int = Field(
        0,
        description="FILTER for bedload fluxes (0=Disabled, 1=Enabled)",
    )
    bedload_limiter: int = Field(
        0,
        description="LIMITER for bedload flux components (0=Disabled, 1=Enabled)",
    )
    suspended_load: int = Field(
        1,
        description="SUSPENDED LOAD (0=Disabled, 1=Enabled)",
    )
    iasym: int = Field(
        0,
        description="WAVE ASYMMETRY (0=Disabled, 1=Enabled)",
    )
    w_asym_max: float = Field(
        0.4,
        description="Maximum wave asymmetry coefficient",
    )
    elfrink_filter: int = Field(
        0,
        description="ELFRINK FILTER for wave-induced bedload (0=Disabled, 1=Enabled)",
    )
    ech_uorb: int = Field(
        200,
        description="Number of bins considered for orbital velocity temporal series",
    )
    bedload_acc: int = Field(
        0,
        description="BEDLOAD TRANSPORT DUE TO WAVE ACCELERATION (0=Disabled, 1=Hoefel and Elgar, 2=Dubarbier et al.)",
    )
    bedload_acc_filter: int = Field(
        0,
        description="FILTER for bedload transport due to wave acceleration (0=Disabled, 1=Enabled)",
    )
    kacc_hoe: float = Field(
        1.4e-4,
        description="Constant used in Hoefel and Elgar formulation",
    )
    kacc_dub: float = Field(
        0.631e-4,
        description="Constant used in Dubarbier et al. formulation",
    )
    thresh_acc_opt: int = Field(
        2,
        description="Method to compute the critical mobility parameter for initiation of sediment transport due to acceleration-skewness",
    )
    acrit: float = Field(
        0.2,
        description="Critical acceleration for acceleration-skewness sediment transport",
    )
    tau_option: int = Field(
        1,
        description="Controls the height at which the current-induced bottom shear stress is derived",
    )


class SEDIMENT(RompyBaseModel):
    sed_core: SED_CORE = Field(description="SED_CORE")
    sed_opt: SED_OPT = Field(description="SED_OPT")
