import unittest
import os
import shutil

from layered_persistence import FileLayer


class TestFileLayer(unittest.TestCase):
    TEST_DIR = "./_test_persistence_files"

    def setUp(self):
        # Clean up before creating
        if os.path.exists(self.TEST_DIR):
            shutil.rmtree(self.TEST_DIR)
        os.mkdir(self.TEST_DIR)
        self.layer = FileLayer(self.TEST_DIR)

    def tearDown(self):
        # Clean up after
        if os.path.exists(self.TEST_DIR):
            shutil.rmtree(self.TEST_DIR)

    def test_set_and_get(self):
        self.assertTrue(self.layer.set("foo", 123))
        res = self.layer.get("foo")
        self.assertIsInstance(res, dict)
        self.assertEqual(res["value"], 123)

    def test_overwrite_value(self):
        self.layer.set("foo", 1)
        self.layer.set("foo", 2)
        res = self.layer.get("foo")
        self.assertEqual(res["value"], 2)

    def test_delete(self):
        self.layer.set("delme", "gone")
        self.assertTrue(self.layer.delete("delme"))
        self.assertIsNone(self.layer.get("delme"))

    def test_keys(self):
        self.layer.set("a", 1)
        self.layer.set("b", 2)
        self.layer.set("c", 3)
        keys = self.layer.keys()
        self.assertCountEqual(keys, ["a", "b", "c"])

    def test_clear(self):
        self.layer.set("one", 1)
        self.layer.set("two", 2)
        self.assertTrue(self.layer.clear())
        self.assertEqual(self.layer.keys(), [])

    def test_missing_key(self):
        self.assertIsNone(self.layer.get("doesnotexist"))
        self.assertFalse(self.layer.delete("doesnotexist"))

    def test_file_corruption(self):
        # Simulate a bad file
        path = os.path.join(self.TEST_DIR, "bad.json")
        with open(path, "w") as f:
            f.write("not json")
        # Should not throw, should just skip
        self.assertIsNone(self.layer.get("bad"))

    def test_filelayer_persistence(self):
        # Data set in one instance is available in another
        self.layer.set("persist", "yes")
        l2 = FileLayer(self.TEST_DIR)
        res = l2.get("persist")
        self.assertEqual(res["value"], "yes")


if __name__ == "__main__":
    unittest.main()
