#!/usr/bin/env python
"""pipify command-line interface."""

from __future__ import annotations

import argparse
from typing import Callable

SubCmd = Callable[[argparse.Namespace], None]


def _build_parser() -> tuple[argparse.ArgumentParser, dict[str, SubCmd]]:
    from .generator import add_common_args, run_generator  # noqa: PLC0415

    parser = argparse.ArgumentParser(prog="pipify", description="Utility for templated Python packages")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_create = subparsers.add_parser("create", help="Create a new project from the template")
    add_common_args(p_create)  # same flags as before
    p_create.add_argument(
        "--non-interactive", action="store_true", help="Fail if a value is missing instead of prompting"
    )

    return parser, {"create": run_generator}


def main(argv: list[str] | None = None) -> None:  # pragma: no cover
    parser, handlers = _build_parser()
    ns = parser.parse_args(argv)
    handlers[ns.command](ns)


if __name__ == "__main__":  # pragma: no cover
    main()
