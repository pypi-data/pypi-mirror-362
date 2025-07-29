import unittest
from unittest.mock import MagicMock, patch
from jbussdieker.storage.cli import register, main
import argparse
import sys
from io import StringIO


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.parser = argparse.ArgumentParser()
        self.subparsers = self.parser.add_subparsers(dest="command")

    def test_register_adds_storage_subparser(self):
        register(self.subparsers)
        # Check that 'storage' is now a subcommand
        subparser_actions = [a for a in self.subparsers.choices]
        self.assertIn("storage", subparser_actions)

    def test_register_sets_default_func(self):
        register(self.subparsers)
        args = self.parser.parse_args(["storage"])
        self.assertTrue(hasattr(args, "func"))
        self.assertEqual(args.func, main)

    def test_main_raises_on_missing_storage_url(self):
        class DummyConfig:
            storage_url = None

        with self.assertRaises(ValueError) as cm:
            main(None, DummyConfig())
        self.assertIn("No storage URL found", str(cm.exception))

    def test_main_raises_on_unsupported_storage_url(self):
        class DummyConfig:
            storage_url = "file:///tmp/foo"

        with self.assertRaises(ValueError) as cm:
            main(None, DummyConfig())
        self.assertIn("Unsupported storage URL", str(cm.exception))

    @patch("jbussdieker.storage.cli.S3Store")
    def test_main_prints_s3_prefixes(self, MockS3Store):
        class DummyConfig:
            storage_url = "s3://mybucket/myprefix"

        mock_store = MockS3Store.return_value
        mock_store.dir.return_value = ["foo/", "bar/"]
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            main(None, DummyConfig())
            output = mock_stdout.getvalue()
        self.assertIn("foo/", output)
        self.assertIn("bar/", output)


if __name__ == "__main__":
    unittest.main()
