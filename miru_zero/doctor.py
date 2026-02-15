import platform
import shutil
import sys
from importlib import metadata


def main(args: object | None = None) -> int:
    print("Miru Zero doctor")
    print()
    print_python()
    print()
    print_packages()
    print()
    print_binaries()
    return 0


def print_python() -> None:
    implementation = platform.python_implementation()
    version = platform.python_version()
    print(f"[python] {implementation} {version}")


def print_packages() -> None:
    names = ["miru-zero", "miru-core", "miru-tools"]
    for name in names:
        try:
            version = metadata.version(name)
            print(f"[package] {name}: {version}")
        except metadata.PackageNotFoundError:
            print(f"[package] {name}: MISSING")


def print_binaries() -> None:
    names = ["mz", "miru-zero", "miru", "adb"]
    for name in names:
        path = shutil.which(name)
        if path is None:
            print(f"[binary] {name}: MISSING")
        else:
            print(f"[binary] {name}: {path}")

