# create pydantic model from the following using the Fields notation with defaults as provided here and descriptions taken from the comments
from pydantic import Field

from rompy.core.types import RompyBaseModel


class MARCO(RompyBaseModel):
    """
    Number of subcycles in ICM kinetics
    """

    nsub: int = Field(1, description="Number of subcycles in ICM kinetics")
    iKe: int = Field(
        0,
        description="Options of formulations for computing light attenuation coefficients",
    )
    Ke0: float = Field(
        0.26, description="Background light extinction coefficient (1/m)"
    )
    KeC: float = Field(0.017, description="Light attenuation due to chlorophyll")
    KeS: float = Field(0.07, description="Light attenuation due to TSS")
    KeSalt: float = Field(
        -0.02, description="Light attenuation due to CDOM (related to salinity)"
    )
    tss2c: float = Field(6.0, description="TSS to carbon ratio")
    iLight: int = Field(0, description="Options of computing light limitation factor")
    alpha: list[float] = Field(
        [8.0, 8.0, 8.0],
        description="Initial slope of P-I curve (g[C]*m2/g[Chl]/E), (iLight=0)",
    )
    iPR: int = Field(1, description="Options of phytoplankton' predation term")
    PRR: list[float] = Field(
        [0.1, 0.2, 0.05],
        description="Predation rate by higher trophic level (day-1, or day-1.g-1.m3)",
    )
    wqc0: list[float] = Field(
        [
            1.0,
            0.5,
            0.05,
            1.0,
            0.5,
            0.5,
            0.15,
            0.15,
            0.05,
            0.01,
            0.05,
            0.005,
            0.005,
            0.01,
            0.05,
            0.0,
            12.0,
        ],
        description="ICM init. value (wqc0), settling velocity (WSP), net settling velocity (WSPn) (m.day-1)",
    )
    WSP: list[float] = Field(
        [
            0.3,
            0.10,
            0.0,
            0.25,
            0.25,
            0.0,
            0.25,
            0.25,
            0.0,
            0.0,
            0.0,
            0.25,
            0.25,
            0.0,
            1.0,
            0.0,
            0.0,
        ],
        description="ICM init. value (wqc0), settling velocity (WSP), net settling velocity (WSPn) (m.day-1)",
    )
    WSPn: list[float] = Field(
        [
            0.3,
            0.10,
            0.0,
            0.25,
            0.25,
            0.0,
            0.25,
            0.25,
            0.0,
            0.0,
            0.0,
            0.25,
            0.25,
            0.0,
            1.0,
            0.0,
            0.0,
        ],
        description="ICM init. value (wqc0), settling velocity (WSP), net settling velocity (WSPn) (m.day-1)",
    )
    iSilica: int = Field(0, description="Silica model (0: OFF; 1: ON)")
    iZB: int = Field(
        0, description="Zooplankton (iZB=1: use zooplankton dynamics; iZB=0: don't use)"
    )
    iPh: int = Field(0, description="PH model (0: OFF; 1: ON)")
    iCBP: int = Field(0, description="ChesBay Program Model (0: OFF; 1: ON)")
    isav_icm: int = Field(0, description="Submerged Aquatic Vegetation switch")
    iveg_icm: int = Field(0, description="Intertidal vegetation switch")
    iSed: int = Field(
        1, description="Sediment module switch. iSed=1: Use sediment flux model"
    )
    iBA: int = Field(0, description="Benthic Algae")
    iRad: int = Field(0, description="Solar radiation")
    isflux: int = Field(0, description="Atmospheric fluxes")
    ibflux: int = Field(0, description="Bottom fluxes")
    iout_icm: int = Field(0, description="ICM station outputs")
    nspool_icm: int = Field(24, description="ICM station outputs")
    iLimit: int = Field(
        0, description="Options of nutrient limitation on phytoplankton growth"
    )
    idry_icm: int = Field(
        0,
        description="idry_icm=1: turn on shallow kinetic biochemical process; idry_icm=0: jump dry elems, keep last wet value; jump won't happen if iveg_icm is turn on and this elem is veg",
    )


#


