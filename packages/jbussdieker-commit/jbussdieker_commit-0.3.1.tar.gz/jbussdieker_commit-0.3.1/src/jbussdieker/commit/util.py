import os
import subprocess
import tempfile
import logging

import openai


def get_staged_changes() -> str:
    """Get the output of git diff --cached"""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to get staged changes: {e}")
        raise
    except FileNotFoundError:
        logging.error("git command not found")
        raise


def get_project_context() -> str:
    """Get additional project context for better commit messages"""
    context_parts = []

    # Get current branch
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=True,
        )
        context_parts.append(f"Current branch: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # Get recent commit messages for context
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", "-5"],
            capture_output=True,
            text=True,
            check=True,
        )
        context_parts.append(f"Recent commits:\n{result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # Get project type (Python, etc.)
    if os.path.exists("pyproject.toml"):
        context_parts.append("Project type: Python (pyproject.toml)")
    elif os.path.exists("package.json"):
        context_parts.append("Project type: Node.js (package.json)")
    elif os.path.exists("Cargo.toml"):
        context_parts.append("Project type: Rust (Cargo.toml)")

    return "\n".join(context_parts)


def generate_commit_message(
    staged_changes: str, project_context: str, api_key: str
) -> str:
    """Generate a conventional commit message using OpenAI (v1.x API)"""
    # Use config API key if provided, otherwise OpenAI library will use OPENAI_API_KEY env var
    if api_key:
        client = openai.OpenAI(api_key=api_key)
    else:
        client = openai.OpenAI()

    prompt = f"""You are a helpful assistant that generates conventional commit messages.

Project Context:
{project_context}

Staged Changes:
{staged_changes}

Please generate a conventional commit message following these rules:
1. First line: Use conventional commit format: <type>(<scope>): <description>
2. Types: feat, fix, docs, style, refactor, test, chore, perf, ci, build, revert
3. Keep the description concise but descriptive
4. If there are breaking changes, add ! after the type and scope
5. If the commit affects multiple areas, use multiple scopes or a general scope
6. The message should be in the imperative mood ("add feature" not "added feature")
7. After the first line, add a blank line, then list the key changes as markdown bullet points (prefixed with "- ")

Example format:
feat(auth): add user authentication system

- Add login and registration endpoints
- Implement JWT token generation
- Add password hashing with bcrypt
- Create user model and database migrations

Generate the commit message with this format:"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that generates conventional commit messages.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=100,
            temperature=0.3,
        )
        content = response.choices[0].message.content
        if content is None:
            raise RuntimeError("OpenAI returned no commit message content.")
        return content.strip()
    except Exception as e:
        logging.error(f"Failed to generate commit message: {e}")
        raise


def edit_commit_message(commit_message: str) -> str:
    """Open editor with prepopulated commit message and return the edited message"""
    editor = os.environ.get("EDITOR", "vim")

    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write(commit_message)
        temp_file = f.name

    try:
        subprocess.run([editor, temp_file], check=True)

        with open(temp_file, "r") as f:
            edited_message = f.read().strip()

        return edited_message
    finally:
        os.unlink(temp_file)


def create_commit(commit_message: str) -> None:
    """Create the git commit with the given message"""
    try:
        subprocess.run(
            ["git", "commit", "-m", commit_message],
            check=True,
        )
        logging.info("Commit created successfully")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to create commit: {e}")
        raise


def run_commit(api_key: str, dry_run: bool = False) -> None:
    """Main function to run the commit process"""
    # Check if we're in a git repository
    try:
        subprocess.run(
            ["git", "rev-parse", "--git-dir"], check=True, capture_output=True
        )
    except subprocess.CalledProcessError:
        logging.error("Not in a git repository")
        return

    # Check if there are staged changes
    staged_changes = get_staged_changes()
    if not staged_changes.strip():
        logging.error("No staged changes to commit")
        return

    # Get project context
    project_context = get_project_context()

    # Generate commit message
    commit_message = generate_commit_message(staged_changes, project_context, api_key)

    if dry_run:
        logging.info("Generated commit message (dry run):")
        logging.info(commit_message)
        return

    # Edit the commit message
    edited_message = edit_commit_message(commit_message)

    if not edited_message.strip():
        logging.info("Commit cancelled (empty message)")
        return

    # Create the commit
    create_commit(edited_message)
