import ssl

from certx import app
from certx.common import service
from certx.conf import CONF

from certx.db.sqlalchemy import models as db_model


def start():
    service.prepare_command()

    with app.app_context():
        db_model.init_db()

    if CONF.enable_https:
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(CONF.server_cert, CONF.server_key, password=CONF.key_pass)
    else:
        ssl_context = None

    app.run(host=CONF.host, port=CONF.port,
            debug=CONF.flask.debug,
            threaded=CONF.flask.threaded,
            ssl_context=ssl_context)


if __name__ == '__main__':
    start()
