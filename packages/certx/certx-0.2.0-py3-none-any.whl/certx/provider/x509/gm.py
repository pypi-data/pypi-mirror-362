from oslo_log import log as logging
from stevedore import driver

from certx.common import exceptions
from certx.common.model.models import DistinguishedName, SignatureAlgorithm, KeyAlgorithm, Validity
from certx.conf import CONF
from certx.provider.x509.base import CertificateProvider

logger = logging.getLogger(__name__)

x509_provider = CONF.gm.x509_provider


class GMCertificateProvider(CertificateProvider):
    def __init__(self, key_algorithm: KeyAlgorithm, signature_algorithm: SignatureAlgorithm, **kwargs):
        super().__init__(key_algorithm, signature_algorithm, **kwargs)

        self.delegate = driver.DriverManager('certx.provider.x509.gm',
                                             x509_provider).driver(key_algorithm,
                                                                   signature_algorithm,
                                                                   **kwargs)

    def generate_ca_certificate(self, dn: DistinguishedName, private_key, validity: Validity,
                                signature_algorithm: SignatureAlgorithm = None,
                                root_cert=None, root_key=None, path_length=0):
        return self.delegate.generate_ca_certificate(dn, private_key, validity,
                                                     signature_algorithm=signature_algorithm,
                                                     root_cert=root_cert,
                                                     root_key=root_key,
                                                     path_length=path_length)

    def generate_certificate(self, ca_cert, ca_key, cert_dn: DistinguishedName, cert_private_key, validity: Validity,
                             signature_algorithm: SignatureAlgorithm = None, key_usage=None,
                             extended_key_usage=None,
                             subject_alternative_name=None,
                             **kwargs):
        return self.delegate.generate_certificate(ca_cert, ca_key, cert_dn, cert_private_key, validity,
                                                  signature_algorithm,
                                                  key_usage=key_usage,
                                                  extended_key_usage=extended_key_usage,
                                                  subject_alternative_name=None,
                                                  **kwargs)

    def load_certificate(self, certificate_data):
        return self.delegate.load_certificate(certificate_data)


class DefaultGmCertificateProvider(CertificateProvider):
    def generate_ca_certificate(self, dn: DistinguishedName, private_key, validity: Validity,
                                signature_algorithm: SignatureAlgorithm = None,
                                root_cert=None, root_key=None, path_length=0):
        raise exceptions.NotImplementException("GM algorithm not supported")

    def generate_certificate(self, ca_cert, ca_key, cert_dn: DistinguishedName, cert_private_key, validity: Validity,
                             signature_algorithm: SignatureAlgorithm = None,
                             key_usage=None,
                             extended_key_usage=None,
                             subject_alternative_name=None,
                             **kwargs):
        raise exceptions.NotImplementException("GM algorithm not supported")

    def load_certificate(self, certificate_data):
        raise exceptions.NotImplementException("GM algorithm not supported")
