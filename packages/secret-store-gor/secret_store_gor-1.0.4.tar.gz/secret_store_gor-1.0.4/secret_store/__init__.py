from .secret_store import connect, SecretStore, SecretNotFoundError  # noqa

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from . import stores  # noqa
