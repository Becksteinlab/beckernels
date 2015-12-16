#!/usr/bin/env python

"""Required kernel for the analysis component of LSDmap directed MD. This mostly
just sets up the environment, then runs `lsdmap` on the combined coordinate files
from the end of each MD simulation to obtain new weights and distances used to generate
new starting points in the post_loop.

Credit to Vivek Balasubramanian for the original content this is based on.

"""

__author__    = "David Dotson <dotsdl@gmail.com>"
__license__   = "MIT"

from radical.ensemblemd.exceptions import NoKernelConfigurationError
from radical.ensemblemd.kernel_plugins.kernel_base import KernelBase

_KERNEL_INFO = {
    "name":         "beckstein.lsdmap",
    "description":  "A kernel for performing the analysis component of LSDmap directed MD.",
    "arguments":   {"--config=":
                        {
                            "mandatory": True,
                            "description": "Config filename"
                        },
                    },
    "machine_configs":
    {
        "xsede.stampede":
        {
            "environment" : {},
            "pre_exec" : [      
                            "module load TACC",
                            "module load -intel +intel/14.0.1.106",
                            "export PYTHONPATH=/home1/02142/dldotson/.local/lib/python2.7/site-packages",
                            "module load python/2.7.6",
                            "export PATH=/home1/02142/dldotson/.local/bin:$PATH"],
            "executable": ["lsdmap"],
            "uses_mpi"   : True
        },
    }
}


class Kernel(KernelBase):

    def __init__(self):
        super(Kernel, self).__init__(_KERNEL_INFO)

    def _bind_to_resource(self, resource_key):
        if resource_key not in self._info["machine_configs"]:
            raise NoKernelConfigurationError(kernel_name=self._info["name"], resource_key=resource_key)

        cfg = self._info["machine_configs"][resource_key]

        arguments = ['-f','{0}'.format(self.get_arg("--config=")),'-c','tmpha.gro','-n','out.nn','-w','weight.w']

        self._executable  = cfg["executable"]
        self._arguments   = arguments
        self._environment = cfg["environment"]
        self._uses_mpi    = cfg["uses_mpi"]
        self._pre_exec    = cfg["pre_exec"]
