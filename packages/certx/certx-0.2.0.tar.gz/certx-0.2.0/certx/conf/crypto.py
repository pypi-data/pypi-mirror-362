from oslo_config import cfg

crypto_opts = [
    cfg.StrOpt('provider', help='Crypter provider type, default is "none", means using plaintext data', default='none'),
    cfg.StrOpt('secret_key', help='Data encryption key')
]


def register_opts(conf):
    conf.register_opts(crypto_opts, group='crypto')
