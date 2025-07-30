"""OpenPGP Card X25519 Agent."""

from importlib.metadata import PackageNotFoundError, version

try:
    dist_name = "openpgpcard-x25519-agent"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError
