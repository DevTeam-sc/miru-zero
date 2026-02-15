import argparse
import sys

from . import doctor, repl, sdk


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mz", description="Miru Zero CLI")
    subparsers = parser.add_subparsers(dest="command")

    doctor_parser = subparsers.add_parser("doctor", help="Check Miru environment")
    doctor_parser.set_defaults(handler=doctor.main)

    repl_parser = subparsers.add_parser("repl", help="Launch Miru REPL")
    repl_parser.set_defaults(handler=_handle_repl_subcommand)

    sdk_parser = subparsers.add_parser("sdk", help="Build Miru SDK")
    sdk_parser.add_argument("--version", help="Miru version")
    sdk_parser.add_argument("--output", help="Output directory")
    sdk_parser.set_defaults(handler=sdk.main)

    return parser


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        parser = build_parser()
        parser.print_help()
        return 1
    first = argv[0]
    if first == "repl":
        return repl.run_with_argv(argv[1:])
    if first in ("-D", "--device", "-U", "--usb", "-R", "--remote", "-H", "--host"):
        return repl.run_with_argv(argv)
    parser = build_parser()
    args = parser.parse_args(argv)
    handler = getattr(args, "handler", None)
    if handler is None:
        parser.print_help()
        return 1
    return int(handler(args) or 0)


def _handle_repl_subcommand(args: argparse.Namespace) -> int:
    return repl.run_with_argv([])


if __name__ == "__main__":
    raise SystemExit(main())
