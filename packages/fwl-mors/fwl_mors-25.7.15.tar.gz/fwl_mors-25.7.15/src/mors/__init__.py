
__version__ = "25.07.15"

# The basic Star class that people should be using
from .star import Star , Percentile

# The basic Cluster class that people should be using
from .cluster import Cluster

# Parameters
from .parameters import PrintParams , NewParams

# Useful function for stellar evolution stuff
from .stellarevo import StarEvo , Value , LoadTrack

# Stellar evolution basic quantities
from .stellarevo import ( Rstar , Lbol , Teff , Itotal , Icore , Ienv , Mcore , Menv , Rcore , tauConv ,
                         dItotaldt , dIcoredt , dIenvdt , dIenvdt , dMcoredt , dRcoredt )

# Functions from physical model
from .physicalmodel import ( dOmegadt , RotationQuantities , ExtendedQuantities , Lxuv , Lx , Leuv , Lly ,
                            OmegaSat , ProtSat , MdotFactor , OmegaBreak , XrayScatter , XUVScatter , aOrbHZ )

# Rotational evolution stuff
from .rotevo import EvolveRotation , EvolveRotationStep

# Spectral synthesis
from .synthesis import *

# Data download
from .data import DownloadEvolutionTracks

# Baraffe tracks
from .baraffe import *

# Spectrum stuff
from .spectrum import *

# Some other stuff
from .miscellaneous import Load , ModelCluster , ActivityLifetime , IntegrateEmission
