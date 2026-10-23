"""Small standard-library API helper. One send per call; no automatic retries."""
import json
import os
import urllib.error
import urllib.parse
import urllib.request
import uuid


class ApiError(RuntimeError):
    def __init__(self, code, status=0, request_id=None):
        self.code, self.status, self.request_id = code, status, request_id
        super().__init__(str(code) + (" (request " + request_id + ")" if request_id else ""))


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class Sarovi:
    def __init__(self, api_key=None, base_url=None, model=None):
        self.key = api_key if api_key is not None else os.environ.get("SAROVI_API_KEY", "")
        self.base = (base_url or os.environ.get("SAROVI_BASE_URL", "https://api.sarovi.site/v1")).rstrip("/")
        self.model = model or os.environ.get("SAROVI_MODEL", "z-ai/glm-5.3-flash")
        u = urllib.parse.urlparse(self.base)
        if u.username or u.password or u.query or u.fragment or not u.hostname or (
            u.scheme != "https" and not (u.scheme == "http" and u.hostname in ("localhost", "127.0.0.1", "::1"))
        ):
            raise ValueError("Use HTTPS, or HTTP on localhost for tests.")
        self.opener = urllib.request.build_opener(NoRedirect())

    def request(self, path, body=None, idempotency_key=None):
        if not self.key or self.key == "YOUR_SAROVI_API_KEY":
            raise ValueError("Set SAROVI_API_KEY on the server.")
        if not path.startswith("/") or path.startswith("//") or ".." in path:
            raise ValueError("Use a relative API resource.")
        headers = {"Authorization": "Bearer " + self.key}
        if body is not None:
            headers.update({"Content-Type": "application/json", "Idempotency-Key": idempotency_key or str(uuid.uuid4())})
        req = urllib.request.Request(self.base + path,
            data=None if body is None else json.dumps(body, ensure_ascii=False).encode("utf-8"),
            headers=headers, method="GET" if body is None else "POST")
        try:
            with self.opener.open(req, timeout=300) as response:
                return json.load(response), response.headers.get("x-request-id")
        except urllib.error.HTTPError as error:
            try:
                code = json.load(error).get("error", {}).get("code", "HTTP_" + str(error.code))
            except (ValueError, AttributeError):
                code = "HTTP_" + str(error.code)
            raise ApiError(code, error.code, error.headers.get("x-request-id")) from None

    def chat(self, messages, idempotency_key=None, **options):
        return self.request("/chat/completions", {"model": self.model, "messages": messages, "max_tokens": 512, **options}, idempotency_key)


def answer(data):
    choice = data.get("choices", [{}])[0]
    if choice.get("finish_reason") == "length":
        raise ApiError("OUTPUT_LIMIT_REACHED", 200)
    if choice.get("finish_reason") != "stop":
        raise ApiError("INCOMPLETE_TEXT_RESULT", 200)
    result = choice.get("message", {}).get("content")
    if not isinstance(result, str):
        raise ApiError("NO_TEXT_RESULT", 502)
    return result
