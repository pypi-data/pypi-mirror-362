import requests
from flask import g


class RequestsSession:
    def __init__(
        self,
        app=None,
    ):
        if app is not None:
            self.init_app(app)

    def init_app(self, app) -> None:
        app.teardown_appcontext(self.teardown)

    def teardown(self, exception) -> None:
        requests_session = g.pop("requests_session", None)
        if requests_session is not None:
            requests_session.close()

    @property
    def session(self) -> requests.Session:
        requests_session = g.get("requests_session", None)
        if requests_session is None:
            g.requests_session = requests.Session()
        return g.requests_session
