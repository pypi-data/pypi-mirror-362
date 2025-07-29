import os
import threading
import time
import webbrowser
import json
from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
from attr import dataclass
from authlib.integrations.requests_client import OAuth2Session
from dotenv import load_dotenv

from common_utils.logger import create_logger
from common_utils.config import ROOT_DIR


@dataclass
class OAuth2Data:
    client_id_env: str
    client_secret_env: str
    redirect_uri_env: str
    scope_env: str
    authorize_url: str
    token_url: str
    state: str | None = None


class OAuth2Handler:
    log = create_logger("OAuth2Handler")
    auth_code = None

    def __init__(self, data: OAuth2Data, cache_path: str | None = None):
        self.client_id = os.environ[data.client_id_env]
        self.client_secret = os.environ[data.client_secret_env]
        self.redirect_uri = os.environ[data.redirect_uri_env]
        self.scope = os.environ[data.scope_env]
        self.authorize_url = data.authorize_url
        self.token_url = data.token_url
        self.state = data.state
        self.port = int(self.redirect_uri.split(":")[-1].split("/")[0])
        self.cache_path = cache_path
        if not cache_path:
            self.cache_name = self.authorize_url.split("/")[2].replace(".", "_")
            self.cache_path = f"{ROOT_DIR}/oauth_tokens/{self.cache_name}.json".replace("\\", "/")

    def callback_app(self, environ, start_response):
        query = environ.get("QUERY_STRING", "")
        params = parse_qs(query)
        self.auth_code = params.get("code", [None])[0]
        start_response("200 OK", [("Content-Type", "text/html")])
        return [b"<h1>Authorization code received. You may close this window.</h1>"]

    def start_temp_server(self):
        httpd = make_server("", self.port, self.callback_app)
        httpd.handle_request()

    def save_token(self, token):
        path = "/".join(self.cache_path.split("/")[:-1])
        os.makedirs(path, exist_ok=True)
        with open(self.cache_path, "w") as file:
            token_str = json.dumps(token)
            file.write(token_str)

    def load_token(self):
        with open(self.cache_path, "r") as file:
            token_str = file.read()
            return json.loads(token_str)

    def get_token(self):
        try:
            token = self.load_token()
            self.log.debug(f"Loaded token from cache: {token}")
            return token
        except FileNotFoundError:
            self.log.debug("No token found in cache. Requesting new token.")

        session = OAuth2Session(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=self.scope,
        )
        authorization_url, state = session.create_authorization_url(self.authorize_url)
        server_thread = threading.Thread(target=self.start_temp_server)
        server_thread.daemon = True
        server_thread.start()
        self.log.debug(f"Opening browser to: {authorization_url}")
        webbrowser.open(authorization_url)
        while self.auth_code is None:
            time.sleep(0.1)
        self.log.debug(f"Received auth code: {self.auth_code}")
        token = session.fetch_token(self.token_url, code=self.auth_code)
        self.log.debug(f"Access token data: {token}")
        self.save_token(token)

        return token


if __name__ == "__main__":
    load_dotenv()
    oauth_data = OAuth2Data(
        client_id_env="TICKTICK_CLIENT_ID",
        client_secret_env="TICKTICK_CLIENT_SECRET",
        redirect_uri_env="TICKTICK_REDIRECT_URI",
        scope_env="TICKTICK_SCOPE",
        authorize_url="https://ticktick.com/oauth/authorize",
        token_url="https://ticktick.com/oauth/token",
    )

    oauth_handler = OAuth2Handler(oauth_data)
    oauth_handler.get_token()

