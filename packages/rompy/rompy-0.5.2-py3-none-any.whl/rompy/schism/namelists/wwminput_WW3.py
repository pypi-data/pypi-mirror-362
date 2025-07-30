# This file was auto generated from a SCHISM namelist file on 2025-01-24.

from datetime import datetime
from typing import List, Optional

from pydantic import Field, field_validator, model_validator

from rompy.schism.namelists.basemodel import NamelistBaseModel


class Proc(NamelistBaseModel):
    procname: Optional[str] = Field(
        "Isabel", description="Project name for the simulation"
    )
    dimmode: Optional[int] = Field(
        2,
        description="Dimensionality of the simulation. Must be 2 when coupled with SCHISM",
    )
    lstea: Optional[bool] = Field(
        False, description="Flag for steady mode (under development)"
    )
    lqstea: Optional[bool] = Field(
        False,
        description="Flag for Quasi-Steady Mode. If True, WWM-II performs subiterations defined as DELTC/NQSITER unless QSCONVI is reached",
    )
    lsphe: Optional[bool] = Field(
        True, description="Flag for using spherical coordinates (longitude/latitude)"
    )
    lnautin: Optional[bool] = Field(
        True,
        description="Flag for using nautical convention for all input angles given in degrees",
    )
    lnautout: Optional[bool] = Field(
        True,
        description="Flag for using nautical convention for output angles. If True, 0 is from north, 90 is from east; if False, mathematical convention is used (0: to east, 90: to north)",
    )
    lmono_in: Optional[bool] = Field(
        False,
        description="Flag for prescribing monochromatic wave height (Hmono) as boundary conditions. Incident wave is defined as Hmono = sqrt(2) * Hs",
    )
    lmono_out: Optional[bool] = Field(
        False, description="Flag for outputting wave heights in terms of Lmono"
    )
    begtc: Optional[str] = Field(
        "20030908.000000",
        description="Start time of the simulation in format 'yyyymmdd.hhmmss'",
    )
    deltc: Optional[int] = Field(
        600, description="Time step in seconds. Must match dt*nstep_wwm in SCHISM"
    )
    unitc: Optional[str] = Field("SEC", description="Unit of time step")
    endtc: Optional[str] = Field(
        "20031008.000000",
        description="End time of the simulation in format 'yyyymmdd.hhmmss'",
    )
    dmin: Optional[float] = Field(
        0.01, description="Minimum water depth. Must be the same as h0 in SCHISM"
    )

    @field_validator("procname")
    @classmethod
    def validate_procname(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Project name cannot be empty")
        return v

    @field_validator("dimmode")
    @classmethod
    def validate_dimmode(cls, v: int) -> int:
        if v != 2:
            raise ValueError("DIMMODE must be 2 when coupled with SCHISM")
        return v

    @field_validator("lstea")
    @classmethod
    def validate_lstea(cls, v: bool) -> bool:
        return v

    @field_validator("lqstea")
    @classmethod
    def validate_lqstea(cls, v: bool) -> bool:
        return v

    @field_validator("lsphe")
    @classmethod
    def validate_lsphe(cls, v: bool) -> bool:
        return v

    @field_validator("lnautin")
    @classmethod
    def validate_lnautin(cls, v: bool) -> bool:
        return v

    @field_validator("lnautout")
    @classmethod
    def validate_lnautout(cls, v: bool) -> bool:
        return v

    @field_validator("lmono_in")
    @classmethod
    def validate_lmono_in(cls, v: bool) -> bool:
        return v

    @field_validator("lmono_out")
    @classmethod
    def validate_lmono_out(cls, v: bool) -> bool:
        return v

    @field_validator("begtc")
    @classmethod
    def validate_begtc(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y%m%d.%H%M%S")
        except ValueError:
            raise ValueError("Invalid date format for BEGTC")
        return v

    @field_validator("deltc")
    @classmethod
    def validate_deltc(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("DELTC must be positive")
        return v

    @field_validator("unitc")
    @classmethod
    def validate_unitc(cls, v: str) -> str:
        if v.upper() != "SEC":
            raise ValueError("UNITC must be SEC")
        return v.upper()

    @field_validator("endtc")
    @classmethod
    def validate_endtc(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y%m%d.%H%M%S")
        except ValueError:
            raise ValueError("Invalid date format for ENDTC")
        return v

    @field_validator("dmin")
    @classmethod
    def validate_dmin(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("DMIN must be positive")
        return v

    @model_validator(mode="after")
    def validate_simulation_time(self) -> "Model":
        start = datetime.strptime(self.begtc, "%Y%m%d.%H%M%S")
        end = datetime.strptime(self.endtc, "%Y%m%d.%H%M%S")
        if end <= start:
            raise ValueError("ENDTC must be later than BEGTC")
        return self


class Coupl(NamelistBaseModel):
    lcpl: Optional[bool] = Field(
        True,
        description="Main switch for coupling with current model. Keep it on for SCHISM-WWM coupling.",
    )
    radflag: Optional[str] = Field(
        "LON",
        description="Flag for radiation stress formulation. 'LON' for Longuet-Higgins formulation, 'VOR' for vortex formulation.",
    )
    letot: Optional[bool] = Field(
        False,
        description="Option to compute wave-induced radiation stress. If True, radiation stress is based on the integrated wave spectrum. If False, it's estimated based on the directional spectra itself as in Roland et al. (2008). False is generally preferred for more accurate results.",
    )
    nlvt: Optional[int] = Field(
        10, description="Number of vertical layers. Not used with SCHISM."
    )
    dtcoup: Optional[float] = Field(
        600.0,
        description="Coupling time step in seconds. Not used when coupled to SCHISM.",
    )

    @field_validator("lcpl")
    @classmethod
    def validate_lcpl(cls, v):
        if not isinstance(v, bool):
            raise ValueError("LCPL must be a boolean value")
        return v

    @field_validator("radflag")
    @classmethod
    def validate_radflag(cls, v):
        if v not in ["LON", "VOR"]:
            raise ValueError('RADFLAG must be either "LON" or "VOR"')
        return v

    @field_validator("letot")
    @classmethod
    def validate_letot(cls, v):
        if not isinstance(v, bool):
            raise ValueError("LETOT must be a boolean value")
        return v

    @field_validator("nlvt")
    @classmethod
    def validate_nlvt(cls, v):
        if not isinstance(v, int) or v <= 0:
            raise ValueError("NLVT must be a positive integer")
        return v

    @field_validator("dtcoup")
    @classmethod
    def validate_dtcoup(cls, v):
        if not isinstance(v, (int, float)) or v <= 0:
            raise ValueError("DTCOUP must be a positive number")
        return v


class Grid(NamelistBaseModel):
    lcird: Optional[bool] = Field(
        True, description="Flag to use full circle in directional space"
    )
    lstag: Optional[bool] = Field(
        False,
        description="Flag to stagger directional bins with a half Dtheta. Can only be True for regular grids to avoid characteristic line aligning with grid line",
    )
    mindir: Optional[float] = Field(
        0.0,
        description="Minimum direction for simulation in degrees (nautical convention; 0: from N; 90: from E). Not used if LCIRD is True",
    )
    maxdir: Optional[float] = Field(
        360.0,
        description="Maximum direction for simulation in degrees. May be less than MINDIR. Not used if LCIRD is True",
    )
    mdc: Optional[int] = Field(36, description="Number of directional bins")
    frlow: Optional[float] = Field(
        0.04,
        description="Low frequency limit of the discrete wave period in Hz (1/period)",
    )
    frhigh: Optional[float] = Field(
        1.0, description="High frequency limit of the discrete wave period in Hz"
    )
    msc: Optional[int] = Field(36, description="Number of frequency bins")
    filegrid: Optional[str] = Field(
        "hgrid_WWM.gr3",
        description="Name of the grid file. Should be 'hgridi_WWM.gr3' if IGRIDTYPE is 3 (SCHISM)",
    )
    igridtype: Optional[int] = Field(
        3,
        description="Grid type used. 1: XFN system.dat, 2: WWM-PERIODIC, 3: SCHISM, 4: old WWM type",
    )
    lslop: Optional[bool] = Field(
        False, description="Flag to use bottom slope limiter (default: False)"
    )
    slmax: Optional[float] = Field(
        0.2, description="Maximum slope when bottom slope limiter is used"
    )
    lvar1d: Optional[bool] = Field(
        False,
        description="Flag for 1D mode if variable dx is used. Not used with SCHISM",
    )
    loptsig: Optional[bool] = Field(
        False,
        description="Flag to use optimal distributions of frequencies in spectral space (fi+1 = fi * 1.1). Care should be taken with the high frequency limit",
    )

    @field_validator("lcird")
    @classmethod
    def validate_lcird(cls, v: bool) -> bool:
        return v

    @field_validator("lstag")
    @classmethod
    def validate_lstag(cls, v: bool) -> bool:
        return v

    @field_validator("mindir")
    @classmethod
    def validate_mindir(cls, v: float) -> float:
        if v < 0 or v >= 360:
            raise ValueError("MINDIR must be between 0 and 360")
        return v

    @field_validator("maxdir")
    @classmethod
    def validate_maxdir(cls, v: float) -> float:
        if v <= 0 or v > 360:
            raise ValueError("MAXDIR must be between 0 and 360")
        return v

    @field_validator("mdc")
    @classmethod
    def validate_mdc(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("MDC must be a positive integer")
        return v

    @field_validator("frlow")
    @classmethod
    def validate_frlow(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("FRLOW must be positive")
        return v

    @field_validator("frhigh")
    @classmethod
    def validate_frhigh(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("FRHIGH must be positive")
        return v

    @field_validator("msc")
    @classmethod
    def validate_msc(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("MSC must be a positive integer")
        return v

    @field_validator("filegrid")
    @classmethod
    def validate_filegrid(cls, v: str) -> str:
        if not v:
            raise ValueError("FILEGRID must not be empty")
        return v

    @field_validator("igridtype")
    @classmethod
    def validate_igridtype(cls, v: int) -> int:
        if v not in [1, 2, 3, 4]:
            raise ValueError("IGRIDTYPE must be 1, 2, 3, or 4")
        return v

    @field_validator("lslop")
    @classmethod
    def validate_lslop(cls, v: bool) -> bool:
        return v

    @field_validator("slmax")
    @classmethod
    def validate_slmax(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("SLMAX must be positive")
        return v

    @field_validator("lvar1d")
    @classmethod
    def validate_lvar1d(cls, v: bool) -> bool:
        return v

    @field_validator("loptsig")
    @classmethod
    def validate_loptsig(cls, v: bool) -> bool:
        return v


class Init(NamelistBaseModel):
    filehot_in: Optional[str] = Field(
        "hotfile_in_WWM.nc",
        description="Full path and filename for the input hot file, which can be copied from FILEHOT_OUT. Used for restarting simulations.",
    )
    hotstyle_in: Optional[int] = Field(
        2,
        description="Specifies the format of the input hot file. 1 for binary format, 2 for NetCDF format (default).",
    )
    ihotpos_in: Optional[int] = Field(
        1,
        description="Position in the hot file for reading data (only applicable for NetCDF files). If LCYCLEHOT=T, this can be 1 or 2 (out of the 2 time records). '1' is the most recent time.",
    )
    multiplein: Optional[int] = Field(
        0,
        description="Specifies whether to read the hot file from a single file (0) or multiple files (1). Multiple files might require the same number of CPUs.",
    )

    @field_validator("filehot_in")
    @classmethod
    def validate_filehot_in(cls, v: str) -> str:
        if not v.endswith(".nc"):
            raise ValueError("FILEHOT_IN must be a NetCDF file with .nc extension")
        return v

    @field_validator("hotstyle_in")
    @classmethod
    def validate_hotstyle_in(cls, v: int) -> int:
        if v not in [1, 2]:
            raise ValueError("HOTSTYLE_IN must be either 1 (binary) or 2 (NetCDF)")
        return v

    @field_validator("ihotpos_in")
    @classmethod
    def validate_ihotpos_in(cls, v: int) -> int:
        if v not in [1, 2]:
            raise ValueError("IHOTPOS_IN must be either 1 or 2")
        return v

    @field_validator("multiplein")
    @classmethod
    def validate_multiplein(cls, v: int) -> int:
        if v not in [0, 1]:
            raise ValueError(
                "MULTIPLEIN must be either 0 (single file) or 1 (multiple files)"
            )
        return v


class Hotfile(NamelistBaseModel):
    lhotf: Optional[bool] = Field(
        True, description="Flag to enable writing of hotfile output"
    )
    filehot_out: Optional[str] = Field(
        "hotfile_out_WWM.nc", description="Name of the output hotfile"
    )
    begtc: Optional[str] = Field(
        "20030908.000000",
        description="Starting time of hotfile writing, format: 'YYYYMMDD.HHMMSS'. When ihot!=0 in SCHISM, this will be the new hotstarted time (even with ihot=2)",
    )
    deltc: Optional[float] = Field(
        86400.0, description="Time interval between hotfile writes"
    )
    unitc: Optional[str] = Field("SEC", description="Time unit used for DELTC")
    endtc: Optional[str] = Field(
        "20031008.000000",
        description="Ending time of hotfile writing, format: 'YYYYMMDD.HHMMSS'. Should be adjusted with BEGTC",
    )
    lcyclehot: Optional[bool] = Field(
        True,
        description="Flag to control hotfile record behavior (applies only to netcdf). If True, hotfile contains 2 last records (1st is the most recent). If False, hotfile contains N records if N outputs have been done. For binary, only one record is used",
    )
    hotstyle_out: Optional[int] = Field(
        2, description="Output format for hotfile. 1: binary, 2: netcdf (default)"
    )
    multipleout: Optional[int] = Field(
        0,
        description="Flag to control hotfile output mode. 0: single file output (binary or netcdf) using MPI_REDUCE (avoid too frequent output), 1: separate files for each process",
    )

    @field_validator("lhotf")
    @classmethod
    def validate_lhotf(cls, v: bool) -> bool:
        return v

    @field_validator("filehot_out")
    @classmethod
    def validate_filehot_out(cls, v: str) -> str:
        if not v.endswith(".nc"):
            raise ValueError("Filename must end with .nc")
        return v

    @field_validator("begtc")
    @classmethod
    def validate_begtc(cls, v: str) -> str:
        import datetime

        try:
            datetime.datetime.strptime(v, "%Y%m%d.%H%M%S")
        except ValueError:
            raise ValueError("Invalid date format. Use YYYYMMDD.HHMMSS")
        return v

    @field_validator("deltc")
    @classmethod
    def validate_deltc(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Time interval must be positive")
        return v

    @field_validator("unitc")
    @classmethod
    def validate_unitc(cls, v: str) -> str:
        valid_units = ["SEC", "MIN", "HOUR", "DAY"]
        if v.upper() not in valid_units:
            raise ValueError(f"Invalid time unit. Choose from {valid_units}")
        return v.upper()

    @field_validator("endtc")
    @classmethod
    def validate_endtc(cls, v: str) -> str:
        import datetime

        try:
            datetime.datetime.strptime(v, "%Y%m%d.%H%M%S")
        except ValueError:
            raise ValueError("Invalid date format. Use YYYYMMDD.HHMMSS")
        return v

    @field_validator("lcyclehot")
    @classmethod
    def validate_lcyclehot(cls, v: bool) -> bool:
        return v

    @field_validator("hotstyle_out")
    @classmethod
    def validate_hotstyle_out(cls, v: int) -> int:
        if v not in [1, 2]:
            raise ValueError("HOTSTYLE_OUT must be 1 (binary) or 2 (netcdf)")
        return v

    @field_validator("multipleout")
    @classmethod
    def validate_multipleout(cls, v: int) -> int:
        if v not in [0, 1]:
            raise ValueError(
                "MULTIPLEOUT must be 0 (single file) or 1 (multiple files)"
            )
        return v

    @model_validator(mode="after")
    def validate_time_range(self) -> "Model":
        import datetime

        start = datetime.datetime.strptime(self.begtc, "%Y%m%d.%H%M%S")
        end = datetime.datetime.strptime(self.endtc, "%Y%m%d.%H%M%S")
        if end <= start:
            raise ValueError("ENDTC must be later than BEGTC")
        return self


class Bouc(NamelistBaseModel):
    lbcse: Optional[bool] = Field(
        True, description="Flag indicating if wave boundary data is time dependent"
    )
    lbinter: Optional[bool] = Field(
        True,
        description="Flag to perform time interpolation if LBCSE is True (not available for quasi-steady mode within subtime steps)",
    )
    lbcwa: Optional[bool] = Field(
        True, description="Flag to use parametric wave spectra for boundary conditions"
    )
    lbcsp: Optional[bool] = Field(
        False,
        description="Flag to specify non-parametric wave spectra, defined in 'FILEWAVE'",
    )
    linhom: Optional[bool] = Field(
        True, description="Flag for non-uniform wave boundary conditions in space"
    )
    lbsp1d: Optional[bool] = Field(
        False,
        description="Flag for 1D (frequency space only) format for FILEWAVE if LBCSP is True and LINHOM is False",
    )
    lbsp2d: Optional[bool] = Field(
        False,
        description="Flag for 2D format for FILEWAVE if LBCSP is True and LINHOM is False",
    )
    begtc: Optional[str] = Field(
        "20030908.000000", description="Begin time of the wave boundary file (FILEWAVE)"
    )
    deltc: Optional[int] = Field(1, description="Time step in FILEWAVE")
    unitc: Optional[str] = Field(
        "HR", description="Time unit for DELTC (HR, MIN, or SEC)"
    )
    endtc: Optional[str] = Field(
        "20031008.000000", description="End time of the wave boundary file"
    )
    filebound: Optional[str] = Field(
        "wwmbnd.gr3",
        description="Boundary file defining boundary conditions and Neumann nodes",
    )
    iboundformat: Optional[int] = Field(
        3,
        description="Format of boundary file (1: WWM, 3: WW3 2D spectra in netcdf, 6: WW3 2D spectra in netcdf with LBCSP=T)",
    )
    filewave: Optional[str] = Field(
        "bndfiles.dat", description="Boundary file defining boundary input from WW3"
    )
    lindsprdeg: Optional[bool] = Field(
        False,
        description="Flag indicating if directional spreading input is in degrees (True) or exponent (False) for 1D wave spectra",
    )
    lparmdir: Optional[bool] = Field(
        False,
        description="Flag to read directional spreading from WBDS in exponential format (only valid for 1D spectra)",
    )
    wbhs: Optional[float] = Field(
        2.0,
        description="Significant wave height at the boundary for parametric spectra",
    )
    wbss: Optional[int] = Field(
        2, description="Spectral shape parameter for parametric spectra"
    )
    wbtp: Optional[float] = Field(
        8.0, description="Peak or mean period at the boundary for parametric spectra"
    )
    wbdm: Optional[float] = Field(
        90.0, description="Average wave direction at the boundary (degrees)"
    )
    wbdsms: Optional[int] = Field(
        1,
        description="Flag indicating if directional spreading value is in degrees (1) or exponent (2)",
    )
    wbds: Optional[float] = Field(
        10.0, description="Directional spreading at the boundary (degrees or exponent)"
    )
    wbgauss: Optional[float] = Field(
        0.1, description="Factor for Gaussian distribution if WBSS=4"
    )
    wbpken: Optional[float] = Field(
        3.3, description="Peak enhancement factor for JONSWAP spectra if WBSS=2"
    )

    @field_validator("lbcse")
    @classmethod
    def validate_lbcse(cls, v: bool) -> bool:
        return v

    @field_validator("lbinter")
    @classmethod
    def validate_lbinter(cls, v: bool) -> bool:
        return v

    @field_validator("lbcwa")
    @classmethod
    def validate_lbcwa(cls, v: bool) -> bool:
        return v

    @field_validator("lbcsp")
    @classmethod
    def validate_lbcsp(cls, v: bool) -> bool:
        return v

    @field_validator("linhom")
    @classmethod
    def validate_linhom(cls, v: bool) -> bool:
        return v

    @field_validator("lbsp1d")
    @classmethod
    def validate_lbsp1d(cls, v: bool) -> bool:
        return v

    @field_validator("lbsp2d")
    @classmethod
    def validate_lbsp2d(cls, v: bool) -> bool:
        return v

    @field_validator("begtc")
    @classmethod
    def validate_begtc(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y%m%d.%H%M%S")
            return v
        except ValueError:
            raise ValueError("Invalid date format for BEGTC")

    @field_validator("deltc")
    @classmethod
    def validate_deltc(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("DELTC must be positive")
        return v

    @field_validator("unitc")
    @classmethod
    def validate_unitc(cls, v: str) -> str:
        if v not in ["HR", "MIN", "SEC"]:
            raise ValueError("UNITC must be HR, MIN, or SEC")
        return v

    @field_validator("endtc")
    @classmethod
    def validate_endtc(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y%m%d.%H%M%S")
            return v
        except ValueError:
            raise ValueError("Invalid date format for ENDTC")

    @field_validator("filebound")
    @classmethod
    def validate_filebound(cls, v: str) -> str:
        if not v.endswith(".gr3"):
            raise ValueError("FILEBOUND must have .gr3 extension")
        return v

    @field_validator("iboundformat")
    @classmethod
    def validate_iboundformat(cls, v: int) -> int:
        if v not in [1, 3, 6]:
            raise ValueError("IBOUNDFORMAT must be 1, 3, or 6")
        return v

    @field_validator("filewave")
    @classmethod
    def validate_filewave(cls, v: str) -> str:
        if not v:
            raise ValueError("FILEWAVE must not be empty")
        return v

    @field_validator("lindsprdeg")
    @classmethod
    def validate_lindsprdeg(cls, v: bool) -> bool:
        return v

    @field_validator("lparmdir")
    @classmethod
    def validate_lparmdir(cls, v: bool) -> bool:
        return v

    @field_validator("wbhs")
    @classmethod
    def validate_wbhs(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("WBHS must be positive")
        return v

    @field_validator("wbss")
    @classmethod
    def validate_wbss(cls, v: int) -> int:
        if v not in [-3, -2, -1, 1, 2, 3, 4]:
            raise ValueError("WBSS must be -3, -2, -1, 1, 2, 3, or 4")
        return v

    @field_validator("wbtp")
    @classmethod
    def validate_wbtp(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("WBTP must be positive")
        return v

    @field_validator("wbdm")
    @classmethod
    def validate_wbdm(cls, v: float) -> float:
        if not 0 <= v <= 360:
            raise ValueError("WBDM must be between 0 and 360")
        return v

    @field_validator("wbdsms")
    @classmethod
    def validate_wbdsms(cls, v: int) -> int:
        if v not in [1, 2]:
            raise ValueError("WBDSMS must be 1 or 2")
        return v

    @field_validator("wbds")
    @classmethod
    def validate_wbds(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("WBDS must be positive")
        return v

    @field_validator("wbgauss")
    @classmethod
    def validate_wbgauss(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("WBGAUSS must be positive")
        return v

    @field_validator("wbpken")
    @classmethod
    def validate_wbpken(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("WBPKEN must be positive")
        return v

    @model_validator(mode="after")
    def validate_lbinter_lbcse(self) -> "Model":
        if self.lbinter and not self.lbcse:
            raise ValueError("LBINTER can only be True if LBCSE is True")
        return self

    @model_validator(mode="after")
    def validate_lbcwa_lbcsp(self) -> "Model":
        if self.lbcwa and self.lbcsp:
            raise ValueError("LBCWA and LBCSP cannot both be True")
        return self

    @model_validator(mode="after")
    def validate_lbsp1d_conditions(self) -> "Model":
        if self.lbsp1d and not (self.lbcsp and not self.linhom):
            raise ValueError(
                "LBSP1D can only be True if LBCSP is True and LINHOM is False"
            )
        return self

    @model_validator(mode="after")
    def validate_lbsp2d_conditions(self) -> "Model":
        if self.lbsp2d and not (self.lbcsp and not self.linhom):
            raise ValueError(
                "LBSP2D can only be True if LBCSP is True and LINHOM is False"
            )
        return self

    @model_validator(mode="after")
    def validate_time_range(self) -> "Model":
        begin = datetime.strptime(self.begtc, "%Y%m%d.%H%M%S")
        end = datetime.strptime(self.endtc, "%Y%m%d.%H%M%S")
        if end <= begin:
            raise ValueError("ENDTC must be later than BEGTC")
        return self


class Engs(NamelistBaseModel):
    mesnl: Optional[int] = Field(
        1,
        description="Nonlinear Interaction NL4 switch: 1 for on (Discrete Interaction approximation), 0 for off",
    )
    mesin: Optional[int] = Field(
        1,
        description="Wind input formulation: 1 - Ardhuin et al. (use LSOURCESWAM = F), 2 - ECMWF physics, 3 - Makin & Stam, 4 - Babanin et al., 5 - Cycle 3, 0 - no wind",
    )
    ifric: Optional[int] = Field(
        1,
        description="Formulation for atmospheric boundary layer: 1 for MESIN = 1, 4 for MESIN = 3",
    )
    mesbf: Optional[int] = Field(
        1,
        description="Bottom friction formulation: 1 - JONSWAP (Default), 2 - Madsen et al. (1989), 3 - SHOWEX",
    )
    fricc: Optional[float] = Field(
        0.067,
        description="Bottom friction coefficient: JONSWAP coefficient [0.038, 0.067] if MESBF=1, physical bottom roughness if MESBF=2, D50 if MESBF=3 (negative value reads from SHOWEX_D50.gr3)",
    )
    mesbr: Optional[int] = Field(
        1, description="Shallow water wave breaking switch: 0 for off, 1 for on"
    )
    ibreak: Optional[int] = Field(
        1,
        description="Wave breaking formulation: 1 - Battjes and Janssen (1978), 2 - Thornton and Guza (1983) Constant weighting, 3 - Thornton and Guza (1983) Skewed weighting, 4 - van der Westhuysen (2010), 5 - Baldock et al (1998) modified by Janssen and Battjes (2007), 6 - Church and Thornton (1993)",
    )
    icrit: Optional[int] = Field(
        1,
        description="Wave breaking criterion: 1 - Constant breaker index, 2,6 - Local steepness adapted from Battjes and Stive (1985), 3 - Biphase threshold, 4 - Sallenger and Holman 1985, 5 - Ruessink et al (2003)",
    )
    brcr: Optional[float] = Field(
        0.78,
        description="Breaker index parameter: gamma for IBREAK=1,5; gamma_TG for IBREAK=2,3; biphase_ref for IBREAK=4",
    )
    a_brcr: Optional[float] = Field(0.76, description="Coefficient for ICRIT = 4, 5")
    b_brcr: Optional[float] = Field(0.29, description="Coefficient for ICRIT = 4, 5")
    min_brcr: Optional[float] = Field(
        0.25, description="Minimum value for ICRIT = 4, 5"
    )
    max_brcr: Optional[float] = Field(0.8, description="Maximum value for ICRIT = 4, 5")
    a_biph: Optional[float] = Field(
        0.2, description="Biphase coefficient, default 0.2 (intended for IBREAK=3)"
    )
    br_coef_method: Optional[int] = Field(
        1, description="Method for the breaking coefficient: 1 - constant, 2 - adaptive"
    )
    b_alp: Optional[float] = Field(
        0.5, description="Breaking coefficient. If BR_COEF_METHOD = 2, B_ALP ~ 40"
    )
    zprof_break: Optional[int] = Field(
        2,
        description="Vertical distribution function of wave breaking source term, only used in 3D run",
    )
    bc_break: Optional[int] = Field(
        1, description="Apply depth-limited breaking at the boundaries: 1 - On, 0 - Off"
    )
    iroller: Optional[int] = Field(
        0, description="Wave roller model: 1 - On, 0 - Off (not used at the moment)"
    )
    alprol: Optional[float] = Field(
        0.85,
        description="Alpha coefficient for the wave roller model (between 0 and 1): 1 - full conversion, 0 - no energy transferred to the roller",
    )
    meveg: Optional[int] = Field(
        0, description="Vegetation on/off. If on, isav must = 1 in param.nml"
    )
    lmaxetot: Optional[bool] = Field(
        True, description="Limit shallow water wave height by wave breaking limiter"
    )
    mesds: Optional[int] = Field(
        1,
        description="Formulation for the whitecapping source function; same value as MESIN",
    )
    mestr: Optional[int] = Field(
        1,
        description="Formulation for the triad 3 wave interactions: 0 - off, 1 - Lumped Triad Approx. (LTA), 2 - corrected version of LTA by Salmon et al. (2016)",
    )
    trico: Optional[float] = Field(
        0.1, description="Proportionality constant (alpha_EB) for triad interactions"
    )
    trira: Optional[float] = Field(
        2.5,
        description="Ratio of max. frequency considered in triads over mean frequency",
    )
    triurs: Optional[float] = Field(
        0.1,
        description="Critical Ursell number; if Ursell # < TRIURS, triads are not computed",
    )

    @field_validator("mesnl")
    @classmethod
    def validate_mesnl(cls, v):
        if v not in [0, 1]:
            raise ValueError("MESNL must be 0 or 1")
        return v

    @field_validator("mesin")
    @classmethod
    def validate_mesin(cls, v):
        if v not in range(6):
            raise ValueError("MESIN must be between 0 and 5")
        return v

    @field_validator("ifric")
    @classmethod
    def validate_ifric(cls, v):
        if v not in [1, 4]:
            raise ValueError("IFRIC must be 1 or 4")
        return v

    @field_validator("mesbf")
    @classmethod
    def validate_mesbf(cls, v):
        if v not in [1, 2, 3]:
            raise ValueError("MESBF must be 1, 2, or 3")
        return v

    @field_validator("fricc")
    @classmethod
    def validate_fricc(cls, v):
        return v

    @field_validator("mesbr")
    @classmethod
    def validate_mesbr(cls, v):
        if v not in [0, 1]:
            raise ValueError("MESBR must be 0 or 1")
        return v

    @field_validator("ibreak")
    @classmethod
    def validate_ibreak(cls, v):
        if v not in range(1, 7):
            raise ValueError("IBREAK must be between 1 and 6")
        return v

    @field_validator("icrit")
    @classmethod
    def validate_icrit(cls, v):
        if v not in range(1, 7):
            raise ValueError("ICRIT must be between 1 and 6")
        return v

    @field_validator("brcr")
    @classmethod
    def validate_brcr(cls, v):
        return v

    @field_validator("a_brcr")
    @classmethod
    def validate_a_brcr(cls, v):
        return v

    @field_validator("b_brcr")
    @classmethod
    def validate_b_brcr(cls, v):
        return v

    @field_validator("min_brcr")
    @classmethod
    def validate_min_brcr(cls, v):
        return v

    @field_validator("max_brcr")
    @classmethod
    def validate_max_brcr(cls, v):
        return v

    @field_validator("a_biph")
    @classmethod
    def validate_a_biph(cls, v):
        return v

    @field_validator("br_coef_method")
    @classmethod
    def validate_br_coef_method(cls, v):
        if v not in [1, 2]:
            raise ValueError("BR_COEF_METHOD must be 1 or 2")
        return v

    @field_validator("b_alp")
    @classmethod
    def validate_b_alp(cls, v):
        return v

    @field_validator("zprof_break")
    @classmethod
    def validate_zprof_break(cls, v):
        if v not in range(1, 7):
            raise ValueError("ZPROF_BREAK must be between 1 and 6")
        return v

    @field_validator("bc_break")
    @classmethod
    def validate_bc_break(cls, v):
        if v not in [0, 1]:
            raise ValueError("BC_BREAK must be 0 or 1")
        return v

    @field_validator("iroller")
    @classmethod
    def validate_iroller(cls, v):
        if v not in [0, 1]:
            raise ValueError("IROLLER must be 0 or 1")
        return v

    @field_validator("alprol")
    @classmethod
    def validate_alprol(cls, v):
        if not 0 <= v <= 1:
            raise ValueError("ALPROL must be between 0 and 1")
        return v

    @field_validator("meveg")
    @classmethod
    def validate_meveg(cls, v):
        if v not in [0, 1]:
            raise ValueError("MEVEG must be 0 or 1")
        return v

    @field_validator("lmaxetot")
    @classmethod
    def validate_lmaxetot(cls, v):
        if not isinstance(v, bool):
            raise ValueError("LMAXETOT must be a boolean")
        return v

    @field_validator("mesds")
    @classmethod
    def validate_mesds(cls, v):
        if v not in range(6):
            raise ValueError("MESDS must be between 0 and 5")
        return v

    @field_validator("mestr")
    @classmethod
    def validate_mestr(cls, v):
        if v not in [0, 1, 2]:
            raise ValueError("MESTR must be 0, 1, or 2")
        return v

    @field_validator("trico")
    @classmethod
    def validate_trico(cls, v):
        if v <= 0:
            raise ValueError("TRICO must be positive")
        return v

    @field_validator("trira")
    @classmethod
    def validate_trira(cls, v):
        if v <= 0:
            raise ValueError("TRIRA must be positive")
        return v

    @field_validator("triurs")
    @classmethod
    def validate_triurs(cls, v):
        if v <= 0:
            raise ValueError("TRIURS must be positive")
        return v

    @model_validator(mode="after")
    def validate_ifric_mesin(self):
        if self.mesin == 1 and self.ifric != 1:
            raise ValueError("When MESIN=1, IFRIC should be 1")
        if self.mesin == 3 and self.ifric != 4:
            raise ValueError("When MESIN=3, IFRIC should be 4")
        return self

    @model_validator(mode="after")
    def validate_fricc_mesbf(self):
        if self.mesbf == 1 and not 0.038 <= self.fricc <= 0.067:
            raise ValueError("When MESBF=1, FRICC should be between 0.038 and 0.067")
        return self

    @model_validator(mode="after")
    def validate_mesds_mesin(self):
        if self.mesds != self.mesin:
            raise ValueError("MESDS should have the same value as MESIN")
        return self


class Nums(NamelistBaseModel):
    icomp: Optional[int] = Field(
        3,
        description="Controls the splitting method and scheme type (implicit/explicit) for spectral advection. 0: Explicit for all dimensions, 1: Implicit for geographical space, explicit for others, 2: Implicit for advection and semi-implicit for source terms, 3: Fully implicit with no splitting.",
    )
    amethod: Optional[int] = Field(
        7,
        description="Controls the methods used in geographical space. 0: No advection, 1-3: Various explicit/implicit schemes, 4-5: PETSc-based methods, 6: BCGS Solver, 7: GAUSS and JACOBI SOLVER.",
    )
    smethod: Optional[int] = Field(
        1,
        description="Controls the integration of source terms. 0: No source terms, 1: Splitting using RK-3 and SI, 2: Semi-implicit, 3: R-K3, 4: Dynamic Splitting, 6: Sub-time steps for breaking term integration.",
    )
    dmethod: Optional[int] = Field(
        2,
        description="Controls the numerical method in directional space. 0: No advection, 1: Crank-Nicholson or Euler Implicit, 2: Ultimate Quickest, 3: RK5-WENO, 4: Explicit FVM Upwind scheme.",
    )
    rtheta: Optional[float] = Field(
        0.5,
        description="Weighing factor for DMETHOD = 1, used in Crank-Nicholson integration.",
    )
    litersplit: Optional[bool] = Field(
        False,
        description="Controls splitting method. True: double Strang split, False: simple split (more efficient).",
    )
    lfilterth: Optional[bool] = Field(
        False,
        description="Use a CFL filter to limit the advection velocity in directional space.",
    )
    maxcflth: Optional[float] = Field(
        1.0,
        description="Maximum CFL number in Theta space, used only if LFILTERTH=True.",
    )
    fmethod: Optional[int] = Field(
        1,
        description="Controls the numerical method used in frequency space. 0: No advection, 1: Ultimate Quickest as in WW3.",
    )
    lfiltersig: Optional[bool] = Field(
        False, description="Limit the advection velocity in frequency space."
    )
    maxcflsig: Optional[float] = Field(
        1.0,
        description="Maximum CFL number in frequency space, used only if LFILTERSIG=True.",
    )
    llimt: Optional[bool] = Field(
        True, description="Switch on/off Action limiter. Must usually be turned on."
    )
    melim: Optional[int] = Field(
        1,
        description="Formulation for the action limiter. 1: WAM group (1988), 2: Hersbach Janssen (1999), 3: For Cycle 4 formulation.",
    )
    limfak: Optional[float] = Field(
        0.1,
        description="Proportionality coefficient for the action limiter MAX_DAC_DT = Limfak * Limiter.",
    )
    ldifr: Optional[bool] = Field(
        False,
        description="Use phase decoupled diffraction approximation according to Holthuijsen et al. (2003).",
    )
    idiffr: Optional[int] = Field(
        1,
        description="Extended WAE accounting for higher order effects. 1: Holthuijsen et al., 2: Liau et al., 3: Toledo et al.",
    )
    lconv: Optional[bool] = Field(
        False,
        description="Estimate convergence criteria and write to disk (quasi-steady - qstea.out).",
    )
    lcfl: Optional[bool] = Field(
        False, description="Write out CFL numbers. Set to False to save time."
    )
    nqsiter: Optional[int] = Field(
        1,
        description="Number of quasi-steady (Q-S) sub-divisions within each WWM time step.",
    )
    qsconv1: Optional[float] = Field(
        0.98,
        description="Fraction of grid points that must fulfill absolute wave height criteria EPSH1.",
    )
    qsconv2: Optional[float] = Field(
        0.98,
        description="Fraction of grid points that must fulfill relative wave height criteria EPSH2.",
    )
    qsconv3: Optional[float] = Field(
        0.98,
        description="Fraction of grid points that must fulfill sum relative wave action criteria EPSH3.",
    )
    qsconv4: Optional[float] = Field(
        0.98,
        description="Fraction of grid points that must fulfill relative average wave steepness criteria EPSH4.",
    )
    qsconv5: Optional[float] = Field(
        0.98,
        description="Fraction of grid points that must fulfill average relative wave period criteria EPSH5.",
    )
    lexpimp: Optional[bool] = Field(
        False,
        description="Use implicit schemes for frequencies lower than FREQEXP. Used only if ICOMP=0.",
    )
    freqexp: Optional[float] = Field(
        0.1,
        description="Minimum frequency for explicit schemes. Used only if LEXPIMP=True and ICOMP=0.",
    )
    epsh1: Optional[float] = Field(
        0.01, description="Convergence criteria for relative wave height."
    )
    epsh2: Optional[float] = Field(
        0.01, description="Convergence criteria for absolute wave height."
    )
    epsh3: Optional[float] = Field(
        0.01, description="Convergence criteria for the relative sum of wave action."
    )
    epsh4: Optional[float] = Field(
        0.01,
        description="Convergence criteria for the relative average wave steepness.",
    )
    epsh5: Optional[float] = Field(
        0.01, description="Convergence criteria for the relative average wave period."
    )
    lvector: Optional[bool] = Field(
        False,
        description="Use optimized propagation routines for large high-performance computers.",
    )
    ivector: Optional[int] = Field(
        2,
        description="Different flavors of communications when LVECTOR=True. 1-6: Various optimization strategies.",
    )
    ladvtest: Optional[bool] = Field(
        False, description="For testing the advection schemes."
    )
    lchkconv: Optional[bool] = Field(
        False, description="Check convergence criteria for quasi-steady mode."
    )
    dtmin_dyn: Optional[float] = Field(
        1.0, description="Minimum time step (seconds) for dynamic integration."
    )
    ndyniter: Optional[int] = Field(
        100,
        description="Maximum iterations for dynamic scheme before applying limiter.",
    )
    dtmin_sin: Optional[float] = Field(
        1.0,
        description="Minimum time step for the full fractional step method (SIN term).",
    )
    dtmin_snl4: Optional[float] = Field(
        1.0, description="Minimum time step for SNL4 term in fractional step method."
    )
    dtmin_sds: Optional[float] = Field(
        1.0, description="Minimum time step for SDS term in fractional step method."
    )
    dtmin_snl3: Optional[float] = Field(
        1.0, description="Minimum time step for SNL3 term in fractional step method."
    )
    dtmin_sbr: Optional[float] = Field(
        0.1, description="Minimum time step for SBR term in fractional step method."
    )
    dtmin_sbf: Optional[float] = Field(
        1.0, description="Minimum time step for SBF term in fractional step method."
    )
    ndyniter_sin: Optional[int] = Field(
        10, description="Maximum iterations for SIN term in fractional step approach."
    )
    ndyniter_snl4: Optional[int] = Field(
        10, description="Maximum iterations for SNL4 term in fractional step approach."
    )
    ndyniter_sds: Optional[int] = Field(
        10, description="Maximum iterations for SDS term in fractional step approach."
    )
    ndyniter_sbr: Optional[int] = Field(
        10, description="Maximum iterations for SBR term in fractional step approach."
    )
    ndyniter_snl3: Optional[int] = Field(
        10, description="Maximum iterations for SNL3 term in fractional step approach."
    )
    ndyniter_sbf: Optional[int] = Field(
        10, description="Maximum iterations for SBF term in fractional step approach."
    )
    lsoubound: Optional[bool] = Field(
        False,
        description="Apply source terms on boundary. Useful for harbor studies and flume experiments.",
    )
    wae_solverthr: Optional[float] = Field(
        1e-06,
        description="Threshold for the Block-Jacobi or Block-Gauss-Seider solver.",
    )
    maxiter: Optional[int] = Field(
        1000, description="Maximum number of iterations for solvers."
    )
    pmin: Optional[float] = Field(
        1.0, description="Maximum percentage of non-converged grid points allowed."
    )
    lnaninfchk: Optional[bool] = Field(
        False,
        description="Check for NaN and INF values. Usually turned off for efficiency.",
    )
    lzeta_setup: Optional[bool] = Field(
        False, description="Compute wave setup using simple momentum equation."
    )
    zeta_meth: Optional[int] = Field(
        0, description="Method for wave setup calculation."
    )
    lsourceswam: Optional[bool] = Field(
        False, description="Use ECMWF WAM formulation for deep water physics."
    )
    block_gauss_seidel: Optional[bool] = Field(
        True,
        description="Use Gauss-Seidel method on each computer block for faster computation with less memory usage.",
    )
    lnonl: Optional[bool] = Field(
        False,
        description="Solve the nonlinear system using simpler algorithm (Patankar).",
    )
    aspar_local_level: Optional[int] = Field(
        0, description="ASPAR locality level for memory allocation and optimization."
    )
    l_solver_norm: Optional[bool] = Field(
        False,
        description="Compute solver norm ||A*x-b|| as termination check of Jacobi-Gauss-Seidel solver.",
    )
    laccel: Optional[bool] = Field(
        False, description="Enable acceleration for solvers."
    )

    @field_validator("icomp")
    @classmethod
    def validate_icomp(cls, v):
        if v not in [0, 1, 2, 3]:
            raise ValueError("ICOMP must be 0, 1, 2, or 3")
        return v

    @field_validator("amethod")
    @classmethod
    def validate_amethod(cls, v):
        if v not in range(8):
            raise ValueError("AMETHOD must be between 0 and 7")
        return v

    @field_validator("smethod")
    @classmethod
    def validate_smethod(cls, v):
        if v not in [0, 1, 2, 3, 4, 6]:
            raise ValueError("SMETHOD must be 0, 1, 2, 3, 4, or 6")
        return v

    @field_validator("dmethod")
    @classmethod
    def validate_dmethod(cls, v):
        if v not in range(5):
            raise ValueError("DMETHOD must be between 0 and 4")
        return v

    @field_validator("rtheta")
    @classmethod
    def validate_rtheta(cls, v):
        if not 0 <= v <= 1:
            raise ValueError("RTHETA must be between 0 and 1")
        return v

    @field_validator("maxcflth")
    @classmethod
    def validate_maxcflth(cls, v):
        if v <= 0:
            raise ValueError("MAXCFLTH must be positive")
        return v

    @field_validator("fmethod")
    @classmethod
    def validate_fmethod(cls, v):
        if v not in [0, 1]:
            raise ValueError("FMETHOD must be 0 or 1")
        return v

    @field_validator("maxcflsig")
    @classmethod
    def validate_maxcflsig(cls, v):
        if v <= 0:
            raise ValueError("MAXCFLSIG must be positive")
        return v

    @field_validator("melim")
    @classmethod
    def validate_melim(cls, v):
        if v not in [1, 2, 3]:
            raise ValueError("MELIM must be 1, 2, or 3")
        return v

    @field_validator("limfak")
    @classmethod
    def validate_limfak(cls, v):
        if v <= 0:
            raise ValueError("LIMFAK must be positive")
        return v

    @field_validator("idiffr")
    @classmethod
    def validate_idiffr(cls, v):
        if v not in [1, 2, 3]:
            raise ValueError("IDIFFR must be 1, 2, or 3")
        return v

    @field_validator("nqsiter")
    @classmethod
    def validate_nqsiter(cls, v):
        if v <= 0:
            raise ValueError("NQSITER must be positive")
        return v

    @field_validator("qsconv1")
    @classmethod
    def validate_qsconv1(cls, v):
        if not 0 <= v <= 1:
            raise ValueError("QSCONV1 must be between 0 and 1")
        return v

    @field_validator("qsconv2")
    @classmethod
    def validate_qsconv2(cls, v):
        if not 0 <= v <= 1:
            raise ValueError("QSCONV2 must be between 0 and 1")
        return v

    @field_validator("qsconv3")
    @classmethod
    def validate_qsconv3(cls, v):
        if not 0 <= v <= 1:
            raise ValueError("QSCONV3 must be between 0 and 1")
        return v

    @field_validator("qsconv4")
    @classmethod
    def validate_qsconv4(cls, v):
        if not 0 <= v <= 1:
            raise ValueError("QSCONV4 must be between 0 and 1")
        return v

    @field_validator("qsconv5")
    @classmethod
    def validate_qsconv5(cls, v):
        if not 0 <= v <= 1:
            raise ValueError("QSCONV5 must be between 0 and 1")
        return v

    @field_validator("freqexp")
    @classmethod
    def validate_freqexp(cls, v):
        if v <= 0:
            raise ValueError("FREQEXP must be positive")
        return v

    @field_validator("epsh1")
    @classmethod
    def validate_epsh1(cls, v):
        if v <= 0:
            raise ValueError("EPSH1 must be positive")
        return v

    @field_validator("epsh2")
    @classmethod
    def validate_epsh2(cls, v):
        if v <= 0:
            raise ValueError("EPSH2 must be positive")
        return v

    @field_validator("epsh3")
    @classmethod
    def validate_epsh3(cls, v):
        if v <= 0:
            raise ValueError("EPSH3 must be positive")
        return v

    @field_validator("epsh4")
    @classmethod
    def validate_epsh4(cls, v):
        if v <= 0:
            raise ValueError("EPSH4 must be positive")
        return v

    @field_validator("epsh5")
    @classmethod
    def validate_epsh5(cls, v):
        if v <= 0:
            raise ValueError("EPSH5 must be positive")
        return v

    @field_validator("ivector")
    @classmethod
    def validate_ivector(cls, v):
        if v not in range(1, 7):
            raise ValueError("IVECTOR must be between 1 and 6")
        return v

    @field_validator("dtmin_dyn")
    @classmethod
    def validate_dtmin_dyn(cls, v):
        if v <= 0:
            raise ValueError("DTMIN_DYN must be positive")
        return v

    @field_validator("ndyniter")
    @classmethod
    def validate_ndyniter(cls, v):
        if v <= 0:
            raise ValueError("NDYNITER must be positive")
        return v

    @field_validator("dtmin_sin")
    @classmethod
    def validate_dtmin_sin(cls, v):
        if v <= 0:
            raise ValueError("DTMIN_SIN must be positive")
        return v

    @field_validator("dtmin_snl4")
    @classmethod
    def validate_dtmin_snl4(cls, v):
        if v <= 0:
            raise ValueError("DTMIN_SNL4 must be positive")
        return v

    @field_validator("dtmin_sds")
    @classmethod
    def validate_dtmin_sds(cls, v):
        if v <= 0:
            raise ValueError("DTMIN_SDS must be positive")
        return v

    @field_validator("dtmin_snl3")
    @classmethod
    def validate_dtmin_snl3(cls, v):
        if v <= 0:
            raise ValueError("DTMIN_SNL3 must be positive")
        return v

    @field_validator("dtmin_sbr")
    @classmethod
    def validate_dtmin_sbr(cls, v):
        if v <= 0:
            raise ValueError("DTMIN_SBR must be positive")
        return v

    @field_validator("dtmin_sbf")
    @classmethod
    def validate_dtmin_sbf(cls, v):
        if v <= 0:
            raise ValueError("DTMIN_SBF must be positive")
        return v

    @field_validator("ndyniter_sin")
    @classmethod
    def validate_ndyniter_sin(cls, v):
        if v <= 0:
            raise ValueError("NDYNITER_SIN must be positive")
        return v

    @field_validator("ndyniter_snl4")
    @classmethod
    def validate_ndyniter_snl4(cls, v):
        if v <= 0:
            raise ValueError("NDYNITER_SNL4 must be positive")
        return v

    @field_validator("ndyniter_sds")
    @classmethod
    def validate_ndyniter_sds(cls, v):
        if v <= 0:
            raise ValueError("NDYNITER_SDS must be positive")
        return v

    @field_validator("ndyniter_sbr")
    @classmethod
    def validate_ndyniter_sbr(cls, v):
        if v <= 0:
            raise ValueError("NDYNITER_SBR must be positive")
        return v

    @field_validator("ndyniter_snl3")
    @classmethod
    def validate_ndyniter_snl3(cls, v):
        if v <= 0:
            raise ValueError("NDYNITER_SNL3 must be positive")
        return v

    @field_validator("ndyniter_sbf")
    @classmethod
    def validate_ndyniter_sbf(cls, v):
        if v <= 0:
            raise ValueError("NDYNITER_SBF must be positive")
        return v

    @field_validator("wae_solverthr")
    @classmethod
    def validate_wae_solverthr(cls, v):
        if v <= 0:
            raise ValueError("WAE_SOLVERTHR must be positive")
        return v

    @field_validator("maxiter")
    @classmethod
    def validate_maxiter(cls, v):
        if v <= 0:
            raise ValueError("MAXITER must be positive")
        return v

    @field_validator("pmin")
    @classmethod
    def validate_pmin(cls, v):
        if not 0 <= v <= 100:
            raise ValueError("PMIN must be between 0 and 100")
        return v

    @field_validator("zeta_meth")
    @classmethod
    def validate_zeta_meth(cls, v):
        if v not in [0, 1]:
            raise ValueError("ZETA_METH must be 0 or 1")
        return v

    @field_validator("aspar_local_level")
    @classmethod
    def validate_aspar_local_level(cls, v):
        if v not in range(6):
            raise ValueError("ASPAR_LOCAL_LEVEL must be between 0 and 5")
        return v

    @model_validator(mode="after")
    def validate_ivector_lvector(self):
        if self.lvector and self.ivector not in range(1, 7):
            raise ValueError("When LVECTOR is True, IVECTOR must be between 1 and 6")
        return self


class History(NamelistBaseModel):
    begtc: Optional[str] = Field(
        "20030908.000000",
        description="Start output time in format 'YYYYMMDD.HHMMSS'. Must fit within the simulation time, otherwise no output is generated. Defaults to PROC%BEGTC if not specified.",
    )
    deltc: Optional[int] = Field(
        1,
        description="Time step for output in seconds. If smaller than simulation time step, the latter is used. Useful for better 1D and 2D spectra analysis when set to output every step.",
    )
    unitc: Optional[str] = Field(
        "SEC",
        description="Unit of time for DELTC. Currently only 'SEC' (seconds) is supported.",
    )
    endtc: Optional[str] = Field(
        "20031008.000000",
        description="Stop time for output in format 'YYYYMMDD.HHMMSS'. Defaults to PROC%ENDC if not specified.",
    )
    definetc: Optional[int] = Field(
        86400,
        description="Time scoop (in seconds) for history files. If unset or negative, only one file is generated. For example, 86400 creates daily output files.",
    )
    outstyle: Optional[str] = Field(
        "NO",
        description="Output option. 'NO' for no output, 'NC' for netCDF, 'XFN' for XFN output (default), or 'SHP' for DARKO SHP output.",
    )
    multipleout: Optional[int] = Field(
        0,
        description="Output style. 0 for single netCDF file using MPI_reduce (default), 1 for separate netCDF files for each process.",
    )
    use_single_out: Optional[bool] = Field(
        True,
        description="Use single precision in the output of model variables if True (default).",
    )
    paramwrite: Optional[bool] = Field(
        True,
        description="Write the physical parametrization and chosen numerical method in the netCDF file if True (default).",
    )
    gridwrite: Optional[bool] = Field(
        True, description="Write the grid in the netCDF history file if True (default)."
    )
    printmma: Optional[bool] = Field(
        False,
        description="Print minimum, maximum, and average value of statistics during runtime if True (default False). Requires MPI_REDUCE.",
    )
    fileout: Optional[str] = Field(
        "wwm_hist.dat", description="Filename for output data."
    )
    hs: Optional[bool] = Field(False, description="significant wave height")
    tm01: Optional[bool] = Field(False, description="mean period")
    tm02: Optional[bool] = Field(False, description="zero-crossing mean period")
    klm: Optional[bool] = Field(False, description="mean wave number")
    wlm: Optional[bool] = Field(False, description="mean wave length")
    etotc: Optional[bool] = Field(False, description="Variable ETOTC")
    etots: Optional[bool] = Field(False, description="Variable ETOTS")
    dm: Optional[bool] = Field(False, description="mean wave direction")
    dspr: Optional[bool] = Field(False, description="directional spreading")
    tppd: Optional[bool] = Field(
        False, description="direaction of the peak ... check source code"
    )
    tpp: Optional[bool] = Field(False, description="peak period")
    cpp: Optional[bool] = Field(False, description="peak phase vel.")
    wnpp: Optional[bool] = Field(False, description="peak wave number")
    cgpp: Optional[bool] = Field(False, description="peak group speed")
    kpp: Optional[bool] = Field(False, description="peak wave number")
    lpp: Optional[bool] = Field(False, description="peak wave length")
    peakd: Optional[bool] = Field(False, description="peak direction")
    peakdspr: Optional[bool] = Field(False, description="peak directional spreading")
    dpeak: Optional[bool] = Field(False, description="peak direction")
    ubot: Optional[bool] = Field(False, description="bottom exc. vel.")
    orbital: Optional[bool] = Field(False, description="bottom orbital vel.")
    botexper: Optional[bool] = Field(False, description="bottom exc.")
    tmbot: Optional[bool] = Field(False, description="bottom period")
    ursell: Optional[bool] = Field(False, description="Ursell number")
    ufric: Optional[bool] = Field(False, description="air friction velocity")
    z0: Optional[bool] = Field(False, description="air roughness length")
    alpha_ch: Optional[bool] = Field(False, description="Charnoch coefficient for air")
    windx: Optional[bool] = Field(False, description="Wind in X direction")
    windy: Optional[bool] = Field(False, description="Wind in Y direction")
    cd: Optional[bool] = Field(False, description="Drag coefficient")
    currtx: Optional[bool] = Field(False, description="current in X direction")
    currty: Optional[bool] = Field(False, description="current in Y direction")
    watlev: Optional[bool] = Field(False, description="water level")
    watlevold: Optional[bool] = Field(
        False, description="water level at previous time step"
    )
    depdt: Optional[bool] = Field(False, description="change of water level in time")
    dep: Optional[bool] = Field(False, description="depth")
    tauw: Optional[bool] = Field(False, description="surface stress from the wave")
    tauhf: Optional[bool] = Field(False, description="high frequency surface stress")
    tautot: Optional[bool] = Field(False, description="total surface stress")
    stokessurfx: Optional[bool] = Field(
        False, description="Surface Stokes drift in X direction"
    )
    stokessurfy: Optional[bool] = Field(
        False, description="Surface Stokes drift in X direction"
    )
    stokesbarox: Optional[bool] = Field(
        False, description="Barotropic Stokes drift in X direction"
    )
    stokesbaroy: Optional[bool] = Field(
        False, description="Barotropic Stokes drift in Y direction"
    )
    rsxx: Optional[bool] = Field(False, description="RSXX potential of LH")
    rsxy: Optional[bool] = Field(False, description="RSXY potential of LH")
    rsyy: Optional[bool] = Field(False, description="RSYY potential of LH")
    cfl1: Optional[bool] = Field(False, description="CFL number 1")
    cfl2: Optional[bool] = Field(False, description="CFL number 2")
    cfl3: Optional[bool] = Field(False, description="CFL number 3")

    @field_validator("begtc")
    @classmethod
    def validate_begtc(cls, v):
        try:
            datetime.strptime(v, "%Y%m%d.%H%M%S")
            return v
        except ValueError:
            raise ValueError("Invalid date format. Use YYYYMMDD.HHMMSS")

    @field_validator("deltc")
    @classmethod
    def validate_deltc(cls, v):
        if v <= 0:
            raise ValueError("DELTC must be a positive integer")
        return v

    @field_validator("unitc")
    @classmethod
    def validate_unitc(cls, v):
        if v.upper() != "SEC":
            raise ValueError("UNITC must be SEC")
        return v.upper()

    @field_validator("endtc")
    @classmethod
    def validate_endtc(cls, v):
        try:
            datetime.strptime(v, "%Y%m%d.%H%M%S")
            return v
        except ValueError:
            raise ValueError("Invalid date format. Use YYYYMMDD.HHMMSS")

    @field_validator("definetc")
    @classmethod
    def validate_definetc(cls, v):
        if v < 0:
            return None
        return v

    @field_validator("outstyle")
    @classmethod
    def validate_outstyle(cls, v):
        valid_options = ["NO", "NC", "XFN", "SHP"]
        if v.upper() not in valid_options:
            raise ValueError(f"OUTSTYLE must be one of {valid_options}")
        return v.upper()

    @field_validator("multipleout")
    @classmethod
    def validate_multipleout(cls, v):
        if v not in [0, 1]:
            raise ValueError("MULTIPLEOUT must be 0 or 1")
        return v

    @field_validator("use_single_out")
    @classmethod
    def validate_use_single_out(cls, v):
        return v

    @field_validator("paramwrite")
    @classmethod
    def validate_paramwrite(cls, v):
        return v

    @field_validator("gridwrite")
    @classmethod
    def validate_gridwrite(cls, v):
        return v

    @field_validator("printmma")
    @classmethod
    def validate_printmma(cls, v):
        return v

    @field_validator("fileout")
    @classmethod
    def validate_fileout(cls, v):
        if not v:
            raise ValueError("FILEOUT must not be empty")
        return v


class Station(NamelistBaseModel):
    begtc: Optional[str] = Field(
        "20030908.000000",
        description="Start simulation time in format 'yyyymmdd.hhmmss'. Must fit the simulation time, otherwise no output. Defaults to PROC%BEGTC if not specified.",
    )
    deltc: Optional[int] = Field(
        600,
        description="Time step for output in seconds. If smaller than simulation time step, the latter is used. Used for better 1D and 2D spectra analysis.",
    )
    unitc: Optional[str] = Field(
        "SEC",
        description="Unit of time for DELTC. Currently only 'SEC' (seconds) is supported.",
    )
    endtc: Optional[str] = Field(
        "20031008.000000",
        description="Stop time of simulation in format 'yyyymmdd.hhmmss'. Defaults to PROC%ENDC if not specified.",
    )
    definetc: Optional[int] = Field(
        86400,
        description="Time interval in seconds for definition of station files. If unset or negative, only one file is generated. For example, 86400 creates daily output files.",
    )
    outstyle: Optional[str] = Field(
        "NO",
        description="Output option. 'NO' for no output, 'STE' for classic station output (default), 'NC' for netCDF output.",
    )
    multipleout: Optional[int] = Field(
        0,
        description="Output file configuration. 0 for a single netCDF file using MPI_reduce (default), 1 for separate netCDF files for each process.",
    )
    use_single_out: Optional[bool] = Field(
        True,
        description="Use single precision in the output of model variables. True by default.",
    )
    paramwrite: Optional[bool] = Field(
        True,
        description="Write the physical parameterization and chosen numerical method in the netCDF file. True by default.",
    )
    fileout: Optional[str] = Field(
        "wwm_sta.dat", description="Output file name (not used)."
    )
    loutiter: Optional[bool] = Field(
        False, description="Boolean flag (purpose not specified in the given content)."
    )
    iouts: Optional[int] = Field(11, description="Number of output stations.")
    nouts: Optional[list] = Field(
        ["P-1", "P-2", "P-3", "P-4", "P-5", "P-6", "P-7", "P-8", "P-9", "P-10", "P-11"],
        description="Names of output stations.",
    )
    xouts: Optional[list] = Field(
        [
            -76.046,
            -76.778,
            -75.81,
            -75.72,
            -74.842,
            -74.703,
            -75.33,
            -72.631,
            -74.835,
            -69.248,
            -72.6,
        ],
        description="X-coordinates of output stations.",
    )
    youts: Optional[list] = Field(
        [
            39.152,
            38.556,
            38.033,
            37.551,
            36.974,
            37.204,
            37.023,
            36.915,
            36.611,
            38.461,
            35.75,
        ],
        description="Y-coordinates of output stations.",
    )
    cutoff: Optional[list] = Field(
        [15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15],
        description="Cutoff frequency (Hz) for each station, consistent with buoys.",
    )
    lsp1d: Optional[bool] = Field(
        True, description="Enable 1D spectral station output."
    )
    lsp2d: Optional[bool] = Field(
        False, description="Enable 2D spectral station output."
    )
    lsigmax: Optional[bool] = Field(
        True,
        description="Adjust the cut-off frequency for the output (e.g., consistent with buoy cut-off frequency).",
    )
    ac: Optional[bool] = Field(False, description="spectrum")
    wk: Optional[bool] = Field(False, description="variable WK")
    acout_1d: Optional[bool] = Field(False, description="variable ACOUT_1D")
    acout_2d: Optional[bool] = Field(False, description="variable ACOUT_2D")
    hs: Optional[bool] = Field(False, description="significant wave height")
    tm01: Optional[bool] = Field(False, description="mean period")
    tm02: Optional[bool] = Field(False, description="zero-crossing mean period")
    klm: Optional[bool] = Field(False, description="mean wave number")
    wlm: Optional[bool] = Field(False, description="mean wave length")
    etotc: Optional[bool] = Field(False, description="Variable ETOTC")
    etots: Optional[bool] = Field(False, description="Variable ETOTS")
    dm: Optional[bool] = Field(False, description="mean wave direction")
    dspr: Optional[bool] = Field(False, description="directional spreading")
    tppd: Optional[bool] = Field(False, description="Discrete Peak Period")
    tpp: Optional[bool] = Field(False, description="Peak Period")
    cpp: Optional[bool] = Field(False, description="")
    wnpp: Optional[bool] = Field(False, description="peak wave number")
    cgpp: Optional[bool] = Field(False, description="peak group speed")
    kpp: Optional[bool] = Field(False, description="peak wave number")
    lpp: Optional[bool] = Field(False, description="peak")
    peakd: Optional[bool] = Field(False, description="peak direction")
    peakdspr: Optional[bool] = Field(False, description="peak directional spreading")
    dpeak: Optional[bool] = Field(False, description="")
    ubot: Optional[bool] = Field(False, description="")
    orbital: Optional[bool] = Field(False, description="")
    botexper: Optional[bool] = Field(False, description="")
    tmbot: Optional[bool] = Field(False, description="")
    ursell: Optional[bool] = Field(False, description="Ursell number")
    ufric: Optional[bool] = Field(False, description="air friction velocity")
    z0: Optional[bool] = Field(False, description="air roughness length")
    alpha_ch: Optional[bool] = Field(False, description="Charnoch coefficient for air")
    windx: Optional[bool] = Field(False, description="Wind in X direction")
    windy: Optional[bool] = Field(False, description="Wind in Y direction")
    cd: Optional[bool] = Field(False, description="Drag coefficient")
    currtx: Optional[bool] = Field(False, description="current in X direction")
    currty: Optional[bool] = Field(False, description="current in Y direction")
    watlev: Optional[bool] = Field(False, description="water level")
    watlevold: Optional[bool] = Field(
        False, description="water level at previous time step"
    )
    depdt: Optional[bool] = Field(False, description="change of water level in time")
    dep: Optional[bool] = Field(False, description="depth")
    tauw: Optional[bool] = Field(False, description="surface stress from the wave")
    tauhf: Optional[bool] = Field(False, description="high frequency surface stress")
    tautot: Optional[bool] = Field(False, description="total surface stress")
    stokessurfx: Optional[bool] = Field(
        False, description="Surface Stokes drift in X direction"
    )
    stokessurfy: Optional[bool] = Field(
        False, description="Surface Stokes drift in X direction"
    )
    stokesbarox: Optional[bool] = Field(
        False, description="Barotropic Stokes drift in X direction"
    )
    stokesbaroy: Optional[bool] = Field(
        False, description="Barotropic Stokes drift in Y direction"
    )
    rsxx: Optional[bool] = Field(False, description="RSXX potential of LH")
    rsxy: Optional[bool] = Field(False, description="RSXY potential of LH")
    rsyy: Optional[bool] = Field(False, description="RSYY potential of LH")
    cfl1: Optional[bool] = Field(False, description="CFL number 1")
    cfl2: Optional[bool] = Field(False, description="CFL number 2")
    cfl3: Optional[bool] = Field(False, description="CFL number 3")

    @field_validator("begtc")
    @classmethod
    def validate_begtc(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y%m%d.%H%M%S")
            return v
        except ValueError:
            raise ValueError("Invalid date format. Use yyyymmdd.hhmmss")

    @field_validator("deltc")
    @classmethod
    def validate_deltc(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("DELTC must be positive")
        return v

    @field_validator("unitc")
    @classmethod
    def validate_unitc(cls, v: str) -> str:
        if v.upper() != "SEC":
            raise ValueError("UNITC must be SEC")
        return v.upper()

    @field_validator("endtc")
    @classmethod
    def validate_endtc(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y%m%d.%H%M%S")
            return v
        except ValueError:
            raise ValueError("Invalid date format. Use yyyymmdd.hhmmss")

    @field_validator("definetc")
    @classmethod
    def validate_definetc(cls, v: int) -> int:
        return v

    @field_validator("outstyle")
    @classmethod
    def validate_outstyle(cls, v: str) -> str:
        if v.upper() not in ["NO", "STE", "NC"]:
            raise ValueError("OUTSTYLE must be NO, STE, or NC")
        return v.upper()

    @field_validator("multipleout")
    @classmethod
    def validate_multipleout(cls, v: int) -> int:
        if v not in [0, 1]:
            raise ValueError("MULTIPLEOUT must be 0 or 1")
        return v

    @field_validator("use_single_out")
    @classmethod
    def validate_use_single_out(cls, v: bool) -> bool:
        return v

    @field_validator("paramwrite")
    @classmethod
    def validate_paramwrite(cls, v: bool) -> bool:
        return v

    @field_validator("loutiter")
    @classmethod
    def validate_loutiter(cls, v: bool) -> bool:
        return v

    @field_validator("iouts")
    @classmethod
    def validate_iouts(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("IOUTS must be positive")
        return v

    @field_validator("nouts")
    @classmethod
    def validate_nouts(cls, v: List[str]) -> List[str]:
        return v

    @field_validator("xouts")
    @classmethod
    def validate_xouts(cls, v: List[float]) -> List[float]:
        return v

    @field_validator("youts")
    @classmethod
    def validate_youts(cls, v: List[float]) -> List[float]:
        return v

    @field_validator("cutoff")
    @classmethod
    def validate_cutoff(cls, v: List[float]) -> List[float]:
        if any(f <= 0 for f in v):
            raise ValueError("All cutoff frequencies must be positive")
        return v

    @field_validator("lsp1d")
    @classmethod
    def validate_lsp1d(cls, v: bool) -> bool:
        return v

    @field_validator("lsp2d")
    @classmethod
    def validate_lsp2d(cls, v: bool) -> bool:
        return v

    @field_validator("lsigmax")
    @classmethod
    def validate_lsigmax(cls, v: bool) -> bool:
        return v

    @model_validator(mode="after")
    def validate_simulation_time(self) -> "Model":
        start = datetime.strptime(self.begtc, "%Y%m%d.%H%M%S")
        end = datetime.strptime(self.endtc, "%Y%m%d.%H%M%S")
        if end <= start:
            raise ValueError("ENDTC must be later than BEGTC")
        return self

    @model_validator(mode="after")
    def validate_nouts_length(self) -> "Model":
        if len(self.nouts) != self.iouts:
            raise ValueError("Length of NOUTS must match IOUTS")
        return self

    @model_validator(mode="after")
    def validate_xouts_length(self) -> "Model":
        if len(self.xouts) != self.iouts:
            raise ValueError("Length of XOUTS must match IOUTS")
        return self

    @model_validator(mode="after")
    def validate_youts_length(self) -> "Model":
        if len(self.youts) != self.iouts:
            raise ValueError("Length of YOUTS must match IOUTS")
        return self

    @model_validator(mode="after")
    def validate_cutoff_length(self) -> "Model":
        if len(self.cutoff) != self.iouts:
            raise ValueError("Length of CUTOFF must match IOUTS")
        return self


class Petscoptions(NamelistBaseModel):
    ksptype: Optional[str] = Field(
        "LGMRES",
        description="Controls the solver used. Options include GMRES (Generalized Minimal Residual method), LGMRES (Augmented GMRES), DGMRES (Deflated GMRES), PGMRES (Pipelined GMRES), and KSPBCGSL (Enhanced BiCGStab(L) algorithm).",
    )
    rtol: Optional[float] = Field(
        1e-20,
        description="The relative convergence tolerance, representing the relative decrease in the residual norm.",
    )
    abstol: Optional[float] = Field(
        1e-20,
        description="The absolute convergence tolerance, representing the absolute size of the residual norm.",
    )
    dtol: Optional[float] = Field(
        10000.0, description="The divergence tolerance for the solver."
    )
    maxits: Optional[int] = Field(
        1000, description="The maximum number of iterations to use in the solver."
    )
    initialguessnonzero: Optional[bool] = Field(
        False,
        description="Indicates whether the initial guess for the iterative solver is nonzero (True) or zero (False).",
    )
    gmrespreallocate: Optional[bool] = Field(
        True,
        description="Determines if GMRES and FGMRES should preallocate all needed work vectors at initial setup (True) or allocate them in chunks when needed (False).",
    )
    pctype: Optional[str] = Field(
        "SOR",
        description="Controls the preconditioner used. Options include SOR (Successive Over Relaxation), ASM (Additive Schwarz Method), HYPRE (LLNL package hypre), SPAI (Sparse Approximate Inverse), and NONE (no preconditioning).",
    )

    @field_validator("ksptype")
    @classmethod
    def validate_ksptype(cls, v):
        valid_types = ["GMRES", "LGMRES", "DGMRES", "PGMRES", "KSPBCGSL"]
        if v.upper() not in valid_types:
            raise ValueError(f"KSPTYPE must be one of {valid_types}")
        return v.upper()

    @field_validator("rtol")
    @classmethod
    def validate_rtol(cls, v):
        if v <= 0:
            raise ValueError("RTOL must be greater than 0")
        return v

    @field_validator("abstol")
    @classmethod
    def validate_abstol(cls, v):
        if v <= 0:
            raise ValueError("ABSTOL must be greater than 0")
        return v

    @field_validator("dtol")
    @classmethod
    def validate_dtol(cls, v):
        if v <= 0:
            raise ValueError("DTOL must be greater than 0")
        return v

    @field_validator("maxits")
    @classmethod
    def validate_maxits(cls, v):
        if v <= 0:
            raise ValueError("MAXITS must be a positive integer")
        return v

    @field_validator("initialguessnonzero")
    @classmethod
    def validate_initialguessnonzero(cls, v):
        return v

    @field_validator("gmrespreallocate")
    @classmethod
    def validate_gmrespreallocate(cls, v):
        return v

    @field_validator("pctype")
    @classmethod
    def validate_pctype(cls, v):
        valid_types = ["SOR", "ASM", "HYPRE", "SPAI", "NONE"]
        if v.upper() not in valid_types:
            raise ValueError(f"PCTYPE must be one of {valid_types}")
        return v.upper()


class Nesting(NamelistBaseModel):
    listbegtc: Optional[str] = Field(
        "",
        description="Start time for the nested grid run. Format should match ListUNITC.",
    )
    listdeltc: Optional[str] = Field("ZERO", description="")
    listunitc: Optional[str] = Field(
        "",
        description="Time unit for ListBEGTC, ListDELTC, and ListENDTC. Should be a valid time unit string.",
    )
    listendtc: Optional[str] = Field(
        "",
        description="End time for the nested grid run. Format should match ListUNITC.",
    )
    listigridtype: Optional[int] = Field(
        0,
        description="Grid type for the nested grid. 0 for regular grid, 1 for irregular grid.",
    )
    listfilegrid: Optional[str] = Field(
        "", description="File name containing the nested grid information."
    )
    listfilebound: Optional[str] = Field(
        "", description="File name containing the nested grid boundary information."
    )
    listprefix: Optional[str] = Field(
        "", description="Prefix for output files from the nested grid run."
    )

    @field_validator("listbegtc")
    @classmethod
    def validate_listbegtc(cls, v):
        if not isinstance(v, str):
            raise ValueError("ListBEGTC must be a string")
        return v

    @field_validator("listunitc")
    @classmethod
    def validate_listunitc(cls, v):
        valid_units = ["", "SECONDS", "MINUTES", "HOURS", "DAYS"]
        if v.upper() not in valid_units:
            raise ValueError(f"ListUNITC must be one of {valid_units}")
        return v

    @field_validator("listendtc")
    @classmethod
    def validate_listendtc(cls, v):
        if not isinstance(v, str):
            raise ValueError("ListENDTC must be a string")
        return v

    @field_validator("listigridtype")
    @classmethod
    def validate_listigridtype(cls, v):
        if v not in [0, 1]:
            raise ValueError("ListIGRIDTYPE must be either 0 or 1")
        return v

    @field_validator("listfilegrid")
    @classmethod
    def validate_listfilegrid(cls, v):
        if not isinstance(v, str):
            raise ValueError("ListFILEGRID must be a string")
        return v

    @field_validator("listfilebound")
    @classmethod
    def validate_listfilebound(cls, v):
        if not isinstance(v, str):
            raise ValueError("ListFILEBOUND must be a string")
        return v

    @field_validator("listprefix")
    @classmethod
    def validate_listprefix(cls, v):
        if not isinstance(v, str):
            raise ValueError("ListPrefix must be a string")
        return v


class Wwminput(NamelistBaseModel):
    proc: Optional[Proc] = Field(default_factory=Proc)
    coupl: Optional[Coupl] = Field(default_factory=Coupl)
    grid: Optional[Grid] = Field(default_factory=Grid)
    init: Optional[Init] = Field(default_factory=Init)
    hotfile: Optional[Hotfile] = Field(default_factory=Hotfile)
    bouc: Optional[Bouc] = Field(default_factory=Bouc)
    engs: Optional[Engs] = Field(default_factory=Engs)
    nums: Optional[Nums] = Field(default_factory=Nums)
    history: Optional[History] = Field(default_factory=History)
    station: Optional[Station] = Field(default_factory=Station)
    petscoptions: Optional[Petscoptions] = Field(default_factory=Petscoptions)
    nesting: Optional[Nesting] = Field(default_factory=Nesting)
