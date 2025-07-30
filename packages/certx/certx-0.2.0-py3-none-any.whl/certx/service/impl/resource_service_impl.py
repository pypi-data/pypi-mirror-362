import os
from pathlib import Path
import shutil

from oslo_log import log as logging
from oslo_utils import uuidutils

from certx.common import exceptions
from certx.common.model import models
from certx.conf import CONF
from certx.db import api as db_api
from certx.service import resource_service

logger = logging.getLogger(__name__)

local_folder = os.path.normpath(CONF.certificate_file_repository.path)


class FileCertificateResourceServiceImpl(resource_service.CertificateResourceService):
    URI_TYPE = 'file'
    CERT_FILE_TAG = 'cert.crt'
    PRIVATE_KEY_FILE_TAG = 'cert.key'

    def _get_base_path(self):
        return Path(local_folder)

    def _check_base_path(self):
        if not os.path.exists(Path(local_folder)):
            logger.info('Create directory for saving certificate. directory={}'.format(local_folder))
            os.makedirs(local_folder)

    def _gen_location(self, certificate_type: models.CertificateResourceType):
        location = os.path.join(local_folder, '{}#{}'.format(certificate_type.value, uuidutils.generate_uuid()))
        if not os.path.exists(location):
            os.makedirs(location)
        return location

    def _get_certificate_type(self, resource_uri):
        return resource_uri.split('#')[-1]

    def _save_certificate(self, certificate_type: models.CertificateResourceType, certificate_data: bytes,
                          private_key_data: bytes) -> str:
        self._check_base_path()
        uri_id = self._gen_location(certificate_type)

        if certificate_data is not None:
            cert_path = os.path.join(uri_id, FileCertificateResourceServiceImpl.CERT_FILE_TAG)
            logger.info('Save certificate to local resource file {}'.format(cert_path))
            with open(cert_path, 'wb') as cp:
                cp.write(certificate_data)

        if private_key_data is not None:
            key_path = os.path.join(uri_id, FileCertificateResourceServiceImpl.PRIVATE_KEY_FILE_TAG)
            logger.info('Save private key to local resource file {}'.format(key_path))
            with open(key_path, 'wb') as kp:
                kp.write(private_key_data)
        return resource_service.build_resource_uri(FileCertificateResourceServiceImpl.URI_TYPE, uri_id)

    def load_certificate(self, resource_uri) -> models.CertificateResource:
        _, uri_id = resource_service.analyze_resource_uri(resource_uri)

        if not os.path.exists(uri_id):
            logger.error('Certificate file path does not exist. {}'.format(uri_id))
            raise exceptions.ServiceException('certificate file does not exist.')

        certificate_type = self._get_certificate_type(resource_uri)

        cert_path = os.path.join(uri_id, FileCertificateResourceServiceImpl.CERT_FILE_TAG)
        if not os.path.exists(cert_path):
            logger.error('Certificate file does not exist. {}'.format(cert_path))
            raise exceptions.ServiceException('certificate file does not exist.')

        with open(cert_path, 'rb') as cp:
            cert_data = cp.read()

        key_path = os.path.join(uri_id, FileCertificateResourceServiceImpl.PRIVATE_KEY_FILE_TAG)
        private_key_data = None

        logger.info('Load certificate from local resource file {}'.format(key_path))
        if os.path.exists(key_path):
            with open(key_path, 'rb') as kp:
                private_key_data = kp.read()

        return models.CertificateResource(certificate_type=certificate_type,
                                          certificate_data=cert_data,
                                          private_key_data=private_key_data)

    def delete_certificate(self, resource_uri: str):
        _, uri_id = resource_service.analyze_resource_uri(resource_uri)
        if not os.path.exists(uri_id):
            logger.info('Certificate file path does not exist, ignore to delete. path={}'.format(uri_id))
            return

        logger.info('Delete local certificate file. path={}'.format(resource_uri))
        shutil.rmtree(uri_id)


class DbCertificateResourceServiceImpl(resource_service.CertificateResourceService):
    dbapi = db_api.get_instance()

    URI_TYPE = 'db'

    def _save_certificate(self, certificate_type: models.CertificateResourceType, certificate_data: bytes,
                          private_key_data: bytes) -> str:
        certificate_resource = {
            'certificate_type': certificate_type.value,
            'certificate_data': certificate_data,
            'private_key_data': private_key_data
        }
        db_res = self.dbapi.create_certificate_resource(certificate_resource)
        return resource_service.build_resource_uri(uri_type=DbCertificateResourceServiceImpl.URI_TYPE,
                                                   uri_id=db_res.id)

    def load_certificate(self, resource_uri: str) -> models.CertificateResource:
        _, obj_id = resource_service.analyze_resource_uri(resource_uri)
        cert_res_model = self.dbapi.get_certificate_resource(obj_id, None)
        if cert_res_model is None:
            logger.log('Certificate resource not found. resource_uri={}'.format(resource_uri))
            raise exceptions.ServiceException('Certificate resource not found')
        return models.CertificateResource(certificate_type=cert_res_model.certificate_type,
                                          certificate_data=cert_res_model.certificate_data,
                                          private_key_data=cert_res_model.private_key_data)

    def delete_certificate(self, resource_uri: str):
        _, obj_id = resource_service.analyze_resource_uri(resource_uri)
        self.dbapi.destroy_certificate_resource(obj_id)