class CORE(RompyBaseModel):
    """
    ICM parameters for water column; PB: phytoplankton
    CBP module parameters are included: (SRPOC,SRPON,SRPOP,PIP)
    """

    GPM: list[float] = Field([2.5, 2.8, 3.5], description="PB growth rates (day-1)")
    TGP: list[float] = Field(
        [15.0, 22.0, 27.0], description="optimal temp. for PB growth (oC)"
    )
    KTGP: list[float] = Field(
        [0.005, 0.004, 0.003, 0.008, 0.006, 0.004],
        description="temp. dependence for PB growth; dim(PB=1:3,1:2) (oC-2)",
    )
    MTR: list[float] = Field(
        [0.0, 0.0, 0.0], description="PB photorespiration coefficient (0<MTR<1)"
    )
    MTB: list[float] = Field(
        [0.01, 0.02, 0.03], description="PB metabolism rates (day-1)"
    )
    TMT: list[float] = Field(
        [20.0, 20.0, 20.0], description="reference temp. for PB metabolism (oC)"
    )
    KTMT: list[float] = Field(
        [0.0322, 0.0322, 0.0322],
        description="temp. dependence for PB metabolism (oC-1)",
    )
    FCP: list[float] = Field(
        [0.35, 0.30, 0.20, 0.55, 0.50, 0.50, 0.10, 0.20, 0.30, 0.0, 0.0, 0.0],
        description="fractions of PB carbon into (RPOC,LPOC,DOC,SRPOC); dim(PB=1:3,3)",
    )
    FNP: list[float] = Field(
        [
            0.35,
            0.35,
            0.35,
            0.50,
            0.50,
            0.50,
            0.10,
            0.10,
            0.10,
            0.05,
            0.05,
            0.05,
            0.0,
            0.0,
            0.0,
        ],
        description="fractions of PB nitrogen into (RPON,LPON,DON,NH4,SRPON)",
    )
    FPP: list[float] = Field(
        [
            0.10,
            0.10,
            0.10,
            0.20,
            0.20,
            0.20,
            0.50,
            0.50,
            0.50,
            0.20,
            0.20,
            0.20,
            0.0,
            0.0,
            0.0,
        ],
        description="fractions of PB Phosphorus into (RPOP,LPOP,DOP,PO4,SRPOP)",
    )
    FCM: list[float] = Field(
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.1, 0.1, 0.0, 0.0, 0.0],
        description="fractions of PB metabolism carbon into (RPOC,LPOC,DOC,SRPOC); dim(PB=1:3,4)",
    )
    FNM: list[float] = Field(
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        description="fractions of PB metabolism N. into (RPON,LPON,DON,NH4,SRPON); dim(PB=1:3,5)",
    )
    FPM: list[float] = Field(
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        description="fractions of PB metabolism P. into (RPOP,LPOP,DOP,PO4,SRPOP); dim(PB=1:3,5)",
    )
    Nit: float = Field(0.07, description="maximum nitrification rate (day-1)")
    TNit: float = Field(27.0, description="optimal temp. for nitrification (oC)")
    KTNit: list[float] = Field(
        [0.0045, 0.0045],
        description="temp. dependence (T<=TNit & T>TNit) for nitrification (oC-2)",
    )
    KhDOn: float = Field(1.0, description="DO half saturation for nitrification (mg/L)")
    KhDOox: float = Field(
        0.5,
        description="DO half saturation for dentrification & DOC's oxic respiration (mg/L)",
    )
    KhNO3dn: float = Field(
        0.1, description="NO3 half saturation for denitrification (mg/L)"
    )
    KC0: list[float] = Field(
        [0.005, 0.075, 0.2], description="minimum decay rate of RPOC,LPOC,DOC (day-1)"
    )
    KN0: list[float] = Field(
        [0.005, 0.075, 0.2], description="minimum decay rate of RPON,LPON,DON (day-1)"
    )
    KP0: list[float] = Field(
        [0.005, 0.075, 0.2], description="minimum decay rate of RPOP,LPOP,DOP (day-1)"
    )
    KCalg: list[float] = Field(
        [0.0, 0.0, 0.0],
        description="algae effect on RPOC,LPOC,DOC decay (day-1.m3.g[C]-1)",
    )
    KNalg: list[float] = Field(
        [0.0, 0.0, 0.0],
        description="algae effect on RPON,LPON,DON decay (day-1.m3.g[C]-1)",
    )
    KPalg: list[float] = Field(
        [0.0, 0.0, 0.0],
        description="algae effect on RPOP,LPOP,DOP decay (day-1.m3.g[C]-1)",
    )
    TRM: list[float] = Field(
        [20.0, 20.0, 20.0], description="reference temp. for (RPOM,LPOM,DOM) decay (oC)"
    )
    KTRM: list[float] = Field(
        [0.069, 0.069, 0.069],
        description="temp. dependence for (RPOM,LPOM,DOM) decay (oC-1)",
    )
    KSR0: list[float] = Field(
        [0.001, 0.001, 0.001], description="decay rates of SRPOC,SRPON,SRPOP (day-1)"
    )
    TRSR: list[float] = Field(
        [20.0, 20.0, 20.0],
        description="reference temp. for (SRPOC,SRPON,SRPOP) decay (oC)",
    )
    KTRSR: list[float] = Field(
        [0.069, 0.069, 0.069],
        description="temp. dependence for (SRPOC,SRPON,SRPOP) decay (oC-1)",
    )
    KPIP: float = Field(0.0, description="dissolution rate of PIP (day-1)")
    KCD: float = Field(1.0, description="oxidation rate of COD at TRCOD (day-1)")
    TRCOD: float = Field(20.0, description="reference temp. for COD oxidation (oC)")
    KTRCOD: float = Field(
        0.041, description="temp. dependence for COD oxidation (oC-1)"
    )
    KhCOD: float = Field(
        1.5, description="COD half saturation for COD oxidation (mg[O2]/L)"
    )
    KhN: list[float] = Field(
        [0.01, 0.01, 0.01], description="nitrogen half saturation (mg/L)"
    )
    KhP: list[float] = Field([0.001, 0.001, 0.001], description="ph")


