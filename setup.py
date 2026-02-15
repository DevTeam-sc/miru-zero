import os
import sys
from pathlib import Path
from typing import Iterator

from setuptools import setup


SOURCE_ROOT = Path(__file__).resolve().parent


def main() -> None:
    version = detect_version()
    setup(
        name="miru-zero",
        version=version,
        description="Miru Zero orchestrator CLI",
        long_description="Miru Zero bootstrap, environment checker, and launcher for Miru.",
        long_description_content_type="text/markdown",
        author="Miru Developers",
        author_email="oleavr@miru.re",
        url="https://miru.re",
        python_requires=">=3.9",
        install_requires=[
            "miru-core>=16.5.7",
            "miru-tools>=16.5.7",
        ],
        license="wxWindows Library Licence, Version 3.1",
        zip_safe=False,
        keywords="miru debugger dynamic instrumentation inject javascript windows macos linux ios android",
        classifiers=[
            "Development Status :: 4 - Beta",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "License :: OSI Approved",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Topic :: Software Development :: Debuggers",
        ],
        packages=["miru_zero"],
        entry_points={
            "console_scripts": [
                "mz = miru_zero.cli:main",
                "miru-zero = miru_zero.cli:main",
            ]
        },
    )


def detect_version() -> str:
    version = os.environ.get("MIRU_ZERO_VERSION")
    if version is not None:
        return version

    releng_location = next(enumerate_releng_locations(), None)
    if releng_location is not None:
        sys.path.insert(0, str(releng_location.parent))
        try:
            from releng.miru_version import detect
        except ImportError:
            from releng.frida_version import detect

        detected = detect(SOURCE_ROOT)
        version = detected.name.replace("-dev.", ".dev")
    else:
        version = "0.0.0"
    return version


def enumerate_releng_locations() -> Iterator[Path]:
    val = os.environ.get("MESON_SOURCE_ROOT")
    if val is not None:
        candidate = Path(val) / "releng"
        if releng_location_exists(candidate):
            yield candidate

    local_releng = SOURCE_ROOT / "releng"
    if releng_location_exists(local_releng):
        yield local_releng


def releng_location_exists(location: Path) -> bool:
    return (location / "miru_version.py").exists() or (location / "frida_version.py").exists()


if __name__ == "__main__":
    main()

