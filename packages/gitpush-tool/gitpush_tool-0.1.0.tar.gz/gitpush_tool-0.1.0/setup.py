from setuptools import setup, find_packages
from pathlib import Path

setup(
    name="gitpush-tool",  # Changed to use hyphen instead of underscore
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "gitpush=gitpush_tool.cli:run"
        ],
    },
    author="Ganesh Sonawane",
    author_email="sonawaneganu3101@example.com",
    description="A simple CLI tool to push git commits with a single command.",
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/gitpush",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)