#!/usr/bin/env python3
"""
GitGuard - Enterprise-Grade Secure Git Workflow
Setup configuration for Python package distribution
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Read requirements from requirements.txt
requirements = []
if (this_directory / "requirements.txt").exists():
    with open(this_directory / "requirements.txt") as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="gitguard",
    version="1.0.1",
    author="Herbert J. Bowers (Project Creator), Claude (Anthropic) - Technical Implementation",
    author_email="HimalayaProject1@gmail.com",
    description="Enterprise-grade secure git workflow system - Part of Project Himalaya demonstrating AI-human collaboration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/herbbowers/gitguard",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators", 
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: Software Development :: Quality Assurance",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0", 
            "flake8>=4.0.0",
            "mypy>=0.991",
            "pre-commit>=2.20.0",
        ],
        "enterprise": [
            "requests>=2.28.0",
            "pyyaml>=6.0",
            "click>=8.0.0",
            "jinja2>=3.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "gitguard=gitguard.cli:main",
            "gitguard-scan=gitguard.scanner:main",
            "gitguard-fix=gitguard.remediator:main",
            "gitguard-audit=gitguard.auditor:main",
        ],
    },
    include_package_data=True,
    package_data={
        "gitguard": [
            "data/*.yaml",
            "data/*.json", 
            "templates/*.txt",
            "templates/*.md",
        ],
    },
    keywords=[
        "git", "security", "credentials", "secrets", "devops", "devsecops", 
        "audit", "compliance", "workflow", "automation", "enterprise"
    ],
    project_urls={
        "Bug Reports": "https://github.com/herbbowers/gitguard/issues",
        "Source": "https://github.com/herbbowers/gitguard",
        "Documentation": "https://gitguard.dev",
        "Changelog": "https://github.com/herbbowers/gitguard/blob/main/CHANGELOG.md",
    },
    zip_safe=False,
)