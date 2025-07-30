try:
    import usocket as socket
except ImportError:
    import socket

try:
    import ujson as json
except ImportError:
    import json


def serve_via_http(
    persistence, port=8080, auth_token=None, default_host="0.0.0.0", log=False
):
    """
    Start a blocking HTTP server for POST requests to handle persistence.
    Arguments:
        persistence: Persistence instance
        port: integer port to bind (default 8080)
        default_host: bind address, defaults to all interfaces
        log: print requests/responses if True
    """

    def _read_http_body(conn, headers):
        # Find the content length
        content_length = 0
        for h in headers:
            if h.lower().startswith("content-length:"):
                content_length = int(h.split(":", 1)[1].strip())
        # Read exactly content_length bytes from conn
        body = b""
        while len(body) < content_length:
            chunk = conn.recv(content_length - len(body))
            if not chunk:
                break
            body += chunk
        return body

    def _send_json(conn, dct):
        response = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n"
        response = response.encode("utf8") + json.dumps(dct).encode("utf8")
        conn.sendall(response)

    def _send_json_array(conn, array):
        response = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n"
        response = response.encode("utf8") + json.dumps(array).encode("utf8")
        conn.sendall(response)

    def _send_404(conn):
        response = "HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n"
        conn.sendall(response.encode("utf8"))

    def _send_400(conn):
        response = "HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\n\r\n"
        conn.sendall(response.encode("utf8"))

    def handle_request(s):
        conn, addr = s.accept()
        with conn:
            # Read until headers/body separator
            data = b""
            while b"\r\n\r\n" not in data:
                d = conn.recv(1024)
                if not d:
                    break
                data += d
            if not data:
                _send_400(conn)
                return
            head, sep, rest = data.partition(b"\r\n\r\n")
            req = head.decode("utf8", "ignore")
            lines = req.splitlines()
            if not lines:
                _send_400(conn)
                return
            # parse method and headers
            try:
                method, path, _ = lines[0].split()
            except Exception:
                _send_400(conn)
                return
            headers = [l for l in lines[1:] if l.strip()]

            authorized = False
            if auth_token is None:
                authorized = True
            else:
                # accept 'Authorization: Bearer <token>' or custom header
                for h in headers:
                    if h.lower().startswith("authorization:"):
                        parts = h.split(":", 1)[1].strip().split()
                        if (
                            len(parts) == 2
                            and parts[0].lower() == "bearer"
                            and parts[1] == auth_token
                        ):
                            authorized = True
            if not authorized:
                conn.sendall(b"HTTP/1.1 401 Unauthorized\r\nContent-Length: 0\r\n\r\n")
                return

            if method != "POST":
                if log:
                    print("Rejecting non-POST request.")
                _send_404(conn)
                return
            # Determine content length and body
            content_length = 0
            for h in headers:
                if h.lower().startswith("content-length:"):
                    try:
                        content_length = int(h.split(":", 1)[1].strip())
                    except Exception:
                        pass
            body = rest
            # If body is incomplete, read more
            while len(body) < content_length:
                chunk = conn.recv(content_length - len(body))
                if not chunk:
                    break
                body += chunk
            if len(body) != content_length:
                if log:
                    print("Body incomplete:", len(body), "/", content_length)
                _send_400(conn)
                return
            try:
                op_payload = json.loads(body.decode("utf-8"))
                if log:
                    print("Request:", op_payload)
                op, payload = op_payload
            except Exception as e:
                if log:
                    print("JSON decode/post error:", e)
                _send_400(conn)
                return

            # dispatch
            try:
                if op == "get":
                    key = payload["key"]
                    result = persistence.get(key)
                    # get may be async-aware or direct
                    if callable(getattr(result, "__await__", None)):
                        import asyncio

                        result = asyncio.run(result)
                    if result is None:
                        _send_json(conn, None)
                    else:
                        _send_json(conn, result)
                elif op == "set":
                    key, value = payload["key"], payload["value"]
                    result = persistence.set(key, value)
                    if callable(getattr(result, "__await__", None)):
                        import asyncio

                        ok = asyncio.run(result)
                    else:
                        ok = result
                    _send_json(conn, {"ok": bool(ok)})
                elif op == "delete":
                    key = payload["key"]
                    result = persistence.delete(key)
                    if callable(getattr(result, "__await__", None)):
                        import asyncio

                        ok = asyncio.run(result)
                    else:
                        ok = result
                    _send_json(conn, {"ok": bool(ok)})
                elif op == "keys":
                    result = persistence.keys()
                    if callable(getattr(result, "__await__", None)):
                        import asyncio

                        result = asyncio.run(result)
                    _send_json_array(conn, list(result))
                elif op == "clear":
                    result = persistence.clear()
                    if callable(getattr(result, "__await__", None)):
                        import asyncio

                        ok = asyncio.run(result)
                    else:
                        ok = result
                    _send_json(conn, {"ok": bool(ok)})
                else:
                    _send_400(conn)
            except Exception as e:
                if log:
                    print("Handler error:", e)
                _send_400(conn)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((default_host, port))
    s.listen(1)
    print(f"Persistence HTTP server listening on port {port}...")
    while True:
        handle_request(s)
