from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

setup(
    name="bivouac-framework",
    version="0.1.0-alpha",
    author="Bivouac Framework Team",
    author_email="team@bivouac-framework.com",
    description="A modular Flask framework for building scalable web applications",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/bivouac-framework/bivouac-framework",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Flask>=2.3.0",
        "Flask-SQLAlchemy>=3.0.0",
        "Flask-User>=1.0.0",
        "Flask-WTF>=1.1.0",
        "WTForms>=3.0.0",
        "SQLAlchemy>=2.0.0",
        "Werkzeug>=2.3.0",
        "click>=8.0.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-flask>=1.2.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "bivouac=bivouac_framework.cli.commands:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
) 