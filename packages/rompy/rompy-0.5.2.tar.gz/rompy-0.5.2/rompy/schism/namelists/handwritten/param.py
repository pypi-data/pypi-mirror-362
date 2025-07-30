from pydantic import Field

from rompy.core.types import RompyBaseModel


class CORE(RompyBaseModel):
    ipre: int = Field(
        description="Pre-processing option. Useful for checking grid violations.",
        default=0,
    )
    ibc: int = Field(
        description="""Baroclinic/barotropic option.
        0 for Baroclinic option
        1 for barotropic
        If ibc=0 (baroclinic model), ibtp is not used.""",
        default=1,
    )
    ibtp: int = Field(
        description="Baroclinic/barotropic option. If ibc=0 (baroclinic model), ibtp is not used.",
        default=0,
    )
    rnday: int = Field(
        description="total run time in days", default=120
    )  # TODO move this to run definition
    dt: float = Field(description="Time step in sec", default=120.0)
    msc2: int = Field(
        description="same as msc in .nml ... for consitency check between SCHISM and WWM",
        default=36,
    )
    mdc2: int = Field(description="same as mdc in .nml", default=36)
    ntracer_gen: int = Field(description="user defined module (USE_GEN)", default=2)
    ntracer_age: int = Field(
        description="age calculation (USE_AGE). Must be =2*N where N is # of age tracers",
        default=4,
    )
    sed_class: int = Field(description="SED3D (USE_SED)", default=5)
    eco_class: int = Field(
        description="EcoSim (USE_ECO): must be between [25,60]", default=27
    )
    nspool: int = Field(..., description="output step spool")
    ihfskip: float = Field(
        description="stack spool; every ihfskip steps will be put into 1_*, 2_*, etc... use 22320.0 for 31 days; 5040 for 7 days; 21600 for 30 days; 20880 for 29 days",
        ihfskip=720,
    )


