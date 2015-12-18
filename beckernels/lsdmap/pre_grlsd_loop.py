#!/usr/bin/env python

"""Required kernel for the pre-loop component of LSDmap directed MD. This mostly
just sets up the environment, then runs `splitter.py` to generate gro files
for each run in the simulation step from the starting gro file.

Credit to Vivek Balasubramanian for the original content this is based on.

"""

__author__    = "David Dotson <dotsdl@gmail.com>"
__license__   = "MIT"

from radical.ensemblemd.exceptions import NoKernelConfigurationError
from radical.ensemblemd.kernel_plugins.kernel_base import KernelBase

_KERNEL_INFO = {
    "name":         "beckstein.pre_grlsd_loop",
    "description":  "Splits the inputfile into 'numCUs' number of smaller files ",
    "arguments":   {"--inputfile=":
                        {
                            "mandatory": True,
                            "description": "Input filename"
                        },
                    "--numCUs=":
                        {
                            "mandatory": True,
                            "description": "No. of files to be generated"
                        }
                    },
    "machine_configs":
    {
        "xsede.stampede": {
            "environment"   : {},
            "pre_exec"      : ["module load TACC","module load python"],
            "executable"    : "python",
            "uses_mpi"      : False
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
        """(PRIVATE) Implements parent class method.
        """
        if resource_key not in _KERNEL_INFO["machine_configs"]:
            raise NoKernelConfigurationError(kernel_name=_KERNEL_INFO["name"], resource_key=resource_key)

        cfg = _KERNEL_INFO["machine_configs"][resource_key]

        arguments = ['splitter.py','{0}'.format(self.get_arg("--numCUs=")), '{0}'.format(self.get_arg("--inputfile="))]

        self._executable  = cfg["executable"]
        self._arguments   = arguments
        self._environment = cfg["environment"]
        self._uses_mpi    = cfg["uses_mpi"]
        self._pre_exec    = cfg["pre_exec"]

