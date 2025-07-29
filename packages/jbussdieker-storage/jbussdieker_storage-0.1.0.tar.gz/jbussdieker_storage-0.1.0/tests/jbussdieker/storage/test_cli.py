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

    def test_main_prints_storage(self):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            main(argparse.Namespace())
            self.assertEqual(mock_stdout.getvalue().strip(), "storage")


if __name__ == "__main__":
    unittest.main()