class SFM(RompyBaseModel):
    """
    Sediment flux model (SFM) parameter
    """

    btemp0: float = Field(5.0, description="Initial temperature (oC)")
    bstc0: float = Field(0.1, description="Surface transfer coefficient")
    bSTR0: float = Field(0.0, description="Benthic stress (day)")
    bThp0: float = Field(0.0, description="Consecutive days of hypoxia (day)")
    bTox0: float = Field(
        0.0, description="Consecutive days of oxic condition after hypoxia event (day)"
    )
    bNH40: float = Field(4.0, description="NH4")
    bNO30: float = Field(1.0, description="NO3")
    bPO40: float = Field(5.0, description="PO4")
    bH2S0: float = Field(250.0, description="H2S")
    bCH40: float = Field(40.0, description="CH4")
    bPOS0: float = Field(500.0, description="POS")
    bSA0: float = Field(500.0, description="SA")
    bPOC0: list[float] = Field([1000.0, 3000.0, 5000.0], description="POC (G=1:3)")
    bPON0: list[float] = Field([150.0, 500.0, 1500.0], description="PON (G=1:3)")
    bPOP0: list[float] = Field([30.0, 300.0, 500.0], description="POP (G=1:3)")
    bdz: float = Field(0.1, description="Sediment thickness (m)")
    bVb: float = Field(
        1.37e-5, description="Burial rate (m.day-1); 1 cm/yr=2.74e-5 m.day-1"
    )
    bsolid: list[float] = Field(
        [0.5, 0.5], description="Sediment solid conc. in Layer 1 and Layer 2 (Kg.L-1)"
    )
    bdiff: float = Field(
        1.8e-7, description="Diffusion coefficient for sediment temp. (m2/s)"
    )
    bTR: int = Field(20, description="Reference temp. for sediment processes")
    bVpmin: float = Field(
        3.0e-6, description="Minimum particle mixing velocity coefficient (m.day-1)"
    )
    bVp: float = Field(
        1.2e-4, description="Particle mixing velocity coefficient (m.day-1)"
    )
    bVd: float = Field(1.0e-3, description="Diffusion velocity coefficient (m.day-1)")
    bKTVp: float = Field(
        1.117, description="Temp. dependence of particle mixing velocity"
    )
    bKTVd: float = Field(1.08, description="Temp. dependence of diffusion velocity")
    bKST: float = Field(
        0.03, description="1st order decay rate of benthic stress (day-1)"
    )
    bSTmax: float = Field(
        20.0,
        description="Maximum value of benthic stress (day) (note: smaller than 1/bKST)",
    )
    bKhDO_Vp: float = Field(
        4.0, description="DO half-saturation of particle mixing (mg/L)"
    )
    bDOc_ST: float = Field(1.0, description="DO criteria for benthic stress (mg/L)")
    banoxic: float = Field(
        10.0,
        description="Consecutive days of hypoxia causing maximum benthic stress (day)",
    )
    boxic: float = Field(
        45.0, description="Time lag for bethos recovery from hypoxia event (day)"
    )
    bp2d: float = Field(
        0.0,
        description="Ratio from mixing coef. to diffusion coef. (benthos enhanced effect)",
    )
    bKC: list[float] = Field(
        [0.035, 0.0018, 0.00], description="Decay rate of POC (3G class) at bTR (day-1)"
    )
    bKN: list[float] = Field(
        [0.035, 0.0018, 0.00], description="Decay rate of PON (3G class) at bTR (day-1)"
    )
    bKP: list[float] = Field(
        [0.035, 0.0018, 0.00], description="Decay rate of POP (3G class) at bTR (day-1)"
    )
    bKTC: list[float] = Field(
        [1.10, 1.150, 1.17], description="Temp. dependence of POC decay (oC-1)"
    )
    bKTN: list[float] = Field(
        [1.10, 1.150, 1.17], description="Temp. dependence of PON decay (oC-1)"
    )
    bKTP: list[float] = Field(
        [1.10, 1.150, 1.17], description="Temp. dependence of POP decay (oC-1)"
    )
    bFCP: list[float] = Field(
        [0.35, 0.55, 0.01, 0.35, 0.55, 0.01, 0.35],
        description="fractions of benthic carbon into (RPOC,LPOC,DOC,SRPOC); dim(G=1:3,4)",
    )


