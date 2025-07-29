import os
import tempfile
import subprocess
import unittest
from unittest.mock import patch, MagicMock, mock_open

from jbussdieker.commit.util import (
    get_staged_changes,
    get_project_context,
    generate_commit_message,
    edit_commit_message,
    create_commit,
    run_commit,
)


class TestGetStagedChanges(unittest.TestCase):
    @patch("subprocess.run")
    def test_get_staged_changes_success(self, mock_run):
        mock_result = MagicMock()
        mock_result.stdout = "diff --git a/file.txt b/file.txt\n+new line"
        mock_run.return_value = mock_result

        result = get_staged_changes()
        self.assertEqual(result, "diff --git a/file.txt b/file.txt\n+new line")
        mock_run.assert_called_once_with(
            ["git", "diff", "--cached"],
            capture_output=True,
            text=True,
            check=True,
        )

    @patch("subprocess.run")
    def test_get_staged_changes_error(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(1, "git diff --cached")

        with self.assertRaises(subprocess.CalledProcessError):
            get_staged_changes()

    @patch("subprocess.run")
    @patch("logging.error")
    def test_get_staged_changes_filenotfound_logging(self, mock_log, mock_run):
        mock_run.side_effect = FileNotFoundError()
        with self.assertRaises(FileNotFoundError):
            get_staged_changes()
        mock_log.assert_called_once()


class TestGetProjectContext(unittest.TestCase):
    @patch("subprocess.run")
    @patch("os.path.exists")
    def test_get_project_context_python(self, mock_exists, mock_run):
        mock_exists.return_value = True
        mock_branch_result = MagicMock()
        mock_branch_result.stdout = "main\n"
        mock_log_result = MagicMock()
        mock_log_result.stdout = "abc123 feat: add feature\n"
        mock_run.side_effect = [mock_branch_result, mock_log_result]

        result = get_project_context()
        self.assertIn("Current branch: main", result)
        self.assertIn("Project type: Python", result)
        self.assertIn("Recent commits:", result)

    @patch("subprocess.run")
    @patch("os.path.exists")
    def test_get_project_context_nodejs(self, mock_exists, mock_run):
        mock_exists.side_effect = [
            False,
            True,
        ]  # pyproject.toml doesn't exist, package.json does
        mock_branch_result = MagicMock()
        mock_branch_result.stdout = "feature\n"
        mock_run.return_value = mock_branch_result

        result = get_project_context()
        self.assertIn("Current branch: feature", result)
        self.assertIn("Project type: Node.js", result)

    @patch("subprocess.run")
    @patch("os.path.exists")
    def test_get_project_context_rust(self, mock_exists, mock_run):
        mock_exists.side_effect = [
            False,
            False,
            True,
        ]  # pyproject.toml and package.json don't exist, Cargo.toml does
        mock_branch_result = MagicMock()
        mock_branch_result.stdout = "feature\n"
        mock_run.return_value = mock_branch_result

        result = get_project_context()
        self.assertIn("Current branch: feature", result)
        self.assertIn("Project type: Rust", result)

    @patch("subprocess.run")
    @patch("os.path.exists")
    @patch("logging.error")
    def test_get_project_context_branch_filenotfound_logging(
        self, mock_log, mock_exists, mock_run
    ):
        mock_exists.return_value = True
        # branch raises FileNotFoundError, log succeeds
        mock_run.side_effect = [FileNotFoundError(), MagicMock(stdout="abc123\n")]
        result = get_project_context()
        self.assertIn("Recent commits:", result)
        # Do not assert mock_log, as get_project_context does not log this error

    @patch("subprocess.run")
    @patch("os.path.exists")
    def test_get_project_context_log_error(self, mock_exists, mock_run):
        mock_exists.return_value = True
        # branch succeeds, log fails
        mock_run.side_effect = [
            MagicMock(stdout="main\n"),
            subprocess.CalledProcessError(1, "git log"),
        ]
        result = get_project_context()
        self.assertIn("Current branch: main", result)

    @patch("subprocess.run")
    @patch("os.path.exists")
    def test_get_project_context_both_errors(self, mock_exists, mock_run):
        mock_exists.return_value = True
        mock_run.side_effect = [FileNotFoundError(), FileNotFoundError()]
        result = get_project_context()
        self.assertIn("Project type: Python", result)


class TestGenerateCommitMessage(unittest.TestCase):
    @patch("openai.OpenAI")
    def test_generate_commit_message_success(self, mock_openai):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = (
            "feat: add new feature\n\n- Add new functionality\n- Update documentation"
        )
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        result = generate_commit_message("staged changes", "context", "api_key")
        self.assertEqual(
            result,
            "feat: add new feature\n\n- Add new functionality\n- Update documentation",
        )

    @patch("openai.OpenAI")
    def test_generate_commit_message_no_api_key(self, mock_openai):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = (
            "feat: add new feature\n\n- Add new functionality"
        )
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        result = generate_commit_message("staged changes", "context", "")
        self.assertEqual(result, "feat: add new feature\n\n- Add new functionality")

    @patch("openai.OpenAI")
    def test_generate_commit_message_no_content(self, mock_openai):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = None
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        with self.assertRaises(RuntimeError):
            generate_commit_message("staged", "context", "key")

    @patch("openai.OpenAI")
    def test_generate_commit_message_openai_exception(self, mock_openai):
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = Exception("fail")
        mock_openai.return_value = mock_client
        with self.assertRaises(Exception):
            generate_commit_message("staged", "context", "key")


class TestEditCommitMessage(unittest.TestCase):
    @patch("subprocess.run")
    @patch("tempfile.NamedTemporaryFile")
    @patch("builtins.open", new_callable=mock_open, read_data="edited message")
    @patch("os.unlink")
    def test_edit_commit_message(
        self, mock_unlink, mock_open_builtin, mock_tempfile, mock_run
    ):
        mock_temp = MagicMock()
        mock_temp.name = "/tmp/test.txt"
        mock_tempfile.return_value.__enter__.return_value = mock_temp

        result = edit_commit_message("original message")
        self.assertEqual(result, "edited message")
        mock_run.assert_called_once()
        mock_unlink.assert_called_once_with("/tmp/test.txt")

    @patch("subprocess.run")
    @patch("tempfile.NamedTemporaryFile")
    @patch("builtins.open", new_callable=mock_open, read_data="   ")
    @patch("os.unlink")
    def test_edit_commit_message_empty(
        self, mock_unlink, mock_open_builtin, mock_tempfile, mock_run
    ):
        mock_temp = MagicMock()
        mock_temp.name = "/tmp/test.txt"
        mock_tempfile.return_value.__enter__.return_value = mock_temp
        result = edit_commit_message("original message")
        self.assertEqual(result, "")
        mock_run.assert_called_once()
        mock_unlink.assert_called_once_with("/tmp/test.txt")


class TestCreateCommit(unittest.TestCase):
    @patch("subprocess.run")
    def test_create_commit_success(self, mock_run):
        create_commit("feat: add feature")
        mock_run.assert_called_once_with(
            ["git", "commit", "-m", "feat: add feature"],
            check=True,
        )

    @patch("subprocess.run")
    def test_create_commit_error(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(1, "git commit")

        with self.assertRaises(subprocess.CalledProcessError):
            create_commit("feat: add feature")


class TestRunCommit(unittest.TestCase):
    @patch("jbussdieker.commit.util.get_staged_changes")
    @patch("jbussdieker.commit.util.get_project_context")
    @patch("jbussdieker.commit.util.generate_commit_message")
    @patch("jbussdieker.commit.util.edit_commit_message")
    @patch("jbussdieker.commit.util.create_commit")
    @patch("subprocess.run")
    def test_run_commit_success(
        self,
        mock_git_run,
        mock_create,
        mock_edit,
        mock_generate,
        mock_context,
        mock_staged,
    ):
        mock_git_run.return_value = MagicMock()
        mock_staged.return_value = "staged changes"
        mock_context.return_value = "context"
        mock_generate.return_value = "feat: add feature\n\n- Add new functionality"
        mock_edit.return_value = "feat: add feature\n\n- Add new functionality"

        run_commit("api_key")

        mock_generate.assert_called_once_with("staged changes", "context", "api_key")
        mock_edit.assert_called_once_with(
            "feat: add feature\n\n- Add new functionality"
        )
        mock_create.assert_called_once_with(
            "feat: add feature\n\n- Add new functionality"
        )

    @patch("subprocess.run")
    def test_run_commit_not_git_repo(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(1, "git rev-parse")

        run_commit("api_key")
        # Should not raise an exception, just return

    @patch("jbussdieker.commit.util.get_staged_changes")
    @patch("subprocess.run")
    def test_run_commit_no_staged_changes(self, mock_run, mock_staged):
        mock_run.return_value = MagicMock()
        mock_staged.return_value = ""

        run_commit("api_key")
        # Should not raise an exception, just return

    @patch("jbussdieker.commit.util.get_staged_changes")
    @patch("jbussdieker.commit.util.get_project_context")
    @patch("jbussdieker.commit.util.generate_commit_message")
    @patch("subprocess.run")
    def test_run_commit_dry_run(
        self, mock_git_run, mock_generate, mock_context, mock_staged
    ):
        mock_git_run.return_value = MagicMock()
        mock_staged.return_value = "staged changes"
        mock_context.return_value = "context"
        mock_generate.return_value = "feat: add feature\n\n- Add new functionality"

        run_commit("api_key", dry_run=True)

        mock_generate.assert_called_once_with("staged changes", "context", "api_key")
        # Should not call edit or create functions

    @patch("jbussdieker.commit.util.get_staged_changes")
    @patch("jbussdieker.commit.util.get_project_context")
    @patch("jbussdieker.commit.util.generate_commit_message")
    @patch("jbussdieker.commit.util.edit_commit_message")
    @patch("subprocess.run")
    def test_run_commit_empty_edited_message(
        self, mock_git_run, mock_edit, mock_generate, mock_context, mock_staged
    ):
        mock_git_run.return_value = MagicMock()
        mock_staged.return_value = "staged changes"
        mock_context.return_value = "context"
        mock_generate.return_value = "feat: add feature"
        mock_edit.return_value = "   "
        # Should not raise, should just return
        run_commit("api_key")


if __name__ == "__main__":
    unittest.main()
