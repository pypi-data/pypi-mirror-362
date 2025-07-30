import abc

from certx.common.model.models import DistinguishedName, KeyAlgorithm, SignatureAlgorithm, Validity


class CertificateProvider(object, metaclass=abc.ABCMeta):
    def __init__(self, key_algorithm: KeyAlgorithm, signature_algorithm: SignatureAlgorithm, **kwargs):
        self.key_algorithm = key_algorithm
        self.signature_algorithm = signature_algorithm
        self.kwargs = kwargs

    @abc.abstractmethod
    def generate_ca_certificate(self, dn: DistinguishedName, private_key, validity: Validity,
                                signature_algorithm: SignatureAlgorithm = None,
                                root_cert=None, root_key=None, path_length=0):
        """生成CA证书
        :param private_key: CA证书私钥
        :param dn: CA证书对象信息
        :param validity: 证书有效时间
        :param signature_algorithm: CA证书证书签名算法
        :param root_cert: 父CA，创建从属子CA时提供
        :param root_key: 父CA的私钥，创建从属CA时提供
        :param path_length: CA证书路径场景，闯将从属CA时生效
        :return: CA证书对象
        """
        pass

    @abc.abstractmethod
    def generate_certificate(self, ca_cert, ca_key, cert_dn: DistinguishedName, cert_private_key,
                             validity: Validity,
                             signature_algorithm: SignatureAlgorithm = None,
                             key_usage=None,
                             extended_key_usage=None,
                             subject_alternative_name=None,
                             **kwargs):
        """ 生成（签发）证书
        :param ca_cert: CA证书（签发者）
        :param ca_key: CA证书密钥
        :param cert_dn: 证书对象信息
        :param cert_private_key: 证书私钥
        :param validity: 证书有效时间
        :param signature_algorithm: 签名算法
        :param key_usage: 密钥用法
        :param extended_key_usage: 扩展密钥用法
        :param subject_alternative_name: 证书主体别名
        :return: 证书对象
        """
        pass

    @abc.abstractmethod
    def load_certificate(self, certificate_data):
        """将证书数据转成证书对象
        :param certificate_data: 证书（内容）数据
        :return: 证书对象
        """
        pass
