try:
    import uos as os
except ImportError:
    import os

try:
    import ujson as json
except ImportError:
    import json


class FileLayer:
    """
    File‐based JSON layer.
    """

    def __init__(self, directory="."):
        self._dir = directory
        self._os = os
        try:
            self._os.mkdir(self._dir)
        except Exception:
            pass

    def _filepath(self, key):
        return f"{self._dir}/{key}.json"

    def get(self, key):
        path = self._filepath(key)
        try:
            with open(path, "r") as f:
                data = json.loads(f.read())
            return data
        except Exception:
            return None

    def set(self, key, value):
        path = self._filepath(key)
        try:
            wrapped = {"value": value}
            with open(path, "w") as f:
                f.write(json.dumps(wrapped))
            return True
        except Exception:
            return False

    def delete(self, key):
        try:
            self._os.remove(self._filepath(key))
            return True
        except Exception:
            return False

    def keys(self):
        try:
            files = self._os.listdir(self._dir)
            return [fn[:-5] for fn in files if fn.endswith(".json")]
        except Exception:
            return []

    def clear(self):
        try:
            for fn in self._os.listdir(self._dir):
                if fn.endswith(".json"):
                    try:
                        self._os.remove(f"{self._dir}/{fn}")
                    except Exception:
                        # suppress error, keep trying
                        pass
            # check if directory is now empty or only contains non-json files
            if not any(fn.endswith(".json") for fn in self._os.listdir(self._dir)):
                return True
            return False
        except Exception:
            # directory missing is equivalent to empty
            return True
