from pydantic import Field

from rompy.core.types import RompyBaseModel


class ICE_IN(RompyBaseModel):
    ice_tests: int = Field(default=0, description="box test flag")
    ice_advection: int = Field(default=1, description="advection on/off")
    ice_therm_on: int = Field(default=1, description="ice thermodynamics on/off flag")
    ievp: int = Field(default=2, description="1: EVP; 2: mEVP")
    ice_cutoff: float = Field(
        default=1.0e-3,
        description="cut-off thickness [m] or fraction for ice. No ice velocity if *<=ice_cuttoff",
    )
    evp_rheol_steps: int = Field(
        default=200, description="the number of sybcycling steps in EVP"
    )
    mevp_rheol_steps: int = Field(
        default=200, description="the number of iterations in mEVP"
    )
    ice_atmos_stress_form: int = Field(
        default=1, description="0-const Cd; 1: FESOM formulation"
    )
    cdwin0: float = Field(
        default=2.0e-3, description="needed if ice_atmos_stress_form=0 (const Cdw)"
    )
    delta_min: float = Field(
        default=2.0e-9,
        description="(1/s) Limit for minimum divergence (Hibler, Hunke normally use 2.0e-9, which does much stronger limiting; valid for both VP and EVP",
    )
    theta_io: float = Field(
        default=0.0,
        description="ice/ocean rotation angle. [degr]. Usually 0 unless vgrid is too coarse",
    )
    mevp_coef: int = Field(
        default=0,
        description="Options for specifying 2 relax coefficients in mEVP only (mevp_coef) 0: constant (mevp_alpha[12] below); 1: both coefficients equal to: mevp_alpha3/tanh(mevp_alpha4*area/dt_ice) In this case, mevp_alpha3 is the min, and at the finer end of mesh, the coeff's are approximately ~mevp_alpha4^-1",
    )
    mevp_alpha1: float = Field(
        default=200.0,
        description="const used in mEVP (constitutive eq), if mevp_coef=0",
    )
    mevp_alpha2: float = Field(
        default=200.0, description="const used in mEVP for momentum eq, if mevp_coef=0"
    )
    mevp_alpha3: float = Field(default=200.0, description="if mevp_coef=1")
    mevp_alpha4: float = Field(default=2.0e-2, description="if mevp_coef=1")
    pstar: float = Field(default=15000.0, description="[N/m^2]")
    ellipse: float = Field(default=2.0, description="ellipticity")
    c_pressure: float = Field(default=20.0, description="C [-]")
    ncyc_fct: int = Field(default=1, description="# of subcycling in transport")
    niter_fct: int = Field(
        default=3, description="# of iterartions in higher-order solve"
    )
    ice_gamma_fct: float = Field(
        default=0.25, description="smoothing parameter; 1 for max positivity preserving"
    )
    depth_ice_fct: float = Field(
        default=5.0, description="cut off depth (m) for non-FCT"
    )
    h_ml0: float = Field(default=0.1, description="ocean mixed layer depth [m]")
    salt_ice: float = Field(default=5.0, description="salinity for ice [PSU] (>=0)")
    salt_water: float = Field(
        default=34.0, description="salinity for water [PSU] (>=0)"
    )
    lead_closing: float = Field(
        default=0.5,
        description="lead closing parameter [m] - larger values slow down freezing-up but increase sea ice thickness",
    )
    Saterm: float = Field(
        default=0.5, description="Semter const -smaller value could slow down melting"
    )
    albsn: float = Field(default=0.85, description="Albedo: frozen snow")
    albsnm: float = Field(default=0.75, description="melting snow (<=albsn)")
    albi: float = Field(default=0.75, description="frozen ice (<=albsn)")
    albm: float = Field(default=0.66, description="melting ice (<=albi)")


class ICE(RompyBaseModel):
    ice_in: ICE_IN = Field(description="ice_in")
