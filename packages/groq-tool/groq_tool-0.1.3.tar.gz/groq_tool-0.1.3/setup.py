# setup.py

from setuptools import setup, find_packages

setup(
    name="groq-tool",
    version="0.1.3",
    packages=find_packages(),
    install_requires=[
        "rich",
        "requests",
        "groq",
        "dotenv",
        "click"
    ],
    entry_points={
        "console_scripts": [
            "groqcli=groqcli.cli:cli",
            "groqcli-files=groqcli.module_each:cli_files",
        ],
    },
    author="daisseur",
    description="A Modern Command-Line Tool for Interacting with Grog LLMs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    project_urls={
        "Source": "https://github.com/daisseur/groqcli",
    },
)
