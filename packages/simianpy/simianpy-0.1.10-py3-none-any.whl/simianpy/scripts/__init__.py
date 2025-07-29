from simianpy.scripts.openephys import OpenEphys
from simianpy.scripts.nex import Nex
from simianpy.scripts.intan import Intan
from simianpy.scripts.trodes import Trodes
from simianpy.scripts.util import util
from simianpy.scripts.spiketrainset import SpikeTrain

import click

@click.group(invoke_without_command=True)
@click.option('-v','--version', is_flag=True)
def simi(version):
    if version:
        from simianpy import __version__
        print(__version__)

simi.add_command(Nex)
simi.add_command(Intan)
simi.add_command(OpenEphys)
simi.add_command(Trodes)
simi.add_command(util)
simi.add_command(SpikeTrain)
if __name__ == '__main__':
    simi()