class Silica(RompyBaseModel):
    FSP: list[float] = Field(
        [0.90, 0.10], description="Fractions of diatom silica into (SU,SA)"
    )
    FSM: list[float] = Field(
        [0.50, 0.50], description="Fractions of diatom metabolism Si into (SU,SA)"
    )
    KS: float = Field(0.03, description="Dissolution rate of SU at TRS (day-1)")
    TRS: float = Field(20.0, description="Reference temp. for SU dissolution (oC)")
    KTRS: float = Field(0.092, description="Temp. dependence for SU dissolution (oC-1)")
    KhS: list[float] = Field(
        [0.05, 0.0, 0.0],
        description="Silica half saturation (mg/L); (0.0: no Si limitation)",
    )
    s2c: list[float] = Field(
        [0.50, 0.0, 0.0],
        description="Silica to carbon ratio for phytolankton; (0.0: no Si uptake)",
    )
    KSAp: float = Field(
        0.0, description="Coefficient relating Silicate(SA) sorption to TSS"
    )


class ZB(RompyBaseModel):
    """
    Zooplankton (ZB) parameters
    ZB prey(1:8)=(ZB1,ZB2,PB1,PB2,PB3,RPOC,LPOC,DOC)
    """

    zGPM: list[float] = Field(
        [
            0.0,
            0.0,
            1.75,
            1.75,
            1.75,
            1.75,
            1.75,
            1.75,
            1.0,
            0.0,
            2.0,
            2.0,
            2.0,
            2.0,
            2.0,
            2.0,
        ],
        description="ZB predation rate (day-1); dim(prey=1:8, ZB=1:2)",
    )
    zKhG: list[float] = Field(
        [
            0.175,
            0.175,
            0.175,
            0.175,
            0.175,
            0.175,
            0.175,
            0.175,
            0.175,
            0.175,
            0.175,
            0.175,
            0.175,
            0.175,
            0.175,
            0.175,
        ],
        description="reference prey conc. (mg/L); dim(prey=1:8, ZB=1:2)",
    )
    zTGP: list[float] = Field(
        [25.0, 25.0], description="optimal temp. for ZB growth (oC)"
    )
    zKTGP: list[float] = Field(
        [0.0035, 0.008, 0.025, 0.030],
        description="temp. dependence for ZB growth (T<=zTGP & T>zTGP); dim(ZB=1:2,1:2) (oC-2)",
    )
    zAG: float = Field(0.75, description="ZB assimilation efficiency ratio (0-1)")
    zRG: float = Field(0.1, description="ZB respiration ratio when it grazes (0-1)")
    zMRT: list[float] = Field([0.02, 0.02], description="ZB mortality rates (day-1)")
    zMTB: list[float] = Field([0.254, 0.186], description="ZB metabolism rates (day-1)")
    zTMT: list[float] = Field(
        [20.0, 20.0], description="reference temp. for ZB metabolism (oC)"
    )
    zKTMT: list[float] = Field(
        [0.0693, 0.0693], description="temp. dependence for ZB metabolism (oC-1)"
    )
    zFCP: list[float] = Field(
        [0.35, 0.55, 0.10], description="fractions of ZB carbon into (RPOC,LPOC,DOC)"
    )
    zFNP: list[float] = Field(
        [0.35, 0.50, 0.10, 0.05],
        description="fractions of ZB nitrogen into (RPON,LPON,DON,NH4)",
    )
    zFPP: list[float] = Field(
        [0.10, 0.20, 0.50, 0.20],
        description="fractions of ZB Phosphorus into (RPOP,LPOP,DOP,PO4)",
    )
    zFSP: list[float] = Field(
        [0.70, 0.25], description="fractions of ZB silica into (SU,SA)"
    )
    zFCM: list[float] = Field(
        [0.10, 0.0],
        description="fractions of ZB metabolism carbon into DOC; dim(ZB=1:2)",
    )
    zFNM: list[float] = Field(
        [0.35, 0.30, 0.50, 0.40, 0.10, 0.20, 0.05, 0.10],
        description="fractions of ZB metabolism N. into (RPON,LPON,DON,NH4); dim(ZB=1:2,4)",
    )
    zFPM: list[float] = Field(
        [0.35, 0.30, 0.50, 0.40, 0.10, 0.20, 0.05, 0.10],
        description="fractions of ZB metabolism P. into (RPOP,LPOP,DOP,PO4); dim(ZB=1:2,4)",
    )
    zFSM: list[float] = Field(
        [0.50, 0.40, 0.50, 0.60],
        description="fractions of ZB metabolism Si into (SU,SA); dim(ZB=1:2,2)",
    )
    zKhDO: list[float] = Field(
        [0.5, 0.5], description="DO half saturation for ZB's DOC excretion (mg/L)"
    )
    zn2c: list[float] = Field(
        [0.20, 0.20], description="nitrogen to carbon ratio for zooplankton"
    )
    zp2c: list[float] = Field(
        [0.02, 0.02], description="phosphorus to carbon ratio for zooplankton"
    )
    zs2c: list[float] = Field(
        [0.50, 0.50], description="silica to carbon ratio for zooplankton"
    )
    z2pr: list[float] = Field(
        [0.5, 0.5],
        description="ratio converting ZB+PB biomass to predation rates on ZB (L.mg-1.day-1)",
    )
    p2pr: float = Field(
        0.25,
        description="ratio converting ZB+PB biomass to predation rates on PB (L.mg-1.day-1)",
    )


