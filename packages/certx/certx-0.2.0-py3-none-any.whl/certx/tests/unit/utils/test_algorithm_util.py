import unittest

from certx.common.model.models import KeyAlgorithm, SignatureAlgorithm
from certx.utils import algorithm_util


class TestAlgorithmUtil(unittest.TestCase):
    def test_validate_key_and_signature_algorithm_with_matched_key_and_signature_alg(self):
        self.assertTrue(
            algorithm_util.validate_key_and_signature_algorithm(KeyAlgorithm.RSA2048, SignatureAlgorithm.SHA256))
        self.assertTrue(
            algorithm_util.validate_key_and_signature_algorithm(KeyAlgorithm.EC256, SignatureAlgorithm.SHA512))
        self.assertTrue(
            algorithm_util.validate_key_and_signature_algorithm(KeyAlgorithm.SM2, SignatureAlgorithm.SM3))

    def test_validate_key_and_signature_algorithm_with_unmatched_key_and_signature_alg(self):
        self.assertFalse(
            algorithm_util.validate_key_and_signature_algorithm(KeyAlgorithm.RSA2048, SignatureAlgorithm.SM3))
        self.assertFalse(
            algorithm_util.validate_key_and_signature_algorithm(KeyAlgorithm.SM2, SignatureAlgorithm.SHA512))

    def test_validate_key_algorithm_for_issuer_and_cert_in_same_items(self):
        self.assertTrue(algorithm_util.validate_key_algorithm(KeyAlgorithm.RSA2048, KeyAlgorithm.RSA2048))
        self.assertTrue(algorithm_util.validate_key_algorithm(KeyAlgorithm.RSA2048, KeyAlgorithm.RSA4096))
        self.assertTrue(algorithm_util.validate_key_algorithm(KeyAlgorithm.RSA3072, KeyAlgorithm.EC256))
        self.assertTrue(algorithm_util.validate_key_algorithm(KeyAlgorithm.SM2, KeyAlgorithm.SM2))

    def test_validate_key_algorithm_for_issuer_and_cert_not_in_same_items(self):
        self.assertFalse(algorithm_util.validate_key_algorithm(KeyAlgorithm.RSA2048, KeyAlgorithm.SM2))
        self.assertFalse(algorithm_util.validate_key_algorithm(KeyAlgorithm.SM2, KeyAlgorithm.RSA4096))
        self.assertFalse(algorithm_util.validate_key_algorithm(KeyAlgorithm.SM2, KeyAlgorithm.EC256))

    def test_validate_signature_algorithm_for_issuer_and_cert_in_same_items(self):
        self.assertTrue(
            algorithm_util.validate_signature_algorithm(SignatureAlgorithm.SHA256, SignatureAlgorithm.SHA512))
        self.assertTrue(
            algorithm_util.validate_signature_algorithm(SignatureAlgorithm.SM3, SignatureAlgorithm.SM3))

    def test_validate_signature_algorithm_for_issuer_and_cert_not_in_same_items(self):
        self.assertFalse(
            algorithm_util.validate_signature_algorithm(SignatureAlgorithm.SHA256, SignatureAlgorithm.SM3))
        self.assertFalse(
            algorithm_util.validate_signature_algorithm(SignatureAlgorithm.SM3, SignatureAlgorithm.SHA512))
