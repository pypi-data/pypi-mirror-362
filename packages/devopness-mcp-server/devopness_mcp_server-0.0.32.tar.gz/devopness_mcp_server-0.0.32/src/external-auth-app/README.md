# External OAuth Authentication App 🚀

> TODO: Remove this `package (external-auth-app)` once the Devopness Web App includes native OAuth integration for the MCP Server.

This is a **temporary** Flask-based OAuth authentication app used by the **Devopness MCP Server** to authenticate users via email and password.

## 📚 Overview

The app provides two main endpoints:

- `GET /login`  
  Presents a login form for the user to enter their email and password.

- `POST /authenticate`  
  Handles the submitted form:
  1. Validates the `next` parameter from the session.
  2. Logs the user in using the Devopness API.
  3. Executes the OAuth authorization step and redirects the user accordingly.

This is a **reference implementation** and should be removed once the official Devopness Web App includes native OAuth integration for the MCP Server.

## 🛠️ Flow Details

1. Users are redirected here with a `next` query parameter (Base64-encoded JSON).
2. `GET /login` saves `next` in the session and renders the login form.
3. `POST /authenticate`:
   - Reads `next` from the session (error if missing/expired).
   - Calls `DevopnessClient.users.login_user()` using provided credentials.
   - Decodes the `next` payload and performs an HTTP GET to `LARAVEL_EXTERNAL_AUTH_URL` with the user's bearer token.
   - Reads the `Location` header and redirects the user to complete the OAuth authorization flow.