class PH_ICM(RompyBaseModel):
    """
    PH model parameter
    """

    ppatch0: int = Field(
        -999, description="Region flag for pH (1: ON all elem.; -999: spatial)"
    )
    pKCACO3: float = Field(60.0, description="Dissolution between CaCO3 and Ca++")
    pKCA: float = Field(
        60.0, description="Sediment surface transfer coefficient from CaCO3 to Ca++"
    )
    pRea: float = Field(1.0, description="Reaeration rate for CO2")
    inu_ph: int = Field(0, description="Nudge option for pH model")


class SAV(RompyBaseModel):
    """
    Submerged Aquatic Vegetation (SAV) parameters
    """

    spatch0: int = Field(
        -999, description="Region flag for SAV. (1: ON all elem.; -999: spatial)"
    )
    stleaf0: int = Field(-999, description="Initial concentration of total SAV leaf")
    ststem0: int = Field(-999, description="Initial concentration of total SAV stem")
    stroot0: int = Field(-999, description="Initial concentration of total SAV root")
    sGPM: float = Field(0.1, description="Maximum growth rate (day-1)")
    sTGP: int = Field(32, description="Optimal growth temperature (oC)")
    sKTGP: str = Field(
        "0.003  0.005",
        description="Temperature dependence for growth (T<=sTGP & T>sTGP)",
    )
    sFAM: float = Field(
        0.2, description="Fraction of leaf production to active metabolism"
    )
    sFCP: str = Field(
        "0.6    0.3    0.1",
        description="Fractions of production to leaf/stem/root biomass",
    )
    sMTB: str = Field(
        "0.02   0.02   0.02", description="Metabolism rates of leaf/stem/root"
    )
    sTMT: str = Field(
        "20     20     20", description="Reference temp. for leaf/stem/root metabolism"
    )
    sKTMT: str = Field(
        "0.069  0.069  0.069",
        description="Temperature dependence of leaf/stem/root metabolism",
    )
    sFCM: str = Field(
        "0.05   0.15   0.3   0.5",
        description="Fractions of metabolism C into (RPOC,LPOC,DOC,CO2)",
    )
    sFNM: str = Field(
        "0.05   0.15   0.3   0.5",
        description="Fractions of metabolism N into (RPON,LPON,DON,NH4)",
    )
    sFPM: str = Field(
        "0.05   0.1    0.35  0.5",
        description="Fractions of metabolism P into (RPOP,LPOP,DOP,PO4)",
    )
    sKhNw: float = Field(0.01, description="Nitrogen half saturation in water column")
    sKhNs: float = Field(0.1, description="Nitrogen half saturation in sediments")
    sKhNH4: float = Field(0.1, description="Ammonium half saturation")
    sKhPw: float = Field(
        0.001, description="Phosphorus half saturation in water column"
    )
    sKhPs: float = Field(0.01, description="Phosphorus half saturation in sediments")
    salpha: float = Field(
        0.006, description="Initial slope of P-I curve (g[C]*m2/g[Chl]/E)"
    )
    sKe: float = Field(0.045, description="Light attenuation due to SAV absorption")
    shtm: str = Field(
        "0.054  2.0", description="Minimum (base) and maximum canopy height"
    )
    s2ht: str = Field(
        "0.0036 0.0036 0.0",
        description="Coefficients converting (leaf,stem,root) to canopy height",
    )
    sc2dw: float = Field(0.38, description="Carbon to dry weight ratio of SAV")
    s2den: int = Field(
        10, description="Coefficient computing SAV density from leaf&stem"
    )
    sn2c: float = Field(0.09, description="Nitrogen to carbon ratio of SAV")
    sp2c: float = Field(0.01, description="Phosphorus to carbon ratio")
    so2c: float = Field(2.67, description="Oxygen to carbon ratio")


