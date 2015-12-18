"""A library of `radical.ensemblemd` kernels specific to Beckstein Lab resources.

"""
from radical.ensemblemd.engine.kernel_registry import kernel_registry

# register our kernels with radical.ensemblemd so that calling by name in
# Kernel constructor works

_kernels = ['beckernels.lsdmap.gromacs',
            'beckernels.lsdmap.lsdmap',
            'beckernels.lsdmap.pre_grlsd_loop',
            'beckernels.lsdmap.pre_lsdmap',
            'beckernels.lsdmap.post_lsdmap']

kernel_registry.extend(_kernels)
