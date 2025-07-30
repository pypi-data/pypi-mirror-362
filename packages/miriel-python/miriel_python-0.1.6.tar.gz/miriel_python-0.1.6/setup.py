import pathlib
import re
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

def read_version():
    version_file = HERE / "miriel" / "__init__.py"
    content = version_file.read_text(encoding="utf-8")
    match = re.search(r'^__version__\s*=\s*[\'"]([^\'"]+)[\'"]', content, re.M)
    if not match:
        raise RuntimeError("Unable to find version string in miriel/__init__.py")
    return match.group(1)

setup(
    name="miriel-python",              # this is your PyPI package name
    version=read_version(),            # no direct import of miriel
    author="David Garcia",
    author_email="david@miriel.ai",
    description="Library for interacting with the Miriel API",
    long_description=(HERE / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/miriel-ai/miriel-python",
    license="MIT",
    packages=find_packages(exclude=["tests", "examples"]),
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
