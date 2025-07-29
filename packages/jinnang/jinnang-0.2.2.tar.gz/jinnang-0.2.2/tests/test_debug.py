import unittest
import sys
from unittest.mock import patch
from jinnang.debug.debug import get_python_execution_info, get_class_info

class TestDebug(unittest.TestCase):

    def test_get_python_execution_info(self):
        info = get_python_execution_info()
        self.assertIn("executable_path", info)
        self.assertIn("version", info)
        self.assertIn("version_info", info)
        self.assertIn("platform", info)
        self.assertEqual(info["executable_path"], sys.executable)
        self.assertEqual(info["version"], sys.version)
        self.assertEqual(info["version_info"], sys.version_info)
        self.assertEqual(info["platform"], sys.platform)

    def test_get_class_info(self):
        class MyClass:
            pass

        info = get_class_info(MyClass)
        self.assertIn("class_name", info)
        self.assertIn("module", info)
        self.assertIn("methods", info)
        self.assertIn("attributes", info)
        self.assertEqual(info["class_name"], "MyClass")
        self.assertIn(info["module"], ["tests.test_debug", "test_debug"])
        self.assertIsInstance(info["methods"], list)
        self.assertIsInstance(info["attributes"], list)

        # Test with a built-in class
        info_str = get_class_info(str)
        self.assertEqual(info_str["class_name"], "str")
        self.assertEqual(info_str["module"], "builtins")
        self.assertIsInstance(info_str["methods"], list)
        self.assertIsInstance(info_str["attributes"], list)