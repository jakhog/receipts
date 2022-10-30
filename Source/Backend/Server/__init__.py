from falcon.asgi import App

from ..Config import Configuration
from ..Workers import Workers

from .Health import Health

def create(config: Configuration, workers: Workers) -> App:
    app = App()

    app.add_middleware(workers)

    app.add_route('/healthz', Health())

    return app
