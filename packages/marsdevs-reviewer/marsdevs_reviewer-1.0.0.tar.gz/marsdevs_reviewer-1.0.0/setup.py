"""
Setup script for MarsDevs Code Reviewer
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="marsdevs-reviewer",
    version="1.0.0",
    author="MarsDevs Team",
    author_email="team@marsdevs.com",
    description="AI-powered code review tool that learns from your repository",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marsdevs/marsdevs-reviewer",
    project_urls={
        "Bug Tracker": "https://github.com/marsdevs/marsdevs-reviewer/issues",
        "Documentation": "https://github.com/marsdevs/marsdevs-reviewer#readme",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Version Control :: Git",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
    entry_points={
        "console_scripts": [
            "marsdevs-reviewer=marsdevs_reviewer.cli:main",
        ],
    },
    keywords="git pre-commit code-review ai conventions linting",
    include_package_data=True,
)