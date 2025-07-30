import base64
import json
import os
from typing import Any, cast
from urllib.parse import urlencode

import httpx
import requests  # type: ignore[import-untyped]
from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, request, session

from devopness import DevopnessClient

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

LARAVEL_API_URL = cast(str, os.getenv("LARAVEL_API_URL"))
LARAVEL_EXTERNAL_AUTH_URL = cast(str, os.getenv("LARAVEL_EXTERNAL_AUTH_URL"))

if not LARAVEL_API_URL or not LARAVEL_EXTERNAL_AUTH_URL:
    raise ValueError(
        "LARAVEL_API_URL and LARAVEL_EXTERNAL_AUTH_URL"
        " environment variables must be set"
    )


@app.route("/login")
def login() -> Any:  # noqa: ANN401
    oauth_next = request.args.get("next")
    if not oauth_next:
        return jsonify(
            {
                "error": "invalid_request",
                "error_description": "The `next` parameter is required",
            }
        )

    session["oauth_next"] = oauth_next

    return render_template("login.html")


@app.route("/authenticate", methods=["POST"])
def authenticate() -> Any:  # noqa: ANN401
    oauth_next = session.get("oauth_next")

    if not oauth_next:
        return jsonify(
            {
                "error": "session_expired",
                "error_description": "Session expired",
            }
        ), 400

    try:
        devopness = DevopnessClient(
            {
                "base_url": LARAVEL_API_URL,
            }
        )

        devopness.users.login_user(
            {
                "email": request.form["email"],
                "password": request.form["password"],
            }
        )

        decoded_next = base64.b64decode(oauth_next).decode("utf-8")
        json_next = json.loads(decoded_next)

        with httpx.Client(follow_redirects=False) as client:
            response = client.get(
                LARAVEL_EXTERNAL_AUTH_URL + "?" + urlencode(json_next),
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "User-Agent": "devopness-mcp-server",
                    "Authorization": f"Bearer {devopness.access_token}",
                },
            )

        location = response.headers.get("Location", str(response.url))

        return redirect(location)

    except requests.exceptions.RequestException as e:
        return jsonify(
            {
                "error": "server_error",
                "error_description": f"Server error: {e}",
            }
        ), 500


if __name__ == "__main__":
    host = os.getenv("FLASK_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_PORT", "5000"))

    app.run(host, port)
