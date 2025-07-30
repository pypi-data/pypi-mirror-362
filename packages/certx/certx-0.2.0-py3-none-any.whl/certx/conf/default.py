import os

from oslo_config import cfg

path_opts = [
    cfg.StrOpt('pybasedir',
               default=os.path.abspath(os.path.join(os.path.dirname(__file__), '../')),
               sample_default='/usr/lib/python/site-packages/certx/certx',
               help='Directory where the certx python module is installed.'),
    cfg.StrOpt('state_path',
               default='$pybasedir',
               help="Top-level directory for maintaining certx's state."),
]

service_opts = [
    cfg.StrOpt('host', help='the server ip', default='127.0.0.1'),
    cfg.IntOpt('port', help='Port for server', default='9999'),
    cfg.BoolOpt('enable_https', help='Enable th server run on HTTPS mode', default=False),
    cfg.StrOpt('server_cert', help='Certificate file for HTTPS'),
    cfg.StrOpt('server_key', help='Certificate key for HTTPS'),
    cfg.StrOpt('key_pass', secret=True, help='Certificate private key password'),
]


def list_opts():
    _default_opt_lists = [
        path_opts,
        service_opts
    ]

    full_opt_list = []
    for options in _default_opt_lists:
        full_opt_list.extend(options)
    return full_opt_list


def register_opts(conf):
    conf.register_opts(path_opts)
    conf.register_opts(service_opts)
