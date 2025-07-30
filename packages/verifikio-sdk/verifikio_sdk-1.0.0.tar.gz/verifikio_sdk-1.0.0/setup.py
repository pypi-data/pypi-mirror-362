"""
Setup script for the Verifik.io Python SDK
"""

from setuptools import setup, find_packages

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="verifikio-sdk",
    version="1.0.0",
    author="Verifik.io",
    author_email="support@verifik.io",
    description="Official Python SDK for Verifik.io trust infrastructure platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/verifik-io/verifikio-python",
    project_urls={
        "Documentation": "https://docs.verifik.io/sdk/python",
        "API Reference": "https://docs.verifik.io/api",
        "Bug Tracker": "https://github.com/verifik-io/verifikio-python/issues",
        "Homepage": "https://verifik.io",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Logging",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.812",
        ],
    },
    keywords="audit logging security ai agents blockchain verification trust infrastructure",
    license="MIT",
    zip_safe=False,
)