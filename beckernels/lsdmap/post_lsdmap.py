#!/usr/bin/env python

"""Required kernel for the post-analysis component of LSDmap directed MD. This mostly
just sets up the environment, then runs `post_analyze.py` on outputs of the
lsdmap analysis to create the new coordinate files as starting points for each new
simulation.

Credit to Vivek Balasubramanian for the original content this is based on.

"""

__author__    = "David Dotson <dotsdl@gmail.com>"
__license__   = "MIT"

from radical.ensemblemd.exceptions import NoKernelConfigurationError
from radical.ensemblemd.kernel_plugins.kernel_base import KernelBase

_KERNEL_INFO = {
    "name":         "beckstein.post_lsdmap",
    "description":  "Generate starting points for next iteration of simulations.",
    "arguments":   {"--num_runs=":
                        {
                            "mandatory": True,
                            "description": "Number of runs to be generated in output file"
                        },
                    "--out=":
                        {
                            "mandatory": True,
                            "description": "Output filename"
                        },
                    "--cycle=":
                        {
                            "mandatory": True,
                            "description": "Current iteration"
                        },
                    "--max_dead_neighbors=":
                        {
                            "mandatory": True,
                            "description": "Max dead neighbors to be considered"
                        },
                    "--max_alive_neighbors=":
                        {
                            "mandatory": True,
                            "description": "Max alive neighbors to be considered"
                        },
                    "--numCUs=":
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
            "pre_exec" : ["module load TACC","module load python",
            "export PYTHONPATH=/home1/02142/dldotson/.local/lib/python2.7/site-packages:$PYTHONPATH",
            "export PYTHONPATH=/home1/02142/dldotson/.local/lib/python2.7/site-packages/lsdmap/rw:$PYTHONPATH",
            "export PYTHONPATH=/home1/02142/dldotson/.local/lib/python2.7/site-packages/util:$PYTHONPATH"],
            "executable" : ["python"],
            "uses_mpi"   : False
        }

    }
}


class Kernel(KernelBase):

    def __init__(self):
        super(Kernel, self).__init__(_KERNEL_INFO)

    def _bind_to_resource(self, resource_key):
        """(PRIVATE) Implements parent class method.
        """
        if resource_key not in self._info["machine_configs"]:
            raise NoKernelConfigurationError(kernel_name=self._info["name"], resource_key=resource_key)

        cfg = self._info["machine_configs"][resource_key]

        arguments = ['post_analyze.py','{0}'.format(self.get_arg("--num_runs=")),'tmpha.ev','ncopies.nc','tmp.gro'
                     ,'out.nn','weight.w','{0}'.format(self.get_arg("--out="))
                     ,'{0}'.format(self.get_arg("--max_alive_neighbors=")),'{0}'.format(self.get_arg("--max_dead_neighbors="))
                     ,'input.gro','{0}'.format(self.get_arg("--cycle=")),'{0}'.format(self.get_arg('--numCUs='))
                     ]

        self._executable  = cfg["executable"]
        self._arguments   = arguments
        self._environment = cfg["environment"]
        self._uses_mpi    = cfg["uses_mpi"]
        self._pre_exec    = cfg["pre_exec"]
