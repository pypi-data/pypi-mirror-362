from certx.provider.key import gm
from certx.provider.key import rsa
from certx.provider.key import ec

from certx.common import exceptions
from certx.common.model.models import KeyAlgorithm

_PROVIDER_MAP = {
    KeyAlgorithm.RSA2048: rsa.RsaKeyProvider,
    KeyAlgorithm.RSA3072: rsa.RsaKeyProvider,
    KeyAlgorithm.RSA4096: rsa.RsaKeyProvider,
    KeyAlgorithm.EC256: ec.EcKeyProvider,
    KeyAlgorithm.EC384: ec.EcKeyProvider,
    KeyAlgorithm.SM2: gm.GmKeyProvider,
}


def get_provider(key_algorithm: KeyAlgorithm):
    if key_algorithm not in _PROVIDER_MAP:
        raise exceptions.UnsupportedAlgorithm(type='key', name=key_algorithm.value if key_algorithm else None)

    return _PROVIDER_MAP.get(key_algorithm)(key_algorithm)
