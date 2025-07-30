from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mcp-notes-server",
    version="0.1.1",
    author="filib",
    author_email="filib@pypi.org",
    description="A Model Context Protocol server for developer note-taking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://mcp-hunt.com/mcp/server/adobe-xd-mcp-server",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "mcp>=0.1.0",
        "pydantic>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "mcp-notes-server=mcp_notes_server.server:main",
        ],
    },
)