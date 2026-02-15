from typing import Any, Iterable, List

import sys


def run_with_argv(argv: Iterable[str]) -> int:
    try:
        from miru_tools import repl as repl_module
    except Exception as exc:
        print(f"miru-zero: unable to import miru_tools.repl: {exc}")
        return 1
    args: List[str] = list(argv)
    old_argv = sys.argv
    try:
        sys.argv = ["miru"] + args
        try:
            repl_module.main()
        except SystemExit as exc:
            code = exc.code
            if code is None:
                return 0
            if isinstance(code, int):
                return code
            return 1
        return 0
    finally:
        sys.argv = old_argv


def main(args: Any | None = None) -> int:
    return run_with_argv([])

