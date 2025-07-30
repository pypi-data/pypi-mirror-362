import ipaddress

from cryptography import x509

from certx.common import exceptions
from certx.common.model.models import SubjectAlternativeNameType

_SUPPORTED_EXTENDED_KEY_USAGE = {
    "server_auth": {
        "oid": x509.OID_SERVER_AUTH,
        "name": "serverAuth"
    },
    "client_auth": {
        "oid": x509.OID_CLIENT_AUTH,
        "name": "clientAuth"
    },
    "code_signing": {
        "oid": x509.OID_CODE_SIGNING,
        "name": "codeSigning",
    },
    "email_protection": {
        "oid": x509.OID_CODE_SIGNING,
        "name": "emailProtection"
    },
    "time_stamping": {
        "oid": x509.OID_TIME_STAMPING,
        "name": "timeStamping"
    },
    "ocsp_signing": {
        "oid": x509.OID_OCSP_SIGNING,
        "name": "OCSPSigning"
    }
}

_ENABLED_KEYS = ['others'] + list(_SUPPORTED_EXTENDED_KEY_USAGE.keys())


def build_x509_extended_key_usage(extended_key_usage: dict) -> x509.ExtendedKeyUsage:
    if not extended_key_usage:
        return None

    usages = set()
    for usage_key, usage_value in extended_key_usage.items():
        if usage_key not in _ENABLED_KEYS:
            raise exceptions.BadRequest('Invalid item: %(key)s, %(val)s', key=usage_key, val=usage_value)

        if usage_key in _SUPPORTED_EXTENDED_KEY_USAGE:
            if usage_value is None:
                continue
            if not isinstance(usage_value, bool):
                raise exceptions.BadRequest('Invalid item: %(key)s, %(val)s', key=usage_key, val=usage_value)
            if not usage_value:
                continue

            usages.add(_SUPPORTED_EXTENDED_KEY_USAGE.get(usage_key).get("oid"))
        else:  # usage_key == 'others'
            if usage_value is None:
                continue
            if not isinstance(usage_value, list):
                raise exceptions.BadRequest('Custom extended key usage must be list')

            for v in usage_value:
                try:
                    usages.add(x509.ObjectIdentifier(v))
                except ValueError:
                    raise exceptions.InvalidParameterValue('Invalid object_identifier: {}'.format(v))

    return x509.ExtendedKeyUsage(usages)


_SUBJECT_ALTERNATIVE_NAME_MAP = {
    SubjectAlternativeNameType.DNS: x509.DNSName,
    SubjectAlternativeNameType.IP: x509.IPAddress,
    SubjectAlternativeNameType.EMAIL: x509.RFC822Name,
    SubjectAlternativeNameType.URI: x509.UniformResourceIdentifier
}


def build_x509_subject_alternative_name(subject_alternative_names: list) -> x509.SubjectAlternativeName:
    if not subject_alternative_names:
        return None

    existed_cache = {}  # key: name_type, value: items of name_value. {name_type: [name_value]}
    general_names = []
    for item in subject_alternative_names:
        name_type = item.get('type')
        name_value = item.get('value')

        existed = existed_cache.get(name_type) or []
        if name_value in existed:
            continue

        if name_type == SubjectAlternativeNameType.IP:
            try:
                name_value = ipaddress.ip_address(item.get('value'))
            except:
                try:
                    name_value = ipaddress.ip_network(item.get('value'))
                except:
                    raise exceptions.InvalidParameterValue('Invalid ip: {}'.format(item.get('value')))

        general_names.append(_SUBJECT_ALTERNATIVE_NAME_MAP.get(name_type)(name_value))
        existed.append(name_value)
        existed_cache[name_type] = existed

    return x509.SubjectAlternativeName(general_names)
