"""CommandError exception class for handling subprocess execution failures"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import os

import signal
import subprocess
import sys


class CommandError(subprocess.CalledProcessError, RuntimeError):
    """Raised when a subprocess execution fails (non-zero exit)

    This custom exception combines the functionality of ``subprocess.CalledProcessError`` and
    ``RuntimeError``. It provides additional features like context messages (msg) and current working
    directory (cwd) tracking.

    Args:
        cmd: The command that was executed (either as a string or list of strings)
        msg: Optional contextual message explaining why the command was executed or failure context
        returncode: Optional return code of the failed command (default: ``CommandError.UNKNOWN_RETURNCODE``)
        stdout: Optional standard output from the command
        stderr: Optional standard error from the command
        cwd: Optional current working directory where the command was executed

    Attributes:
        msg: Additional contextual information about the error
        cwd: The working directory where the command was executed
        cmd: The command that was executed
        returncode: The command's exit code
        stdout: Standard output from the command
        stderr: Standard error from the command

    Examples:
        >>> raise CommandError('mycmd')
        Traceback (most recent call last):
          ...
        datasalad.runners.exception.CommandError: Command 'mycmd' errored with unknown exit status

        A more complex example:

        >>> raise CommandError('invalid', msg='intentional blow', returncode=23)
        Traceback (most recent call last):
          ...
        datasalad.runners.exception.CommandError: Command 'invalid' returned non-zero exit status 23 [intentional blow]

    """

    UNKNOWN_RETURNCODE = 32767

    def __init__(
        self,
        cmd: str | list[str],
        msg: str = '',
        returncode: int = UNKNOWN_RETURNCODE,
        stdout: str | bytes = '',
        stderr: str | bytes = '',
        cwd: str | os.PathLike | None = None,
    ) -> None:
        RuntimeError.__init__(self, msg)
        subprocess.CalledProcessError.__init__(
            self,
            returncode=returncode,
            cmd=cmd,
            output=stdout,
            stderr=stderr,
        )
        self.msg = msg
        self.cwd = cwd

    def __str__(self) -> str:
        # we report the command verbatim, in exactly the form that it has
        # been given to the exception. Previously implementation have
        # beautified output by joining list-format commands with shell
        # quoting. However that implementation assumed that the command
        # actually run locally. In practice, CommandError is also used
        # to report on remote command execution failure. Reimagining
        # quoting and shell conventions based on assumptions is confusing.
        to_str = f'Command {self.cmd!r}'
        if self.returncode and self.returncode < 0:
            try:
                to_str += f' died with {signal.Signals(-self.returncode).name}'
            except ValueError:
                to_str += f' died with unknown signal {-self.returncode}'
        elif self.returncode == CommandError.UNKNOWN_RETURNCODE:
            to_str += ' errored with unknown exit status'
        elif self.returncode:
            to_str += f' returned non-zero exit status {self.returncode}'
        if self.cwd:
            # only if not under standard PWD
            to_str += f' at CWD {self.cwd}'
        if self.msg:
            # typically a command error has no specific idea
            # but we support it, because CommandError derives
            # from RuntimeError which has this feature.
            to_str += f' [{self.msg}]'

        if not self.stderr:
            return to_str

        # make an effort to communicate stderr
        stderr = ''
        if isinstance(self.stderr, bytes):
            # assume that the command output matches the local system
            # encoding
            try:
                # we need to try conversion on the full bytestring to
                # avoid alignment issues with random splits
                stderr = self.stderr.decode(sys.getdefaultencoding())
            except UnicodeDecodeError:
                # we tried, we failed, sorry
                # we are not guessing other encodings. If it doesn't
                # match the system encoding, it is somewhat unlikely
                # to be an informative error message.
                stderr = f'<undecodable {truncate_bytes(self.stderr)}>'
        else:
            stderr = self.stderr

        to_str += f' [stderr: {truncate_str(stderr, (60, 0))}]'

        return to_str

    def __repr__(self) -> str:
        descr = f'{self.__class__.__name__}({self.cmd!r}'
        for kwarg, (val, default) in {
            'msg': (self.msg, ''),
            'returncode': (self.returncode, CommandError.UNKNOWN_RETURNCODE),
            'stdout': (self.stdout, ''),
            'stderr': (self.stderr, ''),
            'cwd': (self.cwd, None),
        }.items():
            if val == default:
                continue
            if kwarg in ('stdout', 'stderr'):
                if TYPE_CHECKING:
                    assert isinstance(val, (str, bytes))
                if isinstance(val, bytes):
                    descr += f", {kwarg}=b'<{truncate_bytes(val)}>'"
                else:
                    descr += f', {kwarg}={truncate_str(val)!r}'
            else:
                descr += f', {kwarg}={val!r}'
        descr += ')'
        return descr


def truncate_bytes(data: bytes) -> str:
    """Describe the length of a byte string.

    Args:
        data: The bytes object

    Returns:
        A string showing the length of the bytes object
    """
    return f'{len(data)} bytes'


def truncate_str(text: str, keep: tuple[int, int] = (20, 20)) -> str:
    """Truncate a string while preserving the beginning and end parts.

    Args:
        text: The string to truncate
        keep: A tuple specifying the number of characters to keep from the start and end
              (default: (20, 20))

    Returns:
        A truncated string with the specified number of characters from the start and end
    """
    # truncation like done below only actually shortens beyond
    # 60 chars input length
    front, back = keep
    if len(text) < (front + back + 14):
        # stringify only
        return f'{text}'
    return (
        f"{text[:front]}<... +{len(text) - front - back} chars>"
        f"{text[-back:] if back > 0 else ''}"
    )
