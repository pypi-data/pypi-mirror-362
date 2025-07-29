#!/usr/bin/env python3
"""
Setup script for QuantumMeta License Server
"""

from setuptools import setup, find_packages
import pathlib

# Read the README file
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="quantummeta-license",
    version="1.1.1",
    description="Universal, secure licensing system for QuantumMeta ecosystem packages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/krish567366/license-server",
    author="Krishna Bajpai",
    author_email="bajpaikrishna715@gmail.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Security :: Cryptography",
        "Topic :: System :: Systems Administration :: Authentication/Directory",
    ],
    keywords="license, licensing, security, quantum, ai, agi, server",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "cryptography>=41.0.0",
        "typer[all]>=0.9.0",
        "pydantic>=2.0.0",
        "psutil>=5.9.0",
        "rich>=13.0.0",
        "platformdirs>=3.0.0",
    ],
    extras_require={
        "server": [
            "fastapi>=0.104.0",
            "uvicorn[standard]>=0.24.0",
            "python-multipart>=0.0.6",
            "jinja2>=3.1.0",
            "aiofiles>=23.0.0",
            "python-dotenv>=1.0.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
        "docs": [
            "mkdocs>=1.5.0",
            "mkdocs-material>=9.0.0",
            "mkdocs-autorefs>=0.5.0",
            "mkdocstrings[python]>=0.22.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "quantum-license=quantummeta_license.cli.main:app",
            "quantum-license-server=api.main:main",
        ],
    },
    package_data={
        "quantummeta_license": ["py.typed"],
        "": ["*.md", "*.txt", "*.yml", "*.yaml"],
    },
    include_package_data=True,
    project_urls={
        "Bug Reports": "https://github.com/krish567366/license-server/issues",
        "Funding": "https://github.com/sponsors/krish567366",
        "Documentation": "https://krish567366.github.io/license-server",
        "Source": "https://github.com/krish567366/license-server",
    },
)
