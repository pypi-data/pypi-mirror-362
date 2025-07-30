from setuptools import setup, find_packages

setup(
    name="kick-mcpserver",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "kick-mcpserver=mcpserver_init:main",
        ],
    },
    author="Manoj",
    description="A CLI tool to scaffold an MCP server project",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