# &VEG
# !-----------------------------------------------------------------------
# !Intertidal Vegetation (VEG), paramters
# !-----------------------------------------------------------------------


class VEG(RompyBaseModel):
    """
    Intertidal Vegetation (VEG), paramters
    """

    vpatch0: int = Field(
        -999, description="Region flag for VEG. (1: ON all elem.; -999: spatial)"
    )
    vtleaf0: list[float] = Field(
        [100.0, 100.0, 100.0], description="Init conc to total veg leaf"
    )
    vtstem0: list[float] = Field(
        [100.0, 100.0, 100.0], description="Init conc to total veg stem"
    )
    vtroot0: list[float] = Field(
        [30.0, 30.0, 30.0], description="Init conc to total veg root"
    )
    vGPM: list[float] = Field(
        [0.1, 0.1, 0.1], description="Maximum growth rate (day-1)"
    )
    vFAM: list[float] = Field(
        [0.2, 0.2, 0.2], description="Fractions of leaf production to active metabolism"
    )
    vTGP: list[float] = Field(
        [32.0, 32.0, 32.0], description="Optimal growth temperature (oC)"
    )
    vKTGP: list[float] = Field(
        [0.003, 0.003, 0.003, 0.005, 0.005, 0.005],
        description="Temp. dependence(3,2) for growth (T<=vTGP & T>vTGP)",
    )
    vFCP: list[float] = Field(
        [0.6, 0.6, 0.6, 0.3, 0.3, 0.3, 0.1, 0.1, 0.1],
        description="Fractions of production to leaf/stem/root biomass; dim(veg,leaf/stem/root)",
    )
    vMTB: list[float] = Field(
        [0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.01, 0.01, 0.01],
        description="Metabolism rates of leaf/stem/root; dim(veg,leaf/stem/root)",
    )
    vTMT: list[float] = Field(
        [20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0],
        description="Reference temp. for leaf/stem/root metabolism",
    )
    vKTMT: list[float] = Field(
        [0.069, 0.069, 0.069, 0.069, 0.069, 0.069, 0.069, 0.069, 0.069],
        description="Temp. dependence for leaf/stem/root metabolism",
    )
    vFNM: list[float] = Field(
        [0.05, 0.05, 0.05, 0.15, 0.15, 0.15, 0.3, 0.3, 0.3, 0.5, 0.5, 0.5],
        description="Fractions(3,4) of metabolism N into (RPON,LPON,DON,NH4)",
    )
    vFPM: list[float] = Field(
        [0.05, 0.05, 0.05, 0.1, 0.1, 0.1, 0.35, 0.35, 0.35, 0.5, 0.5, 0.5],
        description="Fractions(3,4) of metabolism P into (RPOP,LPOP,DOP,PO4)",
    )
    vFCM: list[float] = Field(
        [0.05, 0.05, 0.05, 0.15, 0.15, 0.15, 0.3, 0.3, 0.3, 0.5, 0.5, 0.5],
        description="Fractions(3,4) of metabolism N into (RPOC,LPOC,DOC,CO2)",
    )
    ivNc: int = Field(1, description="Recycled veg N goes to (0: sediment; 1: water)")
    ivPc: int = Field(1, description="Recycled veg P goes to (0: sediment; 1: water)")
    vKhNs: list[float] = Field(
        [0.1, 0.1, 0.1], description="Nitrogen half saturation in sediments"
    )
    vKhPs: list[float] = Field(
        [0.01, 0.01, 0.01], description="Phosphorus half saturation in sediments"
    )
    vScr: float = Field(35.0, description="Reference sality for computing veg growth")
    vSopt: list[float] = Field(
        [35.0, 15.0, 0.0], description="Optimal salinity for veg growth"
    )
    vInun: list[float] = Field(
        [1.0, 1.0, 1.0],
        description="Reference value for inundation stress (nondimensional)",
    )
    ivNs: int = Field(1, description="N limitation on veg growth(0: OFF; 1: ON)")
    ivPs: int = Field(1, description="P limitation on veg growth(0: OFF; 1: ON)")
    ivMRT: int = Field(0, description="Veg mortality term (0: OFF;  1: ON)")
    vTMR: list[float] = Field(
        [17.0, 17.0, 17.0, 17.0, 17.0, 17.0],
        description="Reference temp(3,2) for leaf/stem mortality",
    )
    vKTMR: list[float] = Field(
        [4.0, 4.0, 4.0, 4.0, 4.0, 4.0],
        description="Temp dependence(3,2) for leaf/stem mortality",
    )
    vMR0: list[float] = Field(
        [12.8, 12.8, 12.8, 12.8, 12.8, 12.8],
        description="Base value(3,2) of temp effect on mortality (unit: None)",
    )
    vMRcr: list[float] = Field(
        [15.0, 15.0, 15.0, 15.0, 15.0, 15.0],
        description="Reference value(3,2) for computing mortality (unit: None)",
    )
    valpha: list[float] = Field(
        [0.006, 0.006, 0.006], description="Init. slope of P-I curve"
    )
    vKe: list[float] = Field(
        [0.045, 0.045, 0.045], description="Light attenuation from veg absorption"
    )
    vht0: list[float] = Field(
        [0.054, 0.054, 0.054], description="Base veg canopy hgt (vht)"
    )
    vcrit: list[float] = Field(
        [250.0, 250.0, 250.0], description="Critical mass for computing vht"
    )
    v2ht: list[float] = Field(
        [0.0036, 0.0036, 0.0036, 0.001, 0.001, 0.001],
        description="Coefs. convert mass(3,2) to canopy height",
    )
    vc2dw: list[float] = Field(
        [0.38, 0.38, 0.38], description="Carbon to dry weight ratio of VEG"
    )
    v2den: list[int] = Field([10, 10, 10], description="Coeff. computing veg density")
    vp2c: list[float] = Field(
        [0.01, 0.01, 0.01], description="Phosphorus to carbon ratio"
    )
    vn2c: list[float] = Field(
        [0.09, 0.09, 0.09], description="Nitrogen to carbon ratio"
    )
    vo2c: list[float] = Field([2.67, 2.67, 2.67], description="Oxygen to carbon ratio")


