#!/usr/bin/env python


"""Required kernel for the pre-analysis component of LSDmap directed MD. This mostly
just sets up the environment, then runs `pre_analyze.py` which generates a combined
gro file from all the simulation end points, which is needed for lsdmap.

Credit to Vivek Balasubramanian for the original content this is based on.

"""

__author__    = "David Dotson <dotsdl@gmail.com>"
__license__   = "MIT"

from radical.ensemblemd.exceptions import NoKernelConfigurationError
from radical.ensemblemd.kernel_plugins.kernel_base import KernelBase

_KERNEL_INFO = {
    "name":         "beckstein.pre_lsdmap",
    "description":  "Generate combined gro file of all simulation end points for lsdmap.",
    "arguments":   {"--numCUs=":
                        {
                            "mandatory": True,
                            "description": "No. of CUs"
                        }
                    },
    "machine_configs":
    {
        "xsede.stampede":
        {
            "environment" : {},
            "pre_exec" : ["module purge",
                          "module load gcc/4.9.1",
                          "module load mvapich2/2.1",
                          "module load python",
                          "source /home1/02142/dldotson/Library/gromacs/versions/gromacs-5.1.1/gcc-4.9.1/mvapich2-2.1/fftw3-3.3.4/cuda-6.5/bin/GMXRC.bash"],
            "executable" : ["python"],
            "uses_mpi"   : False
        },
    }
}


class Kernel(KernelBase):

    def __init__(self):
        super(Kernel, self).__init__(_KERNEL_INFO)

    @staticmethod
    def get_name():
        return _KERNEL_INFO["name"]

    def _bind_to_resource(self, resource_key):
        if resource_key not in self._info["machine_configs"]:
            raise NoKernelConfigurationError(kernel_name=self._info["name"], resource_key=resource_key)

        cfg = self._info["machine_configs"][resource_key]

        arguments = ['pre_analyze.py','{0}'.format(self.get_arg("--numCUs=")),'tmp.gro','.'] 

        self._executable  = cfg["executable"]
        self._arguments   = arguments
        self._environment = cfg["environment"]
        self._uses_mpi    = cfg["uses_mpi"]
        self._pre_exec    = cfg["pre_exec"]
