from .runtime_layer import RuntimeLayer


def _is_awaitable(obj):
    return hasattr(obj, "__await__")


def _maybe_await(res):
    if _is_awaitable(res):
        return res

    # wrap a non‐awaitable in an awaitable that returns it immediately
    class _Immediate:
        def __init__(self, v):
            self.v = v

        def __await__(self):
            if False:
                yield None
            return self.v

    return _Immediate(res)


class LayeredPersistence:
    """
    Combines multiple layers.
    set returns False on first layer failure, True if all layers succeed.
    """

    def __init__(self, layers=None, default_data={}):
        if layers is None:
            layers = [RuntimeLayer()]
        self._layers = layers
        self._default_data = default_data

    async def get(self, key):
        """
        Iterate through layers in order. On first non‐None result,
        write that result back into all earlier layers, then return it.
        If no layer has it, return the default value.
        """
        found = None
        found_idx = None

        # 1. Probe each layer in sequence
        for idx, layer in enumerate(self._layers):
            raw = layer.get(key)
            res = await _maybe_await(raw)
            if res is not None:
                found = res
                found_idx = idx
                break

        # 2. If nothing found, return the default
        if found_idx is None:
            if key not in self._default_data:
                return None
            return {"value": self._default_data[key]}

        # 3. Write now‐cached value back to all layers 0..found_idx-1
        #    so that they’ll serve it immediately next time.
        #    We swallow any errors to avoid breaking the get.
        for prior in self._layers[:found_idx]:
            try:
                raw_set = prior.set(key, found["value"])
                await _maybe_await(raw_set)
            except Exception:
                pass

        # 4. Return the located value
        return found

    async def set(self, key, value):
        """
        Write to each layer in turn. If any layer.set(...) returns False
        or raises, stop immediately and return False.
        If all layers succeed, return True.
        """
        for L in self._layers:
            try:
                raw = L.set(key, value)
                ok = await _maybe_await(raw)
            except Exception:
                # error in layer, treat as failure
                return False
            if not ok:
                # layer reported failure
                return False
        return True

    async def delete(self, key):
        deleted = False
        for L in self._layers:
            try:
                raw = L.delete(key)
                d = await _maybe_await(raw)
            except Exception:
                continue
            if d:
                deleted = True
        return deleted

    async def clear(self):
        ok = True
        for L in self._layers:
            try:
                raw = L.clear()
                c = await _maybe_await(raw)
            except Exception:
                ok = False
                continue
            ok = ok and bool(c)
        return ok