class BAG(RompyBaseModel):
    """
    Benthic Algae
    """

    gpatch0: int = Field(
        -999, description="Region flag for BA. (1: ON all elem.; -999: spatial)"
    )
    BA0: float = Field(5.0, description="Initial BA concentration (g[C].m-2)")
    gGPM: float = Field(2.25, description="BA maximum growth rate (day-1)")
    gTGP: float = Field(20.0, description="Optimal temp. for BA growth (oC)")
    gKTGP: str = Field(
        "0.004  0.006", description="Temp. dependence for BA growth (oC-2)"
    )
    gMTB: float = Field(0.05, description="Respiration rate at temp. of gTR (day-1)")
    gPRR: float = Field(0.1, description="Predation rate at temp. of gTR (day-1)")
    gTR: float = Field(
        20.0, description="Reference temperature for BA respiration (oC)"
    )
    gKTR: float = Field(0.069, description="Temp. dependence for BA respiration (oC-1)")
    galpha: float = Field(0.1, description="Init. slope of P-I curve (m2/E)")
    gKSED: float = Field(0.0, description="Light attenuation due to sediment (None)")
    gKBA: float = Field(
        0.01, description="Light attenuation coef. due to BA self-shading (g[C]-1.m2)"
    )
    gKhN: float = Field(
        0.01, description="Nitrogen half saturation for BA growth (g[N]/m2)"
    )
    gKhP: float = Field(
        0.001, description="Phosphorus half saturation for BA growth (g[P]/2)"
    )
    gp2c: float = Field(0.0167, description="Phosphorus to carbon ratio")
    gn2c: float = Field(0.167, description="Nitrogen to carbon ratio")
    go2c: float = Field(2.67, description="Oxygen to carbon ratio")
    gFCP: str = Field(
        "0.5 0.45 0.05",
        description="Fraction of predation BA C into 3G classes in sediment",
    )
    gFNP: str = Field(
        "0.5 0.45 0.05",
        description="Fraction of predation BA N into 3G classes in sediment",
    )
    gFPP: str = Field(
        "0.5 0.45 0.05",
        description="Fraction of predation BA P into 3G classes in sediment",
    )


