import os
import argparse
import tempfile
import unittest
from io import StringIO
from unittest.mock import patch, MagicMock
from contextlib import redirect_stdout
from jbussdieker.commit.cli import main, register


class TestCLICommit(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.config_path = os.path.join(self.tmpdir.name, "config.json")
        os.environ["JBUSSDIEKER_CONFIG"] = self.config_path

    def tearDown(self):
        self.tmpdir.cleanup()
        os.environ.pop("JBUSSDIEKER_CONFIG", None)

    @patch("jbussdieker.commit.cli.run_commit")
    def test_commit_command_success(self, mock_run_commit):
        buf = StringIO()
        args = argparse.Namespace(dry_run=False)
        config = argparse.Namespace(openai_api_key="test")
        with redirect_stdout(buf):
            main(args, config)
        mock_run_commit.assert_called()

    @patch("jbussdieker.commit.cli.run_commit", side_effect=Exception("fail"))
    def test_commit_command_error(self, mock_run_commit):
        buf = StringIO()
        args = argparse.Namespace(dry_run=False)
        config = argparse.Namespace(openai_api_key="test")
        with redirect_stdout(buf):
            result = main(args, config)
        self.assertEqual(result, 1)
        mock_run_commit.assert_called()

    def test_register_function(self):
        """Test the register function to ensure it sets up the parser correctly."""
        mock_subparsers = MagicMock()
        mock_parser = MagicMock()
        mock_subparsers.add_parser.return_value = mock_parser

        register(mock_subparsers)

        # Verify the parser was added with correct name and help
        mock_subparsers.add_parser.assert_called_once_with(
            "commit", help="Generate and create a conventional commit"
        )

        # Verify the dry-run argument was added
        mock_parser.add_argument.assert_called_once_with(
            "--dry-run",
            action="store_true",
            help="Generate commit message without creating commit",
        )

        # Verify the default function was set
        mock_parser.set_defaults.assert_called_once_with(func=main)

    @patch("jbussdieker.commit.cli.run_commit")
    def test_commit_command_with_dry_run(self, mock_run_commit):
        """Test that dry_run argument is passed correctly to run_commit."""
        buf = StringIO()
        args = argparse.Namespace(dry_run=True)
        config = argparse.Namespace(openai_api_key="test")
        with redirect_stdout(buf):
            main(args, config)
        mock_run_commit.assert_called_once_with("test", dry_run=True)
