#!/usr/bin/env python

__author__    = "David Dotson <dotsdl@gmail.com>"
__license__   = "MIT"

from radical.ensemblemd.exceptions import NoKernelConfigurationError
from radical.ensemblemd.kernel_plugins.kernel_base import KernelBase

_KERNEL_INFO = {
    "name":         "beckstein.gromacs-5_1_1",
    "description":  "A kernel for executing gromacs jobs on remote clusters using Beckstein Lab builds.",
    "arguments":   {"--grompp=":
                        {
                            "mandatory": True,
                            "description": "Input parameter filename"
                        },
                    "--topol=":
                        {
                            "mandatory": True,
                            "description": "Topology filename"
                        }
                    },
    "machine_configs": {
        "xsede.stampede":
        {
            "environment" : {},
            "pre_exec" : ["module purge",
                          "module load gcc/4.9.1",
                          "module load mvapich2/2.1",
                          "module load python",
                          "source /home1/02142/dldotson/Library/gromacs/versions/gromacs-5.1.1/gcc-4.9.1/mvapich2-2.1/fftw3-3.3.4/cuda-6.5/bin/GMXRC.bash"],
            "executable" : ["python"],
            "uses_mpi"   : True
        },

    }
}

gmx_versions = 


def use_build(gmx_version):
    """Select which gromacs version to use, and get back a Kernel with the
    correct configuration to use it.

    Parameters
    ----------
    gmx_version : string
        string giving the version, e.g. '5.1.1' of gromacs to use

    """
    

class Kernel(KernelBase):

    def __init__(self):
        super(Kernel, self).__init__(_KERNEL_INFO)

    def _bind_to_resource(self, resource_key):
        if resource_key not in _KERNEL_INFO["machine_configs"]:
            raise NoKernelConfigurationError(kernel_name=_KERNEL_INFO["name"], resource_key=resource_key)

        cfg = _KERNEL_INFO["machine_configs"][resource_key]

        arguments = ['run.py',
                     '--mdp',
                     '{}'.format(self.get_arg("--grompp=")),
                     '--gro',
                     'start.gro',
                     '--top','{}'.format(self.get_arg('--topol=')),
                     '--out',
                     'out.gro']

        self._executable  = cfg["executable"]
        self._arguments   = arguments
        self._environment = cfg["environment"]
        self._uses_mpi    = cfg["uses_mpi"]
        self._pre_exec    = cfg["pre_exec"]
