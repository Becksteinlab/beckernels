#!/usr/bin/env python

"""Kernel for producing a run-input file from a set of input files using grompp.

"""

__author__    = "David Dotson <dotsdl@gmail.com>"
__license__   = "MIT"

from radical.ensemblemd.exceptions import NoKernelConfigurationError
from radical.ensemblemd.kernel_plugins.kernel_base import KernelBase

_KERNEL_INFO = {
    "name":         "beckstein.grompp",
    "description":  "A kernel for building gromacs run input files using Beckstein Lab builds.",
    "arguments":   {
                        "--f=":
                        {
                            "mandatory": True,
                            "description": "mdp file"
                        },
                        "--p=":
                        {
                            "mandatory": True,
                            "description": "top file"
                        },
                        "--c=":
                        {
                            "mandatory": True,
                            "description": "structure file"
                        },
                        "--n=":
                        {
                            "mandatory": True,
                            "description": "index file"
                        },
                        "--maxwarn=":
                        {
                            "mandatory": True,
                            "description": "maximum number of warnings"
                        },
                        "--o=":
                        {
                            "mandatory": True,
                            "description": "output tpr file name"
                        },
                    },

    "machine_configs": 
            {
                "xsede.stampede":
                {
                    "environment" : {},
                    "pre_exec" : ["module purge",
                                  "module load gcc/4.9.1",
                                  "module load python",
                                  "source /home1/02142/dldotson/Library/gromacs/versions/gromacs-5.1.1/gcc-4.9.1/mvapich2-2.1/fftw3-3.3.4/cuda-6.5/bin/GMXRC.bash"],
                    "executable" : ["gmx grompp"],
                    "uses_mpi"   : False
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

        arguments = ['-f', '{}'.format(self.get_arg("--f=")),
                     '-p', '{}'.format(self.get_arg("--p=")),
                     '-c', '{}'.format(self.get_arg("--c=")),
                     '-n', '{}'.format(self.get_arg("--n=")),
                     '-maxwarn', '{}'.format(self.get_arg("--maxwarn=")),
                     '-o', '{}'.format(self.get_arg("--o="))]


        self._executable  = cfg["executable"]
        self._arguments   = arguments
        self._environment = cfg["environment"]
        self._uses_mpi    = cfg["uses_mpi"]
        self._pre_exec    = cfg["pre_exec"]
