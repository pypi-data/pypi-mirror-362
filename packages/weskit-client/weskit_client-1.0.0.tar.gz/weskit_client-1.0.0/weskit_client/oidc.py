import requests
import os
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer


def get_oidc_auth_url(client_id, redirect_port, auth_endpoint):
    params = {
        "client_id": client_id,
        "redirect_uri": f"http://localhost:{redirect_port}",
        "scope": "openid eduperson_entitlement profile",
        "access_type": "offline",
        "response_type": "code",
        "openid.realm": "",
        "state": ""
    }
    auth_url = f"{auth_endpoint}?{urllib.parse.urlencode(params)}"
    return auth_url


class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        code = params.get("code")[0]
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Authorization code received. You can close this window.")
        self.server.auth_code = code


def get_auth_code(redirect_port, auth_url):
    server = HTTPServer(("", redirect_port), CallbackHandler)
    print("Please open the URL in your webbrowser:")
    print(auth_url)
    server.handle_request()
    auth_code = server.auth_code
    return auth_code


def get_auth_tokens(auth_code, redirect_port, client_id, client_secret, token_endpoint):
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": f"http://localhost:{redirect_port}",
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(token_endpoint, data=data)
    tokens = response.json()
    return tokens


def login():
    try:
        client_id = os.environ["WESKIT_OIDC_CLIENT_ID"]
        client_secret = os.environ["WESKIT_OIDC_CLIENT_SECRET"]
        oicd_config = requests.get(os.environ["WESKIT_OIDC_CONFIG"]).json()
        redirect_port = int(os.environ["WESKIT_OIDC_REDIRECT_PORT"])
    except KeyError:
        print("OIDC infos not found in environment variables")
        sys.exit(1)
    auth_url = get_oidc_auth_url(
        client_id=client_id,
        redirect_port=redirect_port,
        auth_endpoint=oicd_config["authorization_endpoint"])
    auth_code = get_auth_code(redirect_port=redirect_port, auth_url=auth_url)
    tokens = get_auth_tokens(
        auth_code=auth_code,
        redirect_port=redirect_port,
        client_id=client_id,
        client_secret=client_secret,
        token_endpoint=oicd_config["token_endpoint"])
    j_user = requests.post(
        headers=dict(Authorization="Bearer " + tokens["access_token"]),
        url=oicd_config["userinfo_endpoint"]).json()
    print(f"Login successful for user '{j_user["preferred_username"]}'.")
    with open(".weskit_access_key", "w") as file:
        file.write(tokens["access_token"])


def logout():
    try:
        os.remove(".weskit_access_key")
        print("Logout successful.")
    except Exception:
        print("Logout successful.")
