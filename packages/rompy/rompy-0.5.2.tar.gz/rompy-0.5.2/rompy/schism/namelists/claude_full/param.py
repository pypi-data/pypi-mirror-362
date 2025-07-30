# This file was auto generated from a schism namelist file on 2024-09-09.

from typing import Literal, Optional

from pydantic import Field, field_validator, model_validator

from rompy.schism.namelists.basemodel import NamelistBaseModel


class Core(NamelistBaseModel):
    """Core (mandatory) parameters"""

    ipre: int = Field(0, description="Pre-processor flag (1: on; 0: off)")
    ibc: int = Field(0, description="Baroclinic option")
    ibtp: int = Field(1)
    rnday: float = Field(30, description="Total run time in days")
    dt: float = Field(100, description="Time step in sec")
    msc2: int = Field(
        24,
        description="Same as msc in .nml ... for consistency check between SCHISM and WWM",
    )
    mdc2: int = Field(30, description="Same as mdc in .nml")
    ntracer_gen: int = Field(2, description="User defined module (USE_GEN)")
    ntracer_age: int = Field(
        4,
        description="Age calculation (USE_AGE). Must be =2*N where N is # of age tracers",
    )
    sed_class: int = Field(5, description="SED3D (USE_SED)")
    eco_class: int = Field(27, description="EcoSim (USE_ECO): must be between [25,60]")
    nspool: int = Field(36, description="Output step spool")
    ihfskip: int = Field(
        864,
        description="Stack spool; every ihfskip steps will be put into 1_*, 2_*, etc...",
    )

    @field_validator("ntracer_age")
    def validate_ntracer_age(cls, v):
        if v % 2 != 0:
            raise ValueError("ntracer_age must be even")
        return v

    @field_validator("eco_class")
    def validate_eco_class(cls, v):
        if not 25 <= v <= 60:
            raise ValueError("eco_class must be between 25 and 60")
        return v


