"""Project generator used by the CLI."""

from __future__ import annotations

import argparse
import re
from importlib import resources as pkg_resources
from pathlib import Path


def get_default_author() -> str:
    try:
        import git  # noqa: PLC0415

        return git.config.GitConfigParser().get_value("user", "name")  # type: ignore[return-value]
    except Exception:
        raise ValueError("Could not get configured Git author; please manually specify the --author argument")


def get_default_email() -> str:
    try:
        import git  # noqa: PLC0415

        return git.config.GitConfigParser().get_value("user", "email")  # type: ignore[return-value]
    except Exception:
        raise ValueError("Could not get configured Git email; please manually specify the --email argument")


def cleanup_url(s: str) -> str:
    s = s.replace(":", "/")
    s = s.replace("git@", "https://")
    s = s.replace(".git", "")
    return s


def get_default_url() -> str:
    try:
        import git  # noqa: PLC0415

        repo = git.Repo(search_parent_directories=True)
        return cleanup_url(repo.remote().url)
    except Exception:
        raise ValueError("Could not get configured Git URL; please manually specify the --url argument")


def _prompt(msg: str, default: str | None, non_interactive: bool) -> str:
    if default is not None and not non_interactive:
        answer = input(f"{msg} [{default}]: ").strip()
        return answer or default
    if non_interactive and default is None:
        raise ValueError(f"Missing value for: {msg}")
    return default or input(f"{msg}: ").strip()


def add_common_args(p: argparse.ArgumentParser) -> None:
    p.add_argument(
        "name",
        nargs="?",
        help="Project name (e.g. kinfer-evals). Can also be given with --name.",
    )
    p.add_argument(
        "--name",
        dest="name",
        metavar="NAME",
        help=argparse.SUPPRESS,
    )
    p.add_argument("--description")
    p.add_argument("--author")
    p.add_argument("--email")
    p.add_argument("--url")
    p.add_argument("--python-version", default="3.11")
    p.add_argument("--python-name", help="Python package name (defaults to project name with hyphens -> underscores)")
    p.add_argument(
        "--git-remote",
        "-g",
        metavar="URL",
        help="If provided, initialise git and set this URL as the origin remote",
    )
    p.add_argument(
        "--target-dir",
        "-o",
        metavar="DIR",
        help="Directory in which the project folder will be created (defaults to current directory)",
    )


def run_generator(args: argparse.Namespace) -> None:
    non_int = getattr(args, "non_interactive", False)

    name = args.name or _prompt("Project name?", None, non_int)
    description = args.description or _prompt("Description", f"The {name} project", non_int)
    try:
        default_author = get_default_author()
    except ValueError:
        default_author = None
    author = args.author or _prompt("Author", default_author, non_int)

    try:
        default_email = get_default_email()
    except ValueError:
        default_email = None
    email = args.email or _prompt("Email", default_email, non_int)

    try:
        default_url = get_default_url()
    except ValueError:
        default_url = None
    url = args.url or _prompt("Repo URL", default_url, non_int)

    git_remote = args.git_remote or _prompt("Git remote URL (blank to skip)", "", non_int).strip()
    py_ver = _prompt("Min Python version", args.python_version, non_int)
    py_name = args.python_name or _prompt("Python package name", name.replace("-", "_"), non_int)

    target_dir = args.target_dir or _prompt("Target directory", str(Path.cwd()), non_int)

    # validation unchanged
    if not re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_-]*", name):
        raise ValueError(f"Invalid project name: {name}")
    if not re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*", py_name):
        raise ValueError(f"Invalid Python package name: {py_name}")

    replacements = {
        "[[PROJECT NAME]]": name,
        "[[PROJECT PYTHON NAME]]": py_name,
        "[[PROJECT DESCRIPTION]]": description,
        "[[PROJECT AUTHOR]]": author,
        "[[PROJECT EMAIL]]": email,
        "[[PROJECT URL]]": url,
        "[[PROJECT PYTHON VERSION]]": py_ver,
    }

    src_dir = Path(str(pkg_resources.files("pipify") / "template"))
    tgt_dir = Path(target_dir).expanduser().resolve() / name
    tgt_dir.mkdir(parents=True, exist_ok=True)

    def copy_tree(src: Path, dst: Path) -> None:
        if src.is_dir():
            if src.name in {"__pycache__", ".git", ".ruff_cache", ".pytest_cache"}:
                return
            dst.mkdir(exist_ok=True)
            for child in src.iterdir():
                copy_tree(child, dst / child.name)
        else:
            text = src.read_text(encoding="utf-8")
            for k, v in replacements.items():
                text = text.replace(k, v)
            (dst).write_text(text, encoding="utf-8")

    copy_tree(src_dir, tgt_dir)
    (tgt_dir / "project").rename(tgt_dir / py_name)
    print(f"🚀  Created project at {tgt_dir}")

    if git_remote:
        try:
            import subprocess  # noqa: PLC0415

            subprocess.run(
                ["git", "init", "--initial-branch", "main"],
                cwd=tgt_dir,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            subprocess.run(
                ["git", "remote", "add", "origin", git_remote],
                cwd=tgt_dir,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            # Do an empty commit and push to set upstream
            (tgt_dir / ".gitkeep").touch()
            subprocess.run(
                ["git", "add", ".gitkeep"],
                cwd=tgt_dir,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            subprocess.run(
                ["git", "commit", "-m", "Initial scaffold"],
                cwd=tgt_dir,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            # first push sets upstream (-u)
            subprocess.run(
                ["git", "push", "-u", "origin", "main"],
                cwd=tgt_dir,
                check=True,
            )

            print(f"📦  Initialised git repository and set origin → {git_remote}")
        except Exception as e:
            print(f"⚠️  Could not initialise git or set remote: {e}")
