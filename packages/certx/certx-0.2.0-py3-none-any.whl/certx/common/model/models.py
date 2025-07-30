import datetime
from enum import Enum


class CaType(Enum):
    ROOT = 'ROOT'
    SUB = 'SUB'


class CaStatus(Enum):
    ISSUE = 'ISSUE'  # 表示正常签发
    REVOKE = 'REVOKE'  # 表示已被吊销


class KeyAlgorithm(Enum):
    RSA2048 = 'RSA2048'
    RSA3072 = 'RSA3072'
    RSA4096 = 'RSA4096'
    EC256 = 'EC256'  # ECDSA with key size 256
    EC384 = 'EC384'  # ECDSA with key size 384
    SM2 = 'SM2'


class SignatureAlgorithm(Enum):
    SHA256 = 'SHA256'
    SHA384 = 'SHA384'
    SHA512 = 'SHA512'
    SM3 = 'SM3'


class ValidityType(Enum):
    """证书有效期类型"""
    YEAR = 'YEAR'  # 年（12个月）
    MONTH = 'MONTH'  # 月（统一按31天）


class DistinguishedName(object):
    def __init__(self, country: str = None, state: str = None, locality: str = None, organization: str = None,
                 organization_unit: str = None, common_name: str = None):
        """
        证书名称配置
        :param country: 国家编码
        :param state: 省市名称
        :param locality: 地区名称
        :param organization: 组织名称
        :param organization_unit: 组织单元名称
        :param common_name: 证书通用名称
        """
        self.country = country
        self.state = state
        self.locality = locality
        self.organization = organization
        self.organization_unit = organization_unit
        self.common_name = common_name


class Validity(object):
    def __init__(self, type: ValidityType = None, value: int = None):
        """
        :param type: 有效期类型，YEAR(年，12个月)/MONTH(月，31天)
        :param value: 证书有效期值
        """
        self.type = type
        self.value = value

        self._not_before = None
        self._not_after = None

    def parse(self):
        """转化为证书有效期开始时间和结束时间
        :return tuple: 开始时间、结束时间
        """
        not_before = datetime.datetime.now(datetime.timezone.utc)
        not_after = not_before + datetime.timedelta(days=self.get_effective_days())
        self._not_before = not_before
        self._not_after = not_after
        return not_before, not_after

    def get_effective_days(self):
        """获取证书有效天数"""
        switcher = {
            ValidityType.YEAR: 12 * 31 * 24,
            ValidityType.MONTH: 31 * 24
        }

        return switcher.get(self.type) * self.value

    @property
    def not_before(self) -> datetime.datetime:
        if not self._not_before:
            self.parse()

        return self._not_before

    @property
    def not_after(self) -> datetime.datetime:
        if not self._not_after:
            self.parse()

        return self._not_after

    @property
    def days(self):
        return self.get_effective_days()


class SubjectAlternativeNameType(Enum):
    DNS = 'DNS'
    IP = 'IP'
    EMAIL = 'EMAIL'
    URI = 'URI'


class PrivateCertificateAuthority(object):
    def __init__(self, id=None, type: CaType = None, status: CaStatus = None, key_algorithm: KeyAlgorithm = None,
                 signature_algorithm: SignatureAlgorithm = None, distinguished_name: DistinguishedName = None,
                 issuer_id=None, path_length=None,
                 not_before=None, not_after=None, created_at=None, updated_at=None, uri=None, password=None):
        self.id = id
        self.type = type
        self.status = status
        self.key_algorithm = key_algorithm
        self.signature_algorithm = signature_algorithm
        self.distinguished_name = distinguished_name
        self.issuer_id = issuer_id
        self.path_length = path_length
        self.not_before = not_before
        self.not_after = not_after
        self.created_at = created_at
        self.updated_at = updated_at
        self.uri = uri
        self.password = password

    @staticmethod
    def from_db(ca_entity):
        dn = DistinguishedName(country=ca_entity.country,
                               state=ca_entity.state,
                               locality=ca_entity.locality,
                               organization=ca_entity.organization,
                               organization_unit=ca_entity.organization_unit,
                               common_name=ca_entity.common_name)
        return PrivateCertificateAuthority(id=ca_entity.id,
                                           type=CaType(ca_entity.type),
                                           status=CaStatus(ca_entity.status),
                                           key_algorithm=KeyAlgorithm(ca_entity.key_algorithm),
                                           signature_algorithm=SignatureAlgorithm(ca_entity.signature_algorithm),
                                           distinguished_name=dn,
                                           issuer_id=ca_entity.issuer_id,
                                           path_length=ca_entity.path_length,
                                           not_before=ca_entity.not_before,
                                           not_after=ca_entity.not_after,
                                           created_at=ca_entity.created_at,
                                           updated_at=ca_entity.updated_at,
                                           uri=ca_entity.uri,
                                           password=ca_entity.password)


class CertificateStatus(Enum):
    ISSUE = 'ISSUE'  # 表示正常签发
    REVOKE = 'REVOKE'  # 表示已被吊销


class PrivateCertificate(object):
    def __init__(self, id=None, status: CertificateStatus = None, issuer_id=None, key_algorithm: KeyAlgorithm = None,
                 signature_algorithm: SignatureAlgorithm = None, distinguished_name: DistinguishedName = None,
                 not_before=None, not_after=None, created_at=None, updated_at=None, uri=None, password=None):
        self.id = id
        self.status = status
        self.issuer_id = issuer_id
        self.key_algorithm = key_algorithm
        self.signature_algorithm = signature_algorithm
        self.distinguished_name = distinguished_name
        self.not_before = not_before
        self.not_after = not_after
        self.created_at = created_at
        self.updated_at = updated_at
        self.uri = uri
        self.password = password

    @staticmethod
    def from_db(cert_entity):
        dn = DistinguishedName(country=cert_entity.country,
                               state=cert_entity.state,
                               locality=cert_entity.locality,
                               organization=cert_entity.organization,
                               organization_unit=cert_entity.organization_unit,
                               common_name=cert_entity.common_name)
        return PrivateCertificate(id=cert_entity.id,
                                  status=CertificateStatus(cert_entity.status),
                                  issuer_id=cert_entity.issuer_id,
                                  key_algorithm=KeyAlgorithm(cert_entity.key_algorithm),
                                  signature_algorithm=SignatureAlgorithm(cert_entity.signature_algorithm),
                                  distinguished_name=dn,
                                  not_before=cert_entity.not_before,
                                  not_after=cert_entity.not_after,
                                  created_at=cert_entity.created_at,
                                  updated_at=cert_entity.updated_at,
                                  uri=cert_entity.uri,
                                  password=cert_entity.password)


class CertificateResourceType(Enum):
    CA = 'CA'
    CERTIFICATE = 'CERTIFICATE'


class CertificateResourceTag(Enum):
    CERTIFICATE = 'CERTIFICATE'
    PRIVATE_KEY = 'PRIVATE_KEY'


class CertificateResource(object):
    def __init__(self, certificate_type: CertificateResourceType,
                 certificate_data: bytes,
                 private_key_data: bytes = None):
        self.certificate_type = certificate_type
        self.certificate_data = certificate_data
        self.private_key_data = private_key_data


class CertificateContent(object):
    def __init__(self, certificate=None, private_key=None, certificate_chain=None):
        self.certificate = certificate
        self.private_key = private_key
        self.certificate_chain = certificate_chain


class DownloadType(Enum):
    APACHE = 'APACHE',
    NGINX = 'NGINX',
    IIS = 'IIS',
    TOMCAT = 'TOMCAT'
    OTHER = 'OTHER'
