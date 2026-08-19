# Repo: evaluation-site
# Path: tools/add_file_headers.py

from pathlib import Path


REPO_ROOT = Path(".").resolve()
REPO_NAME = REPO_ROOT.name


def update_file(file_path):

    rel_path = (
        file_path.resolve()
        .relative_to(REPO_ROOT)
    )

    content = file_path.read_text(
        encoding="utf-8"
    )

    lines = content.splitlines(
        keepends=True
    )

    if not lines:
        lines = []

    # -----------------------------------------
    # Remove legacy single-line path header
    # -----------------------------------------

    if (
        len(lines) >= 1
        and lines[0].startswith("# ")
        and not lines[0].startswith("# Repo:")
        and not lines[0].startswith("# Path:")
        and "/" in lines[0]
    ):
        lines.pop(0)

        if (
            lines
            and lines[0].strip() == ""
        ):
            lines.pop(0)

    # -----------------------------------------
    # Update existing modern header
    # -----------------------------------------

    if (
        len(lines) >= 2
        and lines[0].startswith("# Repo:")
        and lines[1].startswith("# Path:")
    ):

        lines[0] = (
            f"# Repo: {REPO_NAME}\n"
        )

        lines[1] = (
            f"# Path: {rel_path.as_posix()}\n"
        )

    # -----------------------------------------
    # Insert new header
    # -----------------------------------------

    else:

        lines.insert(
            0,
            "\n"
        )

        lines.insert(
            0,
            f"# Path: {rel_path.as_posix()}\n"
        )

        lines.insert(
            0,
            f"# Repo: {REPO_NAME}\n"
        )

    file_path.write_text(
        "".join(lines),
        encoding="utf-8"
    )

    print(f"Updated: {rel_path}")


def process_repo(repo_root):

    repo_root = Path(repo_root)

    for py_file in repo_root.rglob("*.py"):

        if ".venv" in py_file.parts:
            continue

        if "__pycache__" in py_file.parts:
            continue

        update_file(py_file)


if __name__ == "__main__":

    process_repo(".")