from pathlib import Path
from typing import Any


def main(args: Any) -> int:
    version = getattr(args, "version", None)
    output = getattr(args, "output", None)
    if version is None:
        print("miru-zero: sdk command requires --version")
        return 1
    try:
        from tools.release import build_sdk
    except Exception as exc:
        print(f"miru-zero: unable to import build_sdk module: {exc}")
        return 1
    kwargs: dict[str, Any] = {}
    if output is not None:
        kwargs["output_dir"] = Path(output)
    try:
        build_sdk.build_sdk(version=version, **kwargs)
    except AttributeError:
        print("miru-zero: build_sdk.build_sdk entrypoint not found")
        return 1
    except Exception as exc:
        print(f"miru-zero: sdk build failed: {exc}")
        return 1
    return 0

