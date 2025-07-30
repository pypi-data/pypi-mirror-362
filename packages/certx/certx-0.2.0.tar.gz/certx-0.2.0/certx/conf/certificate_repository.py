from oslo_config import cfg

certificate_repository_opts = [
    cfg.StrOpt('default', help='Default Certificate repository type', default='db', choices=('db', 'file')),
]

certificate_file_repository_opts = [
    cfg.StrOpt('path', help='The base path for save CA and certificate files', default='$pybasedir/cert-repo')
]


def register_opts(conf):
    conf.register_opts(certificate_repository_opts, group='certificate_repository')
    conf.register_opts(certificate_file_repository_opts, group='certificate_file_repository')