class OPT(RompyBaseModel):
    ipre2: int = 0
    start_year: int = Field(description="Starting year")
    start_month: int = Field(description="Starting month")
    start_day: int = Field(description="Starting day")
    start_hour: float = Field(description="Starting hour")
    utc_start: float = Field(description="UTC starting time")
    ics: int = Field(
        2,
        description="Coordinate option: 1: Cartesian; 2: lon/lat (hgrid.gr3=hgrid.ll in this case, and orientation of element is outward of earth)",
    )
    ihot: int = Field(
        0,
        description="Hotstart option. 0: cold start; 1: hotstart with time reset to 0; 2: continue from the step in hotstart.nc",
    )
    ieos_type: int = Field(
        0,
        description="Equation of State type used. ieos_type=0: UNESCO 1980 (nonlinear); =1: linear function of T ONLY, i.e. \rho=eos_b+eos_a*T, where eos_a<=0 in kg/m^3/C",
    )
    ieos_pres: int = Field(
        0, description="Used only if ieos_type=0. 0: without pressure effects"
    )
    eos_a: float = Field(-0.1, description="Needed if ieos_type=1; should be <=0")
    eos_b: float = Field(1001.0, description="Needed if ieos_type=1")
    nramp: int = Field(1, description="Ramp-up option (1: on; 0: off)")
    dramp: float = Field(1.0, description="Needed if nramp=1; ramp-up period in days")
    nrampbc: int = Field(0, description="Ramp-up flag for baroclinic force")
    drampbc: float = Field(1.0, description="Not used if nrampbc=0")
    iupwind_mom: int = Field(
        0,
        description="Method for momentum advection. 0: ELM; 1: upwind (not quite working yet)",
    )
    indvel: int = Field(
        1,
        description="Methods for computing velocity at nodes. If indvel=0, conformal linear shape function is used; if indvel=1, averaging method is used. For indvel=0, a stabilization method is needed (see below).",
    )
    ihorcon: int = Field(
        0,
        description="2 stabilization methods, mostly for indvel=0. (1) Horizontal viscosity option. ihorcon=0: no viscosity is used; =1: Lapacian; =2: bi-harmonic. If ihorcon=1, horizontal viscosity _coefficient_ (<=1/8, related to diffusion number) is given in hvis_coef0, and the diffusion # is problem dependent; [0.001-1/8] seems to work well. If ihorcon=2, diffusion number is given by hvis_coef0 (<=0.025). If indvel=1, no horizontal viscosity is needed. (2) Shapiro filter (see below)",
    )
    hvis_coef0: float = Field(
        0.025,
        description="const. diffusion # if ihorcon/=0; <=0.025 for ihorcon=2, <=0.125 for ihorcon=1",
    )
    ishapiro: int = Field(
        1,
        description="2nd stabilization method via Shapiro filter. This should normally be used if indvel=ihorcon=0. To transition between eddying/non-eddying regimes, use indvel=0, ihorcon/=0, and ishapiro=-1 (shapiro.gr3).",
    )
    shapiro0: float = Field(
        0.5,
        description="Shapiro filter strength, needed only if ishapiro=1; max is 0.5",
    )
    niter_shap: int = Field(
        1,
        description="needed if ishapiro/=0 - # of iterations with Shapiro filter. Suggested: 1",
    )
    thetai: float = Field(0.8, description="Implicitness factor (0.5<thetai<=1).")
    icou_elfe_wwm: int = Field(
        1,
        description="If WWM is used, set coupling/decoupling flag. Not used if USE_WWM is distabled in Makefile. 0: decoupled so 2 models will run independently; 1: full coupled (elevation, vel, and wind are all passed to WWM); 2: elevation and currents in wwm, no wave force in SCHISM; 3: no elevation and no currents in wwm, wave force in SCHISM; 4: elevation but no currents in wwm, wave force in SCHISM; 5: elevation but no currents in wwm, no wave force in SCHISM; 6: no elevation but currents in wwm, wave force in SCHISM; 7: no elevation but currents in wwm, no wave force in SCHISM; Note that all these parameters must be present in this file (even though not used).",
    )
    nstep_wwm: int = Field(
        3,
        description="call WWM every this many time steps. If /=1, consider using quasi-steady mode in WWM",
    )
    iwbl: int = Field(
        0,
        description="wave boundary layer formulation (used only if USE_WMM and icou_elfe_wwm/=0 and nchi=1. If icou_elfe_wwm=0, set iwbl=0): 1-modified Grant-Madsen formulation; 2-Soulsby (1997)",
    )
    hmin_radstress: float = Field(
        1.0,
        description="min. total water depth used only in radiation stress calculation [m]",
    )
    nrampwafo: int = Field(
        1, description="ramp-up option for the wave forces (1: on; 0: off)"
    )
    drampwafo: float = Field(
        1.0, description="needed if nrampwafo=1; ramp-up period in days"
    )
    turbinj: float = Field(
        0.15,
        description="% of depth-induced wave breaking energy injected in turbulence (default: 0.15 (15%), as proposed by Feddersen, 2012)",
    )
    imm: int = Field(
        0,
        description="Bed deformation option (0: off; 1: vertical deformation only; 2: 3D bed deformation). If imm=1, bdef.gr3 is needed; if imm=2, user needs to update depth info etc in the code (not working for ics=2 yet).",
    )
    ibdef: int = Field(
        10, description="needed if imm=1; # of steps used in deformation"
    )
    slam0: float = Field(
        120.0,
        description="Reference latitude for beta-plane approximation when ncor=1 (not used if ics=2)",
    )
    sfea0: float = Field(
        -29.0,
        description="Reference latitude for beta-plane approximation when ncor=1 (not used if ics=2)",
    )
    iunder_deep: int = Field(
        0,
        description="Option to deal with under resolution near steep slopes in deeper depths 0: use h[12,_bcc below; /=0: use hw_* below",
    )
    h1_bcc: float = Field(
        50.0,
        description="Baroclinicity calculation in off/nearshore with iunder_deep=ibc=0. The 'below-bottom' gradient is zeroed out if h>=h2_bcc (i.e. like Z) or uses const extrap (i.e. like terrain-following) if h<=h1_bcc(<h2_bcc) (and linear transition in between based on local depth)",
    )
    h2_bcc: float = Field(
        100.0,
        description="Baroclinicity calculation in off/nearshore with iunder_deep=ibc=0. The 'below-bottom' gradient is zeroed out if h>=h2_bcc (i.e. like Z) or uses const extrap (i.e. like terrain-following) if h<=h1_bcc(<h2_bcc) (and linear transition in between based on local depth)",
    )
    hw_depth: float = Field(1.0e6, description="threshold depth in [m]")
    hw_ratio: float = Field(0.5, description="ratio")
    ihydraulics: int = Field(0, description="hydraulic model option")
    if_source: int = Field(0, description="point sources/sinks option (0: no; 1: on)")
    nramp_ss: int = Field(
        1, description="needed if if_source=1; ramp-up flag for source/sinks"
    )
    dramp_ss: int = Field(
        2, description="needed if if_source=1; ramp-up period in days"
    )
    ihdif: int = Field(0, description="horizontal diffusivity option")
    nchi: int = Field(-1, description="bottom friction")
    dzb_min: float = Field(
        0.5, description="needed if nchi=1; min. bottom boundary layer thickness [m]."
    )
    hmin_man: float = Field(
        1.0, description="needed if nchi=-1: min. depth in Manning's formulation [m]"
    )
    ncor: int = Field(1, description="Coriolis")
    rlatitude: float = Field(-29, description="if ncor=-1")
    coricoef: float = Field(0, description="if ncor=0")
    ic_elev: int = Field(
        0, description="elevation initial condition flag for cold start only"
    )
    nramp_elev: int = Field(1, description="elevation boundary condition ramp-up flag")
    inv_atm_bnd: int = Field(
        1, description="optional inverse barometric effects on the elev. b.c."
    )
    prmsl_ref: float = Field(
        101325.0, description="reference atmos. pressure on bnd [Pa]"
    )
    flag_ic: list = Field([0, 0], description="initial condition for T,S")
    flag_ic: list = Field(
        default=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        description="Initial conditions for other tracers",
    )
    gen_wsett: float = Field(
        default=1e-4,
        description="Settling vel [m/s] for GEN module (positive downward)",
    )
    ibcc_mean: int = Field(
        default=0,
        description="Mean T,S profile option. If ibcc_mean=1 (or ihot=0 and flag_ic(1)=2), mean profile is read in from ts.ic, and will be removed when calculating baroclinic force.",
    )
    rmaxvel: float = Field(
        default=20.0,
        description="Max. horizontal velocity magnitude, used mainly to prevent problem in bulk aerodynamic module",
    )
    velmin_btrack: float = Field(
        default=1e-4,
        description="Min. vel for invoking btrack and for abnormal exit in quicksearch",
    )
    btrack_nudge: float = Field(
        default=9.013e-3,
        description="Nudging factors for starting side/node - add noise to avoid underflow",
    )
    ibtrack_openbnd: int = Field(
        default=0,
        description="Behavior when trajectory hits open bnd. If ibtrack_openbnd=0, slide with tangential vel; otherwise, stop and exit btrack (recommended?)",
    )
    ihhat: int = Field(
        default=1,
        description="Wetting and drying. If ihhat=1, \hat{H} is made non-negative to enhance robustness near wetting and drying; if ihhat=0, no retriction is imposed for this quantity.",
    )
    inunfl: int = Field(
        default=0,
        description="Wetting and drying. inunfl=0 is used for normal cases and inunfl=1 is used for more accurate wetting and drying if grid resolution is sufficiently fine.",
    )
    h0: float = Field(
        default=0.01,
        description="Min. water depth for wetting/drying [m]",
    )
    shorewafo: int = Field(
        default=1,
        description="If shorewafo=1, we impose radiation stress R_s = g*grad(eta) (balance between radiation stress gradients and the barotropic gradients) at the numerical shoreline (boundary between dry and wet elements). This option ensures that the shallow depth in dry elements does not create unphysical and very high wave forces at the shoreline (advised for morphodynamics runs).",
    )
    moitn0: int = Field(
        default=50,
        description="Output spool for solver info; used only with JCG",
    )
    mxitn0: int = Field(
        default=1500,
        description="Max. iteration allowed",
    )
    rtol0: float = Field(
        default=1e-12,
        description="Error tolerance",
    )
    nadv: int = Field(
        default=2,
        description="Advection (ELM) option. If nadv=1, backtracking is done using Euler method; nadv=2, using 2nd order Runge-Kutta; if nadv=0, advection in momentum is turned off/on in adv.gr3 (the depths=0,1, or 2 also control methods in backtracking as above).",
    )
    dtb_max: float = Field(
        default=30.0,
        description="Max. step allowed in advection (ELM) - actual step is calculated adaptively based on local gradient.",
    )
    dtb_min: float = Field(
        default=10.0,
        description="Min. step allowed in advection (ELM) - actual step is calculated adaptively based on local gradient.",
    )
    inter_mom: int = Field(
        0,
        description="If inter_mom=0, linear interpolation is used for velocity at foot of char. line. If inter_mom=1 or -1, Kriging is used, and the choice of covariance function is specified in 'kr_co'. If inter_mom=1, Kriging is applied to whole domain; if inter_mom=-1, the regions where Kriging is used is specified in krvel.gr3 (depth=0: no kriging; depth=1: with kriging).",
    )
    kr_co: int = Field(1, description="Not used if inter_mom=0")
    itr_met: int = Field(
        3,
        description="Transport method. If itr_met=1, upwind method is used. If itr_met>=2, TVD or WENO method is used on an element/prism if the total depth (at all nodes of the elem.)>=h_tvd and the flag in tvd.prop = 1 for the elem. (tvd.prop is required in this case); otherwise upwind is used for efficiency. itr_met=3 (horizontal TVD) or 4 (horizontal WENO): implicit TVD in the vertical dimension. Also if itr_met==3 and h_tvd>=1.e5, some parts of the code are bypassed for efficiency. Controls for WENO are not yet in place.",
    )
    h_tvd: float = Field(5.0, description="Used only if itr_met>=2; cut-off depth (m)")
    eps1_tvd_imp: float = Field(
        1.0e-4,
        description="Suggested value is 1.e-4, but for large suspended load, need to use a smaller value (e.g. 1.e-9)",
    )
    eps2_tvd_imp: float = Field(1.0e-14, description="")
    ielm_transport: int = Field(
        0,
        description="Option for writing nonfatal errors on invalid temp. or salinity for density: (0) off; (1) on.",
    )
    max_subcyc: int = Field(
        10,
        description="Used only if ielm_transport/=0. Max # of subcycling per time step in transport allowed",
    )
    ip_weno: int = Field(
        2,
        description="Order of accuracy: 0- upwind; 1- linear polynomial, 2nd order; 2- quadratic polynomial, 3rd order",
    )
    courant_weno: float = Field(0.5, description="Courant number for weno transport")
    nquad: int = Field(
        2, description="Number of quad points on each side, nquad= 1 or 2"
    )
    ntd_weno: int = Field(
        1,
        description="Order of temporal discretization: (1) Euler (default); (3): 3rd-order Runge-Kutta (only for benchmarking)",
    )
    epsilon1: float = Field(
        1.0e-3, description="Coefficient for 2nd order weno smoother"
    )
    epsilon2: float = Field(
        1.0e-10,
        description="1st coefficient for 3rd order weno smoother (larger values are more prone to numerical dispersion, 1.e-10 should be fairly safe, recommended values: 1.e-8 ~ 1.e-6 (from the real applications so far)",
    )
    i_prtnftl_weno: int = Field(
        0,
        description="Option for writing nonfatal errors on invalid temp. or salinity for density: (0) off; (1) on.",
    )
    epsilon3: float = Field(
        1.0e-25,
        description="2nd coefficient for 3rd order weno smoother (inactive at the moment)",
    )
    ielad_weno: int = Field(
        0,
        description="Ielad, if ielad=1, use ELAD method to suppress dispersion (inactive at the moment)",
    )
    small_elad: float = Field(1.0e-4, description="Small (inactive at the moment)")
    nws: int = Field(
        2,
        description="Atmos. option. nws=3 is reserved for coupling with atmospheric model. If nws=0, no atmos. forcing is applied. If nws=1, atmos. variables are read in from wind.th. If nws=2, atmos. variables are read in from sflux_ files. If nws=4, ascii format is used for wind and atmos. pressure at each node (see source code). If nws>0, 'iwindoff' can be used to scale wind speed (with windfactor.gr3).",
    )
    wtiminc: int = Field(
        3600, description="Time step for atmos. forcing. Default: same as dt"
    )
    nrampwind: int = Field(1, description="Ramp-up option for atmos. forcing")
    drampwind: float = Field(
        1.0, description="Needed if nrampwind/=0; ramp-up period in days"
    )
    iwind_form: int = Field(
        1,
        description="Needed if nws/=0   !usually use -1, trialling -2 to see if makes a difference",
    )
    impose_net_flux: int = Field(
        0,
        description="If impose_net_flux/=0 and nws=2, read in net _surface_ heat flux as var 'dlwrf' (Downward Long Wave) in sflux_rad (solar radiation is still used separately), and if PREC_EVAP is on, also read in net P-E as 'prate' (Surface Precipitation Rate) in sflux_prc.",
    )
    ihconsv: int = Field(0, description="Heat exchange option")
    isconsv: int = Field(0, description="Evaporation/precipitation model")
    itur: int = Field(3, description="Turbulence closure")
    dfv0: float = Field(1.0e-6, description="Needed if itur=0")
    dfh0: float = Field(1.0e-6, description="Needed if itur=0")
    mid: str = Field("KL", description="Needed if itur=3,5. Use KE if itur=5")
    stab: str = Field(
        "KC",
        description="Needed if itur=3 or 5. Use 'GA' if turb_met='MY'; otherwise use 'KC'.",
    )
    xlsc0: float = Field(
        0.7,
        description="Needed if itur=3 or 5. Scale for surface & bottom mixing length (>0); default was 0.1",
    )
    inu_elev: int = Field(
        0,
        description="Sponge layer for elevation and vel. If inu_elev=0, no relaxation is applied to elev. If inu_elev=1, relax. constants are specified in elev_nudge.gr3 and applied to eta=0 (thus a depth=0 means no relaxation).",
    )
    inu_uv: int = Field(0, description="Similarly for inu_uv (with input uv_nudge.gr3)")
    inu_tr: list = Field(
        default=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        description="Nudging options for tracers",
    )
    vnh1: float = Field(default=400, description="vertical nudging depth 1")
    vnf1: float = Field(default=0.0, description="vertical relax \in [0,1]")
    vnh2: float = Field(
        default=500, description="vertical nudging depth 2 (must >vnh1)"
    )
    vnf2: float = Field(default=0.0, description="vertical relax")
    step_nu_tr: float = Field(
        default=86400.0,
        description="time step [sec] in all [MOD]_nu.nc (for inu_[MOD]=2)",
    )
    h_bcc1: float = Field(
        default=100.0,
        description="Cut-off depth for cubic spline interpolation near bottom when computing horizontal gradients",
    )
    s1_mxnbt: float = Field(
        default=0.5, description="Dimensioning parameters for inter-subdomain btrack"
    )
    s2_mxnbt: float = Field(
        default=3.0, description="Dimensioning parameters for inter-subdomain btrack"
    )
    iharind: int = Field(
        default=0, description="Flag for harmonic analysis for elevation"
    )
    iflux: int = Field(default=0, description="Conservation check option")
    izonal5: int = Field(
        default=0, description="Williamson test #5 (zonal flow over an isolated mount)"
    )
    ibtrack_test: int = Field(
        default=0, description="Rotating Gausshill test with stratified T,S"
    )
    irouse_test: int = Field(default=0, description="Rouse profile test")
    flag_fib: int = Field(
        default=1, description="Flag to choose FIB model for bacteria decay"
    )
    slr_rate: float = Field(
        default=120.0, description="Marsh model parameters (only if USE_MARSH is on)"
    )
    isav: int = Field(0, description="on/off flag")
    sav_cd: float = Field(1.13, description="only needed if isav=1. Drag coefficient")
    nstep_ice: int = Field(
        1, description="call ice module every nstep_ice steps of SCHISM"
    )
    level_age: int = Field(-999, description="default: -999 (all levels)")
    rearth_pole: float = Field(6378206.4, description="Earth's radii at pole")
    rearth_eq: float = Field(6378206.4, description="Earth's radii at equator")
    shw: float = Field(4184.0, description="Specific heat of water (C_p) in J/kg/K")
    rho0: float = Field(
        1000.0, description="Reference water density for Boussinesq approximation"
    )
    vclose_surf_frac: float = Field(
        1.0,
        description="Fraction of vertical flux closure adjustment applied at surface",
    )
    iadjust_mass_consv0: list = Field(
        [0] * 12,
        description="Option to enforce strict mass conservation for each tracer model",
    )


class SCHOUT(RompyBaseModel):
    nhot: int = Field(
        0,
        description="use 1 to write out hotstart: output *_hotstart every 'hotout_write' steps",
    )
    nhot_write: float = Field(
        22320.0, description="must be a multiple of ihfskip if nhot=1"
    )
    iout_sta: int = Field(0, description="Station output option")
    nspool_sta: int = Field(
        30, description="needed if iout_sta/=0; mod(nhot_write,nspool_sta) must=0"
    )
    iof_hydro: list = Field(
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
        ],
        description="Global output options",
    )


class PARAM(RompyBaseModel):
    core: CORE = Field(description="CORE")
    opt: OPT = Field(description="OPT")
    schout: SCHOUT = Field(description="SCHOUT")
