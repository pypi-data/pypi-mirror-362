"""Unit tests for KDF utilities."""

from hashlib import sha256

import pytest
from openpgpcard_x25519_agent.kdf import (
    KDF_ITERSALTED_S2K,
    NONE,
    SHA256,
    SHA512,
    Kdf,
    KdfError,
)


def test_parse_none():
    kdf = Kdf().parse(None)
    assert kdf.algorithm == NONE
    assert kdf.hash_fn == SHA256
    assert kdf.iterations == 0
    assert kdf.salt == b""


def test_parse_empty():
    kdf = Kdf().parse([])
    assert kdf.algorithm == NONE
    assert kdf.hash_fn == SHA256
    assert kdf.iterations == 0
    assert kdf.salt == b""


def test_parse_garbage():
    with pytest.raises(KdfError, match="not a KDF DO"):
        Kdf().parse([1, 2, 3, 4, 5, 6])


def test_parse_unknown():
    with pytest.raises(KdfError, match="unknown KDF algorithm: 0x1"):
        Kdf().parse(bytearray.fromhex("81 01 01 82 01 08"))


def test_parse_none_do():
    kdf = Kdf().parse(bytearray.fromhex("81 01 00"))
    assert kdf.algorithm == NONE
    assert kdf.hash_fn == SHA256
    assert kdf.iterations == 0
    assert kdf.salt == b""


def test_parse_minimal_do():
    do = """
81 01 03
82 01 08
83 04 00000400
84 08 7465737473616C74
"""
    kdf = Kdf().parse(bytearray.fromhex(do))
    assert kdf.algorithm == KDF_ITERSALTED_S2K
    assert kdf.hash_fn == SHA256
    assert kdf.iterations == 0x400
    assert kdf.salt == b"testsalt"


def test_parse_full_do():
    do = """
81 01 03
82 01 0A
83 04 03E00000
84 08 7573657273616C74
85 08 50554B2053414C54
86 08 73613461646D696E
87 20 AD99174F8F4BD1A8F75FA50BD9FF9B9631478268299B50D4082651D62331D46B
88 20 0F06EF103FA635FE1BC43A691F1DAD7A9EB37BBE77AA366D420968CB60F2A7A2
"""
    kdf = Kdf().parse(bytearray.fromhex(do))
    assert kdf.algorithm == KDF_ITERSALTED_S2K
    assert kdf.hash_fn == SHA512
    assert kdf.iterations == 0x03E00000
    assert kdf.salt == b"usersalt"


def test_derive_none():
    assert Kdf().derive(b"foo") == b"foo"


def test_derive_unknown():
    with pytest.raises(KdfError, match="unknown KDF algorithm: 0x63"):
        Kdf(99).derive(b"foo")


# 1-3 from libgcrypt tests/t-kdf.c
# 4 from openpgp card functional spec
@pytest.mark.parametrize(
    ("algorithm", "hash_fn", "count", "salt", "pin", "key"),
    [
        (
            KDF_ITERSALTED_S2K,
            SHA256,
            1024,
            "D34AEAC9971BCC83",
            b"Long_sentence_used_as_passphrase",
            "35379962072668230547B2A00B2B2B8D",
        ),
        (
            KDF_ITERSALTED_S2K,
            SHA256,
            10240,
            "5E71BD005F96C423",
            b"Long_sentence_used_as_passphrase",
            "A16AEEBADE732525D1ABA0C57EC639A7",
        ),
        (
            KDF_ITERSALTED_S2K,
            SHA512,
            1024,
            "E67D136B39E34405",
            b"Long_sentence_used_as_passphrase",
            "C8CD4BA4F3F1D5B05906F0BB89346AAD",
        ),
        (
            KDF_ITERSALTED_S2K,
            SHA256,
            100_000,
            "3031323334353637",
            b"123456",
            "773784A602B6C81E3F092F4D7D00E17CC822D88F7360FCF2D2EF2D9D901F44B6",
        ),
    ],
)
def test_derive_kdf_itersalted_s2k(algorithm, hash_fn, count, salt, pin, key):
    if isinstance(salt, str):
        salt = bytearray.fromhex(salt)
    if isinstance(pin, str):
        pin = bytearray.fromhex(pin)
    if isinstance(key, str):
        key = bytearray.fromhex(key)

    derived = Kdf(algorithm, hash_fn, count, salt).derive(pin)
    assert derived[: len(key)].hex() == key.hex()


def test_derive_kdf_itersalted_s2k_with_less_iterations_than_bytes():
    expected = sha256(b"testsalt123456").digest()
    actual = Kdf(KDF_ITERSALTED_S2K, SHA256, 3, b"testsalt").derive(b"123456")
    assert actual.hex() == expected.hex()


def test_derive_kdf_itersalted_s2k_with_no_remainder():
    expected = sha256(b"testsalt123456").digest()
    actual = Kdf(KDF_ITERSALTED_S2K, SHA256, 14, b"testsalt").derive(b"123456")
    assert actual.hex() == expected.hex()


def test_derive_kdf_itersalted_s2k_with_salt_only_remainder():
    expected = sha256(b"testsalt123456tes").digest()
    actual = Kdf(KDF_ITERSALTED_S2K, SHA256, 17, b"testsalt").derive(b"123456")
    assert actual.hex() == expected.hex()


def test_derive_kdf_itersalted_s2k_with_multiple_iterations_and_pin_remainder():
    expected = sha256(b"testsalt123456testsalt123456testsalt123").digest()
    actual = Kdf(KDF_ITERSALTED_S2K, SHA256, 39, b"testsalt").derive(b"123456")
    assert actual.hex() == expected.hex()


def test_derive_derive_kdf_itersalted_s2k_with_unknown_hash():
    with pytest.raises(KdfError, match="unknown hash algorithm: 0x63"):
        Kdf(KDF_ITERSALTED_S2K, 99).derive(b"foo")


def test_describe_none():
    assert str(Kdf()) == "None"


def test_describe_unknown():
    assert str(Kdf(99)) == "0x63"


def test_describe_kdf_itersalted_s2k_with_defaults():
    assert (
        str(Kdf(KDF_ITERSALTED_S2K)) == "S2K (0 iterations of SHA-256 with 0-byte salt)"
    )


def test_describe_kdf_itersalted_s2k_with_unknown_hash():
    assert (
        str(Kdf(KDF_ITERSALTED_S2K, 0x21))
        == "S2K (0 iterations of hash algorithm 0x21 with 0-byte salt)"
    )


def test_describe_kdf_itersalted_s2k_with_customized():
    assert (
        str(Kdf(KDF_ITERSALTED_S2K, SHA512, 0x03E00000, b"testsalt"))
        == "S2K (65,011,712 iterations of SHA-512 with 8-byte salt)"
    )
