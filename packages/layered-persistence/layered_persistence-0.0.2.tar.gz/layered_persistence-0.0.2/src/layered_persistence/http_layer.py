try:
    import urequests as requests
except ImportError:
    import requests

try:
    import ujson as json
except ImportError:
    import json


class HttpLayer:
    """
    Remote persistence via HTTP/POST. Uses JSON array [op, payload].
    Methods: get, set, delete, keys, clear.
    """

    def __init__(self, endpoint, auth_token=None):
        self._endpoint = endpoint
        self._auth_token = auth_token

    def _post(self, op, payload=None):
        data = json.dumps([op, payload])
        headers = {"Content-Type": "application/json"}
        if self._auth_token:
            headers["Authorization"] = f"Bearer {self._auth_token}"
        try:
            r = requests.post(self._endpoint, data=data, headers=headers)
            if hasattr(r, "close"):
                # Micropython urequests
                res = r.json()
                r.close()
            else:
                # Some requests, like requests-mock in CPython, may lack 'close'
                res = r.json()
            return res
        except Exception:
            return None

    def get(self, key):
        res = self._post("get", {"key": key})
        return res if res is not None else None

    def set(self, key, value):
        res = self._post("set", {"key": key, "value": value})
        return bool(res and res.get("ok", True))

    def delete(self, key):
        res = self._post("delete", {"key": key})
        return bool(res and res.get("ok", True))

    def keys(self):
        res = self._post("keys")
        # Must return a list of keys
        return res if isinstance(res, list) else []

    def clear(self):
        res = self._post("clear")
        return bool(res and res.get("ok", True))
