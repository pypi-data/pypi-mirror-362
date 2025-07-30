#!/usr/bin/env python3
"""
Setup script for Claude Code Indexer
"""

from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="claude-code-indexer",
    version="1.1.2",
    author="Claude AI Assistant",
    author_email="noreply@anthropic.com",
    description="Code indexing tool using graph database for Claude Code Assistant",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/anthropics/claude-code-indexer",
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
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Documentation",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Software Development :: Version Control :: Git",
        "Environment :: Console",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "claude-code-indexer=claude_code_indexer.cli:main",
            "cci=claude_code_indexer.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "claude_code_indexer": ["templates/*.md", "templates/*.sql"],
    },
    keywords="code indexing, graph database, ensmallen, claude, code analysis, ast, development tools",
    project_urls={
        "Homepage": "https://github.com/anthropics/claude-code-indexer",
        "Documentation": "https://docs.anthropic.com/claude-code",
        "Repository": "https://github.com/anthropics/claude-code-indexer.git",
        "Issues": "https://github.com/anthropics/claude-code-indexer/issues",
        "Changelog": "https://github.com/anthropics/claude-code-indexer/blob/main/CHANGELOG.md",
    },
)