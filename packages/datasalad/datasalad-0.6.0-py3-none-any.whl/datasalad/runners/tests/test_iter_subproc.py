import sys

import pytest

from .. import (
    CommandError,
    iter_subproc,
)


def test_iter_subproc_cwd(tmp_path):
    test_content = 'some'
    test_file_name = 'testfile'
    test_file = tmp_path / test_file_name
    test_file.write_text(test_content)

    check_fx = (
        'import sys\n'
        f"if open('{test_file_name}').read() == '{test_content}':\n"
        "    print('okidoki')"
    )
    # we cannot read the test file without a full path, because
    # CWD is not `tmp_path`
    with pytest.raises(CommandError) as e:  # noqa PT012
        with iter_subproc([sys.executable, '-c', check_fx]):
            pass
        assert 'FileNotFoundError' in e.value

    # but if we make it change to CWD, the same code runs
    with iter_subproc([sys.executable, '-c', check_fx], cwd=tmp_path) as proc:
        out = b''.join(proc)
        assert b'okidoki' in out
