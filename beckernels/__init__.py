"""A library of `radical.ensemblemd` kernels specific to Beckstein Lab resources.

"""
from radical.ensemblemd.engine.kernel_registry import kernel_registry

# register our kernels with radical.ensemblemd so that calling by name in
# Kernel constructor works

_kernels = ['beckernels.dmdmd.gromacs',
            'beckernels.dmdmd.lsdmap',
            'beckernels.dmdmd.grompp',
            'beckernels.dmdmd.mdrun',
            'beckernels.dmdmd.pre_grlsd_loop',
            'beckernels.dmdmd.pre_lsdmap',
            'beckernels.dmdmd.post_lsdmap']

kernel_registry.extend(_kernels)