class ERO(RompyBaseModel):
    """
    Benthic erosion parameter
    """

    ierosion: int = Field(0, description="1: H2S flux; 2: POC flux; 3: H2S&POC flux")
    erosion: int = Field(864, description="erosion rate (kg.m-2.day)")
    etau: float = Field(1e-6, description="critical bottom shear stress (Pa)")
    eporo: float = Field(
        0.8, description="coefficient in erosion formula (see code in icm_sfm.F90)"
    )
    efrac: float = Field(
        0.5,
        description="fraction coefficient in erosion formula (see code in icm_sfm.F90)",
    )
    ediso: float = Field(
        2.5, description="H2S erosion coefficient (see code in icm_sfm.F90)"
    )
    dfrac: str = Field(
        "0.02 0.02",
        description="deposition fraction of POC (negative value: dfrac will be computed)",
    )
    dWS_POC: str = Field(
        "3.0 3.0", description="coefficient in POC erosion (see code in icm_sfm.F90)"
    )


class ICM(RompyBaseModel):
    marco: MARCO = Field(MARCO())
    sfm: SFM = Field(SFM())
    silica: Silica = Field(Silica())
    zb: ZB = Field(ZB())
    ph_icm: PH_ICM = Field(PH_ICM())
    sav: SAV = Field(SAV())
    bag: BAG = Field(BAG())
    ero: ERO = Field(ERO())
    veg: VEG = Field(VEG())
