# mypy: disable-error-code="import-untyped"
#!/usr/bin/env python
"""Setup script for the project."""

import re

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description: str = f.read()


def _clean(reqs: list[str]) -> list[str]:
    return [ln.strip() for ln in reqs if ln.strip() and not ln.startswith("#")]


with open("pipify/requirements.txt", "r", encoding="utf-8") as f:
    requirements = _clean(f.readlines())


with open("pipify/requirements-dev.txt", "r", encoding="utf-8") as f:
    requirements_dev = _clean(f.readlines())


with open("pipify/__init__.py", "r", encoding="utf-8") as fh:
    version_re = re.search(r"^__version__ = \"([^\"]*)\"", fh.read(), re.MULTILINE)
assert version_re is not None, "Could not find version in pipify/__init__.py"
version: str = version_re.group(1)


setup(
    name="pipify",
    version=version,
    description="Utility for making python packages",
    author="alik-git",
    url="https://github.com/kscalelabs/pipify",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={"dev": requirements_dev},
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "pipify=pipify.cli:main",
        ],
    },
)
