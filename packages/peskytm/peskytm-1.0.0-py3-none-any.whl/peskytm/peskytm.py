
from typing import List
from typing import NewType

from logging import Logger
from logging import getLogger

from os import linesep as osLineSep

from sys import version as pyVersion

from subprocess import run
from subprocess import CompletedProcess

from click import command
from click import version_option

__version__:   str = "0.1.0"
__pyVersion__: str = pyVersion.split(" ")[0]

MOUNT_COMMAND:   str = 'mount'
UNMOUNT_COMMAND: str = ''

UTF8_ENCODING: str = 'utf-8'

CommandOutput      = NewType('CommandOutput',    List[str])
TimeMachineLines   = NewType('TimeMachineLines', List[str])
TimeMachineVolumes = NewType('TimeMachineVolumes', List[str])


class UnMountTimeMachine:
    def __init__(self):

        self.logger: Logger = getLogger(__name__)

    def execute(self):
        commandOutput:    CommandOutput        = self._runExternalMountCommand()
        timeMachineLines: TimeMachineLines     = self._extractTimeMachineLines(commandOutput)
        timeMachineVolumes: TimeMachineVolumes = self._extractTimeMachineVolumes(timeMachineLines)

        [self.logger.debug(volume) for volume in timeMachineVolumes]

        self._unMountTimeMachineVolumes(timeMachineVolumes)

    def _runExternalMountCommand(self) -> CommandOutput:

        cp: CompletedProcess = run([MOUNT_COMMAND], capture_output=True, encoding=UTF8_ENCODING)
        output: CommandOutput = cp.stdout.split(osLineSep)

        return output

    def _extractTimeMachineLines(self, output: CommandOutput) -> TimeMachineLines:

        tmLines: TimeMachineLines = TimeMachineLines([])
        for mountLine in output:
            if mountLine.startswith('com.apple.TimeMachine'):
                tmLines.append(mountLine)

        return tmLines

    def _extractTimeMachineVolumes(self, tmLines: TimeMachineLines) -> TimeMachineVolumes:

        timeMachineVolumes: TimeMachineVolumes = TimeMachineVolumes([])
        for tmLine in tmLines:
            parsedTM: List[str] = tmLine.split(' ')
            timeMachineVolumes.append(parsedTM[0])

        return timeMachineVolumes

    def _unMountTimeMachineVolumes(self, timeMachineVolumes: TimeMachineVolumes):

        for fsToUnMount in timeMachineVolumes:
            print(f'Unmount {fsToUnMount}')
            cp: CompletedProcess = run(['sudo', 'umount', fsToUnMount], capture_output=True, encoding="utf-8")
            if cp.returncode == 0:
                print(f'{fsToUnMount} unmounted')
            else:
                print(f'Unmount error: {cp.returncode=}')
                print(f'{cp.stdout=}')


@command()
@version_option(prog_name='peskytm', version=f'{__version__} - Python: {__pyVersion__}')
def commandHandler():
    um: UnMountTimeMachine = UnMountTimeMachine()
    um.execute()


if __name__ == "__main__":

    commandHandler()
