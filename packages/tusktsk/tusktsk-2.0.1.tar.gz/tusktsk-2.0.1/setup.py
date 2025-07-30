#!/usr/bin/env python3
"""
TuskTsk Python SDK Setup
"""
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="tusktsk",
    version="2.0.1",
    description="TuskTsk - Configuration with a Heartbeat. Query databases, use any syntax, never bow to any king!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cyber-boost/tusktsk",
    author="Cyberboost LLC",
    author_email="packages@tuskt.sk",
    # license defined in pyproject.toml
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Configuration",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    # keywords defined in pyproject.toml
    package_dir={"": "."},
    py_modules=["tsk", "tsk_enhanced", "peanut_config"],
    packages=find_packages(where="."),
    python_requires=">=3.8, <4",
    # dependencies defined in pyproject.toml
    # optional dependencies defined in pyproject.toml
    entry_points={
        "console_scripts": [
            "tusk=tsk:main",
            "tusk-peanut=peanut_config:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/cyber-boost/tusktsk/issues",
        "Documentation": "https://tuskt.sk/docs/python",
        "Source": "https://github.com/cyber-boost/tusktsk",
        "Homepage": "https://tuskt.sk",
        "License": "https://tuskt.sk/license",
    },
)