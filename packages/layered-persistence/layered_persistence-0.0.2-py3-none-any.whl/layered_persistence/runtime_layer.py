class RuntimeLayer:
    """
    In‐memory storage layer.
    set returns True on success.
    """

    def __init__(self):
        self._storage = {}

    def get(self, key):
        return self._storage.get(key, None)

    def set(self, key, value):
        try:
            # store
            self._storage[key] = {"value": value}
            return True
        except Exception:
            # swallow any error, indicate failure
            return False

    def delete(self, key):
        return self._storage.pop(key, None) is not None

    def keys(self):
        return list(self._storage.keys())

    def clear(self):
        self._storage.clear()
        return True
