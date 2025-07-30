"""KDF utilities."""

from collections.abc import ByteString  # noqa: PYI057
from hashlib import sha256, sha512
from struct import unpack_from

# KDF algorithms
NONE = 0x00
KDF_ITERSALTED_S2K = 0x03

# hash algorithms
SHA256 = 0x08
SHA512 = 0x0A


class KdfError(Exception):
    """Signals an invalid KDF settings."""


class Kdf:
    """Key derivation function for the card PIN.

    Attributes:
        algorithm (int): KDF algorithm.
        hash_fn (int): Hash algorithm.
        iterations (int): Iteration count.
        salt (bytearray): Salt value.
    """

    def __init__(self, algorithm=NONE, hash_fn=SHA256, iterations=0, salt=None):
        """Intial settings for the KDF.

        Arguments:
            algorithm (int): KDF algorithm.
            hash_fn (int): Hash algorithm.
            iterations (int): Iteration count.
            salt (bytearray): Salt value.
        """
        self.algorithm = algorithm
        self.hash_fn = hash_fn
        self.iterations = iterations
        self.salt = salt or bytearray(0)

    def __str__(self):
        """Outputs human-friendly KDF info.

        Returns:
            str: KDF info.
        """
        if self.algorithm == NONE:
            return "None"
        if self.algorithm == KDF_ITERSALTED_S2K:
            return self.describe_kdf_itersalted_s2k()
        return f"{self.algorithm:#x}"

    def clear(self):
        """Resets KDF settings back to defaults.

        Returns:
            Kdf: Self.
        """
        self.__init__()
        return self

    def parse(self, data):
        """Loads the KDF settings from the specified card data object.

        Arguments:
            data (bytearray): KDF DO.

        Returns:
            Kdf: Self.

        Raises:
            KdfError: If invalid KDF DO.
        """
        if not data:
            return self.clear()
        if not isinstance(data, ByteString):
            data = bytearray(data)
        if data[:2] != bytes.fromhex("81 01"):
            raise KdfError("not a KDF DO")

        self.algorithm = data[2]
        if self.algorithm == NONE:
            return self.clear()
        if self.algorithm != KDF_ITERSALTED_S2K:
            raise KdfError(f"unknown KDF algorithm: {self.algorithm:#x}")

        self.hash_fn = data[5]
        self.iterations = unpack_from(">I", data, 8)[0]
        self.salt = data[14 : (14 + data[13])]
        return self

    def derive(self, pin):
        """Dervies the key for the specified PIN.

        Arguments:
            pin (bytearray): PIN.

        Returns:
            bytearray: Derived key. May return same exact bytearray as specified PIN.

        Raises:
            KdfError: If invalid KDF settings.
        """
        if self.algorithm == NONE:
            return pin
        if self.algorithm == KDF_ITERSALTED_S2K:
            return self.derive_kdf_itersalted_s2k(pin)
        raise KdfError(f"unknown KDF algorithm: {self.algorithm:#x}")

    def derive_kdf_itersalted_s2k(self, pin):
        """Dervies the key for the specified PIN.

        Arguments:
            pin (bytearray): PIN.

        Returns:
            bytearray: Derived key.
        """
        hash_state = _create_hash(self.hash_fn)
        salt = self.salt

        salt_length = len(salt)
        pin_length = len(pin)
        iterations, remainder = _calculate_s2k_iterations(
            self.iterations, salt_length + pin_length
        )

        for _ in range(iterations):
            hash_state.update(salt)
            hash_state.update(pin)

        if remainder > salt_length:
            hash_state.update(salt)
            hash_state.update(memoryview(pin)[: (remainder - salt_length)])
        elif remainder:
            hash_state.update(salt[:remainder])

        return bytearray(hash_state.digest())

    def describe_kdf_itersalted_s2k(self):
        """Describes the KDF settings in a human-friendly way.

        Returns:
            str: KDF info.
        """
        hash_fn = f"hash algorithm {self.hash_fn:#x}"
        if self.hash_fn == SHA256:
            hash_fn = "SHA-256"
        elif self.hash_fn == SHA512:
            hash_fn = "SHA-512"
        return (
            f"S2K ({self.iterations:,} iterations"
            f" of {hash_fn} with {len(self.salt)}-byte salt)"
        )


def _create_hash(algorithm):
    if algorithm == SHA256:
        return sha256()
    if algorithm == SHA512:
        return sha512()
    raise KdfError(f"unknown hash algorithm: {algorithm:#x}")


def _calculate_s2k_iterations(count, length):
    # s2k "iteration count" is actually the byte count, not hash iterations
    iterations, remainder = divmod(count, length)
    # always hash at least full salt + pin once
    if iterations == 0:
        return 1, 0
    return iterations, remainder
