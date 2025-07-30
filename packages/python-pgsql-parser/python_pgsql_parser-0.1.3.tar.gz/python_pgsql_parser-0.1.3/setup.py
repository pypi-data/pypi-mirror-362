from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="python-pgsql-parser",
    version="0.1.2",
    author="Sunny Liu",
    author_email="sunnyliu2@gmail.com",
    description="Advanced PostgreSQL SQL parser for extracting database schema metadata",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/python-pgsql-parser",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.7",
    keywords="sql parser postgresql ddl metadata schema analysis",
    install_requires=[],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0", "coverage>=6.0"],
    },
    project_urls={
        "Documentation": "https://github.com/devsunny/python-pgsql-parser/blob/main/docs/index.md",
        "Source": "https://github.com/devsunny/python-pgsql-parser",
        "Tracker": "https://github.com/devsunny/python-pgsql-parser/issues",
    },
)