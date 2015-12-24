#!/usr/bin/env python

"""Kernel for running gromacs mdrun on a run-input file.

"""

__author__    = "David Dotson <dotsdl@gmail.com>"
__license__   = "MIT"

from radical.ensemblemd.exceptions import NoKernelConfigurationError
from radical.ensemblemd.kernel_plugins.kernel_base import KernelBase

_KERNEL_INFO = {
    "name":         "beckstein.mdrun",
    "description":  "",
    "arguments":   {
                        "--s=":
                        {
                            "mandatory": True,
                            "description": "tpr file"
                        },
                        "--stepout=":
                        {
                            "mandatory": True,
                            "description": "frequency of writouts to log"
                        },
                        "--deffnm=":
                        {
                            "mandatory": True,
                            "description": "default naming for all output files"
                        },
                        "--c=":
                        {
                            "mandatory": True,
                            "description": "name of output structure file"
                        },
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
                    "executable" : ["gmx_mpi mdrun"],
                    "uses_mpi"   : True
                }
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

        arguments = ['-s', '{}'.format(self.get_arg("--s=")),
                     '-stepout', '{}'.format(self.get_arg('--stepout=')),
                     '-deffnm', '{}'.format(self.get_arg('--deffnm=')),
                     '-c', '{}'.format(self.get_arg('--c=')),
                     '-v']

        self._executable  = cfg["executable"]
        self._arguments   = arguments
        self._environment = cfg["environment"]
        self._uses_mpi    = cfg["uses_mpi"]
        self._pre_exec    = cfg["pre_exec"]
