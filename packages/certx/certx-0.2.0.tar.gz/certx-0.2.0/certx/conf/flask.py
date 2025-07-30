from oslo_config import cfg

opts = [
    cfg.BoolOpt('threaded', help='Make server run in multi-thread', default=True),
    cfg.BoolOpt('debug', help='Flask run on debug mode', default=True)
]


def register_opts(conf):
    conf.register_opts(opts, group='flask')
