import os
import shutil
import unittest

from layered_persistence import LayeredPersistence, RuntimeLayer, FileLayer


class TestRuntimeLayer(unittest.TestCase):
    def setUp(self):
        self.layer = RuntimeLayer()

    def test_set_and_get(self):
        self.assertTrue(self.layer.set("a", 123))
        self.assertEqual(self.layer.get("a"), {"value": 123})
        self.assertIsNone(self.layer.get("nonexistent"))

    def test_delete(self):
        self.layer.set("foo", "bar")
        self.assertTrue(self.layer.delete("foo"))
        self.assertFalse(self.layer.delete("foo"))
        self.assertIsNone(self.layer.get("foo"))

    def test_keys_and_clear(self):
        self.layer.set("x", 1)
        self.layer.set("y", 2)
        keys = self.layer.keys()
        self.assertIn("x", keys)
        self.assertIn("y", keys)
        self.layer.clear()
        self.assertEqual(self.layer.keys(), [])


class TestFileLayer(unittest.TestCase):
    TMPDIR = "_tmp_persist_test"

    def setUp(self):
        shutil.rmtree(self.TMPDIR, ignore_errors=True)
        os.mkdir(self.TMPDIR)
        self.layer = FileLayer(directory=self.TMPDIR)

    def tearDown(self):
        shutil.rmtree(self.TMPDIR, ignore_errors=True)

    def test_set_and_get(self):
        self.assertTrue(self.layer.set("a", 999))
        self.assertEqual(self.layer.get("a"), {"value": 999})
        self.assertIsNone(self.layer.get("nope"))

    def test_delete(self):
        self.layer.set("hello", "world")
        self.assertTrue(self.layer.delete("hello"))
        self.assertFalse(self.layer.delete("hello"))
        self.assertIsNone(self.layer.get("hello"))

    def test_keys_and_clear(self):
        self.layer.set("file1", 1)
        self.layer.set("file2", 2)
        keys = self.layer.keys()
        self.assertIn("file1", keys)
        self.assertIn("file2", keys)
        self.layer.clear()
        self.assertEqual(self.layer.keys(), [])


class TestPersistence(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.ram = RuntimeLayer()
        self.file = FileLayer(directory="_tmp_persist_co")
        self.pers = LayeredPersistence(
            layers=[self.ram, self.file], default_data={"dflt": 42}
        )

    def tearDown(self):
        shutil.rmtree("_tmp_persist_co", ignore_errors=True)

    async def test_set_and_get(self):
        ok = await self.pers.set("k", "v")
        self.assertTrue(ok)
        item = await self.pers.get("k")
        self.assertEqual(item, {"value": "v"})

    async def test_default_fallback(self):
        got = await self.pers.get("dflt")
        self.assertEqual(got, {"value": 42})

    async def test_delete_and_clear(self):
        await self.pers.set("a", 1)
        await self.pers.set("b", 2)
        self.assertTrue(await self.pers.delete("a"))
        self.assertIsNone(await self.pers.get("a"))
        self.assertTrue(await self.pers.clear())
        self.assertIsNone(await self.pers.get("b"))

    async def test_layer_backpropagation(self):
        # Set only on disk, then get (should cache in ram)
        self.file.set("zzz", 2023)
        self.assertIsNone(self.ram.get("zzz"))
        got = await self.pers.get("zzz")
        self.assertEqual(got, {"value": 2023})
        # Now ram should also have it
        self.assertEqual(self.ram.get("zzz"), {"value": 2023})


if __name__ == "__main__":
    unittest.main()
