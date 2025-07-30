from . import resource_service
from .impl import certificate_service_impl
from .impl import resource_service_impl

from certx.common.exceptions import ServiceException
from certx.conf import CONF

certificate_service = certificate_service_impl.CertificateServiceImpl()

RESOURCE_SERVICE_MAP = dict((rs.URI_TYPE, rs) for rs in [resource_service_impl.DbCertificateResourceServiceImpl,
                                                         resource_service_impl.FileCertificateResourceServiceImpl])

certificate_repository_conf = CONF.certificate_repository


def get_resource_service(resource_uri=None):
    """查询资源服务
    :param resource_uri. 如果为空，则返回默认实现
    """
    if resource_uri is None:
        uri_type = certificate_repository_conf.default
    else:
        uri_type, _ = resource_service.analyze_resource_uri(resource_uri)

    if uri_type not in RESOURCE_SERVICE_MAP:
        raise ServiceException('Resource service ({}) not found.'.format(uri_type))
    return RESOURCE_SERVICE_MAP[uri_type]()
