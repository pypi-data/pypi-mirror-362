import unittest

from cryptography.hazmat.primitives._serialization import Encoding
from cryptography.x509 import ExtendedKeyUsage
from cryptography.x509 import KeyUsage
from cryptography.x509 import ObjectIdentifier
from cryptography.x509.extensions import BasicConstraints, ExtensionNotFound

from certx.common import exceptions
from certx.common.model.models import DistinguishedName, KeyAlgorithm, SignatureAlgorithm, Validity, ValidityType
from certx.provider.key import rsa
from certx.provider.x509 import default


def mock_private_key():
    return rsa.RsaKeyProvider(KeyAlgorithm.RSA2048).generate_private_key()


class TestDefaultCertificateProvider(unittest.TestCase):
    def setUp(self) -> None:
        self.cert_provider = default.DefaultCertificateProvider(KeyAlgorithm.RSA2048, SignatureAlgorithm.SHA256)

    def mock_generate_ca_certificate(self):
        fake_dn = DistinguishedName(country='CN', common_name='test_ca')
        fake_key = mock_private_key()
        fake_validity = Validity(type=ValidityType.YEAR, value=1)

        ca_cert = self.cert_provider.generate_ca_certificate(fake_dn, fake_key, fake_validity)
        return ca_cert, fake_key

    def test_generate_ca_certificate(self):
        ca, _ = self.mock_generate_ca_certificate()

        self.assertIsNotNone(ca)
        self.assertEqual('v3', ca.version.name)
        self.assertEqual('sha256', ca.signature_hash_algorithm.name)
        self.assertEqual('C=CN,CN=test_ca', ca.subject.rfc4514_string())
        self.assertEqual(ca.issuer.rfc4514_string(), ca.subject.rfc4514_string())  # 根CA issuer和subject相同

        basic_constraints = ca.extensions.get_extension_for_oid(BasicConstraints.oid)
        self.assertIsNotNone(basic_constraints)
        self.assertTrue(basic_constraints.value.ca)
        self.assertIsNone(basic_constraints.value.path_length)  # 尚未支持path_length，设置为None

        # key_usage
        key_usage = ca.extensions.get_extension_for_oid(KeyUsage.oid)
        self.assertIsNotNone(key_usage)
        self.assertTrue(key_usage.value.digital_signature)
        self.assertTrue(key_usage.value.key_cert_sign)
        self.assertTrue(key_usage.value.crl_sign)
        self.assertFalse(key_usage.value.content_commitment)
        self.assertFalse(key_usage.value.key_encipherment)
        self.assertFalse(key_usage.value.data_encipherment)
        self.assertFalse(key_usage.value.key_agreement)

    def test_generate_ca_certificate_by_override_signature_alg(self):
        fake_dn = DistinguishedName(country='CN', common_name='test_ca')
        fake_key = mock_private_key()
        fake_validity = Validity(type=ValidityType.YEAR, value=1)

        ca = self.cert_provider.generate_ca_certificate(fake_dn, fake_key, fake_validity,
                                                        signature_algorithm=SignatureAlgorithm.SHA512)
        self.assertIsNotNone(ca)
        self.assertEqual('v3', ca.version.name)
        self.assertEqual('sha512', ca.signature_hash_algorithm.name)

    def test_generate_ca_certificate_when_ca_cert_and_key_not_match(self):
        fake_dn = DistinguishedName(country='CN', common_name='test_ca')
        fake_key = mock_private_key()
        fake_validity = Validity(type=ValidityType.YEAR, value=1)

        self.assertRaises(exceptions.ServiceException, self.cert_provider.generate_ca_certificate,
                          fake_dn, fake_key, fake_validity,
                          SignatureAlgorithm.SHA512,
                          fake_dn)
        self.assertRaises(exceptions.ServiceException, self.cert_provider.generate_ca_certificate,
                          fake_dn, fake_key, fake_validity,
                          SignatureAlgorithm.SHA512,
                          None, fake_dn)

    def test_generate_certificate(self):
        ca_cert, ca_key = self.mock_generate_ca_certificate()

        cert_dn = DistinguishedName(country='CN', common_name='test_cert')
        cert_key = mock_private_key()
        cert_validity = Validity(type=ValidityType.YEAR, value=1)

        cert = self.cert_provider.generate_certificate(ca_cert, ca_key, cert_dn, cert_key, cert_validity)

        self.assertIsNotNone(cert)
        self.assertEqual('v3', cert.version.name)
        self.assertEqual('sha256', cert.signature_hash_algorithm.name)
        self.assertEqual('C=CN,CN=test_ca', cert.issuer.rfc4514_string())
        self.assertEqual('C=CN,CN=test_cert', cert.subject.rfc4514_string())

        self.assertEqual(cert_validity.not_before.strftime("%Y-%m-%d %H:%M:%S"),
                         cert.not_valid_before_utc.strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(cert_validity.not_after.strftime("%Y-%m-%d %H:%M:%S"),
                         cert.not_valid_after_utc.strftime("%Y-%m-%d %H:%M:%S"))

        basic_constraints = cert.extensions.get_extension_for_oid(BasicConstraints.oid)
        self.assertIsNotNone(basic_constraints)
        self.assertFalse(basic_constraints.value.ca)
        self.assertIsNone(basic_constraints.value.path_length)

        # key_usage：没有提供入参时，证书中找不到
        self.assertRaises(ExtensionNotFound, cert.extensions.get_extension_for_oid, KeyUsage.oid)

    def test_generate_certificate_with_key_usage(self):
        ca_cert, ca_key = self.mock_generate_ca_certificate()

        cert_dn = DistinguishedName(country='CN', common_name='test_cert')
        cert_key = mock_private_key()
        cert_validity = Validity(type=ValidityType.YEAR, value=1)

        fake_key_usage = KeyUsage(True, False, False, False, False, False, False, False, False)
        cert = self.cert_provider.generate_certificate(ca_cert, ca_key, cert_dn, cert_key, cert_validity,
                                                       key_usage=fake_key_usage)

        self.assertIsNotNone(cert)
        self.assertEqual('v3', cert.version.name)
        self.assertEqual('sha256', cert.signature_hash_algorithm.name)
        self.assertEqual('C=CN,CN=test_ca', cert.issuer.rfc4514_string())
        self.assertEqual('C=CN,CN=test_cert', cert.subject.rfc4514_string())

        # key_usage
        key_usage = cert.extensions.get_extension_for_oid(KeyUsage.oid)
        self.assertIsNotNone(key_usage)
        self.assertTrue(key_usage.value.digital_signature)
        self.assertFalse(key_usage.value.key_cert_sign)
        self.assertFalse(key_usage.value.crl_sign)
        self.assertFalse(key_usage.value.content_commitment)
        self.assertFalse(key_usage.value.key_encipherment)
        self.assertFalse(key_usage.value.data_encipherment)
        self.assertFalse(key_usage.value.key_agreement)

    def test_generate_certificate_by_override_signature_alg(self):
        ca_cert, ca_key = self.mock_generate_ca_certificate()

        cert_dn = DistinguishedName(country='CN', common_name='test_cert')
        cert_key = mock_private_key()
        cert_validity = Validity(type=ValidityType.YEAR, value=1)

        cert = self.cert_provider.generate_certificate(ca_cert, ca_key, cert_dn, cert_key, cert_validity,
                                                       signature_algorithm=SignatureAlgorithm.SHA512)

        self.assertIsNotNone(cert)
        self.assertEqual('v3', cert.version.name)
        self.assertEqual('sha512', cert.signature_hash_algorithm.name)
        self.assertEqual('C=CN,CN=test_ca', cert.issuer.rfc4514_string())
        self.assertEqual('C=CN,CN=test_cert', cert.subject.rfc4514_string())

    def test_generate_certificate_with_extended_key_usage(self):
        ca_cert, ca_key = self.mock_generate_ca_certificate()

        cert_dn = DistinguishedName(country='CN', common_name='test_cert')
        cert_key = mock_private_key()
        cert_validity = Validity(type=ValidityType.YEAR, value=1)

        extended_key_usage = ExtendedKeyUsage([ObjectIdentifier("1.3.6.1.5.5.7.3.1")])
        cert = self.cert_provider.generate_certificate(ca_cert, ca_key, cert_dn, cert_key, cert_validity,
                                                       extended_key_usage=extended_key_usage)

        self.assertIsNotNone(cert)
        self.assertEqual('v3', cert.version.name)
        self.assertEqual('sha256', cert.signature_hash_algorithm.name)
        self.assertEqual('C=CN,CN=test_ca', cert.issuer.rfc4514_string())
        self.assertEqual('C=CN,CN=test_cert', cert.subject.rfc4514_string())

        # extended_key_usage
        self.assertEqual(extended_key_usage, cert.extensions.get_extension_for_oid(ExtendedKeyUsage.oid).value)

    def test_load_certificate(self):
        # generate certificate
        ca_cert, ca_key = self.mock_generate_ca_certificate()

        cert_dn = DistinguishedName(country='CN', common_name='test_cert')
        cert_key = mock_private_key()
        cert_validity = Validity(type=ValidityType.YEAR, value=1)

        cert = self.cert_provider.generate_certificate(ca_cert, ca_key, cert_dn, cert_key, cert_validity)
        self.assertIsNotNone(self.cert_provider.load_certificate(cert.public_bytes(Encoding.PEM)))

    def test_load_ca_certificate(self):
        ca_cert, _ = self.mock_generate_ca_certificate()
        self.assertIsNotNone(self.cert_provider.load_certificate(ca_cert.public_bytes(Encoding.PEM)))

    def test_load_certificate_with_invalid_cert_data(self):
        self.assertRaises(TypeError, self.cert_provider.load_certificate, 'xx')
