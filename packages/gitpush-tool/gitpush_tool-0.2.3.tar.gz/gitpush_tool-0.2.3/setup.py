from setuptools import setup, find_packages
from pathlib import Path

setup(
    name="gitpush-tool",
    version="0.2.3",
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.0',
    ],
    entry_points={
        "console_scripts": [
            "gitpush_tool=gitpush_tool.cli:run"
        ],
    },
    author="Ganesh Sonawane",
    author_email="sonawaneganu3101@gmail.com",
    description="A CLI tool to simplify Git push operations with intelligent defaults and options.",
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/inevitablegs/gitpush",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
