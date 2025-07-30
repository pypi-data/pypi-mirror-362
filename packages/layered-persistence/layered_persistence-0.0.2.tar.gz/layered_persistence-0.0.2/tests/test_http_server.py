import unittest
import threading
import time
import os
import shutil

from layered_persistence import (
    LayeredPersistence,
    RuntimeLayer,
    FileLayer,
    serve_via_http,
    HttpLayer,
)

PORT = 8080
TMP_DIR = "./__tmp_storage_unitest"
AUTH_TOKEN = "u39uabdlfbhu94b3bhwdf"


def start_server():
    p = LayeredPersistence([RuntimeLayer(), FileLayer(TMP_DIR)], {"foo": 1})
    serve_via_http(p, port=PORT, auth_token=AUTH_TOKEN)


class TestPersistenceHTTP(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        # Ensure fresh temp directory
        if os.path.exists(TMP_DIR):
            shutil.rmtree(TMP_DIR)
        os.makedirs(TMP_DIR, exist_ok=True)
        # Start server
        cls.server_thread = threading.Thread(target=start_server, daemon=True)
        cls.server_thread.start()
        time.sleep(1)  # Wait for server startup

    @classmethod
    def tearDownClass(cls):
        # Stop server if needed (not shown; you'd need to add this feature)
        # Remove temp dir
        if os.path.exists(TMP_DIR):
            shutil.rmtree(TMP_DIR)

    async def asyncSetUp(self):
        self.p = LayeredPersistence(
            [RuntimeLayer(), HttpLayer(f"http://localhost:{PORT}", AUTH_TOKEN)]
        )

    async def test_unauthorised_access(self):
        p2 = LayeredPersistence([HttpLayer(f"http://localhost:{PORT}")])
        result = await p2.get("foo")
        self.assertIsNone(result)

    async def test_get_set_delete(self):
        foo = await self.p.get("foo")
        self.assertIsInstance(foo, dict)
        self.assertEqual(foo["value"], 1)

        set_ok = await self.p.set("foo", foo["value"] + 1)
        self.assertTrue(set_ok)
        foo2 = await self.p.get("foo")
        self.assertEqual(foo2["value"], 2)

        set_hello = await self.p.set("hello", "world")
        self.assertTrue(set_hello)
        hello = await self.p.get("hello")
        self.assertIsInstance(hello, dict)
        self.assertEqual(hello["value"], "world")

        del_hello = await self.p.delete("hello")
        self.assertTrue(del_hello)
        hello_missing = await self.p.get("hello")
        self.assertTrue(hello_missing is None or hello_missing == {})

    # Optional: add clear test


if __name__ == "__main__":
    unittest.main()
