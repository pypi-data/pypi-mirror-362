from certx.common import exceptions
from certx.common.model import models
from certx.provider.x509 import default, gm

_PROVIDER_MAP = {
    models.KeyAlgorithm.RSA2048: default.DefaultCertificateProvider,
    models.KeyAlgorithm.RSA3072: default.DefaultCertificateProvider,
    models.KeyAlgorithm.RSA4096: default.DefaultCertificateProvider,
    models.KeyAlgorithm.EC256: default.DefaultCertificateProvider,
    models.KeyAlgorithm.EC384: default.DefaultCertificateProvider,
    models.KeyAlgorithm.SM2: gm.GMCertificateProvider,
}


def get_provider(key_algorithm: models.KeyAlgorithm, signature_algorithm: models.SignatureAlgorithm):
    if key_algorithm not in _PROVIDER_MAP:
        raise exceptions.NotImplementException('unsupported key_algorithm')

    return _PROVIDER_MAP.get(key_algorithm)(key_algorithm, signature_algorithm)
