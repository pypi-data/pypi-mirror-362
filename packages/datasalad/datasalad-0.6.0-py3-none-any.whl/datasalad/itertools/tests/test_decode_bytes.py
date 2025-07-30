from __future__ import annotations

import pytest

from ..decode_bytes import decode_bytes


def test_split_decoding():
    encoded = 'ö'.encode()
    part_1, part_2 = encoded[:1], encoded[1:]

    # check that incomplete encodings are caught
    r = tuple(decode_bytes([b'abc' + part_1, part_2 + b'def']))
    assert ''.join(r) == 'abcödef'


def test_unfixable_error_decoding():
    encoded = 'ö'.encode()
    part_1, part_2 = encoded[:1], encoded[1:]

    # check that incomplete encodings are caught
    r = tuple(decode_bytes([b'abc' + part_1 + b'def' + part_1, part_2 + b'ghi']))
    assert ''.join(r) == 'abc\\xc3deföghi'


def test_single_undecodable_byte():
    # check that a single undecodable byte is handled properly
    r = tuple(decode_bytes([b'\xc3']))
    assert ''.join(r) == '\\xc3'
    with pytest.raises(UnicodeDecodeError):
        tuple(decode_bytes([b'\xc3'], backslash_replace=False))


def test_no_empty_strings():
    # check that empty strings are not yielded
    r = tuple(decode_bytes([b'\xc3', b'\xb6']))
    assert r == ('ö',)


def test_multiple_errors():
    r = ''.join(decode_bytes([b'08 War \xaf No \xaf More \xaf Trouble.shn.mp3']))
    assert r == '08 War \\xaf No \\xaf More \\xaf Trouble.shn.mp3'


def test_error_chunks():
    # this verifies that error handling in a previous chunk does not
    # cause data loss in a subsequent chunk
    r = ''.join(decode_bytes([b'08 War \xaf No', b'1234567890']))
    assert r == '08 War \\xaf No1234567890'
