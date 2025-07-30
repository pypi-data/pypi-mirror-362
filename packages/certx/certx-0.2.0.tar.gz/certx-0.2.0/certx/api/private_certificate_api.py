from flask import request
from flask_restx import Resource
from marshmallow.exceptions import ValidationError
from oslo_log import log as logging

from certx import rest_api
from certx.api.model import models as api_model
from certx.service import certificate_service

logger = logging.getLogger(__name__)

cert_ns = rest_api.namespace('', description='Certificate')


@cert_ns.route('/v1/private-certificates')
class PrivateCertificateResources(Resource):
    @cert_ns.doc('ListPrivateCertificates')
    def get(self):
        query_option = api_model.ListPrivateCertificateParameter().load(request.args.to_dict())
        logger.debug('Query parameter: %s', query_option)
        certs = certificate_service.list_certificates(query_option)
        return {'certificates': api_model.PrivateCertificate().dump(certs, many=True)}

    @cert_ns.doc('CreatePrivateCertificate')
    def post(self):
        try:
            req_body = api_model.CreatePrivateCertificateRequestBody().load(rest_api.payload)
            cert_dict = req_body['certificate']
        except ValidationError as e:
            return {'message': 'Validation error', 'errors': e.messages}, 400

        logger.info('Create private certificate with params: %s', cert_dict)
        cert = certificate_service.create_certificate(cert_option=cert_dict)
        return api_model.PrivateCertificate().dump(cert)


@cert_ns.route('/v1/private-certificates/<cert_id>')
class PrivateCertificateAuthorityResource(Resource):
    @cert_ns.doc('ShowPrivateCertificate')
    def get(self, cert_id):
        ca = certificate_service.get_certificate(cert_id)
        return {'certificate': api_model.PrivateCertificate().dump(ca)}

    @cert_ns.doc('DeletePrivateCertificate')
    def delete(self, cert_id):
        logger.info('Delete private certificate %s', cert_id)
        certificate_service.delete_certificate(cert_id)
        return '', 204


@cert_ns.route('/v1/private-certificates/<cert_id>/export')
class PrivateCertificateExportResource(Resource):
    @cert_ns.doc('ExportPrivateCertificate')
    def post(self, cert_id):
        try:
            export_option = api_model.ExportPrivateCertificateRequestBody().load(rest_api.payload)
        except ValidationError as e:
            return {'message': 'Validation error', 'errors': e.messages}, 400

        return api_model.PrivateCertificateContent().dump(
            certificate_service.export_certificate(cert_id, export_option))