class Opt(NamelistBaseModel):
    """Optional parameters"""

    ipre2: int = Field(0, description="2nd pre-proc flag")
    itransport_only: int = Field(0, description="Option to only solve tracer transport")
    iloadtide: int = Field(
        0,
        description="Option to add self-attracting and loading tide (SAL) into tidal potential",
    )
    loadtide_coef: float = Field(0.1, description="Used if iloadtide=2,3")
    start_year: int = Field(2000)
    start_month: int = Field(1)
    start_day: int = Field(1)
    start_hour: float = Field(0)
    utc_start: float = Field(8)
    ics: Literal[1, 2] = Field(
        1, description="Coordinate option: 1: Cartesian; 2: lon/lat"
    )
    ihot: Literal[0, 1, 2] = Field(0, description="Hotstart option")
    ieos_type: Literal[0, 1] = Field(0, description="Equation of State type")
    ieos_pres: int = Field(
        0, description="Used only if ieos_type=0. 0: without pressure effects"
    )
    eos_a: float = Field(-0.1, description="Needed if ieos_type=1; should be <=0")
    eos_b: float = Field(1001, description="Needed if ieos_type=1")
    dramp: float = Field(
        1, description="Ramp-up period in days for b.c. etc (no ramp-up if <=0)"
    )
    drampbc: float = Field(0, description="Ramp-up period in days for baroclinic force")
    iupwind_mom: Literal[0, 1] = Field(
        0, description="Method for momentum advection. 0: ELM; 1: upwind"
    )
    indvel: Literal[0, 1] = Field(
        0, description="Methods for computing velocity at nodes"
    )
    ihorcon: Literal[0, 1, 2] = Field(0, description="Horizontal viscosity option")
    hvis_coef0: float = Field(0.025, description="Const. diffusion # if ihorcon/=0")
    ishapiro: Literal[-1, 0, 1, 2] = Field(1, description="Shapiro filter option")
    niter_shap: int = Field(1, description="# of iterations with Shapiro filter")
    shapiro0: float = Field(0.5, description="Shapiro filter strength")
    thetai: float = Field(0.6, description="Implicitness factor (0.5<thetai<=1)")
    icou_elfe_wwm: Literal[0, 1, 2, 3, 4, 5, 6, 7] = Field(
        0, description="Coupling/decoupling flag for WWM"
    )
    nstep_wwm: int = Field(1, description="Call WWM every this many time steps")
    iwbl: Literal[0, 1, 2] = Field(0, description="Wave boundary layer formulation")
    hmin_radstress: float = Field(
        1,
        description="Min. total water depth used only in radiation stress calculation [m]",
    )
    drampwafo: float = Field(
        0, description="Ramp-up period in days for the wave forces (no ramp-up if <=0)"
    )
    turbinj: float = Field(
        0.15,
        description="% of depth-induced wave breaking energy injected in turbulence",
    )
    turbinjds: float = Field(
        1.0,
        description="% of wave energy dissipated through whitecapping injected in turbulence",
    )
    alphaw: float = Field(
        0.5, description="Scaling parameter for the surface roughness z0s = alphaw*Hm0"
    )
    fwvor_advxy_stokes: Literal[0, 1] = Field(
        1, description="Stokes drift advection (xy), Coriolis"
    )
    fwvor_advz_stokes: Literal[0, 1] = Field(
        1, description="Stokes drift advection (z), Coriolis"
    )
    fwvor_gradpress: Literal[0, 1] = Field(1, description="Pressure term")
    fwvor_breaking: Literal[0, 1] = Field(1, description="Wave breaking")
    fwvor_streaming: Literal[0, 1] = Field(1, description="Wave streaming")
    fwvor_wveg: Literal[0, 1] = Field(
        0, description="Wave dissipation by vegetation acceleration term"
    )
    fwvor_wveg_NL: Literal[0, 1] = Field(
        0, description="Non linear intrawave vegetation force"
    )
    cur_wwm: Literal[0, 1, 2] = Field(0, description="Coupling current in WWM")
    wafo_obcramp: Literal[0, 1] = Field(
        0, description="Ramp on wave forces at open boundary"
    )
    imm: Literal[0, 1, 2] = Field(0, description="Bed deformation option")
    ibdef: int = Field(10, description="# of steps used in deformation")
    slam0: float = Field(
        -124, description="Reference longitude for beta-plane approximation"
    )
    sfea0: float = Field(
        45, description="Reference latitude for beta-plane approximation"
    )
    iunder_deep: int = Field(
        0,
        description="Option to deal with under resolution near steep slopes in deeper depths",
    )
    h1_bcc: float = Field(
        50,
        description="Baroclinicity calculation in off/nearshore with iunder_deep=ibc=0",
    )
    h2_bcc: float = Field(
        100,
        description="Baroclinicity calculation in off/nearshore with iunder_deep=ibc=0",
    )
    hw_depth: float = Field(
        1e6, description="Threshold depth for Hannah-Wright-like ratio"
    )
    hw_ratio: float = Field(0.5, description="Hannah-Wright-like ratio")
    ihydraulics: int = Field(0, description="Hydraulic model option")
    if_source: int = Field(0, description="Point sources/sinks option")
    dramp_ss: float = Field(2, description="Ramp-up period in days for source/sinks")
    meth_sink: Literal[0, 1] = Field(1, description="Options to treat sinks @ dry elem")
    lev_tr_source: list[int] = Field(
        [-9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9],
        description="Vertical level to inject source concentration for each tracer module",
    )
    level_age: list[int] = Field(
        [9, -999], description="Level #'s if age module is invoked"
    )
    ihdif: Literal[0, 1] = Field(0, description="Horizontal diffusivity option")
    nchi: Literal[-1, 0, 1] = Field(0, description="Bottom friction option")
    dzb_min: float = Field(0.5, description="Min. bottom boundary layer thickness [m]")
    hmin_man: float = Field(1, description="Min. depth in Manning's formulation [m]")
    ncor: Literal[-1, 0, 1] = Field(0, description="Coriolis option")
    rlatitude: float = Field(46, description="Latitude if ncor=-1")
    coricoef: float = Field(0, description="Coriolis parameter if ncor=0")
    ic_elev: Literal[0, 1] = Field(
        0, description="Elevation initial condition flag for cold start"
    )
    nramp_elev: Literal[0, 1] = Field(
        0, description="Elevation boundary condition ramp-up flag"
    )
    inv_atm_bnd: Literal[0, 1] = Field(
        0, description="Optional inverse barometric effects on the elev. b.c."
    )
    prmsl_ref: float = Field(
        101325, description="Reference atmos. pressure on bnd [Pa]"
    )
    flag_ic: list[int] = Field(
        [1, 1, 1, -9, 1, 1, 1, 1, 1, 1, 1, 0],
        description="Initial condition flags for tracers",
    )
    gen_wsett: float = Field(0, description="Settling vel [m/s] for GEN module")
    ibcc_mean: Literal[0, 1] = Field(0, description="Mean T,S profile option")
    rmaxvel: float = Field(5, description="Max. horizontal velocity magnitude")
    velmin_btrack: float = Field(
        1e-4,
        description="Min. vel for invoking btrack and for abnormal exit in quicksearch",
    )
    btrack_nudge: float = Field(
        9.013e-3, description="Nudging factors for starting side/node"
    )
    ihhat: Literal[0, 1] = Field(1, description="Wetting and drying option")
    inunfl: Literal[0, 1] = Field(0, description="Wetting and drying option")
    h0: float = Field(0.01, description="Min. water depth for wetting/drying [m]")
    shorewafo: Literal[0, 1] = Field(0, description="Shoreline wave force option")
    moitn0: int = Field(50, description="Output spool for solver info")
    mxitn0: int = Field(1500, description="Max. iteration allowed")
    rtol0: float = Field(1e-12, description="Error tolerance")
    nadv: Literal[0, 1, 2] = Field(1, description="Advection (ELM) option")
    dtb_max: float = Field(30, description="Max time step for backtracking [sec]")
    dtb_min: float = Field(10, description="Min time step for backtracking [sec]")
    inter_mom: Literal[-1, 0, 1] = Field(
        0, description="Interpolation option for velocity at foot of char. line"
    )
    kr_co: int = Field(1, description="Choice of covariance function for Kriging")
    itr_met: Literal[3, 4] = Field(3, description="Tracer transport method")
    h_tvd: float = Field(5, description="Cut-off depth (m) for TVD")
    eps1_tvd_imp: float = Field(1e-4, description="Convergence tolerance for TVD")
    eps2_tvd_imp: float = Field(1e-14, description="Convergence tolerance for TVD")
    ielm_transport: Literal[0, 1] = Field(
        0, description="Optional hybridized ELM transport for efficiency"
    )
    max_subcyc: int = Field(
        10, description="Max # of subcycling per time step in transport allowed"
    )
    ip_weno: Literal[0, 1, 2] = Field(2, description="Order of accuracy for WENO")
    courant_weno: float = Field(0.5, description="Courant number for WENO transport")
    nquad: Literal[1, 2] = Field(
        2, description="Number of quad points on each side for WENO"
    )
    ntd_weno: Literal[1, 3] = Field(
        1, description="Order of temporal discretization for WENO"
    )
    epsilon1: float = Field(
        1e-15, description="Coefficient for 2nd order WENO smoother"
    )
    epsilon2: float = Field(
        1e-10, description="1st coefficient for 3rd order WENO smoother"
    )
    i_prtnftl_weno: Literal[0, 1] = Field(
        0,
        description="Option for writing nonfatal errors on invalid temp. or salinity for density",
    )
    epsilon3: float = Field(
        1e-25, description="2nd coefficient for 3rd order WENO smoother"
    )
    ielad_weno: Literal[0, 1] = Field(
        0, description="Use ELAD method to suppress dispersion"
    )
    small_elad: float = Field(1e-4, description="Small value for ELAD")
    nws: Literal[-1, 0, 1, 2, 4] = Field(0, description="Atmospheric option")
    wtiminc: float = Field(150, description="Time step for atmos. forcing")
    drampwind: float = Field(1, description="Ramp-up period in days for wind")
    iwindoff: Literal[0, 1] = Field(0, description="Wind factor option")
    iwind_form: Literal[-3, -2, -1, 0, 1] = Field(
        1, description="Wind stress calculation method"
    )
    model_type_pahm: Literal[1, 10] = Field(10, description="Hurricane model type")
    ihconsv: Literal[0, 1] = Field(0, description="Heat exchange option")
    isconsv: Literal[0, 1] = Field(0, description="Evaporation/precipitation model")
    i_hmin_airsea_ex: Literal[0, 1, 2] = Field(
        2, description="Option for locally turning off heat exchange"
    )
    hmin_airsea_ex: float = Field(0.2, description="Min depth for heat exchange [m]")
    i_hmin_salt_ex: Literal[0, 1, 2] = Field(
        2, description="Option for locally turning off salt exchange"
    )
    hmin_salt_ex: float = Field(0.2, description="Min depth for salt exchange [m]")
    iprecip_off_bnd: Literal[0, 1] = Field(
        0, description="Turn off precip near land boundary"
    )
    itur: Literal[0, 3, 5] = Field(3, description="Turbulence closure option")
    dfv0: float = Field(1e-2, description="Vertical eddy viscosity if itur=0")
    dfh0: float = Field(1e-4, description="Vertical eddy diffusivity if itur=0")
    mid: Literal["KL", "KE"] = Field("KL", description="Turbulence model if itur=3,5")
    stab: Literal["KC", "GA"] = Field(
        "KC", description="Stability function if itur=3,5"
    )
    xlsc0: float = Field(
        0.1, description="Scale for surface & bottom mixing length if itur=3,5"
    )
    inu_elev: Literal[0, 1] = Field(0, description="Sponge layer for elevation")
    inu_uv: Literal[0, 1] = Field(0, description="Sponge layer for velocity")
    inu_tr: list[int] = Field(
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], description="Nudging options for tracers"
    )
    nu_sum_mult: Literal[1, 2] = Field(1, description="Final relax calculation method")
    vnh1: float = Field(400, description="Vertical nudging depth 1")
    vnf1: float = Field(0, description="Vertical relax 1")
    vnh2: float = Field(500, description="Vertical nudging depth 2")
    vnf2: float = Field(0, description="Vertical relax 2")
    step_nu_tr: float = Field(86400, description="Time step [sec] in all [MOD]_nu.nc")
    h_bcc1: float = Field(
        100, description="Cut-off depth for cubic spline interpolation near bottom"
    )
    s1_mxnbt: float = Field(
        0.5, description="Dimensioning parameter for inter-subdomain btrack"
    )
    s2_mxnbt: float = Field(
        3.5, description="Dimensioning parameter for inter-subdomain btrack"
    )
    iharind: Literal[0, 1] = Field(
        0, description="Flag for harmonic analysis for elevation"
    )
    iflux: Literal[0, 1, 2] = Field(0, description="Conservation check option")
    izonal5: Literal[0, 1] = Field(0, description="Williamson test #5")
    ibtrack_test: Literal[0, 1] = Field(0, description="Rotating Gausshill test")
    irouse_test: Literal[0, 1] = Field(0, description="Rouse profile test")
    flag_fib: Literal[1, 2, 3] = Field(
        1, description="Flag to choose FIB model for bacteria decay"
    )
    slr_rate: float = Field(120, description="Sea-level rise rate in mm/yr")
    isav: Literal[0, 1] = Field(0, description="Vegetation model on/off flag")
    nstep_ice: int = Field(1, description="Coupling step with ICE module")
    rearth_pole: float = Field(6378206.4, description="Earth's radius at pole")
    rearth_eq: float = Field(6378206.4, description="Earth's radius at equator")
    shw: float = Field(4184, description="Specific heat of water (C_p) in J/kg/K")
    rho0: float = Field(
        1000, description="Reference water density for Boussinesq approximation"
    )
    vclose_surf_frac: float = Field(
        1.0,
        description="Fraction of vertical flux closure adjustment applied at surface",
    )
    iadjust_mass_consv0: list[int] = Field(
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        description="Option to enforce strict mass conservation for each tracer model",
    )
    h_massconsv: float = Field(
        2, description="Threshold depth for mass conservation in ICM [m]"
    )
    rinflation_icm: float = Field(
        1e-3, description="Max ratio between H^{n+1} and H^n allowed in ICM"
    )

    @field_validator("thetai")
    def validate_thetai(cls, v):
        if not 0.5 < v <= 1:
            raise ValueError("thetai must be between 0.5 and 1")
        return v

    @field_validator("vclose_surf_frac")
    def validate_vclose_surf_frac(cls, v):
        if not 0 <= v < 1:
            raise ValueError("vclose_surf_frac must be between 0 and 1")
        return v

    @model_validator(mode="after")
    def validate_model(cls, values):
        if values.ihot == 2 and values.iharind != 0:
            raise ValueError("Hotstart ihot=2 is not working with harmonic analysis")
        if values.nchi == 1 and values.iwbl != 0:
            raise ValueError("If iwbl/=0, nchi must =1")
        if values.itr_met in [3, 4] and values.iadjust_mass_consv0[5] != 0:
            raise ValueError("iadjust_mass_consv0(5) must =0")
        return values


