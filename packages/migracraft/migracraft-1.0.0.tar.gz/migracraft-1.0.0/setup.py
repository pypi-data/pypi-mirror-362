#!/usr/bin/env python3
"""
Setup script for MigraCraft - Craft perfect PostgreSQL migrations
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="migracraft",
    version="1.0.0",
    author="Carlos Merchán Carmona",
    author_email="ccarmona.87@outlook.es",
    description="Craft perfect PostgreSQL migrations from YAML schema definitions with multi-language entity generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/carmonac/migracraft",
    project_urls={
        "Bug Reports": "https://github.com/carmonac/migracraft/issues",
        "Source": "https://github.com/carmonac/migracraft",
        "Documentation": "https://github.com/carmonac/migracraft#readme",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Database",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Environment :: Console",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-cov>=6.0.0",
        ],
        "test": [
            "pytest>=8.0.0",
            "pytest-cov>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "migracraft=migracraft.migracraft:main",
        ],
    },
    keywords=[
        "postgresql", "database", "migration", "schema", "yaml", 
        "generator", "entity", "sql", "differential", "craft"
    ],
    include_package_data=True,
    zip_safe=False,
)
