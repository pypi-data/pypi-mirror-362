from abc import ABC, abstractmethod

from certx.common.model import models


def build_resource_uri(uri_type, uri_id):
    return '{}:{}'.format(uri_type, uri_id)


def analyze_resource_uri(resource_uri):
    return resource_uri.split(':', 1)


class CertificateResourceService(ABC):
    def save_certificate(self, certificate_type: models.CertificateResourceType, certificate_data: bytes,
                         private_key_data: bytes) -> str:
        """保存证书
        :param certificate_type: 证书类型
        :param certificate_data: 证书数据。保存的是证书，因此该字段内容不能为空
        :param private_key_data: 密钥数据。为空，表示缺少对应的证书密钥
        :return:
        """
        if certificate_data is None:
            raise Exception('certificate_data required')

        return self._save_certificate(certificate_type, certificate_data, private_key_data)

    @abstractmethod
    def _save_certificate(self, certificate_type: models.CertificateResourceType, certificate_data: bytes,
                          private_key_data: bytes) -> str:
        pass

    @abstractmethod
    def load_certificate(self, resource_uri: str) -> models.CertificateResource:
        pass

    @abstractmethod
    def delete_certificate(self, resource_uri: str):
        pass