class Schout(NamelistBaseModel):
    """Output section parameters"""

    nc_out: Literal[0, 1] = Field(1, description="Main switch to control netcdf output")
    iof_ugrid: Literal[0, 1] = Field(0, description="UGRID option for 3D outputs")
    nhot: Literal[0, 1] = Field(0, description="Option for hotstart outputs")
    nhot_write: int = Field(8640, description="Steps for hotstart output")
    iout_sta: Literal[0, 1] = Field(0, description="Station output option")
    nspool_sta: int = Field(10, description="Output skip for station output")
    iof_hydro: list[int] = Field(
        [
            1,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            1,
            0,
            0,
            0,
            0,
            0,
        ],
        description="Global output options for hydro variables",
    )

    @model_validator(mode="after")
    def validate_model(cls, values):
        if values.nhot == 1 and values.nhot_write % values.nspool_sta != 0:
            raise ValueError("nhot_write must be a multiple of nspool_sta if nhot=1")
        return values


class Param(NamelistBaseModel):
    """Overall model for param.nml file"""

    core: Optional[Core] = Field(
        default_factory=Core, description="Core (mandatory) parameters"
    )
    opt: Optional[Opt] = Field(default_factory=Opt, description="Optional parameters")
    schout: Optional[Schout] = Field(
        default_factory=Schout, description="Output section parameters"
    )
