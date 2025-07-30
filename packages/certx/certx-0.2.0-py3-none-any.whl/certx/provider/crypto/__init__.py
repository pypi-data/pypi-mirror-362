from . import password

from oslo_utils import importutils

from certx.conf import CONF

_ENCRYPTER = None

PASSWORD_PROVIDERS = {
    'none': 'certx.provider.crypto.password.NonePasswordEncoder',
    'fernet': 'certx.provider.crypto.password.FernetPasswordEncoder'
}


def get_crypto():
    global _ENCRYPTER
    if _ENCRYPTER is None:
        _ENCRYPTER = importutils.import_class(PASSWORD_PROVIDERS[CONF.crypto.provider])()

    return _ENCRYPTER


def encrypt(row_data):
    return get_crypto().encrypt(row_data)


def decrypt(cipher_data):
    return get_crypto().decrypt(cipher_data)
