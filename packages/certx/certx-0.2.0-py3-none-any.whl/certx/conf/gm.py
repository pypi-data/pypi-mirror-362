from oslo_config import cfg

gm_opts = [
    cfg.StrOpt('key_provider', default='openssl'),
    cfg.StrOpt('x509_provider', default='openssl')
]

openssl_opts = [
    cfg.StrOpt('path', help='The base path for save CA and certificate files', default='$pybasedir/openssl'),
    cfg.BoolOpt('enable_delete_temp_file', help='Delete key/cert file after created', default=True)
]


def register_opts(conf):
    conf.register_opts(gm_opts, group='gm')
    conf.register_opts(openssl_opts, group='openssl')
